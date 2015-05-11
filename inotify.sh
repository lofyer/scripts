#!/bin/bash
inotifywait -mr --timefmt '%d/%m/%y %H:%M' --format '%T %w %f' -e close_write /tmp/iso-uploads | while read date time dir file; do
    echo `date`
done
