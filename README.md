# Project Tracker CLI

A Python-based command-line tool for managing users, projects, tasks, and their relationships.

## Features

- Create and list users
- Add projects to users and view projects by user
- Add tasks to projects and mark them complete
- Update existing project details
- Persist data locally in JSON files
- Use object-oriented models with clear relationships between users, projects, and tasks
- Support a custom storage file path for flexible data location

## Setup

1. Create and activate a virtual environment if desired.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install the CLI as a package for deployment-style usage:
   ```bash
   pip install .
   ```
4. Run the CLI:
   ```bash
   python main.py add-user --name Alex --email alex@example.com
   ```

## Available Commands

```bash
python main.py add-user --name Alex --email alex@example.com
python main.py list-users
python main.py add-project --user Alex --title "CLI Tool" --description "Build a CLI" --due-date 2026-08-01
python main.py add-task --project "CLI Tool" --title "Implement add-task"
python main.py list-projects --user Alex
python main.py list-tasks
python main.py complete-task --title "Implement add-task"
python main.py update-project --project "CLI Tool" --description "Build a robust CLI tool"
```

## Custom Storage File

You can store data in a different JSON file if needed:

```bash
python main.py --storage /path/to/data.json list-users
```

## Testing

Run the test suite with:

```bash
python -m pytest -q
```

## Project Structure

- src/app.py - CLI entry point and command handling
- src/models - User, Project, Task, and Person model classes
- src/utils/storage.py - JSON persistence layer
- tests - Unit tests for models and storage behavior
