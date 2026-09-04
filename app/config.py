"""
Configuration module for the Task Management API application.

This module contains basic application settings and constants.
All configuration is centralized here for easy maintenance.
"""

# Application settings
APP_NAME = "Task Management API"
APP_VERSION = "1.0.0"
DEBUG_MODE = True

# Validation constraints
MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 100

MIN_EMAIL_LENGTH = 5
MAX_EMAIL_LENGTH = 254

MIN_TASK_TITLE_LENGTH = 1
MAX_TASK_TITLE_LENGTH = 200

MIN_TASK_DESCRIPTION_LENGTH = 0
MAX_TASK_DESCRIPTION_LENGTH = 2000

# Valid task statuses
VALID_TASK_STATUSES = ["pending", "in_progress", "completed"]

# Default task status
DEFAULT_TASK_STATUS = "pending"

# Application messages
SUCCESS_MESSAGES = {
    "user_created": "User created successfully",
    "user_updated": "User updated successfully",
    "user_deleted": "User deleted successfully",
    "task_created": "Task created successfully",
    "task_updated": "Task updated successfully",
    "task_deleted": "Task deleted successfully",
}

# Error messages
ERROR_MESSAGES = {
    "user_not_found": "User not found",
    "task_not_found": "Task not found",
    "invalid_input": "Invalid input provided",
    "validation_failed": "Validation failed",
}
