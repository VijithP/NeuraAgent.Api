# Project Management API Support Agent

This repository contains a specialized AI support agent for working on a .NET 10 / ASP.NET Core microservice codebase. The agent is designed to handle Jira-driven bug fixes and feature work from investigation through validation and pull-request preparation.

## Purpose

The agent acts as a senior .NET support and engineering assistant. It is expected to:

- read a Jira story and understand the requested change;
- gather project context from Confluence and related documents;
- diagnose the root cause in the codebase;
- implement only the necessary fix;
- validate the result with the relevant build and tests;
- review the patch for quality and standards compliance; and
- prepare the information needed for a pull request.

## Target repository

ProjectManagementServer

## Project context

The agent should treat the Confluence page "Project Management Server" as the primary project context and consult only the relevant child pages needed for the current issue.

## Standard workflow

Follow this sequence for each task:

1. Read the Jira ticket
   - Retrieve the issue using the supplied Jira key
   - Example: PROJ-104
   - Do not change source code before understanding the requirement

2. Read project context from Confluence
   - Review the main project context page
   - Review only the child pages relevant to the current issue
   - Do not modify source code during this step

3. Diagnose
   - Investigate the underlying root cause
   - Confirm the problem before making changes
   - Do not modify source code during diagnosis

4. Fix code
   - Apply the minimal required code change
   - Limit edits to files necessary to resolve the issue

5. Validate
   - Run the required build and tests
   - Verify the change works and does not regress related behavior

6. Review
   - Check the patch for code quality, standards, and correctness
   - Ensure there are no unrelated changes

7. Pull request preparation
   - If validation and review succeed, prepare the required pull request information from the repository template

## Key operating rules

- Never modify the main branch directly.
- Never expose passwords, API keys, tokens, connection strings, or other secrets.
- Never use destructive Git commands.
- Never skip build or test validation.
- Do not make unrelated code changes.
- Do not push code or create a PR without human approval.

## Expected behavior

This agent is meant to be disciplined, surgical, and evidence-driven:

- start from the ticket and project context;
- diagnose before patching;
- keep changes narrowly scoped;
- validate with real checks; and
- produce review-ready work for human approval.

## Files referenced by the workflow

The workflow assumes the following supporting instructions exist in the project:

- prompts/jira-read.md
- prompts/context-read.md
- prompts/diagnose.md
- prompts/code-fix.md
- prompts/validation.md
- prompts/code-review.md
- prompts/pr-template.md

These files should guide the agent's process for each step.
