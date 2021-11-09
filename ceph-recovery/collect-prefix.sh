#!/bin/bash
#
# Collect the object with specified prefix to given directory.

if test $# -ne 3; then
    echo usage: $(basename "$0") osd-data-dir prefix output-dir
    echo
    echo e.g. $(basename "$0") /var/lib/ceph/osd/ceph-0 ae1879e2a9e3 /path/to/objects
    echo
    echo ae1879e2a9e3 is one of the prefix found by "'list-prefix-freq.sh'"
    exit 1
fi

osd_data_dir=$1
prefix=$2
output_dir=$3

if test x"$osd_data_dir" = x"$output_dir"; then
    echo "the output directory should not be the same with osd-data-dir"
    exit 1
fi

mkdir -p "$output_dir"

echo "collecting $prefix to directory: $output_dir"

find "$1" -type f \
   -regex ".*rbd.udata.$prefix.*" \
   -exec cp -nup {} "$output_dir" \;

echo $(ls "$output_dir" | wc -l) objects collected.
