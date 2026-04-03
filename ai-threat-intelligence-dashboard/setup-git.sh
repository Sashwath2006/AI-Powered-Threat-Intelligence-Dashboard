#!/bin/bash
# GitHub Setup Script for AI Threat Intelligence Dashboard
# Run this to initialize git and prepare for GitHub deployment

echo "=========================================="
echo "Git Repository Setup"
echo "=========================================="
echo ""

# Initialize git
echo "1. Initializing git repository..."
git init

# Configure git (user should customize these)
echo ""
echo "2. Configuring git..."
echo "Configure your git user info:"
echo ""
read -p "Enter your name (e.g., John Doe): " git_name
read -p "Enter your email (e.g., john@example.com): " git_email

git config user.name "$git_name"
git config user.email "$git_email"

echo "✓ Configured: $git_name <$git_email>"

# Add files
echo ""
echo "3. Adding project files..."
git add .

# Create first commit
echo ""
echo "4. Creating initial commit..."
git commit -m "Initial commit: AI Threat Intelligence Dashboard

- Backend FastAPI server with anomaly detection
- Frontend Streamlit dashboard with visualizations
- ML pipeline using Isolation Forest
- CSV data processing with schema flexibility
- Complete deployment configuration"

# Verify
echo ""
echo "=========================================="
echo "✓ LOCAL GIT REPOSITORY READY"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Create GitHub repository at https://github.com/new"
echo "2. Name it: ai-threat-intelligence-dashboard"
echo "3. Copy the repository URL"
echo "4. Run these commands:"
echo ""
echo "   git remote add origin <YOUR_REPO_URL>"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "5. Then deploy to Streamlit Cloud:"
echo "   - Go to https://streamlit.io/cloud"
echo "   - Click 'New app'"
echo "   - Select your repository"
echo "   - Main file path: frontend/app.py"
echo ""
