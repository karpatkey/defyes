from typing import Iterator

from defyes.generator import camel_to_snake


class DefaultNameFromClass:
    def __get__(self, instance, owner=None) -> str | None:
        return camel_to_snake(owner.__name__) if owner else None


class InstancesManager:
    def __init__(self, manager=None, owner: type = None):
        if manager:
            self._index = manager._index
        else:
            self._index = dict()
        self.owner = owner

    def __get__(self, instance, owner=None):
        return InstancesManager(self, owner)

    def filter(self, **kwargs) -> Iterator:
        for obj in set(self._index.values()):
            if isinstance(obj, self.owner) and all(getattr(obj, attr, None) == value for attr, value in kwargs.items()):
                yield obj

    @property
    def all(self) -> list:
        return list(self.filter())

    def get(self, **kwargs):
        for index_attrs in self.owner.indexes:
            try:
                index = tuple(kwargs[attr] for attr in index_attrs)
            except KeyError:
                continue
            return self._index[index]
        raise LookupError(f"Not found for {self.owner} and {kwargs!r}")

    def create(self, **kwargs):
        obj = self.owner(**kwargs)
        self.add_or_replace(obj)
        return obj

    def add_or_replace(self, obj):
        """
        Add a new obj. Replace if it already exists.
        """
        for index_attrs in self.owner.indexes:
            index = tuple(getattr(obj, attr) for attr in index_attrs)
            self._index[index] = obj

    def get_or_create(self, **kwargs):
        try:
            return self.get(**kwargs)
        except LookupError:
            return self.create(**kwargs)
