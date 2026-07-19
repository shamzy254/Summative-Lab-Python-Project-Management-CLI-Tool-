# Project Tracker CLI

A Python-based command-line tool for managing users, projects, tasks, and their relationships.

## Features

- Create and list users
- Add projects to users and view projects by user
- Add tasks to projects and mark them complete
- Persist data locally with JSON files
- Use object-oriented models with relationships between users, projects, and tasks

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
4. Run the installed CLI:
   ```bash
   project-tracker add-user --name Alex --email alex@example.com
   ```

## Example Commands

```bash
python main.py add-user --name Alex --email alex@example.com
python main.py add-project --user Alex --title "CLI Tool" --description "Build a CLI" --due-date 2026-08-01
python main.py add-task --project "CLI Tool" --title "Implement add-task"
python main.py list-projects --user Alex
python main.py complete-task --title "Implement add-task"
```

## Testing

Run the test suite with:

```bash
python -m unittest discover -s tests
```
