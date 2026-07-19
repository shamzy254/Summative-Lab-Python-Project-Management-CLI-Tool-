import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from models.person import Person
from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import DataStore


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.temp_dir.name) / "data.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_person_name_validation(self):
        person = Person("Alex")
        self.assertEqual(person.name, "Alex")

        with self.assertRaises(ValueError):
            Person("")

    def test_user_project_relationship(self):
        user = User("Alex", "alex@example.com")
        project = Project("CLI Tool", "Build CLI", "2026-08-01", user_id=user.id)
        user.add_project(project)

        self.assertEqual(len(user.projects), 1)
        self.assertEqual(user.projects[0].title, "CLI Tool")

    def test_task_completion_and_assignment(self):
        task = Task("Implement CLI", "pending", assigned_to="Alex")
        task.complete()
        self.assertEqual(task.status, "complete")

    def test_storage_round_trip(self):
        store = DataStore(self.storage_path)
        user = User("Alex", "alex@example.com")
        project = Project("CLI Tool", "Build CLI", "2026-08-01", user_id=user.id)
        user.add_project(project)
        store.save_users([user])
        store.save_projects([project])
        store.save_tasks([])

        reloaded = DataStore(self.storage_path)
        self.assertEqual(len(reloaded.load_users()), 1)
        self.assertEqual(len(reloaded.load_projects()), 1)

    def test_reloaded_users_keep_projects(self):
        store = DataStore(self.storage_path)
        user = User("Alex", "alex@example.com")
        project = Project("CLI Tool", "Build CLI", "2026-08-01", user_id=user.id)
        user.add_project(project)
        store.save_users([user])
        store.save_projects([project])

        reloaded = DataStore(self.storage_path)
        reloaded_user = reloaded.load_users()[0]
        self.assertEqual(len(reloaded_user.projects), 1)
        self.assertEqual(reloaded_user.projects[0].title, "CLI Tool")

    def test_storage_recovers_from_invalid_root_json(self):
        self.storage_path.write_text("[]", encoding="utf-8")
        store = DataStore(self.storage_path)

        self.assertEqual(store.load_users(), [])
        self.assertEqual(store.load_projects(), [])
        self.assertEqual(store.load_tasks(), [])


if __name__ == "__main__":
    unittest.main()
