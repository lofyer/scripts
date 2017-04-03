#!/bin/bash
TODAY=$(date +%Y%m%d)
YESTERDAY=$(date -v-1d +%Y%m%d)
BACKUP=/mnt/backup/engine_db
/usr/share/ovirt-engine/bin/engine-backup.sh --mode=restore --file=$BACKUP/engine_db-$YESTERDAY --log=$BACKUP/resotre-engine_db-$TODAY.log
