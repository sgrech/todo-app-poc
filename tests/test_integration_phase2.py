"""
Phase 2 Integration Tests: Multi-User Todo Management

These tests extend Phase 1 with multi-user functionality.
Each user should be able to manage their own separate todo list.

Expected additions to the package:
- User management functions
- User-scoped todo operations
- User authentication/validation
"""

import pytest
import tempfile
import os
from pathlib import Path


class TestUserManagement:
    """Integration tests for user management functionality."""
    
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
    
    def test_create_user(self, temp_db):
        """Test creating a new user."""
        from todo import init_db, create_user, get_user
        
        init_db(temp_db)
        
        # Create a user
        user_id = create_user(
            username="testuser",
            email="test@example.com",
            db_path=temp_db
        )
        
        assert user_id is not None
        assert isinstance(user_id, int)
        
        # Verify the user was created
        user = get_user(user_id, db_path=temp_db)
        assert user is not None
        assert user['username'] == "testuser"
        assert user['email'] == "test@example.com"
        assert 'created_at' in user
    
    def test_create_duplicate_username(self, temp_db):
        """Test that duplicate usernames are not allowed."""
        from todo import init_db, create_user
        
        init_db(temp_db)
        
        # Create first user
        user1_id = create_user("testuser", "test1@example.com", db_path=temp_db)
        assert user1_id is not None
        
        # Try to create user with same username
        with pytest.raises((ValueError, Exception)):
            create_user("testuser", "test2@example.com", db_path=temp_db)
    
    def test_create_duplicate_email(self, temp_db):
        """Test that duplicate emails are not allowed."""
        from todo import init_db, create_user
        
        init_db(temp_db)
        
        # Create first user
        user1_id = create_user("testuser1", "test@example.com", db_path=temp_db)
        assert user1_id is not None
        
        # Try to create user with same email
        with pytest.raises((ValueError, Exception)):
            create_user("testuser2", "test@example.com", db_path=temp_db)
    
    def test_get_user_by_username(self, temp_db):
        """Test retrieving user by username."""
        from todo import init_db, create_user, get_user_by_username
        
        init_db(temp_db)
        
        # Create a user
        user_id = create_user("testuser", "test@example.com", db_path=temp_db)
        
        # Retrieve by username
        user = get_user_by_username("testuser", db_path=temp_db)
        assert user is not None
        assert user['id'] == user_id
        assert user['username'] == "testuser"
        
        # Test non-existent username
        non_existent = get_user_by_username("nonexistent", db_path=temp_db)
        assert non_existent is None


class TestUserScopedTodos:
    """Integration tests for user-scoped todo operations."""
    
    @pytest.fixture
    def temp_db_with_users(self):
        """Create a temporary database with test users."""
        temp_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        temp_file.close()
        db_path = temp_file.name
        
        from todo import init_db, create_user
        init_db(db_path)
        
        # Create test users
        user1_id = create_user("alice", "alice@example.com", db_path=db_path)
        user2_id = create_user("bob", "bob@example.com", db_path=db_path)
        
        yield db_path, user1_id, user2_id
        
        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)
    
    def test_create_user_todo(self, temp_db_with_users):
        """Test creating todos for specific users."""
        db_path, user1_id, user2_id = temp_db_with_users
        from todo import create_user_todo, get_user_todo
        
        # Create todo for user1
        todo_id = create_user_todo(
            user_id=user1_id,
            title="Alice's Todo",
            description="This belongs to Alice",
            db_path=db_path
        )
        
        assert todo_id is not None
        
        # Verify the todo
        todo = get_user_todo(user_id=user1_id, todo_id=todo_id, db_path=db_path)
        assert todo is not None
        assert todo['title'] == "Alice's Todo"
        assert todo['user_id'] == user1_id
    
    def test_user_todo_isolation(self, temp_db_with_users):
        """Test that users can only access their own todos."""
        db_path, user1_id, user2_id = temp_db_with_users
        from todo import create_user_todo, get_user_todo, list_user_todos
        
        # Create todos for each user
        alice_todo = create_user_todo(
            user_id=user1_id,
            title="Alice's Todo",
            description="Alice's task",
            db_path=db_path
        )
        
        bob_todo = create_user_todo(
            user_id=user2_id,
            title="Bob's Todo",
            description="Bob's task",
            db_path=db_path
        )
        
        # Alice should only see her todo
        alice_todos = list_user_todos(user_id=user1_id, db_path=db_path)
        assert len(alice_todos) == 1
        assert alice_todos[0]['id'] == alice_todo
        assert alice_todos[0]['title'] == "Alice's Todo"
        
        # Bob should only see his todo
        bob_todos = list_user_todos(user_id=user2_id, db_path=db_path)
        assert len(bob_todos) == 1
        assert bob_todos[0]['id'] == bob_todo
        assert bob_todos[0]['title'] == "Bob's Todo"
        
        # Alice should not be able to access Bob's todo
        bob_todo_for_alice = get_user_todo(user_id=user1_id, todo_id=bob_todo, db_path=db_path)
        assert bob_todo_for_alice is None
        
        # Bob should not be able to access Alice's todo
        alice_todo_for_bob = get_user_todo(user_id=user2_id, todo_id=alice_todo, db_path=db_path)
        assert alice_todo_for_bob is None
    
    def test_update_user_todo(self, temp_db_with_users):
        """Test updating user-scoped todos."""
        db_path, user1_id, user2_id = temp_db_with_users
        from todo import create_user_todo, update_user_todo, get_user_todo
        
        # Create todo for user1
        todo_id = create_user_todo(
            user_id=user1_id,
            title="Original Title",
            description="Original description",
            db_path=db_path
        )
        
        # Update the todo
        success = update_user_todo(
            user_id=user1_id,
            todo_id=todo_id,
            title="Updated Title",
            completed=True,
            db_path=db_path
        )
        
        assert success is True
        
        # Verify the update
        todo = get_user_todo(user_id=user1_id, todo_id=todo_id, db_path=db_path)
        assert todo['title'] == "Updated Title"
        assert todo['completed'] is True
        
        # User2 should not be able to update user1's todo
        success = update_user_todo(
            user_id=user2_id,
            todo_id=todo_id,
            title="Hacked Title",
            db_path=db_path
        )
        
        assert success is False
        
        # Verify the todo wasn't changed
        todo = get_user_todo(user_id=user1_id, todo_id=todo_id, db_path=db_path)
        assert todo['title'] == "Updated Title"  # Should remain unchanged
    
    def test_delete_user_todo(self, temp_db_with_users):
        """Test deleting user-scoped todos."""
        db_path, user1_id, user2_id = temp_db_with_users
        from todo import create_user_todo, delete_user_todo, get_user_todo
        
        # Create todo for user1
        todo_id = create_user_todo(
            user_id=user1_id,
            title="To Be Deleted",
            description="This will be deleted",
            db_path=db_path
        )
        
        # User2 should not be able to delete user1's todo
        success = delete_user_todo(user_id=user2_id, todo_id=todo_id, db_path=db_path)
        assert success is False
        
        # Verify todo still exists
        todo = get_user_todo(user_id=user1_id, todo_id=todo_id, db_path=db_path)
        assert todo is not None
        
        # User1 should be able to delete their own todo
        success = delete_user_todo(user_id=user1_id, todo_id=todo_id, db_path=db_path)
        assert success is True
        
        # Verify todo is gone
        todo = get_user_todo(user_id=user1_id, todo_id=todo_id, db_path=db_path)
        assert todo is None


class TestBackwardCompatibility:
    """Test that Phase 1 functionality still works with Phase 2 implementation."""
    
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
    
    def test_phase1_functions_still_work(self, temp_db):
        """Test that all Phase 1 functions still work in Phase 2."""
        from todo import (
            init_db, create_todo, get_todo, update_todo, 
            delete_todo, list_todos
        )
        
        init_db(temp_db)
        
        # Test Phase 1 CRUD operations
        todo_id = create_todo("Test Todo", "Description", db_path=temp_db)
        assert todo_id is not None
        
        todo = get_todo(todo_id, db_path=temp_db)
        assert todo is not None
        assert todo['title'] == "Test Todo"
        
        success = update_todo(todo_id, title="Updated", db_path=temp_db)
        assert success is True
        
        todos = list_todos(db_path=temp_db)
        assert len(todos) == 1
        
        success = delete_todo(todo_id, db_path=temp_db)
        assert success is True


# Expected additional function signatures for Phase 2:
"""
Expected additional functions to implement:

User Management:
1. create_user(username: str, email: str, db_path: str) -> int
   - Create a new user
   - Username and email must be unique
   - Return user ID

2. get_user(user_id: int, db_path: str) -> dict | None
   - Retrieve user by ID
   - Return dict with keys: id, username, email, created_at

3. get_user_by_username(username: str, db_path: str) -> dict | None
   - Retrieve user by username
   - Return user dict or None if not found

User-Scoped Todo Operations:
4. create_user_todo(user_id: int, title: str, description: str = "", db_path: str) -> int
   - Create todo for specific user
   - Return todo ID

5. get_user_todo(user_id: int, todo_id: int, db_path: str) -> dict | None
   - Get todo only if it belongs to the user
   - Return None if todo doesn't exist or doesn't belong to user

6. update_user_todo(user_id: int, todo_id: int, db_path: str, title: str = None, description: str = None, completed: bool = None) -> bool
   - Update todo only if it belongs to the user
   - Return False if todo doesn't exist or doesn't belong to user

7. delete_user_todo(user_id: int, todo_id: int, db_path: str) -> bool
   - Delete todo only if it belongs to the user
   - Return False if todo doesn't exist or doesn't belong to user

8. list_user_todos(user_id: int, db_path: str, completed: bool = None) -> list[dict]
   - List todos for specific user
   - Optional filtering by completion status
"""
