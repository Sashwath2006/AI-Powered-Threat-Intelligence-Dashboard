# GitHub Setup Script for AI Threat Intelligence Dashboard
# Run this in PowerShell to initialize git and prepare for GitHub deployment

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Git Repository Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Initialize git
Write-Host "1. Initializing git repository..." -ForegroundColor Green
git init

# Configure git (user should customize these)
Write-Host ""
Write-Host "2. Configuring git..." -ForegroundColor Green
Write-Host "Configure your git user info:" -ForegroundColor Yellow
Write-Host ""

$git_name = Read-Host "Enter your name (e.g., John Doe)"
$git_email = Read-Host "Enter your email (e.g., john@example.com)"

git config user.name $git_name
git config user.email $git_email

Write-Host "✓ Configured: $git_name <$git_email>" -ForegroundColor Green

# Add files
Write-Host ""
Write-Host "3. Adding project files..." -ForegroundColor Green
git add .

# Create first commit
Write-Host ""
Write-Host "4. Creating initial commit..." -ForegroundColor Green

$commit_msg = @"
Initial commit: AI Threat Intelligence Dashboard

- Backend FastAPI server with anomaly detection
- Frontend Streamlit dashboard with visualizations
- ML pipeline using Isolation Forest
- CSV data processing with schema flexibility
- Complete deployment configuration
"@

git commit -m $commit_msg

# Verify
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "✓ LOCAL GIT REPOSITORY READY" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Create GitHub repository at https://github.com/new" -ForegroundColor White
Write-Host "2. Name it: ai-threat-intelligence-dashboard" -ForegroundColor White
Write-Host "3. Copy the repository URL" -ForegroundColor White
Write-Host "4. Run these commands:" -ForegroundColor White
Write-Host ""
Write-Host "   git remote add origin <YOUR_REPO_URL>" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "5. Then deploy to Streamlit Cloud:" -ForegroundColor White
Write-Host "   - Go to https://streamlit.io/cloud" -ForegroundColor White
Write-Host "   - Click 'New app'" -ForegroundColor White
Write-Host "   - Select your repository" -ForegroundColor White
Write-Host "   - Main file path: frontend/app.py" -ForegroundColor White
Write-Host ""
