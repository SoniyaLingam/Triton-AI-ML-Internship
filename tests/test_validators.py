"""
Unit tests for the validation module.

Tests cover:
- Required field validation
- Email format validation
- Name validation
- Task title and description validation
- Task status validation
- User ID validation
"""

import unittest
from app.validation.validators import (
    ValidationError,
    validate_required_field,
    validate_email,
    validate_name,
    validate_task_title,
    validate_task_description,
    validate_task_status,
    validate_user_id,
)


class TestRequiredFieldValidation(unittest.TestCase):
    """Test required field validation."""
    
    def test_validate_required_field_with_valid_value(self):
        """Required field validation should pass with valid value."""
        # Should not raise any exception
        validate_required_field("valid_value", "test_field")
    
    def test_validate_required_field_with_none(self):
        """Required field validation should fail with None."""
        with self.assertRaises(ValidationError) as context:
            validate_required_field(None, "test_field")
        self.assertIn("test_field is required", str(context.exception))
    
    def test_validate_required_field_with_empty_string(self):
        """Required field validation should fail with empty string."""
        with self.assertRaises(ValidationError) as context:
            validate_required_field("", "test_field")
        self.assertIn("test_field is required", str(context.exception))
    
    def test_validate_required_field_with_whitespace(self):
        """Required field validation should fail with whitespace only."""
        with self.assertRaises(ValidationError) as context:
            validate_required_field("   ", "test_field")
        self.assertIn("test_field is required", str(context.exception))


class TestEmailValidation(unittest.TestCase):
    """Test email validation."""
    
    def test_validate_email_with_valid_email(self):
        """Email validation should pass with valid email."""
        validate_email("user@example.com")
        validate_email("test.user@domain.co.uk")
        validate_email("user+tag@example.com")
    
    def test_validate_email_with_invalid_format(self):
        """Email validation should fail with invalid format."""
        with self.assertRaises(ValidationError) as context:
            validate_email("invalid-email")
        self.assertIn("Invalid email format", str(context.exception))
    
    def test_validate_email_with_missing_at(self):
        """Email validation should fail without @ symbol."""
        with self.assertRaises(ValidationError):
            validate_email("invalid.email.com")
    
    def test_validate_email_with_empty_value(self):
        """Email validation should fail with empty value."""
        with self.assertRaises(ValidationError):
            validate_email("")


class TestNameValidation(unittest.TestCase):
    """Test name validation."""
    
    def test_validate_name_with_valid_name(self):
        """Name validation should pass with valid names."""
        validate_name("John Doe")
        validate_name("Jane O'Connor")
        validate_name("Jean-Pierre")
    
    def test_validate_name_with_too_short(self):
        """Name validation should fail with name too short."""
        with self.assertRaises(ValidationError) as context:
            validate_name("J")
        self.assertIn("between", str(context.exception))
    
    def test_validate_name_with_invalid_characters(self):
        """Name validation should fail with invalid characters."""
        with self.assertRaises(ValidationError):
            validate_name("John123")
    
    def test_validate_name_with_empty_value(self):
        """Name validation should fail with empty value."""
        with self.assertRaises(ValidationError):
            validate_name("")


class TestTaskTitleValidation(unittest.TestCase):
    """Test task title validation."""
    
    def test_validate_task_title_with_valid_title(self):
        """Task title validation should pass with valid title."""
        validate_task_title("Complete project")
        validate_task_title("A")
    
    def test_validate_task_title_with_empty_value(self):
        """Task title validation should fail with empty value."""
        with self.assertRaises(ValidationError):
            validate_task_title("")
    
    def test_validate_task_title_with_very_long_title(self):
        """Task title validation should fail with very long title."""
        with self.assertRaises(ValidationError):
            validate_task_title("x" * 300)


class TestTaskDescriptionValidation(unittest.TestCase):
    """Test task description validation."""
    
    def test_validate_task_description_with_valid_description(self):
        """Task description validation should pass with valid description."""
        validate_task_description("This is a valid description")
    
    def test_validate_task_description_with_empty_string(self):
        """Task description validation should pass with empty string."""
        validate_task_description("")
    
    def test_validate_task_description_with_none(self):
        """Task description validation should pass with None."""
        validate_task_description(None)
    
    def test_validate_task_description_with_very_long_description(self):
        """Task description validation should fail with very long description."""
        with self.assertRaises(ValidationError):
            validate_task_description("x" * 3000)


class TestTaskStatusValidation(unittest.TestCase):
    """Test task status validation."""
    
    def test_validate_task_status_with_valid_status(self):
        """Task status validation should pass with valid status."""
        validate_task_status("pending")
        validate_task_status("in_progress")
        validate_task_status("completed")
    
    def test_validate_task_status_with_invalid_status(self):
        """Task status validation should fail with invalid status."""
        with self.assertRaises(ValidationError) as context:
            validate_task_status("invalid_status")
        self.assertIn("must be one of", str(context.exception))
    
    def test_validate_task_status_with_empty_value(self):
        """Task status validation should fail with empty value."""
        with self.assertRaises(ValidationError):
            validate_task_status("")


class TestUserIdValidation(unittest.TestCase):
    """Test user ID validation."""
    
    def test_validate_user_id_with_valid_id(self):
        """User ID validation should pass with valid ID."""
        validate_user_id("123e4567-e89b-12d3-a456-426614174000")
        validate_user_id("any-user-id")
    
    def test_validate_user_id_with_empty_value(self):
        """User ID validation should fail with empty value."""
        with self.assertRaises(ValidationError):
            validate_user_id("")
    
    def test_validate_user_id_with_none(self):
        """User ID validation should fail with None."""
        with self.assertRaises(ValidationError):
            validate_user_id(None)


if __name__ == "__main__":
    unittest.main()
