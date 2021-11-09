#!/bin/bash

N=4

export LD_LIBRARY_PATH=/lib64/:/lib64/ceph:${LD_LIBRARY_PATH}

for obj in `cat 12C1942FC1B54C60-85585506D3044932.data | awk '{print $1}'`; do
    (
        echo $obj
        hex_obj=`echo $obj | awk -F'.' '{print $3}'`
        dec_obj=`echo $((0x$hex_obj))`
        ./rados get $obj xxx -p pool-272921F1-4B60-461E-8972-6FE286FDF8F5 --row --path 0
        dd if=xxx of=image seek=$dec_obj count=1 bs=4194304 conv=notrunc
    ) &

    # allow to execute up to $N jobs in parallel
    if [[ $(jobs -r -p | wc -l) -ge $N ]]; then
        # now there are $N jobs already running, so wait here for any job
        # to be finished so there is a place to start next one.
        wait
    fi

done

# no more jobs to be started but wait for pending jobs
# (all need to be finished)
wait

echo "all done"
