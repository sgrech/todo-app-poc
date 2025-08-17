# Prompt 2: Basic Todo CRUD Package (With Quality Gates)

You are tasked with implementing a Python package for basic todo management. This is a purely functional library - no CLI or GUI interfaces needed.

## Requirements

Create a `todo` package that provides CRUD operations for managing todo items. The package should:

1. **Use SQLite as the database backend** with SQLAlchemy ORM
2. **Use Alembic for database migrations**  
3. **Be purely functional** - all functions should be importable from the main package
4. **Follow the interface defined by the integration tests**
5. **PASS ALL QUALITY GATES before proceeding to the next function**

## Project Setup with uv

Use `uv` for all dependency management and script execution:

```bash
# Initialize project
uv init --python 3.10

# Add core dependencies
uv add sqlalchemy alembic

# Add quality gate tools
uv add --dev pytest ruff pyright vulture
```

## Quality Gates - MANDATORY

You MUST set up and use these quality gates from the very beginning:

### 1. Ruff (Linting and Formatting)
```bash
uv run ruff check .          # Linting
uv run ruff format .         # Formatting
```

### 2. Pyright (Type Checking)
```bash
uv run pyright .            # Type checking
```

### 3. Vulture (Dead Code Detection)
```bash
uv run vulture .            # Find unused code
```

### 4. Pytest (Testing)
```bash
uv run pytest tests/        # Run tests
```

## CRITICAL IMPLEMENTATION APPROACH

**IMPLEMENT ONE FUNCTION AT A TIME** and ensure ALL quality gates pass before moving to the next function:

1. **Set up quality gate configuration first**
2. **Implement each function incrementally**
3. **After each function, run ALL quality gates:**
   - `uv run ruff check .` (must pass with no errors)
   - `uv run ruff format .` (apply formatting)
   - `uv run pyright .` (must pass with no type errors)
   - `uv run vulture .` (check for unused code)
   - `uv run pytest tests/test_integration_phase1.py -v` (relevant tests must pass)
4. **Do NOT implement the next function until current one passes all gates**
5. **Fix any quality gate violations immediately**

## Implementation Order

Implement in this exact order, ensuring quality gates pass at each step:

1. **Project setup and configuration** (pyproject.toml, quality gate configs)
2. **Database models** (models.py)
3. **Database connection setup** (database.py)
4. **Alembic configuration and initial migration**
5. **init_db function**
6. **create_todo function**
7. **get_todo function**
8. **list_todos function**
9. **update_todo function**
10. **delete_todo function**

## Expected Package Structure

```
.
├── pyproject.toml      # Project config with uv and quality gate settings
├── todo/
│   ├── __init__.py      # Main package exports with proper type hints
│   ├── models.py        # SQLAlchemy models with full typing
│   ├── database.py      # Database connection and setup
│   ├── crud.py          # CRUD operations with type annotations
│   ├── py.typed         # Mark package as typed
│   └── alembic/         # Migration files
│       ├── alembic.ini
│       ├── env.py
│       ├── script.py.mako
│       └── versions/
└── tests/
    └── test_integration_phase1.py
```

## Quality Gate Configuration

### pyproject.toml example:
```toml
[project]
name = "todo"
version = "0.1.0"
description = "Todo management package"
requires-python = ">=3.10"
dependencies = [
    "sqlalchemy>=2.0.0",
    "alembic>=1.8.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
    "pyright>=1.1.0",
    "vulture>=2.7",
]

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "W", "C90", "I", "N", "UP", "YTT", "S", "BLE", "FBT", "B", "A", "COM", "C4", "DTZ", "T10", "EM", "EXE", "FA", "ISC", "ICN", "G", "INP", "PIE", "T20", "PYI", "PT", "Q", "RSE", "RET", "SLF", "SLOT", "SIM", "TID", "TCH", "INT", "ARG", "PTH", "TD", "FIX", "ERA", "PD", "PGH", "PL", "TRY", "FLY", "NPY", "AIR", "PERF", "FURB", "LOG", "RUF"]

[tool.pyright]
include = ["todo"]
typeCheckingMode = "strict"
reportMissingTypeStubs = false
```

## Core Functions to Implement (with proper typing)

Your package must implement these functions with full type annotations:

1. `init_db(db_path: str) -> None` - Initialize database and run migrations
2. `create_todo(title: str, description: str = "", db_path: str) -> int` - Create todo, return ID
3. `get_todo(todo_id: int, db_path: str) -> dict[str, Any] | None` - Get todo by ID
4. `update_todo(todo_id: int, db_path: str, title: str | None = None, description: str | None = None, completed: bool | None = None) -> bool` - Update todo
5. `delete_todo(todo_id: int, db_path: str) -> bool` - Delete todo
6. `list_todos(db_path: str, completed: bool | None = None) -> list[dict[str, Any]]` - List todos with optional filtering

## Database Schema

The todo table should have these fields:
- `id` (primary key, auto-increment)
- `title` (string, required)
- `description` (string, optional)
- `completed` (boolean, default False)
- `created_at` (timestamp)
- `updated_at` (timestamp)

## Integration Tests

Your implementation must pass the integration tests in `tests/test_integration_phase1.py`. Run tests frequently to ensure you're on track.

## Quality Standards

- **No unused imports** (ruff will catch these)
- **No type errors** (pyright will catch these)
- **No unused code** (vulture will catch these)
- **Consistent formatting** (ruff format will handle this)
- **All tests passing** (pytest will verify this)

## Implementation Steps

1. **Initialize project**: `uv init --python 3.10`
2. **Add dependencies**: `uv add sqlalchemy alembic && uv add --dev pytest ruff pyright vulture`
3. **Configure pyproject.toml with quality gate settings**
4. **Set up basic package structure with __init__.py**
5. **Run quality gates to ensure setup is clean**: `uv run ruff check . && uv run pyright . && uv run vulture .`
6. **Implement models.py with full type annotations**
7. **Run quality gates (fix any issues before continuing)**
8. **Implement database.py**
9. **Run quality gates (fix any issues before continuing)**
10. **Set up Alembic configuration**
11. **Run quality gates (fix any issues before continuing)**
12. **Continue with each function, running quality gates after each implementation**

## Quality Gate Commands

Use these `uv run` commands for all quality checks:

```bash
# Run all quality gates in sequence
uv run ruff check .
uv run ruff format .
uv run pyright .
uv run vulture .
uv run pytest tests/test_integration_phase1.py -v

# Fix issues immediately when they arise
uv run ruff check . --fix        # Auto-fix some issues
uv run ruff format .             # Apply formatting
```

## IMPORTANT REMINDERS

- **Quality gates are not optional suggestions - they are mandatory checkpoints**
- **Do not proceed to the next function if any quality gate fails**
- **Fix all issues immediately when they arise**
- **Type annotations are required on all functions**
- **All code must be formatted with ruff**
- **No unused imports or dead code allowed**
- **Every function must have tests passing before moving on**

The integration tests are your specification, and the quality gates ensure your code is maintainable and robust. Success is measured by both functionality AND code quality.
