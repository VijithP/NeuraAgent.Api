param(
    [Parameter(Mandatory = $true)]
    [string]$IssueKey
)

$JiraUrl   = $env:JIRA_BASE_URL
$Email     = $env:JIRA_EMAIL
$ApiToken  = $env:JIRA_API_TOKEN

if ([string]::IsNullOrWhiteSpace($JiraUrl)) {
    throw "JIRA_BASE_URL environment variable is missing."
}

if ([string]::IsNullOrWhiteSpace($Email)) {
    throw "JIRA_EMAIL environment variable is missing."
}

if ([string]::IsNullOrWhiteSpace($ApiToken)) {
    throw "JIRA_API_TOKEN environment variable is missing."
}

$credentials = "${Email}:${ApiToken}"

$bytes = [System.Text.Encoding]::ASCII.GetBytes($credentials)

$base64 = [Convert]::ToBase64String($bytes)

$headers = @{
    Authorization = "Basic $base64"
    Accept        = "application/json"
}

$uri = "$JiraUrl/rest/api/3/issue/$IssueKey"

Write-Host "Reading Jira issue: $IssueKey"

$response = Invoke-RestMethod `
    -Uri $uri `
    -Method Get `
    -Headers $headers

$response | ConvertTo-Json -Depth 20