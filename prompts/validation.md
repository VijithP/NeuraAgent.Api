# Validate Code Changes

Act as a .NET build and test engineer.

Validate the changes made for the current issue.

## Step 1

Run:

dotnet restore

## Step 2

Run:

dotnet build

Build must succeed.

If build fails:

1. Read the compiler error.
2. Determine whether the change caused it.
3. Fix only problems related to the current change.
4. Run build again.

## Step 3

Run:

dotnet test

If no test project exists, report:

No automated test project found.

Do not report tests as successful if no tests ran.

## Output

Build Result:
Test Result:
Tests Executed:
Tests Passed:
Tests Failed:
Warnings:
Validation Status: