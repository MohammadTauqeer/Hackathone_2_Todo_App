# Data Model: Phase V - Advanced Cloud Deployment

## Overview
This document defines the data models for Phase V of the Cloud Native Todo Chatbot project, including new entities for advanced features and event-driven architecture.

## Core Task Entity

### Task
Represents a single task in the todo list with enhanced properties for Phase V.

```json
{
  "id": "string (UUID)",
  "title": "string (required)",
  "description": "string (optional)",
  "priority": {
    "level": "enum (LOW, MEDIUM, HIGH)",
    "value": "integer (1-3, where 3 is highest)"
  },
  "tags": [
    {
      "id": "string (UUID)",
      "name": "string",
      "color": "string (hex color code)"
    }
  ],
  "dueDate": "datetime (ISO 8601, optional)",
  "recurrence": {
    "pattern": "enum (DAILY, WEEKLY, MONTHLY, YEARLY)",
    "interval": "integer (e.g., every 2 weeks)",
    "endDate": "datetime (optional, when recurrence ends)"
  },
  "status": "enum (TODO, IN_PROGRESS, DONE, ARCHIVED)",
  "createdAt": "datetime (ISO 8601)",
  "updatedAt": "datetime (ISO 8601)",
  "createdBy": "string (user ID)",
  "assignedTo": "string (user ID, optional)",
  "parentTaskId": "string (UUID, for subtasks, optional)"
}
```

## Supporting Entities

### Tag
Category for organizing tasks.

```json
{
  "id": "string (UUID)",
  "name": "string (unique)",
  "description": "string (optional)",
  "color": "string (hex color code)",
  "createdAt": "datetime (ISO 8601)",
  "updatedAt": "datetime (ISO 8601)",
  "createdBy": "string (user ID)"
}
```

### Priority
Priority level definition.

```json
{
  "id": "string (UUID)",
  "name": "enum (LOW, MEDIUM, HIGH)",
  "value": "integer (1-3, where 3 is highest)",
  "description": "string",
  "color": "string (hex color code)"
}
```

### Reminder
Definition for task reminders.

```json
{
  "id": "string (UUID)",
  "taskId": "string (UUID, required)",
  "triggerTime": "datetime (ISO 8601, when to trigger)",
  "method": "enum (EMAIL, PUSH_NOTIFICATION, SMS)",
  "status": "enum (PENDING, SENT, CANCELLED)",
  "createdAt": "datetime (ISO 8601)",
  "sentAt": "datetime (ISO 8601, when sent)"
}
```

### RecurringTask
Configuration for recurring tasks.

```json
{
  "id": "string (UUID)",
  "originalTaskId": "string (UUID, required)",
  "pattern": "enum (DAILY, WEEKLY, MONTHLY, YEARLY)",
  "interval": "integer (e.g., every 2 weeks)",
  "occurrences": "integer (optional, max occurrences)",
  "endDate": "datetime (optional, when recurrence ends)",
  "exceptions": [
    "datetime (dates to skip)"
  ],
  "nextOccurrence": "datetime (when next instance will be created)",
  "createdAt": "datetime (ISO 8601)",
  "updatedAt": "datetime (ISO 8601)"
}
```

## Event Models

### TaskEvent
Base event for task-related activities.

```json
{
  "eventId": "string (UUID)",
  "eventType": "enum (TASK_CREATED, TASK_UPDATED, TASK_DELETED, TASK_COMPLETED)",
  "taskId": "string (UUID)",
  "timestamp": "datetime (ISO 8601)",
  "source": "string (service that generated event)",
  "payload": {
    // Contains the relevant task data depending on event type
  },
  "version": "string (event schema version)"
}
```

### ReminderEvent
Event for triggering reminders.

```json
{
  "eventId": "string (UUID)",
  "eventType": "REMINDER_TRIGGERED",
  "taskId": "string (UUID)",
  "reminderId": "string (UUID)",
  "timestamp": "datetime (ISO 8601)",
  "targetTime": "datetime (when reminder was scheduled)",
  "method": "enum (EMAIL, PUSH_NOTIFICATION, SMS)",
  "version": "string (event schema version)"
}
```

## Relationships

### Task Relationships
- One Task can have many Tags (many-to-many via task_tags junction table)
- One Task can have one parent Task (self-referencing for subtasks)
- One Task can have many child Tasks (self-referencing for subtasks)
- One Task can have many Reminders (one-to-many)

### Tag Relationships
- One Tag can be associated with many Tasks (many-to-many via task_tags junction table)

### RecurringTask Relationships
- One RecurringTask configuration creates many Task instances (one-to-many)

## Dapr State Store Considerations

### State Store Configuration
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: task-statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: localhost:6379
  - name: redisPassword
    value: ""
  - name: actorStateStore
    value: "true"
```

### State Store Patterns
- Use composite keys for related data: `task||{taskId}`, `user-tasks||{userId}||{taskId}`
- Leverage ETags for concurrency control
- Use transactions for atomic updates across multiple entities

## Kafka/Event Stream Topics

### Topic Definitions
- `task-events`: For all task-related events (create, update, delete)
- `reminder-events`: For reminder-triggered events
- `notification-events`: For notification delivery events

### Message Format
Events will follow CloudEvents specification with custom data payload:
```json
{
  "specversion": "1.0",
  "type": "com.example.task.created",
  "source": "/tasks",
  "id": "A234-1234-5678",
  "time": "2026-02-05T14:30:00Z",
  "datacontenttype": "application/json",
  "data": {
    // Task-specific data
  }
}
```

## Indexes and Queries

### Common Queries
1. Get tasks by user with filters (priority, tags, status)
2. Get tasks by due date range
3. Find recurring tasks that need new instances created
4. Get upcoming reminders

### Recommended Indexes
- `{ userId: 1, createdAt: -1 }` for user task timelines
- `{ userId: 1, status: 1, priority.value: -1 }` for filtered task views
- `{ userId: 1, dueDate: 1 }` for due date queries
- `{ recurrence.nextOccurrence: 1 }` for recurring task processing
- `{ reminder.triggerTime: 1, status: 1 }` for reminder processing