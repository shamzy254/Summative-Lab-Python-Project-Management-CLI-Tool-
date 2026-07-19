"""Base model for person-like entities."""


class Person:
    """Represents a human entity with a validated name."""

    def __init__(self, name: str):
        self.name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()

    def __str__(self) -> str:
        return self.name
