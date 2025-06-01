# Generate realistic commit history
$StartDate = Get-Date -Date "2025-06-02T09:00:00"
$Messages = @(
    "chore: initial project setup",
    "feat: add database models",
    "feat: implement webhook ingestion",
    "feat: add API key authentication",
    "feat: implement replay service",
    "test: add initial tests",
    "docs: update README",
    "refactor: clean up imports",
    "fix: handle edge cases",
    "style: format code"
)

$CurrentDate = $StartDate
for ($i = 0; $i -lt 95; $i++) {
    $Hours = Get-Random -Minimum 4 -Maximum 24
    $CurrentDate = $CurrentDate.AddHours($Hours)
    $formattedDate = $CurrentDate.ToString("yyyy-MM-ddTHH:mm:ss")
    $env:GIT_AUTHOR_DATE = $formattedDate
    $env:GIT_COMMITTER_DATE = $formattedDate
    $msg = $Messages | Get-Random
    git commit --allow-empty -m "$msg"
    Write-Host " Commit $($i + 1)/95"
}
Write-Host "Done!"
