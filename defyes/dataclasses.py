def repr_for(*attrs):
    """
    Easy create your class repr function including the specific attributes `attrs`.

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
    No magical alternative to mitigate the extreme complexity of dataclasses when dealing with inheritance.
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
        Make derivative clases with "fozen" instances to reduce incoherent states and all the good behaviours of
        inmutable data ;)
        """
        raise Exception("read-only")
