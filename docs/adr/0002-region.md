# ADR-0002: Primary region ap-south-1 (Mumbai)

- Status: Accepted
- Date: 2026-10-02

## Context
The developer is in Bengaluru. The project needs SageMaker AI training,
Pipelines, Model Registry, serverless MLflow, ECR, Lambda, and API Gateway.

## Decision
Deploy all regional resources to ap-south-1.

## Alternatives considered
- us-east-1: often slightly cheaper and gets features first, but has higher latency from India.
- ap-south-2 (Hyderabad): newer region with a narrower ML feature set (no MLflow Apps).

## Consequences
Low latency and in-country data residency. Some prices are a few percent higher
than us-east-1. Billing data and Budgets are global and appear under us-east-1.
