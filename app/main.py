"""
Main application module for the Task Management API.

This module demonstrates how to use the different modules of the application
(UserService, TaskService, validation, etc.) together. It serves as an
executable demonstration of the modular architecture.

Do NOT put actual business logic here - only demonstration of how to use the modules.
All the real logic lives in the service modules.
"""

from app.config import APP_NAME, APP_VERSION
from app.users.user_service import UserService
from app.tasks.task_service import TaskService
from app.validation.validators import ValidationError


def print_separator(title=""):
    """Print a formatted separator line."""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    else:
        print(f"{'-'*60}\n")


def print_success(message):
    """Print a success message."""
    print(f"✓ {message}")


def print_error(message):
    """Print an error message."""
    print(f"✗ {message}")


def print_task_details(task):
    """Print detailed information about a task."""
    print(f"  Task ID: {task.task_id}")
    print(f"  Title: {task.title}")
    print(f"  Description: {task.description}")
    print(f"  Status: {task.status}")
    print(f"  User ID: {task.user_id}")
    print(f"  Created: {task.created_at}")
    print(f"  Updated: {task.updated_at}")


def print_user_details(user):
    """Print detailed information about a user."""
    print(f"  User ID: {user.user_id}")
    print(f"  Name: {user.name}")
    print(f"  Email: {user.email}")
    print(f"  Created: {user.created_at}")
    print(f"  Updated: {user.updated_at}")


def demo_user_management(user_service):
    """Demonstrate user management functionality."""
    print_separator("USER MANAGEMENT DEMO")
    
    # Create users
    print("Creating users...")
    try:
        user1 = user_service.create_user("John Doe", "john@example.com")
        print_success(f"Created user: {user1.name} ({user1.email})")
        
        user2 = user_service.create_user("Jane Smith", "jane@example.com")
        print_success(f"Created user: {user2.name} ({user2.email})")
    except ValidationError as e:
        print_error(f"Validation Error: {e}")
        return None, None
    
    print_separator()
    
    # Get specific user
    print("Retrieving user by ID...")
    try:
        retrieved_user = user_service.get_user(user1.user_id)
        print_success("User retrieved successfully:")
        print_user_details(retrieved_user)
    except Exception as e:
        print_error(f"Error: {e}")
    
    print_separator()
    
    # Get all users
    print("Retrieving all users...")
    all_users = user_service.get_all_users()
    print_success(f"Found {len(all_users)} user(s):")
    for user in all_users:
        print(f"  • {user.name} ({user.email})")
    
    print_separator()
    
    # Update user
    print("Updating user...")
    try:
        updated_user = user_service.update_user(user1.user_id, name="John Anderson")
        print_success(f"User updated successfully: {updated_user.name}")
    except ValidationError as e:
        print_error(f"Validation Error: {e}")
    
    print_separator()
    
    return user1, user2


def demo_task_management(task_service, user1, user2):
    """Demonstrate task management functionality."""
    print_separator("TASK MANAGEMENT DEMO")
    
    # Create tasks for user1
    print("Creating tasks for user1...")
    try:
        task1 = task_service.create_task(
            title="Complete project documentation",
            user_id=user1.user_id,
            description="Write comprehensive documentation for the project",
            status="in_progress"
        )
        print_success(f"Created task: {task1.title}")
        
        task2 = task_service.create_task(
            title="Review code",
            user_id=user1.user_id,
            description="Review pull requests and provide feedback",
            status="pending"
        )
        print_success(f"Created task: {task2.title}")
    except (ValidationError, KeyError) as e:
        print_error(f"Error: {e}")
        return None
    
    # Create task for user2
    print("\nCreating task for user2...")
    try:
        task3 = task_service.create_task(
            title="Deploy application",
            user_id=user2.user_id,
            description="Deploy the application to production environment",
            status="pending"
        )
        print_success(f"Created task: {task3.title}")
    except (ValidationError, KeyError) as e:
        print_error(f"Error: {e}")
    
    print_separator()
    
    # Get specific task
    print("Retrieving task by ID...")
    try:
        retrieved_task = task_service.get_task(task1.task_id)
        print_success("Task retrieved successfully:")
        print_task_details(retrieved_task)
    except Exception as e:
        print_error(f"Error: {e}")
    
    print_separator()
    
    # Get all tasks
    print("Retrieving all tasks...")
    all_tasks = task_service.get_all_tasks()
    print_success(f"Found {len(all_tasks)} task(s):")
    for task in all_tasks:
        print(f"  • [{task.status.upper()}] {task.title} (User: {task.user_id[:8]}...)")
    
    print_separator()
    
    # Get tasks by user
    print(f"Getting tasks for user1...")
    user1_tasks = task_service.get_user_tasks(user1.user_id)
    print_success(f"Found {len(user1_tasks)} task(s) for user1:")
    for task in user1_tasks:
        print(f"  • {task.title} [{task.status}]")
    
    print_separator()
    
    # Get tasks by status
    print("Getting tasks by status (pending)...")
    pending_tasks = task_service.get_tasks_by_status("pending")
    print_success(f"Found {len(pending_tasks)} pending task(s):")
    for task in pending_tasks:
        print(f"  • {task.title} (User: {task.user_id[:8]}...)")
    
    print_separator()
    
    # Update task
    print("Updating task status...")
    try:
        updated_task = task_service.update_task(
            task1.task_id,
            status="completed",
            description="Documentation is now complete"
        )
        print_success(f"Task updated: {updated_task.title} is now [{updated_task.status}]")
    except (ValidationError, KeyError) as e:
        print_error(f"Error: {e}")
    
    print_separator()
    
    return task1, task2, task3


def demo_error_handling(user_service, task_service):
    """Demonstrate error handling and validation."""
    print_separator("ERROR HANDLING & VALIDATION DEMO")
    
    # Invalid email format
    print("Attempting to create user with invalid email...")
    try:
        user_service.create_user("Invalid User", "not-an-email")
    except ValidationError as e:
        print_error(f"Expected validation error: {e}")
    
    print()
    
    # Duplicate email
    print("Attempting to create user with duplicate email...")
    try:
        user_service.create_user("First User", "duplicate@example.com")
        user_service.create_user("Second User", "duplicate@example.com")
    except ValidationError as e:
        print_error(f"Expected validation error: {e}")
    
    print()
    
    # Non-existent user
    print("Attempting to retrieve non-existent user...")
    try:
        user_service.get_user("nonexistent-id-12345")
    except KeyError as e:
        print_error(f"Expected error: {e}")
    
    print()
    
    # Invalid task status
    print("Attempting to create task with invalid status...")
    try:
        user = user_service.create_user("Test User", "test@example.com")
        task_service.create_task("Test", user.user_id, status="invalid_status")
    except ValidationError as e:
        print_error(f"Expected validation error: {e}")
    
    print()
    
    # Task with non-existent user
    print("Attempting to create task for non-existent user...")
    try:
        task_service.create_task("Test", "nonexistent-user-id")
    except KeyError as e:
        print_error(f"Expected error: {e}")
    
    print_separator()


def main():
    """
    Main application entry point.
    
    This function demonstrates how the different modules work together:
    - UserService for user management
    - TaskService for task management
    - Validation module for input validation
    - Helper utilities for common operations
    
    Everything is modularized into separate files and services,
    showing how production applications organize code.
    """
    print_separator(f"{APP_NAME} v{APP_VERSION}")
    print("This demonstration shows how modular Python development works.")
    print("The code is organized into separate modules for:")
    print("  • User Management (users/)")
    print("  • Task Management (tasks/)")
    print("  • Validation (validation/)")
    print("  • Utilities (utils/)")
    print("  • Configuration (config.py)")
    print()
    
    # Initialize services
    print("Initializing services...")
    user_service = UserService()
    task_service = TaskService(user_service)
    print_success("Services initialized successfully\n")
    
    # Run demonstrations
    user1, user2 = demo_user_management(user_service)
    
    if user1 and user2:
        demo_task_management(task_service, user1, user2)
    
    demo_error_handling(user_service, task_service)
    
    print_separator("DEMONSTRATION COMPLETE")
    print("Review the code in each module to understand:")
    print("  • How modules import from each other")
    print("  • How validation is separated from business logic")
    print("  • How utilities provide reusable functions")
    print("  • How services manage domain objects")
    print()
    print("All business logic is in the service classes, not in main.py!")
    print("This is how production applications are structured.")
    print()


if __name__ == "__main__":
    main()
