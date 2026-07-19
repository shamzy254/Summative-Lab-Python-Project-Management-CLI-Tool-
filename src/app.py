"""CLI entry point for the project tracker."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from rich.console import Console
from rich.table import Table

from models.project import Project
from models.task import Task
from models.user import User
from utils.storage import DataStore

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger("tracker")


class ProjectTrackerCLI:
    """Simple command-line interface for managing users, projects, and tasks."""

    def __init__(self, storage_path: str | Path | None = None):
        self.console = Console()
        self.storage = DataStore(storage_path)
        self.users = self.storage.load_users()
        self.projects = self.storage.load_projects()
        self.tasks = self.storage.load_tasks()

    def add_user(self, name: str, email: str) -> str:
        """Create a new user and persist it."""
        user = User(name, email)
        self.users.append(user)
        self.storage.save_users(self.users)
        logger.info("Added user %s", user.name)
        return f"Added user {user.name}"

    def add_project(self, user_name: str, title: str, description: str, due_date: str) -> str:
        """Create a new project for an existing user."""
        user = self._find_user(user_name)
        if user is None:
            raise ValueError(f"User {user_name} not found")
        project = Project(title, description, due_date, user_id=user.user_id)
        self.projects.append(project)
        user.add_project(project)
        self.storage.save_users(self.users)
        self.storage.save_projects(self.projects)
        logger.info("Added project %s for %s", project.title, user.name)
        return f"Added project {project.title} for {user.name}"

    def add_task(self, project_title: str, title: str, assigned_to: str | None = None) -> str:
        """Attach a task to a project."""
        project = self._find_project(project_title)
        if project is None:
            raise ValueError(f"Project {project_title} not found")
        task = Task(title, assigned_to=assigned_to)
        project.add_task(task)
        self.tasks.append(task)
        self.storage.save_projects(self.projects)
        self.storage.save_tasks(self.tasks)
        logger.info("Added task %s", task.title)
        return f"Added task {task.title} to {project.title}"

    def list_users(self) -> str:
        """Return a human-readable list of users."""
        if not self.users:
            return "No users found"
        table = Table(title="Users")
        table.add_column("Name", style="cyan")
        table.add_column("Email", style="magenta")
        for user in self.users:
            table.add_row(user.name, user.email)
        return table

    def list_projects(self, user_name: str | None = None) -> str:
        """List all projects or a user's assigned projects."""
        if user_name is None:
            projects = self.projects
        else:
            user = self._find_user(user_name)
            if user is None:
                raise ValueError(f"User {user_name} not found")
            projects = user.projects
        if not projects:
            return "No projects found"
        table = Table(title=f"Projects{' for ' + user_name if user_name else ''}")
        table.add_column("Title", style="green")
        table.add_column("Due Date", style="yellow")
        table.add_column("Description")
        for project in projects:
            table.add_row(project.title, project.due_date, project.description)
        return table

    def list_tasks(self) -> str:
        """Return a simple task summary."""
        if not self.tasks:
            return "No tasks found"
        table = Table(title="Tasks")
        table.add_column("Title", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("Assigned To")
        for task in self.tasks:
            table.add_row(task.title, task.status, task.assigned_to or "Unassigned")
        return table

    def complete_task(self, task_title: str) -> str:
        """Mark a matching task as complete."""
        task = self._find_task(task_title)
        if task is None:
            raise ValueError(f"Task {task_title} not found")
        task.complete()
        self.storage.save_tasks(self.tasks)
        logger.info("Completed task %s", task.title)
        return f"Completed task {task.title}"

    def update_project(self, project_title: str, new_title: str | None = None, description: str | None = None, due_date: str | None = None) -> str:
        """Update an existing project's metadata."""
        project = self._find_project(project_title)
        if project is None:
            raise ValueError(f"Project {project_title} not found")
        if new_title:
            project.title = new_title
        if description is not None:
            project.description = description
        if due_date is not None:
            project.due_date = due_date
        self.storage.save_projects(self.projects)
        return f"Updated project {project.title}"

    def _find_user(self, name: str) -> User | None:
        return next((user for user in self.users if user.name.lower() == name.lower()), None)

    def _find_project(self, title: str) -> Project | None:
        return next((project for project in self.projects if project.title.lower() == title.lower()), None)

    def _find_task(self, title: str) -> Task | None:
        return next((task for task in self.tasks if task.title.lower() == title.lower()), None)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Project tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_user = subparsers.add_parser("add-user", help="Add a user")
    add_user.add_argument("--name", required=True)
    add_user.add_argument("--email", required=True)

    subparsers.add_parser("list-users", help="List all users")

    add_project = subparsers.add_parser("add-project", help="Add a project for a user")
    add_project.add_argument("--user", required=True)
    add_project.add_argument("--title", required=True)
    add_project.add_argument("--description", default="")
    add_project.add_argument("--due-date", required=True)

    add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    add_task.add_argument("--project", required=True)
    add_task.add_argument("--title", required=True)
    add_task.add_argument("--assigned-to")

    list_projects = subparsers.add_parser("list-projects", help="List projects")
    list_projects.add_argument("--user")

    subparsers.add_parser("list-tasks", help="List all tasks")

    complete_task = subparsers.add_parser("complete-task", help="Complete a task")
    complete_task.add_argument("--title", required=True)

    update_project = subparsers.add_parser("update-project", help="Update a project")
    update_project.add_argument("--project", required=True)
    update_project.add_argument("--title")
    update_project.add_argument("--description")
    update_project.add_argument("--due-date")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    cli = ProjectTrackerCLI(Path("data/data.json"))
    try:
        if args.command == "add-user":
            print(cli.add_user(args.name, args.email))
        elif args.command == "list-users":
            cli.console.print(cli.list_users())
        elif args.command == "add-project":
            print(cli.add_project(args.user, args.title, args.description, args.due_date))
        elif args.command == "add-task":
            print(cli.add_task(args.project, args.title, args.assigned_to))
        elif args.command == "list-projects":
            cli.console.print(cli.list_projects(args.user))
        elif args.command == "list-tasks":
            cli.console.print(cli.list_tasks())
        elif args.command == "complete-task":
            print(cli.complete_task(args.title))
        elif args.command == "update-project":
            print(cli.update_project(args.project, new_title=args.title, description=args.description, due_date=args.due_date))
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    main()
