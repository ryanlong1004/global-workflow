"""
# Definition of the suite test
suite test
   edit ECF_HOME "$HOME/course"  # replace '$HOME' with the path to your home directory
   task t1
endsuite
"""
import os
import shutil
from typing import List, Union
from abc import ABC
from itertools import chain


class Node(ABC):
    """represents any leaf of the ecf tree"""

    def __init__(self, name: str, parent: Union[None, "Node"]):
        if name == "__ROOT__":
            raise ValueError("__ROOT__ node already exists.")
        self.name = name
        self.parent = parent
        self.children = []
        self.manuals = []
        self.edits = []

        if parent:
            parent.add_child(self)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.name}/>"

    def __str__(self) -> str:
        parent_name = "None" if self.parent is None else self.parent.name
        return f"<{self.__class__.__name__} name='{self.name}' parent='{parent_name}' children=[{len(self.children)}]>"

    def __iter__(self):
        return iter(self.children)

    def add_manual(self, text: Union[List[str], str]):
        """
        A manual page allows documentation in an ecf script to be viewable in ecflow_ui.
        https://confluence.ecmwf.int/display/ECFLOW/Add+Manual
        """
        self.manuals.append(list(text))

    def add_edit(self, text: Union[List[str], str]):
        """
        Adds an edit to either a suite, task, or family. The parent defines
        what object will get the edit object.

        Also edits set variables %VAR%
        """
        self.edits.append(list(text))

    def add_child(self, node: "Node"):
        """add a child node to the current node"""
        self.children.append(node)

    def add_parent(self, node: "Node"):
        """assign a new parent node"""
        self.parent = node
        node.add_child(self)


class Suite(Node):
    """collection of families"""

    def add_family(self, family: "Family"):
        """add family to suite"""
        family.parent = self
        self.add_child(family)

    def add_task(self, _task: "Task"):
        """adds a task to the suite"""
        print("Here")
        _task.parent = self
        self.add_child(_task)

    def define_limit(self):
        """https://confluence.ecmwf.int/display/ECFLOW/Limits"""


class Family(Node):
    """Collection of other families and tasks"""

    def add_repeat(self, repeat):
        """https://confluence.ecmwf.int/display/ECFLOW/Repeat"""

    def add_event(self, event):
        """add an event"""
        raise NotImplementedError

    def add_family(self, family: "Family"):
        """add a family"""
        family.parent = self
        self.add_child(family)

    def add_task(self, task: "Task"):
        """add a task"""
        task.parent = self
        self.add_child(task)

    def use_limit(self):
        """https://confluence.ecmwf.int/display/ECFLOW/Limits"""
        raise NotImplementedError


class Task(Node):
    """represents task"""

    def __init__(self, name: str, parent: Union[Node, None]):
        self.trigger: Union["Trigger", None] = None
        super().__init__(name, parent)

    def add_cron(self):
        """
        https://confluence.ecmwf.int/display/ECFLOW/Add+a+Cron
        """
        raise NotImplementedError

    def add_label(self):
        """
        https://confluence.ecmwf.int/display/ECFLOW/Labels
        """
        raise NotImplementedError

    def add_repeat(self, repeat):
        """https://confluence.ecmwf.int/display/ECFLOW/Repeat"""
        raise NotImplementedError

    def add_trigger(self, trigger: "Trigger"):
        """sets the Task trigger"""
        if self.trigger is not None:
            raise ValueError(f"trigger already defined. [{self.name}]-> {self.trigger}")
        self.trigger = trigger

    def add_event(self, event: "Event"):
        """add event to the Task"""
        raise NotImplementedError


class Trigger:
    """
    Where possible you should give preference to triggers on the definitions, since these are checked on creation, whereas embedded triggers are checked at run time.

    Embeded triggers?
    https://confluence.ecmwf.int/display/ECFLOW/Embedded+Triggers
    """


class Event:
    """
    An event is a message that a task will report to ecflow_server while it is running.
    Events have names and a task can set several of them.

    https://confluence.ecmwf.int/display/ECFLOW/Add+an+event
    """


class Repeat:
    pass


class Complete:
    """
    Sometimes a task should not be run when a certain condition is met.
    The condition can be signalled by an event. For example, event t2:b
    might indicate that task t2 did not manage to produce the expected result, so
    we do not need to run task t4.
    In this case, you can use the complete expression keyword.
    This has a similar syntax to the trigger keyword but sets a task
    complete rather than running it.

    https://confluence.ecmwf.int/display/ECFLOW/Add+a+complete
    """


class Meter:
    """
    A meter is very similar to an event.
    Instead of being a boolean value (on/off), it can take a range of integer values.
    Other tasks are then triggered when the meter reaches a certain value.
    Like events, meters have names and a task can have several of them.

    https://confluence.ecmwf.int/display/ECFLOW/Add+a+meter
    """


class TimeDependency:
    """
    TODO:
    https://confluence.ecmwf.int/display/ECFLOW/Time+Dependencies
    """


class TimeTrigger:
    """
    TODO:

    https://confluence.ecmwf.int/display/ECFLOW/Time+Triggers
    """


def query_state():
    """https://confluence.ecmwf.int/display/ECFLOW/Query+state"""
    pass


def generate_ecflow_task(ecfhome, suite, parents, name, template, scriptrepo):
    """
    Uses the parameters passed in to define the folder path and then
    looks in the script repository for the task name with a .ecf suffix or
    template name with a .ecf suffix and then copies that script content
    from the script repo over to the destination provided by the parameters

    Parameters
    ----------
    ecfhome : str
        Path to the root level directory to place the scripts.
    suite : str
        Suite name to add the scripts to that will be appended to the
        ecfhome
    parents: str
        Any parent folders that are appended to the ecfhome and suite
        folders.

    Returns
    -------
    None
    """
    if template == "skip":
        return
    script_name = f"{name()}.ecf"
    ecfscript = None
    search_script = f"{template}.ecf" if template is not None else script_name
    if parents:
        script_path = f"{ecfhome}/{suite}/{parents.replace('>','/')}/{script_name}"
    else:
        script_path = f"{ecfhome}/{suite}/{script_name}"
    for root, _, files in os.walk(scriptrepo):
        if search_script in files and ecfscript is None:
            ecfscript = os.path.join(root, search_script)
    if ecfscript is not None:
        shutil.copyfile(ecfscript, script_path, follow_symlinks=True)


if __name__ == "__main__":
    suite = Suite("root_suite", None)
    family = Family("first family", suite)
    task = Task("my_task", suite)
    task2 = Task("my 2nd task", suite)

    def _unwind(root, accum):
        for x in root:
            accum.append(x)
            if len(x.children) >= 0:
                accum.append(_unwind(x.children, accum))
        return accum

    print(_unwind(suite, []))

# level_1_child_1 = Node(34, parent=root)
# level_1_child_2 = Node(89, parent=root)
# level_2_child_1 = Node(45, parent=level_1_child_1)
# level_2_child_2 = Node(50, parent=level_1_child_2)
