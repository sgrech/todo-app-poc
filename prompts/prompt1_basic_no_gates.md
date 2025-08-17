# Prompt 1: Basic Todo CRUD Package (No Quality Gates)

You are tasked with implementing a Python package for basic todo management. This is a purely functional library - no CLI or GUI interfaces needed.

## Requirements

Create a `todo` package that provides CRUD operations for managing todo items. The package should:

1. **Use SQLite as the database backend** with SQLAlchemy ORM
2. **Use Alembic for database migrations**  
3. **Be purely functional** - all functions should be importable from the main package
4. **Follow the interface defined by the integration tests**

## Project Setup

Use `uv` for dependency management and Python package handling:

```bash
# Initialize project with uv
uv init --python 3.10
uv add sqlalchemy alembic pytest
```

## Expected Package Structure

```
.
├── pyproject.toml       # Project configuration with uv
├── todo/
│   ├── __init__.py      # Main package exports
│   ├── models.py        # SQLAlchemy models
│   ├── database.py      # Database connection and setup
│   ├── crud.py          # CRUD operations
│   └── alembic/         # Migration files
│       ├── alembic.ini
│       ├── env.py
│       ├── script.py.mako
│       └── versions/
└── tests/
    └── test_integration_phase1.py
```

## Core Functions to Implement

Your package must implement these functions (importable from `todo`):

1. `init_db(db_path: str) -> None` - Initialize database and run migrations
2. `create_todo(title: str, description: str = "", db_path: str) -> int` - Create todo, return ID
3. `get_todo(todo_id: int, db_path: str) -> dict | None` - Get todo by ID
4. `update_todo(todo_id: int, db_path: str, title: str = None, description: str = None, completed: bool = None) -> bool` - Update todo
5. `delete_todo(todo_id: int, db_path: str) -> bool` - Delete todo
6. `list_todos(db_path: str, completed: bool = None) -> list[dict]` - List todos with optional filtering

## Database Schema

The todo table should have these fields:
- `id` (primary key, auto-increment)
- `title` (string, required)
- `description` (string, optional)
- `completed` (boolean, default False)
- `created_at` (timestamp)
- `updated_at` (timestamp)

## Integration Tests

Your implementation must pass the integration tests in `tests/test_integration_phase1.py`. These tests define the exact expected behavior and interface.

Key test expectations:
- All functions work with temporary SQLite databases
- Proper error handling for invalid inputs
- Correct data types and structure in returned dictionaries
- Database initialization works properly
- CRUD operations work as expected

## Dependencies Management

Use `uv` to manage dependencies:

```bash
# Core dependencies
uv add sqlalchemy alembic

# Testing dependencies
uv add --dev pytest
```

Required packages:
- `sqlalchemy` - ORM
- `alembic` - Database migrations  
- `pytest` - For running tests

## Implementation Notes

- Focus on getting all tests to pass
- The package should handle database connections efficiently
- Error handling should be appropriate for each operation
- Use SQLAlchemy best practices for the ORM layer
- Make sure the Alembic setup works for database initialization

## Getting Started

1. **Initialize project with uv**: `uv init --python 3.10`
2. **Add dependencies**: `uv add sqlalchemy alembic && uv add --dev pytest`
3. **Set up the basic package structure**
4. **Define the SQLAlchemy models**
5. **Configure Alembic for migrations**
6. **Implement the CRUD functions**
7. **Run tests**: `uv run pytest tests/test_integration_phase1.py -v`

The integration tests are your specification - make sure your implementation satisfies all test cases.
