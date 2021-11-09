#!/bin/bash
#
# Build the volume according to the prefix string.

set -e

if test $# -ne 4; then
    echo usage: $(basename "$0") object-dir rbd-prefix dest-dir image-size
    echo
    echo e.g. $(basename "$0") /path/to/objects /mnt/saved ae1879e2a9e3 100G
    echo
    echo object_dir - the directory with objects, previously used by collect-prefix.sh
    echo rbd-prefix - the rbd-prefix of the target image
    echo dest-dir   - where to save the target image
    echo image-size - the size of the image, from "'rbd info'"
    exit 1
fi

object_dir="$1"
img_dst_dir="$2"
rbd_prefix="$3"
image_size="$4"

n=`ls -l "$object_dir" | wc -l`
if test $n -eq 0; then
    echo "No object found under $object_dir"
    exit 1
fi

dstfile="$img_dst_dir/$rbd_prefix.raw"

get-idx() {
    idx=`echo "$1" | awk -F[.] '{print $NF}' | cut -d_ -f1`
    echo $((0x$idx))
}

last_prefix_file=`find $object_dir -type f -regex ".*udata.$rbd_prefix.*" | sort | tail -1`
last_index=$((1+$(get-idx "$last_prefix_file")))

echo allocating $dstfile, size=$image_size
fallocate -l $image_size "$dstfile" || exit 1

for f in `find $object_dir -type f -regex ".*udata.$rbd_prefix.*" | sort`; do
    idx=$(get-idx "$f")
    size=$(stat -c "%s" "$f")

    echo "merging $(basename $f)"
    dd if="$f" of="$dstfile" seek=$idx bs=4M count=1 conv=notrunc >/dev/null 2>&1
done

echo the image is saved to: $dstfile
