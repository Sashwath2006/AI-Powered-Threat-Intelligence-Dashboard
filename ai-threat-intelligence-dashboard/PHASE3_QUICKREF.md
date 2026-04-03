# Phase 3: Streamlit Dashboard - Quick Start

## 🚀 30-Second Start

### Step 1: Install Dependencies
```bash
cd frontend
pip install -r requirements.txt
```

### Step 2: Ensure Backend Running
```bash
# In another terminal
cd backend
python -m uvicorn app.main:app --reload
```

### Step 3: Start Dashboard
```bash
cd frontend
streamlit run app.py
```

### Step 4: Open Browser
```
http://localhost:8501
```

## ✨ You're Done!

Dashboard should load with 4 tabs:
- 📊 Analysis
- 📈 Visualizations
- 🔍 Details
- ℹ️ About

## 🎮 Try It Now

### Quick Test:
1. Click **Analysis** tab
2. In sidebar, select **"Use Sample Data"**
3. Sample logs auto-load
4. Click **"🚀 Analyze Logs"**
5. See results and charts!

## 📊 What You Can Do

✅ **Upload CSV** - Your own log files  
✅ **Use Samples** - Pre-loaded test data  
✅ **Manual Entry** - Type logs directly  
✅ **View Charts** - Multiple visualizations  
✅ **Filter Data** - By severity, status  
✅ **Export CSV/JSON** - Save results  
✅ **Check Status** - Backend health indicator  

## 🛠️ If Errors Occur

**"Backend Offline"**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

**Port 8501 in use**
```bash
streamlit run app.py --server.port 8502
```

## 📖 Key Features

| Feature | Location | What It Does |
|---------|----------|--------------|
| **Upload CSV** | Analysis Tab | Upload your log files |
| **Sample Data** | Analysis Tab | Use pre-made test data |
| **Analyze Button** | Analysis Tab | Run ML analysis |
| **Metrics** | Analysis Tab | Show key statistics |
| **Charts** | Visualizations | Beautiful data charts |
| **Filter** | Details Tab | Filter by criteria |
| **Export** | Analysis Tab | Download CSV/JSON |
| **Status** | About Tab | Check backend health |

## 💡 Example CSV Columns

```
timestamp,source_ip,destination_ip,port,protocol,bytes_sent,bytes_received,duration
2024-01-01T10:00:00,192.168.1.1,8.8.8.8,443,TCP,1024,2048,5.5
```

## 🎯 Severity Guide

- 🔴 **CRITICAL** (0.9-1.0) - Stop activity immediately
- 🟠 **HIGH** (0.75-0.9) - Investigate urgently
- 🟡 **MEDIUM** (0.5-0.75) - Monitor closely
- 🟢 **LOW** (0.0-0.5) - Normal traffic

## 🔗 URLs

| What | URL |
|------|-----|
| Dashboard | http://localhost:8501 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Health | http://localhost:8000/health |

## 📚 Next Commands

```bash
# Start both services (2 terminals)
# Terminal 1:
cd backend && python -m uvicorn app.main:app --reload

# Terminal 2:
cd frontend && streamlit run app.py

# Then open: http://localhost:8501
```

That's it! 🎉 Dashboard is ready to use!
