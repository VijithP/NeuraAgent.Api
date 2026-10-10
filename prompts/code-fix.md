# Code Fix

Act as a senior .NET developer.

The root cause has already been identified.

Implement the smallest safe change required
to fix the reported issue.

## Before Changing Code

Check:

git status

Make sure unrelated user changes are not overwritten.

Create or use an issue branch.

Branch naming:

agent/issue-{issue-id}

Example:

agent/issue-SUP-001

## Coding Rules

Follow the existing project architecture.

Use existing:

- Controllers
- Services
- Repositories
- DTOs
- Dependency Injection
- Logging
- Configuration patterns

Do not rewrite unrelated code.

Do not introduce unnecessary packages.

Do not hardcode passwords or secrets.

Do not change production configuration unless
the issue specifically requires it.

## After Modification

Show:

Files Modified:
Reason:
Summary of Changes: