"""
This module provides utility functions and classes for working with data classes in Python.

It includes the following:

- `repr_for(*attrs)`: A function that simplifies the creation of a `__repr__` method for your class by including specific attributes.

- `repr_dict()`: A function that creates a `__repr__` method for your class that includes all attributes.

- `FrozenKwInit`: A base class that provides a frozen, read-only implementation of keyword-based initialization.
"""


def repr_for(*attrs):
    """
    This function simplifies the creation of a `__repr__` method for your class by including specific attributes.

    The `__repr__` method returns a string that describes how to recreate the object in Python code.

    Example:
        class A:
            ...
            __repr__ = repr_for("a", "b")

        repr(A(...)) -> "A(a=1, b=2)"
    """

    def __repr__(self):
        pairs = ", ".join(f"{name}={getattr(self, name)!r}" for name in attrs)
        return f"{self.__class__.__name__}({pairs})"

    return __repr__


def repr_dict():
    def __repr__(self):
        pairs = ", ".join(f"{name}={value!r}" for name, value in vars(self).items())
        return f"{self.__class__.__name__}({pairs})"

    return __repr__


class FrozenKwInit:
    """
    A base class that provides a frozen, read-only implementation of keyword-based initialization for data classes.

    This class allows setting all keyword arguments defined by `attrs` as instance attributes.

    Methods:
        __post_init__: Can be overridden in subclasses instead of `__init__`.
        __setattr__: Raises an exception to ensure instances remain "frozen" and immutable.

    By using `FrozenKwInit` as a base class, derivative classes can have "frozen" instances, which helps reduce
    incoherent states and ensures the immutability of data.
    """

    def __init__(self, /, **attrs):
        """
        Set all keyword arguments defined by `attrs` as instance attributes.
        Call __post_init__, like dataclass.
        """
        self.__dict__.update(attrs)
        self.__post_init__()

    def __post_init__(self):
        """
        Override this method in subclasses instead of __init__.
        """

    def __setattr__(self, name, value):
        """
        Make derivative classes with "frozen" instances to reduce incoherent states and ensure all the good behaviors of
        immutable data.
        """
        raise Exception("read-only")
