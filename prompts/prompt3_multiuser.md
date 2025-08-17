# Prompt 3: Add Multi-User Functionality

You have successfully implemented a basic todo CRUD package. Now you need to extend it with multi-user functionality while maintaining all existing Phase 1 functionality.

## New Requirements

Extend your existing `todo` package to support multiple users, where each user can manage their own separate todo list. The package should:

1. **Add user management functionality**
2. **Add user-scoped todo operations**  
3. **Maintain backward compatibility** with all Phase 1 functions
4. **Ensure complete user isolation** - users can only access their own todos
5. **Continue following quality gates** (if you implemented with gates)
6. **Use uv for any additional dependencies**: `uv add <package-name>`

## New Integration Tests

Your implementation must pass the integration tests in `tests/test_integration_phase2.py`. These tests define the exact expected behavior for the multi-user functionality.

## Database Schema Changes

### New User Table
Add a `users` table with these fields:
- `id` (primary key, auto-increment)
- `username` (string, unique, required)
- `email` (string, unique, required)
- `created_at` (timestamp)

### Modified Todo Table
Update the existing `todos` table to include:
- `user_id` (foreign key to users.id, nullable for backward compatibility)

## New Functions to Implement

Add these functions to your package (importable from `todo`):

### User Management
1. `create_user(username: str, email: str, db_path: str) -> int`
   - Create a new user with unique username and email
   - Raise exception for duplicate username or email
   - Return user ID

2. `get_user(user_id: int, db_path: str) -> dict[str, Any] | None`
   - Retrieve user by ID
   - Return dict with keys: id, username, email, created_at
   - Return None if not found

3. `get_user_by_username(username: str, db_path: str) -> dict[str, Any] | None`
   - Retrieve user by username
   - Return user dict or None if not found

### User-Scoped Todo Operations
4. `create_user_todo(user_id: int, title: str, description: str = "", db_path: str) -> int`
   - Create todo for specific user
   - Return todo ID

5. `get_user_todo(user_id: int, todo_id: int, db_path: str) -> dict[str, Any] | None`
   - Get todo only if it belongs to the user
   - Return None if todo doesn't exist or doesn't belong to user

6. `update_user_todo(user_id: int, todo_id: int, db_path: str, title: str | None = None, description: str | None = None, completed: bool | None = None) -> bool`
   - Update todo only if it belongs to the user
   - Return False if todo doesn't exist or doesn't belong to user

7. `delete_user_todo(user_id: int, todo_id: int, db_path: str) -> bool`
   - Delete todo only if it belongs to the user
   - Return False if todo doesn't exist or doesn't belong to user

8. `list_user_todos(user_id: int, db_path: str, completed: bool | None = None) -> list[dict[str, Any]]`
   - List todos for specific user only
   - Optional filtering by completion status

## Critical Requirements

### 1. Backward Compatibility
All Phase 1 functions (`create_todo`, `get_todo`, `update_todo`, `delete_todo`, `list_todos`) must continue to work exactly as before. Existing code using these functions should not break.

### 2. User Isolation
- Users must only be able to access their own todos
- User-scoped functions should return None/False when trying to access other users' todos
- No cross-user data leakage allowed

### 3. Database Migration
- Create proper Alembic migration to add the users table
- Add user_id column to todos table (nullable for backward compatibility)
- Ensure existing todos continue to work

## Implementation Approach

### If You Used Quality Gates (Prompt 2):
Continue using the same quality gate approach:
1. **Implement one function at a time**
2. **Run all quality gates after each function**
3. **Fix any violations before proceeding**
4. **Maintain type annotations and code quality**

### If You Didn't Use Quality Gates (Prompt 1):
Implement all functionality to pass the integration tests, focusing on:
1. **Functional correctness**
2. **Backward compatibility**
3. **User isolation**

## Testing

Your implementation must pass:
1. **All Phase 1 tests** - `uv run pytest tests/test_integration_phase1.py`
2. **All Phase 2 tests** - `uv run pytest tests/test_integration_phase2.py`

The Phase 2 tests include specific tests for backward compatibility to ensure Phase 1 functionality still works.

### If Using Quality Gates:
Continue running all quality gates after each implementation:
```bash
uv run ruff check .
uv run ruff format .
uv run pyright .
uv run vulture .
uv run pytest tests/ -v
```

## Implementation Notes

- Consider how to handle the nullable user_id in existing todos
- Think about the relationship between users and todos in your SQLAlchemy models
- Ensure proper foreign key constraints
- Handle edge cases like non-existent users gracefully
- Maintain the same error handling patterns established in Phase 1

## Database Relationships

```
users (1) ----< todos (many)
         user_id (foreign key)
```

## Expected Package Updates

Update your existing files:
- `models.py` - Add User model, update Todo model with user_id
- `crud.py` - Add user management and user-scoped CRUD functions
- `__init__.py` - Export new functions
- `alembic/versions/` - Add migration for new schema

## Success Criteria

1. ✅ All Phase 1 integration tests pass
2. ✅ All Phase 2 integration tests pass  
3. ✅ Users can only access their own todos
4. ✅ Backward compatibility maintained
5. ✅ Database migration works properly
6. ✅ (If using quality gates) All quality gates pass

Your goal is to extend the functionality while maintaining the quality and reliability of the existing codebase.
