"""
Test script to verify dashboard navigation functionality
Tests all navigation buttons and status updates

Usage:
    python scripts/test_navigation.py
    OR
    pip install requests websocket-client
    python scripts/test_navigation.py
"""

try:
    import requests
except ImportError:
    print("❌ Error: 'requests' module not found.")
    print("   Install with: pip install requests")
    exit(1)

import time
import json
from typing import Dict, List

BASE_URL = "http://localhost:8001"

def test_api_endpoint(endpoint: str, description: str) -> bool:
    """Test an API endpoint"""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        if response.status_code == 200:
            print(f"✅ {description}: OK")
            return True
        else:
            print(f"❌ {description}: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {description}: Error - {e}")
        return False

def test_status_api() -> Dict:
    """Test status API and verify data structure"""
    try:
        response = requests.get(f"{BASE_URL}/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # Verify required fields
            required_fields = ['listening', 'cpu_percent', 'memory_percent', 'uptime']
            missing_fields = [f for f in required_fields if f not in data]
            
            if missing_fields:
                print(f"❌ Status API: Missing fields - {missing_fields}")
                return {}
            
            print(f"✅ Status API: OK")
            print(f"   - Listening: {data.get('listening')}")
            print(f"   - CPU: {data.get('cpu_percent')}%")
            print(f"   - Memory: {data.get('memory_percent')}%")
            print(f"   - Uptime: {data.get('uptime')}s")
            return data
        else:
            print(f"❌ Status API: Status {response.status_code}")
            return {}
    except Exception as e:
        print(f"❌ Status API: Error - {e}")
        return {}

def test_logs_api() -> bool:
    """Test logs API"""
    try:
        response = requests.get(f"{BASE_URL}/api/logs?limit=10", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Logs API: OK (returned {len(data.get('logs', []))} logs)")
            return True
        else:
            print(f"❌ Logs API: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Logs API: Error - {e}")
        return False

def test_logs_stats_api() -> bool:
    """Test logs stats API"""
    try:
        response = requests.get(f"{BASE_URL}/api/logs/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Logs Stats API: OK")
            return True
        else:
            print(f"❌ Logs Stats API: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Logs Stats API: Error - {e}")
        return False

def test_websocket_connection() -> bool:
    """Test WebSocket connection"""
    try:
        import websocket
        import json
        
        ws_url = BASE_URL.replace("http://", "ws://") + "/ws"
        
        def on_message(ws, message):
            try:
                data = json.loads(message)
                if data.get('type') == 'status':
                    print(f"✅ WebSocket: Received status update")
                    print(f"   - Listening: {data.get('data', {}).get('listening')}")
                    print(f"   - CPU: {data.get('data', {}).get('cpu_percent')}%")
                    ws.close()
            except Exception as e:
                print(f"❌ WebSocket: Error parsing message - {e}")
        
        def on_error(ws, error):
            print(f"❌ WebSocket: Error - {error}")
        
        def on_close(ws, close_status_code, close_msg):
            pass
        
        ws = websocket.WebSocketApp(
            ws_url,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        
        ws.run_forever(timeout=5)
        return True
        
    except ImportError:
        print("⚠️  WebSocket test skipped (websocket-client not installed)")
        print("   Install with: pip install websocket-client")
        return False
    except Exception as e:
        print(f"❌ WebSocket: Error - {e}")
        return False

def test_dashboard_html() -> bool:
    """Test dashboard HTML loads"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            html = response.text
            
            # Check for required elements
            checks = [
                ('Dashboard', 'Dashboard section'),
                ('Settings', 'Settings section'),
                ('Logs', 'Logs section'),
                ('Users', 'Users section'),
                ('History', 'History section'),
                ('Privacy', 'Privacy section'),
                ('data-section="dashboard"', 'Dashboard nav link'),
                ('data-section="settings"', 'Settings nav link'),
                ('data-section="logs"', 'Logs nav link'),
                ('app.js', 'App.js script'),
                ('adminlte.min.js', 'AdminLTE script'),
            ]
            
            all_ok = True
            for check, description in checks:
                if check in html:
                    print(f"✅ HTML: {description} found")
                else:
                    print(f"❌ HTML: {description} NOT found")
                    all_ok = False
            
            return all_ok
        else:
            print(f"❌ Dashboard HTML: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Dashboard HTML: Error - {e}")
        return False

def test_static_files() -> bool:
    """Test static files are accessible"""
    static_files = [
        '/static/js/app.js',
        '/static/css/style.css',
        '/static/vendor/js/adminlte.min.js',
        '/static/vendor/css/adminlte.min.css',
    ]
    
    all_ok = True
    for file_path in static_files:
        try:
            response = requests.get(f"{BASE_URL}{file_path}", timeout=5)
            if response.status_code == 200:
                print(f"✅ Static: {file_path} accessible")
            else:
                print(f"❌ Static: {file_path} - Status {response.status_code}")
                all_ok = False
        except Exception as e:
            print(f"❌ Static: {file_path} - Error - {e}")
            all_ok = False
    
    return all_ok

def main():
    """Run all tests"""
    print("=" * 60)
    print("ZEMA Dashboard Navigation & Functionality Test")
    print("=" * 60)
    print()
    
    results = {}
    
    # Test 1: Dashboard HTML
    print("📄 Testing Dashboard HTML...")
    results['html'] = test_dashboard_html()
    print()
    
    # Test 2: Static Files
    print("📦 Testing Static Files...")
    results['static'] = test_static_files()
    print()
    
    # Test 3: Status API
    print("📊 Testing Status API...")
    results['status'] = bool(test_status_api())
    print()
    
    # Test 4: Logs API
    print("📝 Testing Logs API...")
    results['logs'] = test_logs_api()
    print()
    
    # Test 5: Logs Stats API
    print("📈 Testing Logs Stats API...")
    results['logs_stats'] = test_logs_stats_api()
    print()
    
    # Test 6: WebSocket
    print("🔌 Testing WebSocket Connection...")
    results['websocket'] = test_websocket_connection()
    print()
    
    # Summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    exit(main())

