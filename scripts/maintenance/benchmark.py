#!/usr/bin/env python3
"""
System Performance Baseline Script
Measures BOSGAME P3 Lite baseline performance

Usage:
    python scripts/maintenance/benchmark.py

Exit codes:
    0: Benchmark completed successfully
    1: Benchmark failed
"""

import sys
import json
import time
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("WARNING: psutil not installed. Install with: pip install psutil")

def get_system_info() -> Dict[str, Any]:
    """Get system information"""
    info = {
        'platform': platform.system(),
        'platform_release': platform.release(),
        'platform_version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor(),
    }
    
    if PSUTIL_AVAILABLE:
        info['cpu_count'] = psutil.cpu_count(logical=True)
        info['cpu_count_physical'] = psutil.cpu_count(logical=False)
    
    return info

def benchmark_cpu() -> Dict[str, Any]:
    """Benchmark CPU performance"""
    print("=" * 60)
    print("Step 1: Benchmarking CPU...")
    print("=" * 60)
    
    if not PSUTIL_AVAILABLE:
        print("⚠️  WARNING: psutil not available")
        return {}
    
    # Measure idle CPU
    print("   Measuring idle CPU usage...")
    idle_cpu = psutil.cpu_percent(interval=1)
    
    # Measure CPU under load
    print("   Testing CPU under load...")
    start_time = time.time()
    cpu_percent = psutil.cpu_percent(interval=3)
    load_time = time.time() - start_time
    
    # Simple CPU test
    print("   Running CPU computation test...")
    computation_start = time.time()
    result = sum(i * i for i in range(1000000))
    computation_time = time.time() - computation_start
    
    return {
        "cpu_cores": psutil.cpu_count(logical=True),
        "cpu_cores_physical": psutil.cpu_count(logical=False),
        "idle_percent": idle_cpu,
        "load_percent": cpu_percent,
        "load_test_time": load_time,
        "computation_test_time": computation_time,
        "computation_result": result
    }

def benchmark_memory() -> Dict[str, Any]:
    """Benchmark memory"""
    print("\n" + "=" * 60)
    print("Step 2: Benchmarking Memory...")
    print("=" * 60)
    
    if not PSUTIL_AVAILABLE:
        print("⚠️  WARNING: psutil not available")
        return {}
    
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    print(f"   Total RAM: {memory.total / 1024 / 1024 / 1024:.2f} GB")
    print(f"   Available RAM: {memory.available / 1024 / 1024 / 1024:.2f} GB")
    print(f"   Used RAM: {memory.used / 1024 / 1024 / 1024:.2f} GB")
    print(f"   RAM Usage: {memory.percent}%")
    
    return {
        "total_gb": memory.total / 1024 / 1024 / 1024,
        "available_gb": memory.available / 1024 / 1024 / 1024,
        "used_gb": memory.used / 1024 / 1024 / 1024,
        "percent": memory.percent,
        "swap_total_gb": swap.total / 1024 / 1024 / 1024,
        "swap_used_gb": swap.used / 1024 / 1024 / 1024,
        "swap_percent": swap.percent
    }

def benchmark_disk() -> Dict[str, Any]:
    """Benchmark disk I/O"""
    print("\n" + "=" * 60)
    print("Step 3: Benchmarking Disk I/O...")
    print("=" * 60)
    
    if not PSUTIL_AVAILABLE:
        print("⚠️  WARNING: psutil not available")
        return {}
    
    disk = psutil.disk_usage('/')
    
    print(f"   Total disk: {disk.total / 1024 / 1024 / 1024:.2f} GB")
    print(f"   Free disk: {disk.free / 1024 / 1024 / 1024:.2f} GB")
    print(f"   Used disk: {disk.used / 1024 / 1024 / 1024:.2f} GB")
    print(f"   Disk usage: {disk.percent}%")
    
    # Test disk write speed
    print("   Testing disk write speed...")
    test_file = Path("data/benchmark_test.tmp")
    test_file.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        write_start = time.time()
        with open(test_file, 'wb') as f:
            # Write 100MB
            data = b'x' * (1024 * 1024)  # 1MB chunks
            for _ in range(100):
                f.write(data)
        write_time = time.time() - write_start
        write_speed_mbps = 100 / write_time
        
        # Test disk read speed
        print("   Testing disk read speed...")
        read_start = time.time()
        with open(test_file, 'rb') as f:
            while f.read(1024 * 1024):  # Read 1MB chunks
                pass
        read_time = time.time() - read_start
        read_speed_mbps = 100 / read_time
        
        # Cleanup
        test_file.unlink()
        
        print(f"   Write speed: {write_speed_mbps:.2f} MB/s")
        print(f"   Read speed: {read_speed_mbps:.2f} MB/s")
        
        disk_io = {
            "write_speed_mbps": write_speed_mbps,
            "read_speed_mbps": read_speed_mbps
        }
    except Exception as e:
        print(f"   ⚠️  WARNING: Disk speed test failed: {e}")
        disk_io = {}
    
    return {
        "total_gb": disk.total / 1024 / 1024 / 1024,
        "free_gb": disk.free / 1024 / 1024 / 1024,
        "used_gb": disk.used / 1024 / 1024 / 1024,
        "percent": disk.percent,
        **disk_io
    }

def benchmark_thermal() -> Dict[str, Any]:
    """Benchmark thermal performance"""
    print("\n" + "=" * 60)
    print("Step 4: Checking thermal performance...")
    print("=" * 60)
    
    if not PSUTIL_AVAILABLE:
        print("⚠️  WARNING: psutil not available")
        return {}
    
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            print("   Temperature sensors found:")
            thermal_data = {}
            for name, entries in temps.items():
                for entry in entries:
                    print(f"   {name}: {entry.current}°C")
                    thermal_data[name] = {
                        "current": entry.current,
                        "high": entry.high if hasattr(entry, 'high') else None,
                        "critical": entry.critical if hasattr(entry, 'critical') else None
                    }
            return thermal_data
        else:
            print("   ℹ️  No temperature sensors available")
            return {}
    except Exception as e:
        print(f"   ⚠️  WARNING: Thermal check failed: {e}")
        return {}

def main():
    """Run all benchmarks"""
    print("\n" + "=" * 60)
    print("ZEMA AI - System Performance Baseline")
    print("=" * 60)
    print()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "system_info": get_system_info(),
        "cpu": benchmark_cpu(),
        "memory": benchmark_memory(),
        "disk": benchmark_disk(),
        "thermal": benchmark_thermal()
    }
    
    print("\n" + "=" * 60)
    print("BENCHMARK RESULTS")
    print("=" * 60)
    print(json.dumps(results, indent=2))
    
    # Save results
    output_file = Path("data/performance_baseline.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Results saved to: {output_file}")
    print("\n⚠️  NOTE: Performance targets may vary based on hardware")
    print("   Full functionality requires real hardware (BOSGAME P3 Lite)")
    print("\n✅ System benchmark complete")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

