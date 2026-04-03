# GitHub & Streamlit Cloud Deployment Guide

## 📋 Prerequisites

- GitHub account (free at https://github.com)
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- Git installed on your machine (`git --version` to verify)

---

## Step 1: Initialize Git Repository (LOCAL)

Run these commands in your project directory:

```bash
cd f:\Intern Project\ai-threat-intelligence-dashboard

# Initialize git repo
git init

# Configure git (replace with your info)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files (except those in .gitignore)
git add .

# Create first commit
git commit -m "Initial commit: AI Threat Intelligence Dashboard"

# Check status
git status
```

---

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Fill in details:
   - **Repository name:** `ai-threat-intelligence-dashboard`
   - **Description:** "AI-powered threat intelligence dashboard using FastAPI and Streamlit"
   - **Visibility:** Choose Public (for Streamlit Cloud free tier)
   - **Initialize repo:** Leave unchecked (you already have local repo)
3. Click **Create repository**
4. **COPY the repository URL** (looks like `https://github.com/YOUR_USERNAME/ai-threat-intelligence-dashboard.git`)

---

## Step 3: Connect Local Repo to GitHub

```bash
# Add remote origin (replace with your URL from Step 2)
git remote add origin https://github.com/YOUR_USERNAME/ai-threat-intelligence-dashboard.git

# Verify remote
git remote -v

# Push to GitHub (first time)
git branch -M main
git push -u origin main

# Future pushes (just this)
git push
```

---

## Step 4: Deploy to Streamlit Cloud

### Important: Frontend-Only Deployment

**Note:** Streamlit Cloud hosts the **frontend only**. The backend API needs separate hosting.

### For Frontend (Streamlit App):

1. Go to https://streamlit.io/cloud
2. Click **"New app"**
3. Select your GitHub repository:
   - **Repository:** `YOUR_USERNAME/ai-threat-intelligence-dashboard`
   - **Branch:** `main`
   - **Main file path:** `frontend/app.py`
4. Click **Deploy**

Streamlit will handle:
- Installing requirements from `frontend/requirements.txt`
- Running the app
- Assigning you a public URL

---

## Step 5: Configure Backend API (Separate Hosting)

Since Streamlit Cloud only hosts the frontend, you need to host the backend API elsewhere:

### Option A: Heroku (Free tier retired, but still popular)
```bash
# Install Heroku CLI
# Create Procfile for backend:
web: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Option B: Railway.app (Recommended - has free tier)
1. Go to https://railway.app
2. Connect your GitHub repo
3. Select the backend service for deployment
4. Railway auto-detects and deploys

### Option C: Render.com (Free tier available)
1. Go to https://render.com
2. Create new web service
3. Connect GitHub repo
4. Configuration:
   - **Build command:** `pip install -r backend/requirements.txt`
   - **Start command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Option D: PythonAnywhere (Python-specific hosting)
1. Go to https://www.pythonanywhere.com
2. Upload code and configure WSGI app
3. Point to FastAPI app

---

## Step 6: Update Frontend Config for Production

After backend is deployed, update the API URL in your frontend:

**File:** `frontend/app.py`

```python
# Local development
BACKEND_URL = "http://localhost:8000"

# Update to production backend URL
BACKEND_URL = "https://your-api.onrender.com"  # or your backend URL
```

Then push to GitHub:

```bash
git add frontend/app.py
git commit -m "Update backend URL for production"
git push
```

Streamlit Cloud will auto-redeploy with the new config.

---

## Common Git Commands

```bash
# Check what files changed
git status

# Add specific files
git add file.py

# Add all changes
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push

# Pull latest from GitHub
git pull

# View commit history
git log --oneline

# Create new branch
git checkout -b feature/your-feature

# Switch branch
git checkout main
```

---

## Troubleshooting Streamlit Cloud

### App shows "No logs to analyze"
- Check that backend API URL is correct in `frontend/app.py`
- Verify backend is running and accessible
- Check Streamlit logs (click "Manage app" → "Logs")

### 502 Bad Gateway errors
- Backend API may be down
- Check backend logs on hosting platform
- Verify API URL is correct

### Slow startup
- First deployment may take 2-3 minutes
- Streamlit installs dependencies from requirements.txt
- Optimize requirements by removing unused packages

### Import errors
- Ensure all dependencies are in `frontend/requirements.txt`
- Use `pip freeze > requirements.txt` to capture exact versions
- Test locally: `pip install -r frontend/requirements.txt`

---

## Project Structure for Deployment

```
ai-threat-intelligence-dashboard/
├── .git/                          # Git repo (auto-created)
├── .gitignore                     # Files to ignore
├── .streamlit/
│   └── config.toml               # Streamlit config
├── frontend/
│   ├── app.py                    # Streamlit app (DEPLOYED)
│   ├── requirements.txt          # Frontend dependencies
│   └── components/
├── backend/
│   ├── main.py                   # FastAPI entry point
│   ├── requirements.txt          # Backend dependencies
│   └── app/
├── ml/
│   ├── data/
│   │   └── sample_logs.csv      # Sample data
│   └── ...
├── README.md                      # Project documentation
└── DEPLOYMENT_GUIDE.md           # This file
```

---

## Environment Variables (Optional)

If you need API keys or secrets:

1. Create `.env` file locally (DO NOT commit to GitHub)
2. In Streamlit Cloud dashboard:
   - Click "Deploy app" → "Advanced settings"
   - Add environment variables in "Secrets"
3. Access in code:
   ```python
   import streamlit as st
   api_key = st.secrets["api_key"]
   ```

---

## Monitoring & Updates

### View Streamlit Cloud Logs
1. Go to https://share.streamlit.io
2. Click your app
3. Click "Manage app" → "Logs"

### Auto-redeploy on GitHub push
- Streamlit Cloud watches your GitHub repo
- Any push to main branch → auto-redeploy
- Redeploy takes ~1-2 minutes

### Update code
```bash
# Make changes
# Commit
git commit -m "Fixed XYZ"
# Push
git push
# Streamlit Cloud auto-deploys!
```

---

## Production Checklist

- [ ] Git repo initialized and pushed to GitHub
- [ ] .gitignore configured properly
- [ ] Backend API deployed (Railway/Render/Heroku)
- [ ] Frontend deployed to Streamlit Cloud
- [ ] Backend URL updated in `frontend/app.py`
- [ ] Environment variables configured (if needed)
- [ ] App tested with sample data
- [ ] Logs reviewed for errors
- [ ] Performance tested

---

## Support & Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **Streamlit Cloud Docs:** https://docs.streamlit.io/streamlit-cloud/get-started
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Git Documentation:** https://git-scm.com/doc

---

## Next Steps

1. Create GitHub account (if needed)
2. Run Step 1-3 commands locally
3. Choose backend hosting (Railway recommended)
4. Deploy backend
5. Deploy frontend to Streamlit Cloud
6. Test end-to-end
7. Share your public URL!

**Your app will be live at:** `https://your-app-name.streamlit.app` 🚀
