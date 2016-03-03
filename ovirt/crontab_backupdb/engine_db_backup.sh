#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP=/mnt/backup/engine_db
/usr/share/ovirt-engine/bin/engine-backup.sh --mode=backup --file=$BACKUP/engine_db-$DATE --log=$BACKUP/engine_db-$DATE.log
