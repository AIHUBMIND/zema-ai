#!/bin/bash
# Cleanup script for Zema AI

set -e

echo "Cleaning up temporary files..."

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Remove pytest cache
find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true

# Remove coverage files
find . -type f -name ".coverage" -delete 2>/dev/null || true
find . -type d -name "htmlcov" -exec rm -r {} + 2>/dev/null || true

# Remove old log files (keep last 7 days)
find data/logs -name "*.log" -mtime +7 -delete 2>/dev/null || true

echo "Cleanup complete!"

