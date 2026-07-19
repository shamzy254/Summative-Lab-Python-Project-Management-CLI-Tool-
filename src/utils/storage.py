"""Utility helpers for persisting tracker data to JSON files."""

from __future__ import annotations

import json
from pathlib import Path
from typing import List

from models.user import User
from models.project import Project
from models.task import Task


class DataStore:
    """Persists users, projects, and tasks to a local JSON file."""

    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path is not None else Path("data/data.json")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{\"users\": [], \"projects\": [], \"tasks\": []}", encoding="utf-8")

    def load_users(self) -> List[User]:
        data = self._read_data()
        users = [User.from_dict(item) for item in data.get("users", [])]
        projects = self.load_projects()
        for user in users:
            user.projects = [project for project in projects if project.user_id == user.id]
        return users

    def load_projects(self) -> List[Project]:
        data = self._read_data()
        return [Project.from_dict(item) for item in data.get("projects", [])]

    def load_tasks(self) -> List[Task]:
        data = self._read_data()
        return [Task.from_dict(item) for item in data.get("tasks", [])]

    def save_users(self, users: List[User]) -> None:
        data = self._read_data()
        data["users"] = [user.to_dict() for user in users]
        self._write_data(data)

    def save_projects(self, projects: List[Project]) -> None:
        data = self._read_data()
        data["projects"] = [project.to_dict() for project in projects]
        self._write_data(data)

    def save_tasks(self, tasks: List[Task]) -> None:
        data = self._read_data()
        data["tasks"] = [task.to_dict() for task in tasks]
        self._write_data(data)

    def _read_data(self) -> dict:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {"users": [], "projects": [], "tasks": []}

    def _write_data(self, data: dict) -> None:
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")
