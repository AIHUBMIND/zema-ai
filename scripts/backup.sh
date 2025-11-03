#!/bin/bash
# Backup script for Zema AI

set -e

BACKUP_DIR="data/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="zema_backup_${TIMESTAMP}.tar.gz"

echo "Creating backup: ${BACKUP_NAME}"

mkdir -p "${BACKUP_DIR}"

# Backup important files
tar -czf "${BACKUP_DIR}/${BACKUP_NAME}" \
    src/ \
    data/db/ \
    data/config/ \
    .env \
    requirements.txt \
    --exclude="__pycache__" \
    --exclude="*.pyc" \
    --exclude="venv" \
    --exclude=".git"

echo "Backup created: ${BACKUP_DIR}/${BACKUP_NAME}"
echo "Size: $(du -h ${BACKUP_DIR}/${BACKUP_NAME} | cut -f1)"

# Keep only last 10 backups
cd "${BACKUP_DIR}"
ls -t zema_backup_*.tar.gz | tail -n +11 | xargs rm -f 2>/dev/null || true

echo "Backup complete!"

