# Quick Dashboard Testing Guide

## 🚀 Fastest Way: Live Development with Auto-Reload

**Best for active development** - Automatically reloads on code changes:

```bash
# From project root (C:\AI_Cloude_Files\ZEMA-AI)
python -m uvicorn src.api.server:app --reload --host 0.0.0.0 --port 8000
```

**Benefits:**
- ✅ Auto-reloads when you change code
- ✅ Fastest feedback loop
- ✅ No need to restart manually
- ✅ Works from project root (no import issues)

**Access:** `http://localhost:8000`

---

## 📝 Alternative: Test Script (Fixed)

The test script now works correctly:

```bash
# From project root
python scripts/test_dashboard.py
```

**Note:** Must be run from project root (`C:\AI_Cloude_Files\ZEMA-AI`), not from inside `scripts/`

---

## 🔧 What Was Wrong?

**Problem:** When running `python scripts/test_dashboard.py`, Python couldn't find the `src` module because:
- Python adds the script's directory (`scripts/`) to `sys.path`
- The `src` module is in the parent directory
- Python couldn't resolve `from src.config.settings import settings`

**Solution:** Added code to automatically add the project root to Python's path before imports.

---

## 💡 Recommended Development Workflow

1. **Start development server with auto-reload:**
   ```bash
   python -m uvicorn src.api.server:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Make changes** to:
   - `src/api/static/index.html` - Dashboard HTML
   - `src/api/static/css/style.css` - Styles
   - `src/api/static/js/app.js` - JavaScript
   - `src/api/server.py` - API endpoints

3. **Save files** - Server automatically reloads!

4. **Refresh browser** - See changes immediately

---

## 🎯 Quick Commands Reference

```bash
# Live development (auto-reload)
python -m uvicorn src.api.server:app --reload --host 0.0.0.0 --port 8000

# Test script (no auto-reload)
python scripts/test_dashboard.py

# Production mode (no reload)
python -m uvicorn src.api.server:app --host 0.0.0.0 --port 8000
```

---

## 📍 Important: Always Run from Project Root

All commands should be run from:
```
C:\AI_Cloude_Files\ZEMA-AI\
```

NOT from:
```
C:\AI_Cloude_Files\ZEMA-AI\scripts\
```

---

## ✅ Verification

After starting, you should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Then open: `http://localhost:8000`

