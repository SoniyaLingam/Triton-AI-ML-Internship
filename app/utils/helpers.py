"""
Utility helper functions for the Task Management API application.

This module provides reusable utility functions such as ID generation,
text formatting, and other helper functions used across the application.
These functions are independent from business logic.
"""

import uuid
from datetime import datetime


def generate_unique_id():
    """
    Generate a unique ID using UUID4.
    
    Returns:
        str: A unique identifier string.
    
    Example:
        >>> uid = generate_unique_id()
        >>> len(uid) > 0
        True
    """
    return str(uuid.uuid4())


def get_current_timestamp():
    """
    Get the current timestamp.
    
    Returns:
        str: Current timestamp in ISO format (YYYY-MM-DD HH:MM:SS).
    
    Example:
        >>> ts = get_current_timestamp()
        >>> len(ts) > 0
        True
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_text(text):
    """
    Clean and format text by trimming whitespace and converting to lowercase.
    
    Args:
        text (str): The text to format.
    
    Returns:
        str: Formatted text (lowercase, stripped of leading/trailing whitespace).
    
    Example:
        >>> format_text("  Hello World  ")
        "hello world"
    """
    if not isinstance(text, str):
        return text
    return text.strip().lower()


def capitalize_words(text):
    """
    Capitalize the first letter of each word.
    
    Args:
        text (str): The text to capitalize.
    
    Returns:
        str: Text with each word capitalized.
    
    Example:
        >>> capitalize_words("john doe")
        "John Doe"
    """
    if not isinstance(text, str):
        return text
    return text.title()


def truncate_text(text, max_length=100):
    """
    Truncate text to a maximum length with ellipsis.
    
    Args:
        text (str): The text to truncate.
        max_length (int): Maximum length allowed (default: 100).
    
    Returns:
        str: Truncated text with "..." if it exceeds max_length.
    
    Example:
        >>> truncate_text("a" * 150, max_length=10)
        "aaaaaaaaaa..."
    """
    if not isinstance(text, str):
        return text
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def is_empty_or_none(value):
    """
    Check if a value is empty, None, or contains only whitespace.
    
    Args:
        value: The value to check.
    
    Returns:
        bool: True if value is empty, None, or whitespace-only; False otherwise.
    
    Example:
        >>> is_empty_or_none(None)
        True
        >>> is_empty_or_none("  ")
        True
        >>> is_empty_or_none("hello")
        False
    """
    if value is None:
        return True
    if isinstance(value, str):
        return len(value.strip()) == 0
    return False
