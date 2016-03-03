#!/bin/bash
DATE=$(date +%Y%m%d)
BACKUP=/mnt/backup/storengine_db
mysqldump -uroot -p123456 storengine > $BACKUP/storengine-$DATE.sql
