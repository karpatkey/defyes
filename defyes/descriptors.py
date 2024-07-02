from typing import Iterator

from defyes.generator import camel_to_snake


class DefaultNameFromClass:
    """
    A descriptor class that returns the snake_case version of the owner class's name when accessed.

    This class uses the `__get__` method to convert the name of the owner class from CamelCase to snake_case.
    If the owner is None, it returns None.

    Example:
        class MyClass:
            name = DefaultNameFromClass()

        obj = MyClass()
        print(obj.name)  # Outputs: 'my_class'
    """

    def __get__(self, instance, owner=None) -> str | None:
        return camel_to_snake(owner.__name__) if owner else None


class InstancesManager:
    """
    A class that manages instances of another class, providing methods to filter, get, create, and replace instances.

    Attributes:
        _index (dict): A dictionary to store instances.
        owner (type): The class of the instances being managed.
    """

    def __init__(self, manager=None, owner: type = None):
        if manager:
            self._index = manager._index
        else:
            self._index = dict()
        self.owner = owner

    def __get__(self, instance, owner=None):
        return InstancesManager(self, owner)

    def filter(self, **kwargs) -> Iterator:
        """
        Yield instances that match the specified keyword arguments.
        If no arguments are provided, it returns all instances.
        """
        for obj in set(self._index.values()):
            if isinstance(obj, self.owner) and all(getattr(obj, attr, None) == value for attr, value in kwargs.items()):
                yield obj

    @property
    def all(self) -> list:
        """
        Return a list of all instances.
        """
        return list(self.filter())

    def get(self, **kwargs):
        """
        Return the first instance that matches the keyword arguments, or raise a LookupError if no match is found.
        It return only one instance, even if there are multiple matches.
        """
        for index_attrs in self.owner.indexes:
            try:
                index = tuple(kwargs[attr] for attr in index_attrs)
            except KeyError:
                continue
            return self._index[index]
        raise LookupError(f"Not found for {self.owner} and {kwargs!r}")

    def create(self, **kwargs):
        """
        Create a new instance with the specified keyword arguments, add it to the index, and return it.
        """
        obj = self.owner(**kwargs)
        self.add_or_replace(obj)
        return obj

    def add_or_replace(self, obj):
        """
        Add a new instance to the index. If an instance with the same index attributes already exists, replace it.
        """
        for index_attrs in self.owner.indexes:
            index = tuple(getattr(obj, attr) for attr in index_attrs)
            self._index[index] = obj

    def get_or_create(self, **kwargs):
        """
        Return the first instance that matches the specified keyword arguments. If no match is found, create a new instance.
        """
        try:
            return self.get(**kwargs)
        except LookupError:
            return self.create(**kwargs)
