"""
Unit tests for the user service module.

Tests cover:
- User creation with valid data
- User creation with invalid data
- Duplicate email handling
- User retrieval by ID
- Get all users
- User update
- User deletion
- User existence check
"""

import unittest
from app.users.user_service import UserService, User
from app.validation.validators import ValidationError


class TestUserModel(unittest.TestCase):
    """Test User model."""
    
    def test_user_to_dict(self):
        """User to_dict should return dictionary with all fields."""
        user = User("user-123", "John Doe", "john@example.com", "2024-01-01 12:00:00")
        user_dict = user.to_dict()
        
        self.assertEqual(user_dict["user_id"], "user-123")
        self.assertEqual(user_dict["name"], "John Doe")
        self.assertEqual(user_dict["email"], "john@example.com")
        self.assertIn("created_at", user_dict)
        self.assertIn("updated_at", user_dict)
    
    def test_user_repr(self):
        """User repr should return formatted string."""
        user = User("user-123", "John Doe", "john@example.com", "2024-01-01 12:00:00")
        self.assertIn("John Doe", repr(user))
        self.assertIn("user-123", repr(user))


class TestUserCreation(unittest.TestCase):
    """Test user creation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = UserService()
    
    def test_create_user_with_valid_data(self):
        """User creation should succeed with valid data."""
        user = self.service.create_user("John Doe", "john@example.com")
        
        self.assertIsNotNone(user.user_id)
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertIsNotNone(user.created_at)
    
    def test_create_user_email_lowercased(self):
        """User email should be lowercased."""
        user = self.service.create_user("John Doe", "John@EXAMPLE.COM")
        self.assertEqual(user.email, "john@example.com")
    
    def test_create_user_name_capitalized(self):
        """User name should be properly capitalized."""
        user = self.service.create_user("john doe", "john@example.com")
        self.assertEqual(user.name, "John Doe")
    
    def test_create_user_with_invalid_email(self):
        """User creation should fail with invalid email."""
        with self.assertRaises(ValidationError):
            self.service.create_user("John Doe", "invalid-email")
    
    def test_create_user_with_short_name(self):
        """User creation should fail with name too short."""
        with self.assertRaises(ValidationError):
            self.service.create_user("J", "john@example.com")
    
    def test_create_user_with_duplicate_email(self):
        """User creation should fail with duplicate email."""
        self.service.create_user("John Doe", "john@example.com")
        
        with self.assertRaises(ValidationError) as context:
            self.service.create_user("John Smith", "john@example.com")
        self.assertIn("already in use", str(context.exception))
    
    def test_create_user_with_duplicate_email_different_case(self):
        """User creation should fail with duplicate email regardless of case."""
        self.service.create_user("John Doe", "john@example.com")
        
        with self.assertRaises(ValidationError):
            self.service.create_user("John Smith", "JOHN@EXAMPLE.COM")


class TestUserRetrieval(unittest.TestCase):
    """Test user retrieval functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = UserService()
        self.user = self.service.create_user("John Doe", "john@example.com")
    
    def test_get_user_by_id(self):
        """User retrieval should return correct user."""
        retrieved = self.service.get_user(self.user.user_id)
        
        self.assertEqual(retrieved.user_id, self.user.user_id)
        self.assertEqual(retrieved.name, self.user.name)
        self.assertEqual(retrieved.email, self.user.email)
    
    def test_get_user_with_nonexistent_id(self):
        """User retrieval should fail with non-existent ID."""
        with self.assertRaises(KeyError):
            self.service.get_user("nonexistent-id")
    
    def test_get_all_users(self):
        """Get all users should return all created users."""
        self.service.create_user("Jane Doe", "jane@example.com")
        self.service.create_user("Bob Smith", "bob@example.com")
        
        all_users = self.service.get_all_users()
        
        self.assertEqual(len(all_users), 3)
    
    def test_get_all_users_empty(self):
        """Get all users should return empty list when no users."""
        service = UserService()
        all_users = service.get_all_users()
        self.assertEqual(len(all_users), 0)


class TestUserUpdate(unittest.TestCase):
    """Test user update functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = UserService()
        self.user = self.service.create_user("John Doe", "john@example.com")
    
    def test_update_user_name(self):
        """User update should change name."""
        updated = self.service.update_user(self.user.user_id, name="John Smith")
        
        self.assertEqual(updated.name, "John Smith")
    
    def test_update_user_email(self):
        """User update should change email."""
        updated = self.service.update_user(self.user.user_id, email="john.new@example.com")
        
        self.assertEqual(updated.email, "john.new@example.com")
    
    def test_update_user_both_fields(self):
        """User update should change both name and email."""
        updated = self.service.update_user(
            self.user.user_id,
            name="Jane Doe",
            email="jane@example.com"
        )
        
        self.assertEqual(updated.name, "Jane Doe")
        self.assertEqual(updated.email, "jane@example.com")
    
    def test_update_user_with_invalid_email(self):
        """User update should fail with invalid email."""
        with self.assertRaises(ValidationError):
            self.service.update_user(self.user.user_id, email="invalid-email")
    
    def test_update_user_with_duplicate_email(self):
        """User update should fail with duplicate email."""
        self.service.create_user("Jane Doe", "jane@example.com")
        
        with self.assertRaises(ValidationError):
            self.service.update_user(self.user.user_id, email="jane@example.com")
    
    def test_update_user_with_nonexistent_id(self):
        """User update should fail with non-existent ID."""
        with self.assertRaises(KeyError):
            self.service.update_user("nonexistent-id", name="New Name")
    
    def test_update_user_updates_timestamp(self):
        """User update should set the updated_at timestamp."""
        updated = self.service.update_user(self.user.user_id, name="New Name")
        
        # Verify updated_at is set and follows expected format
        self.assertIsNotNone(updated.updated_at)
        self.assertIn(":", updated.updated_at)  # Contains time separator
        self.assertTrue(len(updated.updated_at) >= 10)  # YYYY-MM-DD minimum


class TestUserDeletion(unittest.TestCase):
    """Test user deletion functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = UserService()
        self.user = self.service.create_user("John Doe", "john@example.com")
    
    def test_delete_user(self):
        """User deletion should remove the user."""
        self.service.delete_user(self.user.user_id)
        
        with self.assertRaises(KeyError):
            self.service.get_user(self.user.user_id)
    
    def test_delete_user_with_nonexistent_id(self):
        """User deletion should fail with non-existent ID."""
        with self.assertRaises(KeyError):
            self.service.delete_user("nonexistent-id")


class TestUserExistenceCheck(unittest.TestCase):
    """Test user existence check functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = UserService()
        self.user = self.service.create_user("John Doe", "john@example.com")
    
    def test_user_exists(self):
        """User existence check should return True for existing user."""
        self.assertTrue(self.service.user_exists(self.user.user_id))
    
    def test_user_does_not_exist(self):
        """User existence check should return False for non-existent user."""
        self.assertFalse(self.service.user_exists("nonexistent-id"))


if __name__ == "__main__":
    unittest.main()
