param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[A-Za-z][A-Za-z0-9]+-\d+$')]
    [string]$IssueKey
)

$ErrorActionPreference = "Stop"

$AgentRoot = Split-Path -Parent $PSScriptRoot


function Get-AgentEnvironmentVariable {

    param(
        [Parameter(Mandatory = $true)]
        [string]$VariableName
    )

    Write-Host "Reading environment variable: $VariableName"

    $value = [Environment]::GetEnvironmentVariable(
        $VariableName,
        [EnvironmentVariableTarget]::Process
    )

    if ([string]::IsNullOrWhiteSpace($value)) {

        $value = [Environment]::GetEnvironmentVariable(
            $VariableName,
            [EnvironmentVariableTarget]::User
        )
    }

    return $value
}


$ProjectPath = Get-AgentEnvironmentVariable `
    -VariableName "PROJECT_REPO_PATH"

$ProjectContext = Get-AgentEnvironmentVariable `
    -VariableName "PROJECT_CONTEXT_PAGE"


if ([string]::IsNullOrWhiteSpace($ProjectPath)) {
    throw "PROJECT_REPO_PATH is not configured."
}

if (!(Test-Path -LiteralPath $ProjectPath)) {
    throw "Repository does not exist: $ProjectPath"
}


Write-Host ""
Write-Host "======================================="
Write-Host " Project Management AI Support Agent"
Write-Host "======================================="
Write-Host "Issue      : $IssueKey"
Write-Host "Agent Root : $AgentRoot"
Write-Host "Repository : $ProjectPath"
Write-Host "Context    : $ProjectContext"
Write-Host ""

Set-Location -LiteralPath $AgentRoot


$prompt = @"
Process Jira issue $IssueKey.

Follow all instructions in CLAUDE.md.

Target repository:
$ProjectPath

Context page:
$ProjectContext

Workflow:

1. Retrieve Jira issue $IssueKey.
2. Read the complete Jira issue.
3. Follow prompts/jira-read.md.
4. Follow prompts/context-read.md.
5. Follow prompts/diagnose.md.
6. Inspect the target repository.
7. Identify the root cause.
8. Follow prompts/code-fix.md if a source-code change is required.
9. Run dotnet build.
10. Run dotnet test.
11. Follow prompts/code-review.md.
12. Show the final git diff.

Do not modify unrelated files.
Do not push code.
Do not create a pull request without human approval.
"@

claude --print $prompt