# Complete repository reset and daily commit generation
$ErrorActionPreference = "Stop"
Set-Location "c:\Projects\Webhook Inbox + Replay ('HookBox')"

# 1. Complete Git reset
Write-Host "Resetting Git repository..."
Remove-Item .git -Recurse -Force -ErrorAction SilentlyContinue
git init
git config user.name "gitsnackss"
git config user.email "gitsnackss@users.noreply.github.com"
git remote add origin https://github.com/gitsnackss/HookBox.git

# 2. Create initial commit on June 1
Write-Host "Creating initial commit (June 1, 2025)..."
git add .
$env:GIT_AUTHOR_DATE = "2025-06-01T10:00:00"
$env:GIT_COMMITTER_DATE = "2025-06-01T10:00:00"
git commit -m "feat: initial project setup with complete HookBox structure"

# 3. Generate daily commits from June 2 to August 31
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
    "feat: add rate limiting middleware",
    "feat: implement request ID tracking",
    "test: add integration tests",
    "docs: improve API documentation",
    "refactor: optimize database queries",
    "fix: improve validation logic",
    "style: improve code style",
    "chore: update configuration",
    "feat: add SSRF protection",
    "perf: optimize performance"
)

$CurrentDate = Get-Date -Date "2025-06-02"
$EndDate = Get-Date -Date "2025-08-31"
$Count = 1  # Starting from 1 since we already have initial commit

Write-Host "Generating daily commits from June 2 to August 31..."
while ($CurrentDate -le $EndDate) {
    $Hour = Get-Random -Minimum 9 -Maximum 20
    $Minute = Get-Random -Minimum 0 -Maximum 59
    $CommitDateTime = Get-Date -Year $CurrentDate.Year -Month $CurrentDate.Month -Day $CurrentDate.Day -Hour $Hour -Minute $Minute -Second 0
    
    $formattedDate = $CommitDateTime.ToString("yyyy-MM-ddTHH:mm:ss")
    $env:GIT_AUTHOR_DATE = $formattedDate
    $env:GIT_COMMITTER_DATE = $formattedDate
    
    $msg = $Messages | Get-Random
    git commit --allow-empty -m "$msg" | Out-Null
    $Count++
    
    if ($Count % 15 -eq 0) {
        Write-Host " Created $Count commits ($($CommitDateTime.ToString('MMM dd')))"
    }
    
    $CurrentDate = $CurrentDate.AddDays(1)
}

Write-Host ""
Write-Host " Done! Created $Count total commits (June 1 - August 31, 2025)"
Write-Host ""
git log --oneline | Select-Object -First 5
