"""
User Management Service for the Task Management API.

This module handles all user-related operations including creating,
retrieving, updating, and deleting users. Users are stored in memory
during this session. Each user has a unique ID, name, and email.
"""

from app.utils.helpers import generate_unique_id, get_current_timestamp, capitalize_words
from app.validation.validators import validate_name, validate_email, validate_user_id, ValidationError


class User:
    """
    Represents a User in the system.
    
    Attributes:
        user_id (str): Unique identifier for the user.
        name (str): User's full name.
        email (str): User's email address.
        created_at (str): Timestamp when the user was created.
        updated_at (str): Timestamp when the user was last updated.
    """
    
    def __init__(self, user_id, name, email, created_at, updated_at=None):
        """Initialize a User object."""
        self.user_id = user_id
        self.name = name
        self.email = email
        self.created_at = created_at
        self.updated_at = updated_at or created_at
    
    def to_dict(self):
        """
        Convert User object to dictionary.
        
        Returns:
            dict: User data as dictionary.
        """
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    def __repr__(self):
        """String representation of User."""
        return f"User(user_id={self.user_id}, name={self.name}, email={self.email})"


class UserService:
    """
    Service for managing users.
    
    This service handles user CRUD operations (Create, Read, Update, Delete).
    Users are stored in an in-memory dictionary for this task.
    """
    
    def __init__(self):
        """Initialize the UserService with an empty users storage."""
        self._users = {}  # Dictionary to store users: {user_id: User}
    
    def create_user(self, name, email):
        """
        Create a new user.
        
        Args:
            name (str): User's full name.
            email (str): User's email address.
        
        Returns:
            User: The created user object.
        
        Raises:
            ValidationError: If name or email is invalid.
        
        Example:
            >>> service = UserService()
            >>> user = service.create_user("John Doe", "john@example.com")
            >>> user.name
            "John Doe"
        """
        # Validate inputs
        validate_name(name)
        validate_email(email)
        
        # Check if email already exists
        for user in self._users.values():
            if user.email.lower() == email.lower():
                raise ValidationError(f"Email '{email}' is already in use")
        
        # Create new user
        user_id = generate_unique_id()
        timestamp = get_current_timestamp()
        new_user = User(user_id, capitalize_words(name), email.lower(), timestamp)
        
        # Store user
        self._users[user_id] = new_user
        
        return new_user
    
    def get_user(self, user_id):
        """
        Retrieve a user by ID.
        
        Args:
            user_id (str): The unique identifier of the user.
        
        Returns:
            User: The user object if found.
        
        Raises:
            ValidationError: If user_id is not provided.
            KeyError: If user is not found.
        
        Example:
            >>> service = UserService()
            >>> user = service.create_user("Jane Doe", "jane@example.com")
            >>> retrieved = service.get_user(user.user_id)
            >>> retrieved.name
            "Jane Doe"
        """
        validate_user_id(user_id)
        
        if user_id not in self._users:
            raise KeyError(f"User with ID '{user_id}' not found")
        
        return self._users[user_id]
    
    def get_all_users(self):
        """
        Retrieve all users.
        
        Returns:
            list: List of all User objects.
        
        Example:
            >>> service = UserService()
            >>> service.create_user("User One", "user1@example.com")
            >>> service.create_user("User Two", "user2@example.com")
            >>> len(service.get_all_users())
            2
        """
        return list(self._users.values())
    
    def update_user(self, user_id, name=None, email=None):
        """
        Update user information.
        
        Args:
            user_id (str): The unique identifier of the user.
            name (str, optional): New name for the user.
            email (str, optional): New email for the user.
        
        Returns:
            User: The updated user object.
        
        Raises:
            ValidationError: If inputs are invalid.
            KeyError: If user is not found.
        
        Example:
            >>> service = UserService()
            >>> user = service.create_user("John Doe", "john@example.com")
            >>> updated = service.update_user(user.user_id, name="John Smith")
            >>> updated.name
            "John Smith"
        """
        validate_user_id(user_id)
        
        if user_id not in self._users:
            raise KeyError(f"User with ID '{user_id}' not found")
        
        user = self._users[user_id]
        
        # Update name if provided
        if name is not None:
            validate_name(name)
            user.name = capitalize_words(name)
        
        # Update email if provided
        if email is not None:
            validate_email(email)
            
            # Check if email already exists (excluding current user)
            for other_user in self._users.values():
                if other_user.user_id != user_id and other_user.email.lower() == email.lower():
                    raise ValidationError(f"Email '{email}' is already in use")
            
            user.email = email.lower()
        
        # Update timestamp
        user.updated_at = get_current_timestamp()
        
        return user
    
    def delete_user(self, user_id):
        """
        Delete a user.
        
        Args:
            user_id (str): The unique identifier of the user.
        
        Raises:
            ValidationError: If user_id is not provided.
            KeyError: If user is not found.
        
        Example:
            >>> service = UserService()
            >>> user = service.create_user("John Doe", "john@example.com")
            >>> service.delete_user(user.user_id)
            >>> service.get_user(user.user_id)
            KeyError: User with ID '...' not found
        """
        validate_user_id(user_id)
        
        if user_id not in self._users:
            raise KeyError(f"User with ID '{user_id}' not found")
        
        del self._users[user_id]
    
    def user_exists(self, user_id):
        """
        Check if a user exists.
        
        Args:
            user_id (str): The unique identifier of the user.
        
        Returns:
            bool: True if user exists, False otherwise.
        
        Example:
            >>> service = UserService()
            >>> user = service.create_user("John Doe", "john@example.com")
            >>> service.user_exists(user.user_id)
            True
            >>> service.user_exists("nonexistent-id")
            False
        """
        return user_id in self._users
