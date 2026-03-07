#!/bin/bash
BACKUP_DIR="/home/ubuntu/kiosk-monitor/backup"
DATE=$(date +%Y%m%d_%H%M)
cp /home/ubuntu/kiosk-monitor/monitor.db "$BACKUP_DIR/monitor_${DATE}.db"

# 7일 이상된 백업 삭제
find "$BACKUP_DIR" -name "monitor_*.db" -mtime +7 -delete

echo "$(date) 백업 완료: monitor_${DATE}.db"
