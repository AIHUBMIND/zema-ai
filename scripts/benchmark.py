#!/usr/bin/env python3
"""
System Benchmark Script
Measures BOSGAME P3 Lite baseline performance
"""

import sys
import json
import time
import psutil
from pathlib import Path
from datetime import datetime

def benchmark_cpu():
    """Benchmark CPU performance"""
    print("Testing CPU...")
    start = time.time()
    # Simple CPU test
    result = sum(i * i for i in range(1000000))
    cpu_time = time.time() - start
    cpu_percent = psutil.cpu_percent(interval=1)
    return {
        "cpu_cores": psutil.cpu_count(),
        "cpu_percent": cpu_percent,
        "test_time": cpu_time
    }

def benchmark_memory():
    """Benchmark memory"""
    print("Testing Memory...")
    memory = psutil.virtual_memory()
    return {
        "total_gb": memory.total / 1024 / 1024 / 1024,
        "available_gb": memory.available / 1024 / 1024 / 1024,
        "percent": memory.percent
    }

def benchmark_disk():
    """Benchmark disk I/O"""
    print("Testing Disk I/O...")
    disk = psutil.disk_usage('/')
    return {
        "total_gb": disk.total / 1024 / 1024 / 1024,
        "free_gb": disk.free / 1024 / 1024 / 1024,
        "percent": disk.percent
    }

def main():
    """Run all benchmarks"""
    print("=" * 60)
    print("Zema AI - System Benchmark")
    print("=" * 60)
    print()
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "cpu": benchmark_cpu(),
        "memory": benchmark_memory(),
        "disk": benchmark_disk()
    }
    
    print()
    print("=" * 60)
    print("BENCHMARK RESULTS")
    print("=" * 60)
    print(json.dumps(results, indent=2))
    
    # Save results
    output_file = Path("data/performance_baseline.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()

