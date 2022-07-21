"""
# Definition of the suite test
suite test
   edit ECF_HOME "$HOME/course"  # replace '$HOME' with the path to your home directory
   task t1
endsuite
"""
from collections import UserDict, UserList
import sys
import os
import re
import shutil
from datetime import datetime, timedelta
from typing import List, Union
from abc import ABC, abstractmethod

Comment = str
Edit = str

class Node(ABC):
    """represents any leaf of the ecf tree"""

    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.manuals = []
        self.edits = []

    @abstractmethod
    def add_manual(self, text: Union[List[str], str] ):
        """
        A manual page allows documentation in an ecf script to be viewable in ecflow_ui.
        https://confluence.ecmwf.int/display/ECFLOW/Add+Manual
        """
        self.manuals.append(list(text))

    @abstractmethod
    def add_edit(self, text: Union[List[str], str]):
        """
        Adds an edit to either a suite, task, or family. The parent defines
        what object will get the edit object.

        Also edits set variables %VAR%
        """
        self.edits.append(list(text))


    def add_event(self, event):
        """
        Adds an event to the parent node. Events can only be associated with
        families or tasks so if the parent is None, nothing will be added.
        This was done to avoid errors.

        Parameters
        ----------
        event : str
            A string that is passed to the ecflow.Event object
        parent : str
            String for the parent node that will get the events added.

        Returns
        -------
        None
        """
        raise NotImplementedError

        

    @abstractmethod
    def set_trigger(self, trigger: 'Trigger'):
        """
        Adds a trigger to the parent node. Triggers can be added to families
        and tasks.

        ** A node can only have one trigger expression **
        https://confluence.ecmwf.int/display/ECFLOW/Add+Trigger
        """
        if self.trigger != None:
            raise ValueError("Trigger already defined: [%s] -> [%s]", self.name, self.trigger)
        self.trigger = trigger


class Meter:
    """
    A meter is very similar to an event.
    Instead of being a boolean value (on/off), it can take a range of integer values.
    Other tasks are then triggered when the meter reaches a certain value.
    Like events, meter‘s have names and a task can have several of them.

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

class Event:
    """
    An event is a message that a task will report to ecflow_server while it is running.
    Events have names and a task can set several of them.

    https://confluence.ecmwf.int/display/ECFLOW/Add+an+event
    """

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

class Repeat:
    pass

class Trigger:
    """
    Where possible you should give preference to triggers on the definitions, since these are checked on creation, whereas embedded triggers are checked at run time.

    Embeded triggers?
    https://confluence.ecmwf.int/display/ECFLOW/Embedded+Triggers
    """

class Task(Node):
    """represents task"""
    def __init__(self, name):
        self.trigger: Union[Trigger,None] = None
        super().__init__(name)
    

    def add_cron(self):
        """
        https://confluence.ecmwf.int/display/ECFLOW/Add+a+Cron
        """
        pass

    def add_label(self):
        """
        https://confluence.ecmwf.int/display/ECFLOW/Labels
        """
        pass

    
    def add_repeat(self, repeat):
        """https://confluence.ecmwf.int/display/ECFLOW/Repeat
        """

    def add_trigger(self, trigger):
        self.trigger: Union[Trigger,None] = None


class Suite(Node):
    """collection of families"""

    def define_limit(self):
        """https://confluence.ecmwf.int/display/ECFLOW/Limits"""
        pass

class Family(Node):
    """Collection of other families and tasks"""

    def __init__(self, tasks: List[Task], families: List['Family']):
        self.tasks = tasks
        self.families = families

    
    def add_repeat(self, repeat):
        """https://confluence.ecmwf.int/display/ECFLOW/Repeat
        """

    def use_limit(self):
        """https://confluence.ecmwf.int/display/ECFLOW/Limits"""
        pass





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
    search_script = f"{template}.ecf" if template is not \
                                                None else script_name
    if parents:
        script_path = f"{ecfhome}/{suite}/{parents.replace('>','/')}/{script_name}"
    else:
        script_path = f"{ecfhome}/{suite}/{script_name}"
    for root,_,files in os.walk(scriptrepo):
        if search_script in files and ecfscript is None:
            ecfscript = os.path.join(root, search_script)
    if ecfscript is not None:
        shutil.copyfile(ecfscript, script_path, follow_symlinks=True)
        




