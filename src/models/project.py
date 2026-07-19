"""Project model for the project tracker."""

from __future__ import annotations


class Project:
    """Represents a project owned by a user and containing tasks."""

    _next_id = 1

    def __init__(self, title: str, description: str, due_date: str, user_id: int | None = None, project_id: int | None = None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.user_id = user_id if user_id is not None else 0
        self.project_id = project_id if project_id is not None else Project._next_id
        self.tasks = []
        Project._next_id = max(Project._next_id, self.project_id + 1)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value.strip()

    def add_task(self, task) -> None:
        """Add a task to the project."""
        self.tasks.append(task)

    def to_dict(self) -> dict:
        return {
            "id": self.project_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "user_id": self.user_id,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        project = cls(
            data["title"],
            data.get("description", ""),
            data.get("due_date", ""),
            user_id=data.get("user_id", 0),
            project_id=data.get("id", None),
        )
        return project

    def __str__(self) -> str:
        return f"{self.title} (due {self.due_date})"
