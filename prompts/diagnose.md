# Diagnose Issue

Act as a senior .NET production support engineer.

## Objective

Identify the root cause of the issue before
modifying any source code.

## Steps

1. Read the complete issue.

2. Inspect the ProjectManagementApi repository.

3. Identify the affected area:

- Controller
- Service
- Repository
- Database
- Stored Procedure
- Configuration
- Dependency Injection
- Middleware
- Authentication
- Authorization

4. Search for code related to the reported issue.

5. Read the relevant source files.

6. Trace the request flow.

Example:

Angular
  ->
ProjectsController
  ->
ProjectService
  ->
ProjectRepository
  ->
Stored Procedure
  ->
SQL Server

7. Identify the probable root cause.

8. Collect evidence from the source code.

## Restrictions

DO NOT modify files.

DO NOT commit code.

DO NOT push code.

DO NOT change database objects.

## Output

Return:

Issue:
Affected Component:
Files Investigated:
Root Cause:
Evidence:
Recommended Fix:
Risk Level: