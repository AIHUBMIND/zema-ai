# Simple browser-based navigation test instructions

## Manual Navigation Test

1. **Open Browser Console** (F12 or Right-click → Inspect → Console)

2. **Test Each Navigation Button:**
   - Click "Dashboard" → Should see console logs: `🖱️ Clicked nav link: dashboard`
   - Click "Settings" → Should see: `🖱️ Clicked nav link: settings`
   - Click "Logs" → Should see: `🖱️ Clicked nav link: logs`
   - Click "Users" → Should see: `🖱️ Clicked nav link: users`
   - Click "History" → Should see: `🖱️ Clicked nav link: history`
   - Click "Privacy" → Should see: `🖱️ Clicked nav link: privacy`

3. **Verify Navigation Works:**
   - Each click should:
     - Show console log messages
     - Change the active navigation item (highlighted in blue)
     - Display the correct content section
     - Update the page title and breadcrumb

4. **Check Status Boxes:**
   - System Status box should show "Listening" or "Not Listening"
   - CPU Usage box should show a percentage (e.g., "15.2%")
   - Memory Usage box should show a percentage (e.g., "45.8%")
   - Uptime box should show time (e.g., "5m" or "2h 30m")

5. **Test Logs Section:**
   - Click "Logs" navigation item
   - Should see logs viewer with controls
   - Try filtering by log level
   - Try searching logs
   - Try refresh button
   - Try live stream toggle

## Expected Console Output

When page loads, you should see:
```
🚀 Initializing Zema Dashboard...
🔧 Setting up navigation handlers...
🚀 Initial section: dashboard
✅ Section displayed: dashboard
✅ Active link updated: dashboard
✅ Navigation handlers setup complete
```

When clicking navigation items:
```
🖱️ Clicked nav link: settings
🔄 Showing section: settings
✅ Section displayed: settings
✅ Active link updated: settings
```

## Quick Test Commands

Open browser console and run:

```javascript
// Test if navigation is set up
console.log('Navigation links:', $('.sidebar a[data-section]').length);

// Test clicking dashboard programmatically
$('.sidebar a[data-section="dashboard"]').trigger('click');

// Test clicking settings programmatically
$('.sidebar a[data-section="settings"]').trigger('click');

// Check if sections exist
['dashboard', 'settings', 'logs', 'users', 'history', 'privacy'].forEach(id => {
    const el = document.getElementById(id);
    console.log(`${id}:`, el ? '✅ Found' : '❌ Missing');
});
```

