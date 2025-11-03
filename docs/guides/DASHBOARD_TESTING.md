# Dashboard Testing & Template Integration Guide

## 1. Testing the Dashboard

### Method 1: Live Development with Auto-Reload (RECOMMENDED - Fastest!)

**Best for active development** - Automatically reloads when you change code:

```bash
# From project root (C:\AI_Cloude_Files\ZEMA-AI)
# Activate virtual environment first
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Run with auto-reload
python -m uvicorn src.api.server:app --reload --host 0.0.0.0 --port 8000
```

**Benefits:**
- ✅ Auto-reloads on code changes
- ✅ Fastest feedback loop
- ✅ No manual restart needed
- ✅ Works from project root (no import issues)

**Access:** `http://localhost:8000`

### Method 2: Using the Test Script

```bash
# IMPORTANT: Must run from project root, not from scripts directory!
# From project root (C:\AI_Cloude_Files\ZEMA-AI)
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# Run the dashboard test script
python scripts/test_dashboard.py
```

**Note:** The script now includes path fixes, but you must still run it from the project root directory.

The dashboard will start at:
- **Default URL:** `http://localhost:8000`
- **Or check your `.env` file** for `DASHBOARD_HOST` and `DASHBOARD_PORT`

### Method 3: Quick Test with Python

```python
# Quick test script
import asyncio
from src.config.settings import settings
from src.api.server import start_dashboard

asyncio.run(start_dashboard(settings))
```

### Accessing the Dashboard

Once running, open your browser:
- **Main Dashboard:** `http://localhost:8000`
- **Logs Section:** `http://localhost:8000#logs`
- **API Docs:** `http://localhost:8000/docs` (FastAPI auto-generated)

### Testing Features

1. **Dashboard Page:** Should show status cards
2. **Logs Section:** Click "Logs" in sidebar
   - Filter by level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
   - Search logs
   - Toggle Live Stream
   - View statistics
3. **WebSocket:** Should connect automatically for real-time updates
4. **API Endpoints:** Test via `/docs` or directly:
   - `GET /api/logs` - View logs
   - `GET /api/logs/stats` - Get statistics
   - `GET /api/status` - System status

---

## 2. Using GitHub Admin Dashboard Templates

Yes! You can absolutely use templates from GitHub. Here's how to integrate them:

### Popular Admin Dashboard Templates

1. **AdminLTE 3** (PHP/HTML - Most Popular)
   - GitHub: `https://github.com/ColorlibHQ/AdminLTE`
   - License: MIT
   - Features: Bootstrap 4, Dark mode, Many widgets

2. **CoreUI** (React/Vue/Angular)
   - GitHub: `https://github.com/coreui/coreui-free-react-admin-template`
   - License: MIT
   - Modern, component-based

3. **Tabler** (HTML/CSS)
   - GitHub: `https://github.com/tabler/tabler`
   - License: MIT
   - Free, open-source admin dashboard

4. **Material Dashboard** (Material Design)
   - GitHub: `https://github.com/creativetimofficial/material-dashboard`
   - License: MIT
   - Google Material Design

5. **Volt Dashboard** (Bootstrap 5)
   - GitHub: `https://github.com/themesberg/volt-bootstrap-5-dashboard`
   - License: MIT
   - Modern Bootstrap 5

### Integration Steps

#### Option A: Replace Current Dashboard (Simple)

1. **Download Template:**
   ```bash
   # Clone or download template
   git clone https://github.com/ColorlibHQ/AdminLTE.git temp_adminlte
   cd temp_adminlte
   ```

2. **Copy Template Files:**
   ```bash
   # Copy HTML/CSS/JS to your static folder
   cp -r dist/* ../src/api/static/
   # or copy specific files you need
   ```

3. **Update API Integration:**
   - Keep your existing API endpoints (`/api/logs`, `/api/status`, etc.)
   - Update template's JavaScript to call your FastAPI endpoints
   - Replace template's API calls with your endpoints

4. **Modify Template:**
   - Update `src/api/static/index.html` with template's HTML
   - Update CSS/JS references
   - Integrate your existing JavaScript (`app.js`)

#### Option B: Hybrid Integration (Recommended)

1. **Keep Current Structure:**
   - Keep your existing `src/api/static/` structure
   - Keep your API endpoints

2. **Add Template Assets:**
   ```bash
   # Create directories for template assets
   mkdir -p src/api/static/vendor/css
   mkdir -p src/api/static/vendor/js
   mkdir -p src/api/static/vendor/fonts
   ```

3. **Copy Template Assets:**
   ```bash
   # Copy CSS/JS from template
   cp template/dist/css/* src/api/static/vendor/css/
   cp template/dist/js/* src/api/static/vendor/js/
   cp template/dist/fonts/* src/api/static/vendor/fonts/
   ```

4. **Update Your HTML:**
   ```html
   <!-- In src/api/static/index.html -->
   <!DOCTYPE html>
   <html>
   <head>
       <!-- Template CSS -->
       <link rel="stylesheet" href="/static/vendor/css/adminlte.min.css">
       <!-- Your custom CSS -->
       <link rel="stylesheet" href="/static/css/style.css">
   </head>
   <body>
       <!-- Template HTML structure -->
       <!-- Your dashboard content -->
       
       <!-- Template JS -->
       <script src="/static/vendor/js/adminlte.min.js"></script>
       <!-- Your custom JS -->
       <script src="/static/js/app.js"></script>
   </body>
   </html>
   ```

5. **Integrate Your APIs:**
   - Update template's JavaScript to use your FastAPI endpoints
   - Replace template's example API calls with your real endpoints

### Example: Integrating AdminLTE 3

1. **Download AdminLTE:**
   ```bash
   git clone https://github.com/ColorlibHQ/AdminLTE.git adminlte_temp
   ```

2. **Copy Required Files:**
   ```bash
   # Copy CSS
   cp adminlte_temp/dist/css/adminlte.min.css src/api/static/vendor/css/
   cp adminlte_temp/dist/css/adminlte.min.css.map src/api/static/vendor/css/
   
   # Copy JS
   cp adminlte_temp/dist/js/adminlte.min.js src/api/static/vendor/js/
   
   # Copy fonts (if needed)
   cp -r adminlte_temp/dist/fonts src/api/static/vendor/
   ```

3. **Update Your HTML:**
   ```html
   <!-- src/api/static/index.html -->
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Zema Dashboard</title>
       
       <!-- AdminLTE CSS -->
       <link rel="stylesheet" href="/static/vendor/css/adminlte.min.css">
       <!-- Your custom CSS -->
       <link rel="stylesheet" href="/static/css/style.css">
   </head>
   <body class="hold-transition sidebar-mini layout-fixed">
       <div class="wrapper">
           <!-- Sidebar -->
           <aside class="main-sidebar sidebar-dark-primary elevation-4">
               <div class="sidebar">
                   <nav class="mt-2">
                       <ul class="nav nav-pills nav-sidebar flex-column">
                           <li class="nav-item">
                               <a href="#dashboard" class="nav-link active">
                                   <i class="nav-icon fas fa-tachometer-alt"></i>
                                   <p>Dashboard</p>
                               </a>
                           </li>
                           <li class="nav-item">
                               <a href="#logs" class="nav-link">
                                   <i class="nav-icon fas fa-file-alt"></i>
                                   <p>Logs</p>
                               </a>
                           </li>
                           <!-- More menu items -->
                       </ul>
                   </nav>
               </div>
           </aside>
           
           <!-- Main content -->
           <div class="content-wrapper">
               <!-- Your dashboard content here -->
               <section id="dashboard" class="content">
                   <!-- Your existing dashboard content -->
               </section>
               
               <section id="logs" class="content">
                   <!-- Your existing logs viewer -->
               </section>
           </div>
       </div>
       
       <!-- AdminLTE JS -->
       <script src="/static/vendor/js/adminlte.min.js"></script>
       <!-- Your custom JS -->
       <script src="/static/js/app.js"></script>
   </body>
   </html>
   ```

4. **Update Your JavaScript:**
   ```javascript
   // Keep your existing API calls
   // Template will handle UI components
   // Your app.js handles data fetching
   ```

### Key Points for Integration

1. **Keep Your APIs:** Don't change your FastAPI endpoints
2. **Update Template JS:** Replace template's API calls with your endpoints
3. **Preserve Functionality:** Keep your existing features (logs viewer, etc.)
4. **Test Thoroughly:** Test all features after integration

### Recommended Template for Your Project

**AdminLTE 3** is recommended because:
- ✅ Most popular and well-maintained
- ✅ Bootstrap 4 (easy to customize)
- ✅ Dark mode support
- ✅ Many widgets/components
- ✅ Free and MIT licensed
- ✅ Good documentation
- ✅ Works well with FastAPI

### Quick Start with AdminLTE

```bash
# 1. Download AdminLTE
git clone https://github.com/ColorlibHQ/AdminLTE.git temp_adminlte

# 2. Copy assets
mkdir -p src/api/static/vendor/{css,js,fonts}
cp temp_adminlte/dist/css/adminlte.min.css src/api/static/vendor/css/
cp temp_adminlte/dist/js/adminlte.min.js src/api/static/vendor/js/
cp -r temp_adminlte/dist/fonts src/api/static/vendor/

# 3. Update your HTML to use AdminLTE classes
# 4. Keep your existing API endpoints
# 5. Update JavaScript to call your APIs
# 6. Test dashboard
python scripts/test_dashboard.py
```

---

## 3. Testing Checklist

After integrating a template:

- [ ] Dashboard loads without errors
- [ ] All navigation links work
- [ ] API endpoints respond correctly
- [ ] Logs viewer displays correctly
- [ ] WebSocket connection works
- [ ] Dark mode works (if template supports it)
- [ ] Mobile responsive
- [ ] All custom features still work

---

## Need Help?

- Check template's documentation
- Review FastAPI static file serving: `src/api/server.py`
- Test API endpoints: `http://localhost:8000/docs`
