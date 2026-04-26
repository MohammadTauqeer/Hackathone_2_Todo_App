"""
Task Manager for the Todo App.

This module provides the TaskManager class which handles all CRUD operations
for tasks in memory.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from src.models.task import Task, RecurrenceEnum
from src.services.storage_manager import StorageManager


class TaskManager:
    """
    Manages tasks in memory with CRUD operations.

    The TaskManager handles all operations related to tasks including
    adding, retrieving, updating, deleting, and toggling completion status.
    """

    def __init__(self, storage_manager: StorageManager = None):
        """
        Initialize the TaskManager with an empty task storage.

        Args:
            storage_manager: Optional StorageManager for persistence
        """
        self.storage_manager = storage_manager or StorageManager()

        # Load existing tasks if available
        self._tasks = self.storage_manager.load_tasks()

        # Determine the next ID based on loaded tasks
        if self._tasks:
            self._next_id = max(self._tasks.keys()) + 1
        else:
            self._next_id = 1

    def add_task(self, title: str, description: str = "", priority=None, tags=None, due_date=None, recurrence=None) -> Task:
        """
        Add a new task to the collection.

        Args:
            title: The title of the task
            description: Optional description of the task
            priority: Priority level of the task
            tags: List of tags for the task
            due_date: Due date for the task
            recurrence: Recurrence pattern for the task

        Returns:
            The newly created Task object with a unique ID

        Raises:
            ValueError: If title is empty or invalid
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        task_id = self._next_id
        self._next_id += 1

        # Use defaults if not provided
        if priority is None:
            from src.models.task import PriorityEnum
            priority = PriorityEnum.MEDIUM
        if tags is None:
            tags = []
        
        task = Task(
            id=task_id, 
            title=title.strip(), 
            description=description.strip(),
            priority=priority,
            tags=tags,
            due_date=due_date,
            recurrence=recurrence
        )
        self._tasks[task_id] = task

        # Save tasks to storage
        self.storage_manager.save_tasks(self._tasks)

        return task

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks in the collection.

        Returns:
            A list of all Task objects
        """
        return list(self._tasks.values())

    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None, completed: Optional[bool] = None,
                   priority: Optional = None, tags: Optional[List[str]] = None,
                   due_date: Optional[datetime] = None, recurrence: Optional = None) -> Optional[Task]:
        """
        Update an existing task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)
            completed: New completion status for the task (optional)
            priority: New priority for the task (optional)
            tags: New tags for the task (optional)
            due_date: New due date for the task (optional)
            recurrence: New recurrence pattern for the task (optional)

        Returns:
            The updated Task object if successful, None if task doesn't exist
        """
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]

        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty")
            task.title = title.strip()

        if description is not None:
            task.description = description.strip()
            
        if completed is not None:
            task.completed = completed
            
        if priority is not None:
            task.priority = priority
            
        if tags is not None:
            task.tags = tags
            
        if due_date is not None:
            task.due_date = due_date
            
        if recurrence is not None:
            task.recurrence = recurrence

        # Save tasks to storage
        self.storage_manager.save_tasks(self._tasks)

        return task

    def toggle_task_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task.
        If the task has recurrence, create a new task with the same properties.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            The updated Task object if successful, None if task doesn't exist
        """
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]
        previous_completed_status = task.completed
        task.completed = not task.completed

        # If task was marked as completed and has recurrence, create a new recurring task
        if not previous_completed_status and task.completed and task.recurrence:
            new_task = self._create_recurring_task(task)
            if new_task:
                return new_task

        # Save tasks to storage
        self.storage_manager.save_tasks(self._tasks)

        return task

    def mark_task_completed(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as completed.
        If the task has recurrence, create a new task with the same properties.

        Args:
            task_id: The ID of the task to mark as completed

        Returns:
            The updated Task object if successful, None if task doesn't exist
        """
        if task_id not in self._tasks:
            return None

        task = self._tasks[task_id]
        
        # Only process recurrence if task wasn't already completed
        if not task.completed:
            task.completed = True
            
            # If task has recurrence, create a new recurring task
            if task.recurrence:
                new_task = self._create_recurring_task(task)
                if new_task:
                    return new_task

        # Save tasks to storage
        self.storage_manager.save_tasks(self._tasks)

        return task

    def _create_recurring_task(self, original_task: Task) -> Optional[Task]:
        """
        Create a new task based on the recurrence pattern of the original task.

        Args:
            original_task: The original task that was completed

        Returns:
            The new recurring Task object if successful
        """
        # Calculate the next due date based on recurrence pattern
        next_due_date = None
        if original_task.due_date:
            if original_task.recurrence == RecurrenceEnum.DAILY:
                next_due_date = original_task.due_date + timedelta(days=1)
            elif original_task.recurrence == RecurrenceEnum.WEEKLY:
                next_due_date = original_task.due_date + timedelta(weeks=1)
            elif original_task.recurrence == RecurrenceEnum.MONTHLY:
                # Simple month addition (doesn't handle end-of-month complexities)
                next_due_date = original_task.due_date + timedelta(days=30)
        
        # Create a new task with the same properties except for completion status
        new_task = self.add_task(
            title=original_task.title,
            description=original_task.description,
            priority=original_task.priority,
            tags=original_task.tags[:],  # Copy the tags list
            due_date=next_due_date,
            recurrence=original_task.recurrence
        )
        
        return new_task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task from the collection.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if it didn't exist
        """
        if task_id not in self._tasks:
            return False

        del self._tasks[task_id]

        # Save tasks to storage
        self.storage_manager.save_tasks(self._tasks)

        return True

    def get_next_id(self) -> int:
        """
        Get the next available task ID without incrementing the counter.

        Returns:
            The next available task ID
        """
        return self._next_id