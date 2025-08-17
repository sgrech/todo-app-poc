"""
Phase 1 Integration Tests: Basic Todo CRUD Operations

These tests define the expected interface and behavior for a basic todo management package.
The implementation should be purely functional - no CLI or GUI interfaces.

Expected package structure:
- A todo package with CRUD operations
- SQLite database backend using SQLAlchemy
- Alembic for database migrations
- All functions should be importable from the main package
"""

import pytest
import tempfile
import os
from pathlib import Path
from datetime import datetime, timezone


class TestTodoCRUD:
    """Integration tests for basic todo CRUD operations."""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        temp_file.close()
        db_path = temp_file.name
        
        yield db_path
        
        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    def test_create_todo(self, temp_db):
        """Test creating a new todo item."""
        # This should be importable from the main todo package
        from todo import create_todo, get_todo
        
        # Initialize database
        from todo import init_db
        init_db(temp_db)
        
        # Create a todo
        todo_id = create_todo(
            title="Test Todo",
            description="This is a test todo item",
            db_path=temp_db
        )
        
        assert todo_id is not None
        assert isinstance(todo_id, int)
        
        # Verify it was created
        todo = get_todo(todo_id, db_path=temp_db)
        assert todo is not None
        assert todo['title'] == "Test Todo"
        assert todo['description'] == "This is a test todo item"
        assert todo['completed'] is False
        assert 'created_at' in todo
        assert 'updated_at' in todo
    
    def test_get_todo(self, temp_db):
        """Test retrieving a todo item."""
        from todo import create_todo, get_todo, init_db
        
        init_db(temp_db)
        
        # Create a todo first
        todo_id = create_todo(
            title="Get Todo Test",
            description="Testing get functionality",
            db_path=temp_db
        )
        
        # Retrieve it
        todo = get_todo(todo_id, db_path=temp_db)
        
        assert todo is not None
        assert todo['id'] == todo_id
        assert todo['title'] == "Get Todo Test"
        assert todo['description'] == "Testing get functionality"
        assert todo['completed'] is False
        
        # Test non-existent todo
        non_existent = get_todo(99999, db_path=temp_db)
        assert non_existent is None
    
    def test_update_todo(self, temp_db):
        """Test updating a todo item."""
        from todo import create_todo, update_todo, get_todo, init_db
        
        init_db(temp_db)
        
        # Create a todo
        todo_id = create_todo(
            title="Original Title",
            description="Original description",
            db_path=temp_db
        )
        
        # Update it
        success = update_todo(
            todo_id,
            title="Updated Title",
            description="Updated description",
            completed=True,
            db_path=temp_db
        )
        
        assert success is True
        
        # Verify the update
        todo = get_todo(todo_id, db_path=temp_db)
        assert todo['title'] == "Updated Title"
        assert todo['description'] == "Updated description"
        assert todo['completed'] is True
        
        # Test partial update (only title)
        success = update_todo(
            todo_id,
            title="Partially Updated",
            db_path=temp_db
        )
        
        assert success is True
        todo = get_todo(todo_id, db_path=temp_db)
        assert todo['title'] == "Partially Updated"
        assert todo['description'] == "Updated description"  # Should remain unchanged
        assert todo['completed'] is True  # Should remain unchanged
    
    def test_delete_todo(self, temp_db):
        """Test deleting a todo item."""
        from todo import create_todo, delete_todo, get_todo, init_db
        
        init_db(temp_db)
        
        # Create a todo
        todo_id = create_todo(
            title="To Be Deleted",
            description="This will be deleted",
            db_path=temp_db
        )
        
        # Verify it exists
        todo = get_todo(todo_id, db_path=temp_db)
        assert todo is not None
        
        # Delete it
        success = delete_todo(todo_id, db_path=temp_db)
        assert success is True
        
        # Verify it's gone
        deleted_todo = get_todo(todo_id, db_path=temp_db)
        assert deleted_todo is None
        
        # Test deleting non-existent todo
        success = delete_todo(99999, db_path=temp_db)
        assert success is False
    
    def test_list_todos(self, temp_db):
        """Test listing all todo items."""
        from todo import create_todo, list_todos, init_db
        
        init_db(temp_db)
        
        # Initially should be empty
        todos = list_todos(db_path=temp_db)
        assert len(todos) == 0
        
        # Create several todos
        todo1_id = create_todo("Todo 1", "Description 1", db_path=temp_db)
        todo2_id = create_todo("Todo 2", "Description 2", db_path=temp_db)
        todo3_id = create_todo("Todo 3", "Description 3", db_path=temp_db)
        
        # List all todos
        todos = list_todos(db_path=temp_db)
        assert len(todos) == 3
        
        # Verify they're all there
        todo_ids = [todo['id'] for todo in todos]
        assert todo1_id in todo_ids
        assert todo2_id in todo_ids
        assert todo3_id in todo_ids
    
    def test_list_todos_by_status(self, temp_db):
        """Test filtering todos by completion status."""
        from todo import create_todo, update_todo, list_todos, init_db
        
        init_db(temp_db)
        
        # Create todos
        todo1_id = create_todo("Incomplete Todo 1", "Not done", db_path=temp_db)
        todo2_id = create_todo("Incomplete Todo 2", "Also not done", db_path=temp_db)
        todo3_id = create_todo("Complete Todo", "This will be completed", db_path=temp_db)
        
        # Mark one as complete
        update_todo(todo3_id, completed=True, db_path=temp_db)
        
        # Test filtering by completed status
        incomplete_todos = list_todos(completed=False, db_path=temp_db)
        assert len(incomplete_todos) == 2
        
        completed_todos = list_todos(completed=True, db_path=temp_db)
        assert len(completed_todos) == 1
        assert completed_todos[0]['id'] == todo3_id
        
        # Test listing all (default behavior)
        all_todos = list_todos(db_path=temp_db)
        assert len(all_todos) == 3


class TestDatabaseInitialization:
    """Tests for database setup and migrations."""
    
    def test_init_db_creates_tables(self, temp_db):
        """Test that database initialization creates the required tables."""
        from todo import init_db
        
        # Initialize database
        init_db(temp_db)
        
        # Basic check - we should be able to import and use the functions
        # without errors after initialization
        from todo import create_todo, list_todos
        
        # Create a todo to verify tables exist
        todo_id = create_todo("Test", "Test description", db_path=temp_db)
        assert todo_id is not None
        
        # Verify we can list todos
        todos = list_todos(db_path=temp_db)
        assert len(todos) == 1


class TestErrorHandling:
    """Tests for proper error handling."""
    
    def test_operations_without_init(self):
        """Test that operations fail gracefully without database initialization."""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_file:
            temp_db = temp_file.name
        
        try:
            from todo import create_todo
            
            # Should handle gracefully (either raise appropriate exception or return None)
            with pytest.raises((Exception, ConnectionError, FileNotFoundError)):
                create_todo("Test", "Description", db_path=temp_db)
        finally:
            if os.path.exists(temp_db):
                os.unlink(temp_db)
    
    def test_invalid_database_path(self):
        """Test operations with invalid database path."""
        from todo import create_todo
        
        # Should handle gracefully
        with pytest.raises((Exception, ConnectionError, FileNotFoundError)):
            create_todo("Test", "Description", db_path="/invalid/path/database.db")


# Expected function signatures for reference:
"""
Expected functions to implement:

1. init_db(db_path: str) -> None
   - Initialize database and run migrations
   - Create all necessary tables

2. create_todo(title: str, description: str = "", db_path: str) -> int
   - Create a new todo item
   - Return the todo ID

3. get_todo(todo_id: int, db_path: str) -> dict | None
   - Retrieve a todo by ID
   - Return dict with keys: id, title, description, completed, created_at, updated_at
   - Return None if not found

4. update_todo(todo_id: int, db_path: str, title: str = None, description: str = None, completed: bool = None) -> bool
   - Update existing todo (partial updates allowed)
   - Return True if successful, False if todo not found

5. delete_todo(todo_id: int, db_path: str) -> bool
   - Delete a todo by ID
   - Return True if successful, False if todo not found

6. list_todos(db_path: str, completed: bool = None) -> list[dict]
   - List all todos, optionally filtered by completion status
   - Return list of todo dictionaries
"""
