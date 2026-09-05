"""
Unit tests for the task service module.

Tests cover:
- Task creation with valid data
- Task creation with invalid data
- Task retrieval by ID
- Get all tasks
- Get tasks by user
- Get tasks by status
- Task update
- Task deletion
- Task existence check
"""

import unittest
from app.users.user_service import UserService
from app.tasks.task_service import TaskService, Task
from app.validation.validators import ValidationError


class TestTaskModel(unittest.TestCase):
    """Test Task model."""
    
    def test_task_to_dict(self):
        """Task to_dict should return dictionary with all fields."""
        task = Task(
            "task-123",
            "Complete project",
            "Finish all tasks",
            "pending",
            "user-123",
            "2024-01-01 12:00:00"
        )
        task_dict = task.to_dict()
        
        self.assertEqual(task_dict["task_id"], "task-123")
        self.assertEqual(task_dict["title"], "Complete project")
        self.assertEqual(task_dict["description"], "Finish all tasks")
        self.assertEqual(task_dict["status"], "pending")
        self.assertEqual(task_dict["user_id"], "user-123")
    
    def test_task_repr(self):
        """Task repr should return formatted string."""
        task = Task(
            "task-123",
            "Complete project",
            "",
            "pending",
            "user-123",
            "2024-01-01 12:00:00"
        )
        self.assertIn("Complete project", repr(task))


class TestTaskCreation(unittest.TestCase):
    """Test task creation functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.user_service = UserService()
        self.task_service = TaskService(self.user_service)
        self.user = self.user_service.create_user("John Doe", "john@example.com")
    
    def test_create_task_with_valid_data(self):
        """Task creation should succeed with valid data."""
        task = self.task_service.create_task("Complete project", self.user.user_id)
        
        self.assertIsNotNone(task.task_id)
        self.assertEqual(task.title, "Complete project")
        self.assertEqual(task.user_id, self.user.user_id)
        self.assertEqual(task.status, "pending")
        self.assertIsNotNone(task.created_at)
    
    def test_create_task_with_all_fields(self):
        """Task creation should succeed with all fields provided."""
        task = self.task_service.create_task(
            title="Complete project",
            user_id=self.user.user_id,
            description="A detailed task",
            status="in_progress"
        )
        
        self.assertEqual(task.title, "Complete project")
        self.assertEqual(task.description, "A detailed task")
        self.assertEqual(task.status, "in_progress")
    
    def test_create_task_with_invalid_title(self):
        """Task creation should fail with empty title."""
        with self.assertRaises(ValidationError):
            self.task_service.create_task("", self.user.user_id)
    
    def test_create_task_with_invalid_status(self):
        """Task creation should fail with invalid status."""
        with self.assertRaises(ValidationError):
            self.task_service.create_task(
                "Task",
                self.user.user_id,
                status="invalid_status"
            )
    
    def test_create_task_with_nonexistent_user(self):
        """Task creation should fail with non-existent user."""
        with self.assertRaises(KeyError):
            self.task_service.create_task("Task", "nonexistent-user-id")


class TestTaskRetrieval(unittest.TestCase):
    """Test task retrieval functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.user_service = UserService()
        self.task_service = TaskService(self.user_service)
        self.user1 = self.user_service.create_user("John Doe", "john@example.com")
        self.user2 = self.user_service.create_user("Jane Doe", "jane@example.com")
        
        self.task1 = self.task_service.create_task("Task 1", self.user1.user_id)
        self.task2 = self.task_service.create_task("Task 2", self.user1.user_id)
        self.task3 = self.task_service.create_task("Task 3", self.user2.user_id)
    
    def test_get_task_by_id(self):
        """Task retrieval should return correct task."""
        retrieved = self.task_service.get_task(self.task1.task_id)
        
        self.assertEqual(retrieved.task_id, self.task1.task_id)
        self.assertEqual(retrieved.title, self.task1.title)
    
    def test_get_task_with_nonexistent_id(self):
        """Task retrieval should fail with non-existent ID."""
        with self.assertRaises(KeyError):
            self.task_service.get_task("nonexistent-id")
    
    def test_get_all_tasks(self):
        """Get all tasks should return all created tasks."""
        all_tasks = self.task_service.get_all_tasks()
        
        self.assertEqual(len(all_tasks), 3)
    
    def test_get_user_tasks(self):
        """Get user tasks should return only tasks for that user."""
        user1_tasks = self.task_service.get_user_tasks(self.user1.user_id)
        user2_tasks = self.task_service.get_user_tasks(self.user2.user_id)
        
        self.assertEqual(len(user1_tasks), 2)
        self.assertEqual(len(user2_tasks), 1)
        
        for task in user1_tasks:
            self.assertEqual(task.user_id, self.user1.user_id)
    
    def test_get_tasks_by_status(self):
        """Get tasks by status should return tasks with that status."""
        # Update some tasks
        self.task_service.update_task(self.task1.task_id, status="completed")
        self.task_service.update_task(self.task2.task_id, status="in_progress")
        
        pending_tasks = self.task_service.get_tasks_by_status("pending")
        completed_tasks = self.task_service.get_tasks_by_status("completed")
        in_progress_tasks = self.task_service.get_tasks_by_status("in_progress")
        
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(len(in_progress_tasks), 1)


class TestTaskUpdate(unittest.TestCase):
    """Test task update functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.user_service = UserService()
        self.task_service = TaskService(self.user_service)
        self.user = self.user_service.create_user("John Doe", "john@example.com")
        self.task = self.task_service.create_task("Original Task", self.user.user_id)
    
    def test_update_task_title(self):
        """Task update should change title."""
        updated = self.task_service.update_task(self.task.task_id, title="Updated Task")
        
        self.assertEqual(updated.title, "Updated Task")
    
    def test_update_task_description(self):
        """Task update should change description."""
        updated = self.task_service.update_task(
            self.task.task_id,
            description="New description"
        )
        
        self.assertEqual(updated.description, "New description")
    
    def test_update_task_status(self):
        """Task update should change status."""
        updated = self.task_service.update_task(
            self.task.task_id,
            status="completed"
        )
        
        self.assertEqual(updated.status, "completed")
    
    def test_update_task_all_fields(self):
        """Task update should change multiple fields."""
        updated = self.task_service.update_task(
            self.task.task_id,
            title="New Title",
            description="New Description",
            status="in_progress"
        )
        
        self.assertEqual(updated.title, "New Title")
        self.assertEqual(updated.description, "New Description")
        self.assertEqual(updated.status, "in_progress")
    
    def test_update_task_with_invalid_status(self):
        """Task update should fail with invalid status."""
        with self.assertRaises(ValidationError):
            self.task_service.update_task(self.task.task_id, status="invalid_status")
    
    def test_update_task_with_nonexistent_id(self):
        """Task update should fail with non-existent ID."""
        with self.assertRaises(KeyError):
            self.task_service.update_task("nonexistent-id", title="New Title")
    
    def test_update_task_updates_timestamp(self):
        """Task update should set the updated_at timestamp."""
        updated = self.task_service.update_task(self.task.task_id, status="completed")
        
        # Verify updated_at is set and follows expected format
        self.assertIsNotNone(updated.updated_at)
        self.assertIn(":", updated.updated_at)  # Contains time separator
        self.assertTrue(len(updated.updated_at) >= 10)  # YYYY-MM-DD minimum


class TestTaskDeletion(unittest.TestCase):
    """Test task deletion functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.user_service = UserService()
        self.task_service = TaskService(self.user_service)
        self.user = self.user_service.create_user("John Doe", "john@example.com")
        self.task = self.task_service.create_task("Task to Delete", self.user.user_id)
    
    def test_delete_task(self):
        """Task deletion should remove the task."""
        self.task_service.delete_task(self.task.task_id)
        
        with self.assertRaises(KeyError):
            self.task_service.get_task(self.task.task_id)
    
    def test_delete_task_with_nonexistent_id(self):
        """Task deletion should fail with non-existent ID."""
        with self.assertRaises(KeyError):
            self.task_service.delete_task("nonexistent-id")


class TestTaskExistenceCheck(unittest.TestCase):
    """Test task existence check functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.user_service = UserService()
        self.task_service = TaskService(self.user_service)
        self.user = self.user_service.create_user("John Doe", "john@example.com")
        self.task = self.task_service.create_task("Task", self.user.user_id)
    
    def test_task_exists(self):
        """Task existence check should return True for existing task."""
        self.assertTrue(self.task_service.task_exists(self.task.task_id))
    
    def test_task_does_not_exist(self):
        """Task existence check should return False for non-existent task."""
        self.assertFalse(self.task_service.task_exists("nonexistent-id"))


if __name__ == "__main__":
    unittest.main()
