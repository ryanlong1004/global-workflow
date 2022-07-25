import pytest
from ecflow_definitions_v2 import Family, Suite, Task


@pytest.fixture
def _setup():
    suite = Suite("root_suite", None)
    family = Family("first family", suite)
    task = Task("my_task", family)
    family2 = Family("second family", family)
    task2 = Task("my 2nd task", family)
    Task3 = Task("abcd", family)
    task4 = Task("efgh", None)
    family2.add_task(task4)

    task4.add_manual("this is cool")
    task4.add_manual(["so it this", "this too"])
    task4.add_edit("abcd = efgh")

    print(task4.manuals)
    print(task4.edits)
    print(task4.traverse_up())
    print(task4.traverse_down())
    print(suite.traverse_down())
    print(suite.local_path)
    print(task4.local_path)


def test_suite():
    """tests the Suite class"""
    suite = Suite("root_suite", None)
    family = Family("first family", suite)
    task = Task("my_task", family)
    task2 = Task("my_task2", None)

    assert suite.name == "root_suite"
    assert len(suite.children) == 1

    suite.add_child(task2)
    assert len(suite.children) == 2
    assert len(suite.traverse_down()) == 4
    assert len(suite.traverse_up()) == 1


def test_family():
    """tests the Suite class"""
    suite = Suite("root_suite", None)
    family = Family("first family", suite)
    task = Task("my_task", family)
    task2 = Task("my_task2", None)

    assert family.name == "first family"
    assert len(family.children) == 1

    family.add_child(task2)
    assert len(family.children) == 2
    assert len(family.traverse_down()) == 3
    assert len(family.traverse_up()) == 2


def test_task():
    """tests the Suite class"""
    suite = Suite("root_suite", None)
    family = Family("first family", suite)
    task = Task("my_task", family)
    task2 = Task("my_task2", None)

    assert task.name == "my_task"
    assert len(task.children) == 0

    task.add_manual("this is for users and not code")
    assert len(task.children) == 0
    assert len(task.traverse_down()) == 1
    assert len(task.traverse_up()) == 3
