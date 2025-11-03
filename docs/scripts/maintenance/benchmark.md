# benchmark.py Documentation

## File Location
`scripts/maintenance/benchmark.py`

## Purpose
This script measures and establishes baseline performance metrics for the BOSGAME P3 Lite mini PC. It benchmarks CPU, memory, and disk performance to help identify performance bottlenecks and verify system capabilities.

## Why It Was Created
Performance benchmarking is crucial for understanding system capabilities, especially on resource-constrained hardware like mini PCs. This script helps:
- Establish baseline performance metrics
- Identify performance regressions
- Verify system meets minimum requirements
- Track performance over time

## How It Works

### Main Functions

#### `benchmark_cpu()`
**Purpose**: Measures CPU performance
**How it works**:
1. Runs a simple computational test (sum of squares)
2. Measures execution time
3. Gets CPU usage percentage
4. Returns CPU core count, usage percentage, and test execution time

**Returns**: Dictionary with:
- `cpu_cores`: Number of CPU cores
- `cpu_percent`: Current CPU usage percentage
- `test_time`: Time taken for computational test

#### `benchmark_memory()`
**Purpose**: Measures memory (RAM) statistics
**How it works**:
1. Uses `psutil` to get virtual memory information
2. Converts bytes to GB
3. Returns total, available, and usage percentage

**Returns**: Dictionary with:
- `total_gb`: Total RAM in GB
- `available_gb`: Available RAM in GB
- `percent`: Memory usage percentage

#### `benchmark_disk()`
**Purpose**: Measures disk I/O and storage statistics
**How it works**:
1. Uses `psutil` to get disk usage information
2. Converts bytes to GB
3. Returns total, free, and usage percentage

**Returns**: Dictionary with:
- `total_gb`: Total disk space in GB
- `free_gb`: Free disk space in GB
- `percent`: Disk usage percentage

#### `main()`
**Purpose**: Orchestrates all benchmark tests
**How it works**:
1. Runs all benchmark functions
2. Collects results into a dictionary
3. Prints formatted results
4. Saves results to `data/performance_baseline.json`
5. Includes timestamp for tracking over time

## Dependencies
- `psutil`: System and process utilities
- `json`: JSON serialization
- `time`: Time measurement
- `pathlib.Path`: Path handling
- `datetime`: Timestamp generation

## Usage
```bash
# From project root
python scripts/maintenance/benchmark.py
```

## Output
The script:
1. Prints benchmark results to console
2. Saves results to `data/performance_baseline.json`

## Example Output
```json
{
  "timestamp": "2025-11-02T10:30:00",
  "cpu": {
    "cpu_cores": 4,
    "cpu_percent": 25.5,
    "test_time": 0.123
  },
  "memory": {
    "total_gb": 8.0,
    "available_gb": 5.2,
    "percent": 35.0
  },
  "disk": {
    "total_gb": 128.0,
    "free_gb": 85.5,
    "percent": 33.2
  }
}
```

## When to Use
- After initial system setup
- When investigating performance issues
- Before deploying to production
- Periodically to track performance trends

## Integration
This script can be integrated into:
- CI/CD pipelines for performance regression testing
- Scheduled maintenance tasks
- System health monitoring

