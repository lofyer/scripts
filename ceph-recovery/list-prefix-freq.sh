#!/bin/bash
#
# List the rbd prefixes and its total count.

if test $# -ne 1; then
    echo usage: $(basename "$0") osd-data-dir
    echo
    echo e.g. $(basename "$0") /var/lib/ceph/osd/ceph-0
    exit 1
fi

echo "   prefix    count"
find "$1" -type f \
  | awk -F[.] '/rbd.udata/{a[$(NF-1)]++}END{for(k in a) print k, a[k]}' \
  | sort -k2 -n
