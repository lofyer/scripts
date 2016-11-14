#!/bin/bash
MAX_STOR=30
BACKUP_DIR=/mnt/backup/
BASE=engine_db
# rm db and log 30 days ago
find $BACKUP_DIR -name "$BASE*.db" -a -type f -mtime +$MAX_STOR -exec rm {} \;
