"""
Task Management Service for the Task Management API.

This module handles all task-related operations including creating,
retrieving, updating, listing, and deleting tasks. Tasks are stored
in memory during this session. Each task has a unique ID, title,
description, status, and is associated with a user.
"""

from app.config import DEFAULT_TASK_STATUS
from app.utils.helpers import generate_unique_id, get_current_timestamp
from app.validation.validators import (
    validate_task_title,
    validate_task_description,
    validate_task_status,
    validate_user_id,
    ValidationError,
)


class Task:
    """
    Represents a Task in the system.
    
    Attributes:
        task_id (str): Unique identifier for the task.
        title (str): Task title.
        description (str): Task description.
        status (str): Task status (pending, in_progress, or completed).
        user_id (str): ID of the user who owns this task.
        created_at (str): Timestamp when the task was created.
        updated_at (str): Timestamp when the task was last updated.
    """
    
    def __init__(self, task_id, title, description, status, user_id, created_at, updated_at=None):
        """Initialize a Task object."""
        self.task_id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.user_id = user_id
        self.created_at = created_at
        self.updated_at = updated_at or created_at
    
    def to_dict(self):
        """
        Convert Task object to dictionary.
        
        Returns:
            dict: Task data as dictionary.
        """
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    def __repr__(self):
        """String representation of Task."""
        return f"Task(task_id={self.task_id}, title={self.title}, status={self.status})"


class TaskService:
    """
    Service for managing tasks.
    
    This service handles task CRUD operations (Create, Read, Update, Delete)
    and task listing. Tasks are stored in an in-memory dictionary for this task.
    Tasks are associated with users via user_id.
    """
    
    def __init__(self, user_service):
        """
        Initialize the TaskService.
        
        Args:
            user_service: UserService instance for validating user existence.
        """
        self._tasks = {}  # Dictionary to store tasks: {task_id: Task}
        self._user_service = user_service
    
    def create_task(self, title, user_id, description="", status=DEFAULT_TASK_STATUS):
        """
        Create a new task.
        
        Args:
            title (str): Task title.
            user_id (str): ID of the user who owns this task.
            description (str, optional): Task description (default: "").
            status (str, optional): Task status (default: "pending").
        
        Returns:
            Task: The created task object.
        
        Raises:
            ValidationError: If inputs are invalid.
            KeyError: If user_id does not exist.
        
        Example:
            >>> from app.users.user_service import UserService
            >>> user_service = UserService()
            >>> task_service = TaskService(user_service)
            >>> user = user_service.create_user("John Doe", "john@example.com")
            >>> task = task_service.create_task("Complete project", user.user_id)
            >>> task.title
            "Complete project"
        """
        # Validate inputs
        validate_task_title(title)
        validate_task_description(description)
        validate_task_status(status)
        validate_user_id(user_id)
        
        # Verify user exists
        if not self._user_service.user_exists(user_id):
            raise KeyError(f"User with ID '{user_id}' not found")
        
        # Create new task
        task_id = generate_unique_id()
        timestamp = get_current_timestamp()
        new_task = Task(task_id, title, description, status, user_id, timestamp)
        
        # Store task
        self._tasks[task_id] = new_task
        
        return new_task
    
    def get_task(self, task_id):
        """
        Retrieve a task by ID.
        
        Args:
            task_id (str): The unique identifier of the task.
        
        Returns:
            Task: The task object if found.
        
        Raises:
            KeyError: If task is not found.
        
        Example:
            >>> from app.users.user_service import UserService
            >>> user_service = UserService()
            >>> task_service = TaskService(user_service)
            >>> user = user_service.create_user("Jane Doe", "jane@example.com")
            >>> task = task_service.create_task("Fix bug", user.user_id)
            >>> retrieved = task_service.get_task(task.task_id)
            >>> retrieved.title
            "Fix bug"
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID '{task_id}' not found")
        
        return self._tasks[task_id]
    
    def get_all_tasks(self):
        """
        Retrieve all tasks.
        
        Returns:
            list: List of all Task objects.
        
        Example:
            >>> from app.users.user_service import UserService
            >>> user_service = UserService()
            >>> task_service = TaskService(user_service)
            >>> user = user_service.create_user("User", "user@example.com")
            >>> task_service.create_task("Task 1", user.user_id)
            >>> task_service.create_task("Task 2", user.user_id)
            >>> len(task_service.get_all_tasks())
            2
        """
        return list(self._tasks.values())
    
    def get_user_tasks(self, user_id):
        """
        Retrieve all tasks for a specific user.
        
        Args:
            user_id (str): The ID of the user.
        
        Returns:
            list: List of Task objects belonging to the user.
        
        Raises:
            ValidationError: If user_id is not provided.
        
        Example:
            >>> from app.users.user_service import UserService
            >>> user_service = UserService()
            >>> task_service = TaskService(user_service)
            >>> user = user_service.create_user("Alice", "alice@example.com")
            >>> task_service.create_task("Task 1", user.user_id)
            >>> tasks = task_service.get_user_tasks(user.user_id)
            >>> len(tasks)
            1
        """
        validate_user_id(user_id)
        
        user_tasks = [task for task in self._tasks.values() if task.user_id == user_id]
        return user_tasks
    
    def update_task(self, task_id, title=None, description=None, status=None):
        """
        Update task information.
        
        Args:
            task_id (str): The unique identifier of the task.
            title (str, optional): New title for the task.
            description (str, optional): New description for the task.
            status (str, optional): New status for the task.
        
        Returns:
            Task: The updated task object.
        
        Raises:
            ValidationError: If inputs are invalid.
            KeyError: If task is not found.
        
        Example:
            >>> from app.users.user_service import UserService
            >>> user_service = UserService()
            >>> task_service = TaskService(user_service)
            >>> user = user_service.create_user("Bob", "bob@example.com")
            >>> task = task_service.create_task("Original", user.user_id)
            >>> updated = task_service.update_task(task.task_id, title="Updated")
            >>> updated.title
            "Updated"
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID '{task_id}' not found")
        
        task = self._tasks[task_id]
        
        # Update title if provided
        if title is not None:
            validate_task_title(title)
            task.title = title
        
        # Update description if provided
        if description is not None:
            validate_task_description(description)
            task.description = description
        
        # Update status if provided
        if status is not None:
            validate_task_status(status)
            task.status = status
        
        # Update timestamp
        task.updated_at = get_current_timestamp()
        
        return task
    
    def delete_task(self, task_id):
        """
        Delete a task.
        
        Args:
            task_id (str): The unique identifier of the task.
        
        Raises:
            KeyError: If task is not found.
        
        Example:
            >>> from app.users.user_service import UserService
            >>> user_service = UserService()
            >>> task_service = TaskService(user_service)
            >>> user = user_service.create_user("Charlie", "charlie@example.com")
            >>> task = task_service.create_task("Temporary", user.user_id)
            >>> task_service.delete_task(task.task_id)
            >>> task_service.get_task(task.task_id)
            KeyError: Task with ID '...' not found
        """
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID '{task_id}' not found")
        
        del self._tasks[task_id]
    
    def get_tasks_by_status(self, status):
        """
        Retrieve all tasks with a specific status.
        
        Args:
            status (str): The status to filter by.
        
        Returns:
            list: List of Task objects with the specified status.
        
        Raises:
            ValidationError: If status is invalid.
        
        Example:
            >>> from app.users.user_service import UserService
            >>> user_service = UserService()
            >>> task_service = TaskService(user_service)
            >>> user = user_service.create_user("David", "david@example.com")
            >>> task_service.create_task("Task", user.user_id, status="pending")
            >>> pending_tasks = task_service.get_tasks_by_status("pending")
            >>> len(pending_tasks)
            1
        """
        validate_task_status(status)
        
        filtered_tasks = [task for task in self._tasks.values() if task.status == status]
        return filtered_tasks
    
    def task_exists(self, task_id):
        """
        Check if a task exists.
        
        Args:
            task_id (str): The unique identifier of the task.
        
        Returns:
            bool: True if task exists, False otherwise.
        
        Example:
            >>> from app.users.user_service import UserService
            >>> user_service = UserService()
            >>> task_service = TaskService(user_service)
            >>> user = user_service.create_user("Eve", "eve@example.com")
            >>> task = task_service.create_task("Exist", user.user_id)
            >>> task_service.task_exists(task.task_id)
            True
            >>> task_service.task_exists("nonexistent-id")
            False
        """
        return task_id in self._tasks
