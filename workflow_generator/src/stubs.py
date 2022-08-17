from typing import Any


class Root(object):  # from where Suite and Node derive
    """generic tree node"""

    def __init__(self):
        self.load = None  # to be filled with ecFlow item
        # CWN(self)

    @property
    def real(self):
        return self.load

    def __enter__(self):
        # CWN(self)
        return iter([])

    def __exit__(self, type, value, traceback):
        pass

    def __get_attr__(self, attr):
        return getattr(self.load, attr)

    def get_parent(self):
        pass

    def __str__(self):
        return self.fullname()

    def __repr__(self):
        return "%s" % self.load

    def is_eq(self, node):
        """return super(self, self.__eq__), (self, node)"""

    def __eq__(self, node):
        """
        if isinstance(self.load, stubs.Node):
            return "%s == " % self + str(node)
        return self  # False
        """

    def __ne__(self, node):
        """
        if isinstance(self.load, stubs.Node):
            return "%s != " % self + str(node)
        return False
        """

    def __and__(self, node):
        """
        if isinstance(self.load, stubs.Node):
            return "%s and " % self + str(node)
        return False
        """

    def __or__(self, node):
        """
        if isinstance(self.load, stubs.Alias):
            return True
        if isinstance(self.load, stubs.Node):
            return "%s or " % self + str(node)
        return False
        """

    def get_abs_node_path(self):
        return self.fullname()

    def fullname(self):
        """simple syntax"""
        pass

    def repeat(self, name="YMD", start=20120101, end=20321212, step=1, kind="date"):
        """add repeat attribute"""
        pass

    def __add__(self, item):
        self.add(item)

    def append(self, item=None, *args):
        """we get compatible with list then"""
        return self.add(item, args)

    def add(self, item=None, *args):
        """add a task, a family or an attribute"""
        return self

    def limit(self, name=None, size=1, inlimit=0):
        """add limit attribute"""
        return self

    def inlimit(self, full_path):
        """add inlimit attribute"""
        return self

    # follow pyflow
    shape = None

    def draw_tree(self):
        pass

    def _tree(self, dot):
        pass

    def draw_graph(self):
        pass

    def _graph(self, dot):
        pass

    def to_html(self):
        # from .html import HTMLWrapper
        pass

    def _repr_html_(self):
        return str(self.to_html())


class Node(Root):  # from where Task and Family derive
    """Node class is shared by family and task"""

    def __enter__(self):
        return self

    # def __exit__(self, exc_type, exc_val, exc_tb): pass  # return self

    def events(self):
        pass

    def meters(self):
        pass

    def name(self):
        pass

    def find_variable(self, name):
        if self.load:
            return self.load.find_variable(name)
        return None

    # def event(self, name=1):
    #     """ add event attribute"""
    #     if USE_EVENT:
    #         self.load.add_event(name)
    #     return self

    # def meter(self, name, start, end, threshold=None):
    #     """ add meter attribute"""
    #     if threshold is None:
    #         threshold = end
    #     self.load.add_meter(name, start, end, threshold)
    #     return self

    # def label(self, name, default=""):
    #     """ add label attribute"""
    #     self.load.add_label(name, default)
    #     return self

    def edit(self, name, value=""):
        """add variable attribute"""
        print(f"adding edit {name}:{value}")

    def variable(self, name, value=""):
        """add variable attribute"""

    def cron(self, time, dom=False, wdays=False, month=False):
        """wrapper for add_cron"""

    def complete(self, arg):
        """add complete attribute"""

    def complete_and(self, arg):
        """append to existing complete"""

    def complete_or(self, arg):
        """append to existing complete"""

    def up(self):
        """get parent, one level up"""


class Defs(object):
    """wrapper for the definition"""

    def __init__(self):
        self.load = []

    def __get_attr__(self, attr):
        return getattr(self.load, attr)

    @property
    def real(self):
        return self.load

    def auto_add_externs(self, true):
        pass

    def check(self):
        pass

    def simulate(self):
        pass

    def generate_scripts(self):
        pass

    def add_extern(self, path):
        pass

    def save_as_defs(self, fname):
        pass

    def get_all_tasks(self):
        pass

    def suites(self):
        pass

    def add_suite(self, node):
        pass

    def __str__(self):
        return "%s" % self.load

    __repr__ = __str__

    def __add__(self, item):
        self.add(item)

    def append(self, item=None, *args):
        """get compatible with list"""
        pass

    def add(self, item):
        pass

    def find_abs_node(self, name):
        pass

    def find_node(self, name):
        pass

    def suite(self, name):
        """add suite providing its name"""
        suite = Suite(name)
        self.add(suite)
        return suite


class Client(object):
    """wrapper around client"""

    def __init__(self, host="localhost", port="31415"):
        self.host = host
        self.port = port

    def load(self, defs):
        pass

    def get_file(self, node, kind="script"):
        pass

    def replace(self, path, defs=None, parent=True, force=False):
        pass

    def suites(self):
        pass

    def begin_suite(self, name):
        pass

    def resume(self, path):
        pass

    def suspend(self, path):
        pass

    def ping(self):
        pass

    def version(self):
        pass

    def __str__(self):
        pass


class Suite(Root):
    """wrapper for a suite"""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __init__(self, name):
        pass

    def name(self):
        pass

    def family(self, name):
        """add a family"""
        pass

    def task(self, name):
        """add a task"""
        pass

    def add_to(self, defs):
        pass

    # def __enter__(self): return self

    # def __exit__(self, *args): pass


class Family(Node):
    """wrapper around family"""

    def __init__(self, name):
        pass

    def family(self, name):
        """add a family"""
        pass

    def task(self, name):
        """add a task"""
        pass

    def add_to(self, node):
        pass

    def nodes(self):
        pass

    # def __enter__(self): return self

    # def __exit__(self, *args): pass


class Task(Node):
    """wrapper around task"""

    def __init__(self, name):
        pass

    def add_to(self, node):
        pass

    def add_family(self, node):
        pass

    def add_task(self, node):
        pass


class Alias(Root):  # from where Suite and Node derive
    def __get_attr__(self, attr):
        return None

    def nodes(self):
        return None


class Edit:
    def __init__(self, *args, **kwargs):
        pass


class Trigger:
    def __init__(self, *args, **kwargs):
        pass


class Event:
    def __init__(self, *args, **kwargs):
        pass
