"""Task model for the project tracker."""

from __future__ import annotations


class Task:
    """Represents an actionable task within a project."""

    _next_id = 1

    def __init__(self, title: str, status: str = "pending", assigned_to: str | None = None, task_id: int | None = None):
        self.title = title
        self.status = status
        self.assigned_to = assigned_to
        self.task_id = task_id if task_id is not None else Task._next_id
        Task._next_id = max(Task._next_id, self.task_id + 1)

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value or not value.strip():
            raise ValueError("Task title cannot be empty")
        self._title = value.strip()

    def complete(self) -> None:
        """Mark the task as complete."""
        self.status = "complete"

    def to_dict(self) -> dict:
        return {
            "id": self.task_id,
            "title": self.title,
            "status": self.status,
            "assigned_to": self.assigned_to,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(data["title"], data.get("status", "pending"), data.get("assigned_to"), task_id=data.get("id", None))

    def __str__(self) -> str:
        return f"{self.title} [{self.status}]"
