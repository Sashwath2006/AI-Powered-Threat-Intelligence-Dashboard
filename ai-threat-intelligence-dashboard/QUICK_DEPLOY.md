# Deploy to GitHub & Streamlit Cloud - QUICK START

## ⚡ 5-Minute Setup

### Step 1: Initialize Git Locally (< 1 min)

**Option A: PowerShell (Windows)**
```powershell
cd "f:\Intern Project\ai-threat-intelligence-dashboard"
.\setup-git.ps1
```

**Option B: Bash (Mac/Linux/WSL)**
```bash
cd ~/ai-threat-intelligence-dashboard
bash setup-git.sh
```

**Option C: Manual Git Commands**
```bash
cd "f:\Intern Project\ai-threat-intelligence-dashboard"
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
git add .
git commit -m "Initial commit: AI Threat Intelligence Dashboard"
```

---

### Step 2: Create GitHub Repository (< 1 min)

1. Go to **https://github.com/new**
2. **Repository name:** `ai-threat-intelligence-dashboard`
3. **Description:** "AI-powered threat intelligence dashboard"
4. **Public** (required for Streamlit Cloud free tier)
5. Click **Create repository**
6. **COPY the URL** (you'll need it next)

---

### Step 3: Connect & Push to GitHub (< 1 min)

```bash
# Replace YOUR_URL with the URL from Step 2
git remote add origin https://github.com/YOUR_USERNAME/ai-threat-intelligence-dashboard.git
git branch -M main
git push -u origin main
```

✅ **Your code is now on GitHub!**

---

### Step 4: Deploy to Streamlit Cloud (< 3 min)

1. Go to **https://streamlit.io/cloud**
2. Click **"New app"**
3. Select:
   - **Repository:** `YOUR_USERNAME/ai-threat-intelligence-dashboard`
   - **Branch:** `main`
   - **Main file path:** `frontend/app.py`
4. Click **Deploy**
5. Wait 2-3 minutes for deployment
6. Your app URL: `https://your-app-name.streamlit.app`

✅ **Your frontend is now live!**

---

### Step 5 (Optional): Deploy Backend

**Without this step:** Dashboard works but "Analyze" button won't work

Choose one backend host (free tier):

<details>
<summary><b>Railway.app (Recommended)</b></summary>

1. Go to **https://railway.app**
2. Click **"New Project"** → **"Deploy from GitHub"**
3. Connect your GitHub repo
4. Railway auto-detects FastAPI
5. Add environment variable (if needed)
6. Deploy
7. Copy the public URL
8. Update `BACKEND_URL` in `frontend/app.py` to the Railway URL
9. Push update: `git push`
10. Streamlit Cloud auto-redeploys

</details>

<details>
<summary><b>Render.com</b></summary>

1. Go to **https://render.com**
2. Click **"New+"** → **"Web Service"**
3. Connect GitHub repo
4. **Build command:** `pip install -r backend/requirements.txt`
5. **Start command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000`
6. Deploy
7. Copy the public URL
8. Update `frontend/app.py` with new backend URL
9. Push: `git push`

</details>

---

## 📝 Important Files

These files control your deployment:

| File | Purpose | Location |
|------|---------|----------|
| `frontend/app.py` | Streamlit app | Deployed to Streamlit Cloud |
| `frontend/requirements.txt` | Python dependencies | Auto-installed on deployment |
| `BACKEND_URL` | API endpoint | Set in `frontend/app.py` line ~61 |
| `.gitignore` | Ignored files | Prevents secrets/large files |

---

## 🔗 After Deployment - Update Backend URL

Once backend is deployed, update frontend:

**File:** `frontend/app.py` (around line 61)

```python
# BEFORE (local development)
BACKEND_URL = "http://localhost:8000"

# AFTER (production - replace with your Railway/Render URL)
BACKEND_URL = "https://your-backend-xyz.railway.app"
```

Then:
```bash
git add frontend/app.py
git commit -m "Update backend URL for production"
git push
```

Streamlit Cloud auto-redeploys instantly!

---

## ✅ Verification Checklist

After each step, verify:

- [ ] **Git init:** `git status` shows files tracked
- [ ] **GitHub:** Repository visible at github.com/YOUR_USERNAME/ai-threat-intelligence-dashboard
- [ ] **Streamlit:** App deployed at streamlit.app (check logs for errors)
- [ ] **Backend:** (If deployed) API responds to `https://your-backend/health`
- [ ] **Dashboard:** Can upload CSV and analyze logs

---

## 🐛 Troubleshooting

### "fatal: not a git repository"
```bash
# Re-run setup
cd "f:\Intern Project\ai-threat-intelligence-dashboard"
.\setup-git.ps1
```

### "fatal: 'origin' does not appear to be a 'git' repository"
```bash
# List remotes
git remote -v

# If empty, add it
git remote add origin https://github.com/YOUR_USERNAME/ai-threat-intelligence-dashboard.git
```

### "permission denied (publickey)"
```bash
# Set up SSH key or use HTTPS
# See: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
```

### Streamlit says "No module named 'requests'"
- All dependencies missing from `frontend/requirements.txt`
- Add: `requests==2.31.0` to the file
- Push update: `git push`
- Streamlit auto-redeploys

### Dashboard shows "No logs to analyze"
- Backend URL might be wrong
- Check `frontend/app.py` line 61
- Verify backend is running/deployed
- Check Streamlit logs: click "Manage app" → "Logs"

---

## 🎯 Quick Reference

```bash
# See what changed
git status

# Add specific file
git add filename.py

# Add all changes  
git add .

# Commit
git commit -m "Your message"

# Push to GitHub
git push

# Pull latest
git pull

# View history
git log --oneline

# Create branch
git checkout -b feature-name

# Switch branch
git checkout main
```

---

## 📚 Full Documentation

- **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** - Comprehensive deployment guide
- **[README.md](./README.md)** - Project overview & features
- **[DEBUGGING_GUIDE.md](./DEBUGGING_GUIDE.md)** - Troubleshooting

---

## 🚀 You're Ready!

Your project is configured for GitHub and Streamlit Cloud deployment.

**Next action:** Run the setup script! 👆

```powershell
# Windows PowerShell
.\setup-git.ps1

# Or manually follow Step 1-5 above
```

---

**Issues?** Check [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed help!
