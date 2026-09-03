"""
Validation module for the Task Management API application.

This module provides validation functions for user inputs including
email validation, name validation, task validation, and general field validation.
All validation errors are returned with clear, user-friendly messages.
"""

import re
from app.config import (
    MIN_NAME_LENGTH,
    MAX_NAME_LENGTH,
    MIN_EMAIL_LENGTH,
    MAX_EMAIL_LENGTH,
    MIN_TASK_TITLE_LENGTH,
    MAX_TASK_TITLE_LENGTH,
    MIN_TASK_DESCRIPTION_LENGTH,
    MAX_TASK_DESCRIPTION_LENGTH,
    VALID_TASK_STATUSES,
)
from app.utils.helpers import is_empty_or_none


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def validate_required_field(value, field_name):
    """
    Validate that a required field is not empty.
    
    Args:
        value: The value to validate.
        field_name (str): The name of the field (for error messages).
    
    Raises:
        ValidationError: If the field is empty or None.
    
    Example:
        >>> validate_required_field("john", "name")
        >>> validate_required_field(None, "name")
        ValidationError: name is required
    """
    if is_empty_or_none(value):
        raise ValidationError(f"{field_name} is required")


def validate_email(email):
    """
    Validate email format.
    
    Args:
        email (str): The email to validate.
    
    Raises:
        ValidationError: If email is invalid.
    
    Example:
        >>> validate_email("user@example.com")
        >>> validate_email("invalid-email")
        ValidationError: Invalid email format
    """
    validate_required_field(email, "email")
    
    # Check length
    if len(email) < MIN_EMAIL_LENGTH or len(email) > MAX_EMAIL_LENGTH:
        raise ValidationError(
            f"email must be between {MIN_EMAIL_LENGTH} and {MAX_EMAIL_LENGTH} characters"
        )
    
    # Basic email regex pattern
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        raise ValidationError("Invalid email format")


def validate_name(name, field_name="name"):
    """
    Validate a name field.
    
    Args:
        name (str): The name to validate.
        field_name (str): The name of the field (default: "name").
    
    Raises:
        ValidationError: If name is invalid.
    
    Example:
        >>> validate_name("John Doe")
        >>> validate_name("J")
        ValidationError: name must be at least 2 characters
    """
    validate_required_field(name, field_name)
    
    # Check length
    if len(name) < MIN_NAME_LENGTH or len(name) > MAX_NAME_LENGTH:
        raise ValidationError(
            f"{field_name} must be between {MIN_NAME_LENGTH} and {MAX_NAME_LENGTH} characters"
        )
    
    # Check that name contains only letters, spaces, and hyphens
    name_pattern = r"^[a-zA-Z\s\-']+$"
    if not re.match(name_pattern, name):
        raise ValidationError(f"{field_name} can only contain letters, spaces, hyphens, and apostrophes")


def validate_task_title(title):
    """
    Validate a task title.
    
    Args:
        title (str): The task title to validate.
    
    Raises:
        ValidationError: If title is invalid.
    
    Example:
        >>> validate_task_title("Complete project")
        >>> validate_task_title("")
        ValidationError: task_title is required
    """
    validate_required_field(title, "task_title")
    
    # Check length
    if len(title) < MIN_TASK_TITLE_LENGTH or len(title) > MAX_TASK_TITLE_LENGTH:
        raise ValidationError(
            f"task_title must be between {MIN_TASK_TITLE_LENGTH} and {MAX_TASK_TITLE_LENGTH} characters"
        )


def validate_task_description(description):
    """
    Validate a task description.
    
    Args:
        description (str): The task description to validate.
    
    Raises:
        ValidationError: If description is invalid.
    
    Example:
        >>> validate_task_description("Some description")
        >>> validate_task_description("x" * 3000)
        ValidationError: task_description must be at most 2000 characters
    """
    # Description is optional, but if provided, validate length
    if description is not None and isinstance(description, str):
        if len(description) < MIN_TASK_DESCRIPTION_LENGTH or len(description) > MAX_TASK_DESCRIPTION_LENGTH:
            raise ValidationError(
                f"task_description must be between {MIN_TASK_DESCRIPTION_LENGTH} and {MAX_TASK_DESCRIPTION_LENGTH} characters"
            )


def validate_task_status(status):
    """
    Validate a task status.
    
    Args:
        status (str): The task status to validate.
    
    Raises:
        ValidationError: If status is invalid.
    
    Example:
        >>> validate_task_status("pending")
        >>> validate_task_status("invalid_status")
        ValidationError: status must be one of: pending, in_progress, completed
    """
    validate_required_field(status, "status")
    
    if status not in VALID_TASK_STATUSES:
        raise ValidationError(
            f"status must be one of: {', '.join(VALID_TASK_STATUSES)}"
        )


def validate_user_id(user_id):
    """
    Validate that a user ID is provided.
    
    Args:
        user_id: The user ID to validate.
    
    Raises:
        ValidationError: If user_id is empty.
    
    Example:
        >>> validate_user_id("123e4567-e89b-12d3-a456-426614174000")
        >>> validate_user_id(None)
        ValidationError: user_id is required
    """
    validate_required_field(user_id, "user_id")
