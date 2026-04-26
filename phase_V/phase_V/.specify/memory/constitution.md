<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles: None (completely new constitution)
Added sections: Preamble, Core Principles (7), Amendments and Enforcement
Removed sections: Template placeholders
Templates requiring updates: 
- ✅ .specify/templates/plan-template.md - Updated to reflect new principles
- ✅ .specify/templates/spec-template.md - Updated to reflect new principles  
- ✅ .specify/templates/tasks-template.md - Updated to reflect new principles
- ⚠️  .specify/templates/commands/*.md - May need review for outdated references
- ⚠️  README.md - May need review for principle references
Follow-up TODOs: None
-->

# Phase V: Advanced Cloud Deployment Constitution

## Preamble
This constitution establishes the governing principles, rules, and constraints for Phase V of the Cloud Native Todo Chatbot project. It ensures alignment with Spec-Driven Development (SDD) methodologies, promotes agentic workflows, and enforces the use of AI-assisted tools for advanced feature implementation, event-driven architecture, and cloud-native deployments. All actions in this phase must adhere to these principles to maintain consistency, traceability, efficiency, and scalability across local and cloud environments.

## Core Principles

### Spec-Driven Development (SDD) Supremacy
All work begins with a clear, comprehensive specification (spec.md). No implementation proceeds without an approved spec. The spec drives planning, task breakdown, and execution. Blueprints and specs are used for infrastructure automation, treating infrastructure, features, and deployments as code governed by SDD.

### Agentic Workflow Mandate
Development follows the Agentic Dev Stack: Write spec → Generate plan → Break into tasks → Implement via AI agents (e.g., Claude Code). Human intervention is limited to review and iteration. This includes using AI for code generation, feature implementation, Dapr configurations, Kafka integrations, and cloud deployments.

### No Manual Coding
Direct manual coding by humans is prohibited. All code, manifests, charts, scripts, and configurations must be generated via AI tools like Claude Code, kubectl-ai, or Kagent. For cloud operations, use AI-generated CLI commands or scripts if direct AI tools are limited.

### Tool-Centric Operations
Feature Development: Use Claude Code for generating advanced features (e.g., recurring tasks, priorities) and integrations (e.g., Dapr, Kafka).
Local Operations: Build on Phase IV; use Minikube, Helm, kubectl-ai, and Kagent for deployments and AIOps.
Cloud Operations: Prioritize cloud-native tools (e.g., Azure CLI, gcloud, OCI CLI) generated via AI. Deploy to AKS/GKE/OKE; use managed services like Redpanda Cloud for Kafka if access issues arise.
Distributed Runtime: Mandate full Dapr usage: Pub/Sub (for event-driven), State management, Bindings (e.g., cron for reminders), Secrets, and Service Invocation.
CI/CD and Monitoring: AI-generate GitHub Actions workflows; configure basic monitoring/logging via cloud provider tools.

### Traceability and Review
All prompts, iterations, AI responses, and outputs must be documented. Post-phase review evaluates the process, including adherence to SDD, tool efficacy, feature completeness, and cloud readiness. Assess how specs govern AI agents for advanced managed services.

### Security and Compliance
Ensure secure container images, Dapr sidecar injections, Kafka topic security, and cloud best practices (e.g., RBAC, network policies). Use secrets management via Dapr. Comply with free tier limits to avoid costs.

### Innovation through Research
Incorporate insights from prior phases and cloud setups (e.g., Oracle Always Free for sustainable learning). Favor Oracle OKE for cost-free experimentation.

## Amendments and Enforcement
- Amendments require consensus from project stakeholders and must be documented in updates to this file.
- Violations (e.g., manual coding) invalidate the phase and require restart from the spec stage.
- Success Metrics: Functional advanced features, successful local/cloud deployments, event-driven ops verified via AI checks.

**Version**: 1.1.0 | **Ratified**: 2026-02-05 | **Last Amended**: 2026-02-05