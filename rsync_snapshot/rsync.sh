#!/bin/bash
# $1 = snapshot_dir|USER@IP
# $2 = USER@IP     |snapshot_dir
rsync -av --delete --exclude-from exclude.list -e ssh $1 $2
