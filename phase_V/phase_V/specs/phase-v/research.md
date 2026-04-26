# Research: Phase V - Advanced Cloud Deployment

## Objective
Research and document the technical approach for implementing Phase V of the Cloud Native Todo Chatbot project, focusing on advanced features, event-driven architecture, and cloud deployment.

## Key Technologies to Investigate

### Dapr (Distributed Application Runtime)
- **Pub/Sub Building Block**: For event-driven communication between services
- **State Management**: For persisting task data reliably
- **Bindings**: For connecting to external systems (e.g., cron for reminders)
- **Secrets Management**: For secure configuration
- **Service Invocation**: For inter-service communication

### Kafka vs Alternative Pub/Sub Solutions
- **Kafka**: Robust event streaming platform with strong ordering guarantees
- **Redpanda**: Kafka-compatible alternative with lower resource requirements
- **Dapr-built-in Pub/Sub**: Redis Streams, Azure Service Bus, AWS SQS, GCP Pub/Sub
- **Considerations**: Free tier availability, resource requirements, complexity

### Cloud Platforms for Deployment
- **Oracle Cloud Infrastructure (OCI)**: Offers Always Free tier with OKE cluster
- **Microsoft Azure**: $200 credit for 30 days, AKS managed Kubernetes
- **Google Cloud Platform**: $300 credit for 90 days, GKE managed Kubernetes
- **Comparison**: Resource limits, free tier duration, regional availability

### Event-Driven Architecture Patterns
- **Event Sourcing**: Storing state as a sequence of events
- **CQRS (Command Query Responsibility Segregation)**: Separating read and write operations
- **Saga Pattern**: Managing distributed transactions across services
- **Reactive Programming**: Asynchronous, non-blocking operations

## Implementation Approach

### Feature Development
1. **Intermediate Features** (Priority 1):
   - Priorities: Implement priority levels (low/medium/high) for tasks
   - Tags: Allow tagging tasks for categorization
   - Search/Filter/Sort: Enable querying tasks by various criteria

2. **Advanced Features** (Priority 2):
   - Recurring Tasks: Support for daily/weekly/monthly repeating tasks
   - Due Dates & Reminders: Date assignment with reminder notifications

### Event-Driven Architecture
1. **Event Producers**: Services that publish task-related events (create, update, delete)
2. **Event Consumers**: Services that react to events (notification service, reminder service)
3. **Event Topics**: Kafka topics for different event types (task.created, task.updated, etc.)

### Dapr Integration Points
1. **State Store Component**: For persisting task data
2. **Pub/Sub Component**: For event-driven communication
3. **Bindings Component**: For cron-based reminders
4. **Secrets Store Component**: For configuration management

## Architecture Considerations

### Scalability
- Microservices should be independently scalable
- Use Kubernetes Horizontal Pod Autoscaler (HPA)
- Consider event processing backlogs and scaling consumers accordingly

### Reliability
- Implement circuit breaker patterns
- Use Dapr's built-in retry mechanisms
- Ensure at-least-once delivery for critical events

### Security
- Use Dapr's mTLS for service-to-service communication
- Implement proper authentication and authorization
- Secure Kafka connections with SSL/TLS

### Monitoring and Observability
- Distributed tracing with Dapr
- Centralized logging
- Metrics collection for performance monitoring

## Potential Challenges and Solutions

### Challenge: Kafka Access Limitations
- **Solution**: Use Redpanda Cloud or alternative Dapr-supported Pub/Sub components

### Challenge: Resource Constraints on Free Tiers
- **Solution**: Optimize resource usage, use lightweight alternatives where possible

### Challenge: Event Ordering Requirements
- **Solution**: Use Kafka partitioning strategies or consider alternatives for strict ordering

### Challenge: Reminder Synchronization
- **Solution**: Use Dapr bindings with cron expressions or external schedulers

## Recommended Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API    │    │   Dapr Sidecar  │
│   (Next.js)     │◄──►│   (FastAPI)      │◄──►│                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                      │
                                                      ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Kafka/        │    │   Reminder       │    │   Dapr Sidecar  │
│   Redpanda      │◄──►│   Service        │◄──►│                 │
│                 │    │                  │    └─────────────────┘
└─────────────────┘    └──────────────────┘
                              │
                              ▼
                   ┌─────────────────────────┐
                   │   Notification Service  │
                   │                         │
                   └─────────────────────────┘
```

## Next Steps
1. Prototype Dapr integration with the existing application
2. Set up Kafka/Redpanda for event streaming
3. Implement intermediate features (priorities, tags, search/filter)
4. Implement advanced features (recurring tasks, due dates)
5. Develop event-driven communication between services
6. Test locally on Minikube
7. Deploy to cloud platform