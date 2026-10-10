# Code Review

Act as a senior .NET code reviewer.

Review the complete change before it is committed.

Run:

git status

git diff

Review every modified file.

## Check

- Does the change fix the reported issue?
- Are there unrelated modifications?
- Does the project still follow its architecture?
- Is error handling correct?
- Is async/await used correctly?
- Are nullable values handled?
- Are secrets exposed?
- Are connection strings exposed?
- Are security controls weakened?
- Were unnecessary files modified?

## Security Check

Look specifically for:

- API keys
- passwords
- access tokens
- connection strings
- private keys

## Decision

Return one of:

APPROVED

or

REJECTED

If rejected, explain what must be corrected.

Do not commit rejected code.