# benchmark.py Documentation

## File Location
`scripts/maintenance/benchmark.py`

## Purpose
System performance baseline script. Measures BOSGAME P3 Lite baseline performance including CPU, memory, disk I/O, and thermal sensors to establish performance baseline and identify bottlenecks.

## Why It Was Created
Performance benchmarking is crucial for understanding system capabilities, especially on resource-constrained hardware like mini PCs. This script helps:
- Establish baseline performance metrics
- Identify performance regressions
- Verify system meets minimum requirements
- Track performance over time
- Monitor thermal sensors for overheating

## How It Works

### Function: `get_system_info() -> Dict[str, Any]`
**Purpose**: Get system information
**How it works**:
1. Uses `platform` module to get system details
2. Extracts CPU count (logical and physical)
3. Gets platform, architecture, processor info
4. Returns system information dictionary

**Returns**: Dictionary with system information

### Function: `benchmark_cpu() -> Dict[str, Any]`
**Purpose**: Benchmark CPU performance
**How it works**:
1. Runs CPU load test (sum of squares computation)
2. Measures execution time
3. Gets CPU usage percentage during test
4. Measures CPU load percentage
5. Returns CPU performance metrics

**Returns**: Dictionary with:
- `cpu_cores`: Number of CPU cores
- `cpu_percent`: Current CPU usage percentage
- `load_percent`: CPU load percentage during test
- `test_time`: Time taken for computational test

### Function: `benchmark_memory() -> Dict[str, Any]`
**Purpose**: Benchmark memory performance
**How it works**:
1. Uses `psutil` to get virtual memory information
2. Converts bytes to GB
3. Gets memory usage statistics
4. Returns memory metrics

**Returns**: Dictionary with:
- `total_gb`: Total RAM in GB
- `available_gb`: Available RAM in GB
- `used_gb`: Used RAM in GB
- `percent`: Memory usage percentage

### Function: `benchmark_disk() -> Dict[str, Any]`
**Purpose**: Benchmark disk I/O performance
**How it works**:
1. Measures disk read speed (sequential read test)
2. Measures disk write speed (sequential write test)
3. Gets disk usage statistics
4. Returns disk performance metrics

**Returns**: Dictionary with:
- `total_gb`: Total disk space in GB
- `free_gb`: Free disk space in GB
- `used_gb`: Used disk space in GB
- `percent`: Disk usage percentage
- `read_speed_mb_s`: Disk read speed in MB/s
- `write_speed_mb_s`: Disk write speed in MB/s

### Function: `benchmark_thermal() -> Dict[str, Any]`
**Purpose**: Benchmark thermal sensors
**How it works**:
1. Uses `psutil` to get thermal sensors
2. Extracts CPU temperature
3. Checks for other thermal sensors
4. Returns thermal metrics

**Returns**: Dictionary with:
- `cpu_temp_c`: CPU temperature in Celsius
- `sensors_available`: Number of thermal sensors

### Main Execution Flow
1. **Get system info**: Collects system information
2. **Benchmark CPU**: Tests CPU performance
3. **Benchmark memory**: Tests memory performance
4. **Benchmark disk**: Tests disk I/O performance
5. **Benchmark thermal**: Tests thermal sensors
6. **Save results**: Saves to `data/performance_baseline.json`

## Dependencies
- `psutil`: System and process utilities
- `json`: JSON serialization
- `time`: Time measurement
- `pathlib.Path`: Path handling
- `datetime`: Timestamp generation
- `platform`: System information

## Usage

### Basic Usage
```bash
python scripts/maintenance/benchmark.py
```

### Expected Output
```
============================================================
ZEMA AI - System Performance Baseline
============================================================

System Information:
Platform: Linux
CPU Cores: 4
Architecture: x86_64

Step 1: Benchmarking CPU...
[OK] CPU cores: 4
[OK] CPU usage: 25.5%
[OK] CPU load: 45.2%
[OK] Test time: 0.123s

Step 2: Benchmarking Memory...
[OK] Total RAM: 8.0 GB
[OK] Available RAM: 5.2 GB
[OK] Memory usage: 35.0%

Step 3: Benchmarking Disk...
[OK] Total disk: 128.0 GB
[OK] Free disk: 85.5 GB
[OK] Disk usage: 33.2%
[OK] Read speed: 125.5 MB/s
[OK] Write speed: 98.3 MB/s

Step 4: Benchmarking Thermal...
[OK] CPU temperature: 45.2°C
[OK] Sensors available: 1

VERIFICATION SUMMARY
[OK] Benchmark completed successfully
[OK] Results saved: data/performance_baseline.json
```

### Exit Codes
- `0`: Benchmark completed successfully
- `1`: Benchmark failed

## Output Files
- `data/performance_baseline.json`: Performance baseline results
  - Includes timestamp
  - CPU metrics
  - Memory metrics
  - Disk metrics
  - Thermal metrics

## Example Output JSON
```json
{
  "timestamp": "2025-11-03T10:30:00",
  "system_info": {
    "platform": "Linux",
    "cpu_count": 4,
    "architecture": "x86_64"
  },
  "cpu": {
    "cpu_cores": 4,
    "cpu_percent": 25.5,
    "load_percent": 45.2,
    "test_time": 0.123
  },
  "memory": {
    "total_gb": 8.0,
    "available_gb": 5.2,
    "used_gb": 2.8,
    "percent": 35.0
  },
  "disk": {
    "total_gb": 128.0,
    "free_gb": 85.5,
    "used_gb": 42.5,
    "percent": 33.2,
    "read_speed_mb_s": 125.5,
    "write_speed_mb_s": 98.3
  },
  "thermal": {
    "cpu_temp_c": 45.2,
    "sensors_available": 1
  }
}
```

## Error Handling

### Docker/Windows Environments
Script gracefully handles:
- Missing `psutil` (warns but continues)
- Missing thermal sensors (reports unavailable)
- Disk I/O errors (reports error but continues)

### Error Messages
- Clear warnings for missing dependencies
- Graceful fallbacks for unavailable features

## Integration
- **Phase 0.5**: Hardware Verification (HARDWARE-005)
- **Maintenance**: Run periodically to track performance trends
- **CI/CD**: Can be integrated into build pipeline
- **Monitoring**: Can be used for system health monitoring

## Benefits
1. **Baseline Establishment**: Creates performance baseline
2. **Performance Tracking**: Tracks performance over time
3. **Bottleneck Identification**: Identifies performance issues
4. **Thermal Monitoring**: Monitors CPU temperature
5. **Disk I/O Testing**: Measures disk read/write speeds
6. **Clear Output**: ASCII-compatible output (no emojis)

## Testing
```bash
# Run benchmark
python scripts/maintenance/benchmark.py

# Check exit code
echo $?  # Should be 0 if successful

# View results
cat data/performance_baseline.json
```

## When to Use
- After initial system setup
- Before deploying to production
- When investigating performance issues
- Periodically to track performance trends
- After hardware changes

## Troubleshooting

### psutil Not Available
1. Install psutil: `pip install psutil`
2. Verify installation: `python -c "import psutil; print(psutil.cpu_count())"`

### Thermal Sensors Not Available
1. Check if sensors are enabled in BIOS
2. Install `lm-sensors`: `sudo apt-get install lm-sensors`
3. Run `sensors-detect` to configure sensors

### Disk I/O Test Failed
1. Check disk permissions
2. Verify disk is not in use
3. Check disk space availability

## Phase 0.5 Context
This script is part of **HARDWARE-005: System Performance Baseline** in Phase 0.5 Hardware Verification. It establishes baseline performance metrics before proceeding to Phase 1 Voice Interaction.

