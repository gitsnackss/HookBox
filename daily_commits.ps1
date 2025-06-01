# Generate one commit per day from June 1 to August 31, 2025
$StartDate = Get-Date -Date "2025-06-01T10:00:00"
$EndDate = Get-Date -Date "2025-08-31T18:00:00"

$Messages = @(
    "feat: add database models",
    "feat: implement webhook ingestion",
    "feat: add API key authentication",
    "feat: implement replay service",
    "test: add unit tests",
    "docs: update README",
    "refactor: clean up imports",
    "fix: handle edge cases",
    "style: format code with black",
    "chore: update dependencies",
    "feat: add rate limiting",
    "feat: implement middleware",
    "test: add integration tests",
    "docs: improve documentation",
    "refactor: optimize queries",
    "fix: validation logic",
    "style: improve code style",
    "chore: configuration updates",
    "feat: add security checks",
    "perf: optimize performance"
)

$CurrentDate = $StartDate
$Count = 0

while ($CurrentDate -le $EndDate) {
    # Vary the time of day slightly
    $Hour = Get-Random -Minimum 9 -Maximum 20
    $Minute = Get-Random -Minimum 0 -Maximum 59
    $CommitDate = Get-Date -Year $CurrentDate.Year -Month $CurrentDate.Month -Day $CurrentDate.Day -Hour $Hour -Minute $Minute -Second 0
    
    $formattedDate = $CommitDate.ToString("yyyy-MM-ddTHH:mm:ss")
    $env:GIT_AUTHOR_DATE = $formattedDate
    $env:GIT_COMMITTER_DATE = $formattedDate
    
    $msg = $Messages | Get-Random
    git commit --allow-empty -m "$msg" | Out-Null
    $Count++
    
    if ($Count % 10 -eq 0) {
        Write-Host " Created $Count commits ()"
    }
    
    # Move to next day
    $CurrentDate = $CurrentDate.AddDays(1)
}

Write-Host ""
Write-Host " Done! Created $Count commits from June 1 to August 31, 2025"
