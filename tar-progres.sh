#!/bin/bash
tar cf - $1 -P | pv -s $(du -sb $1 | awk '{print $1}') | gzip > $1.tar.gz
