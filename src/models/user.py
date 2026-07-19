"""User model for the project tracker."""

from __future__ import annotations

from .person import Person


class User(Person):
    """Represents a user who can own multiple projects."""

    _next_id = 1

    def __init__(self, name: str, email: str, user_id: int | None = None):
        super().__init__(name)
        self.email = email
        self.user_id = user_id if user_id is not None else User._next_id
        self.projects = []
        User._next_id = max(User._next_id, self.user_id + 1)

    @property
    def id(self) -> int:
        return self.user_id

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        if "@" not in value:
            raise ValueError("Email must contain '@'")
        self._email = value

    def add_project(self, project) -> None:
        """Attach a project to this user."""
        self.projects.append(project)

    def to_dict(self) -> dict:
        return {
            "id": self.user_id,
            "name": self.name,
            "email": self.email,
            "projects": [project.title for project in self.projects],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "User":
        user = cls(data["name"], data["email"], user_id=data.get("id", None))
        return user

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
