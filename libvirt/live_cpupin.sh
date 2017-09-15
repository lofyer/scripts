#!/bin/bash
export CPUPIN_STRIPE=0
HOST_CPU_NUM=$(virsh nodecpumap|awk 'NR==1 {print $3}')
RESERVE_CPU_NUM=2
AVAILABLE_CPU_NUM=$(expr $HOST_CPU_NUM - $RESERVE_CPU_NUM)

DOMAIN_LIST=$(virsh list|awk 'NR>2 {print $1}'|sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
if [[ -z $DOMAIN_LIST ]]
then
    exit 1
fi

for DOMAIN in $DOMAIN_LIST
do
    DOMAIN_LIVE_CPU_NUM=$(virsh vcpucount $DOMAIN|awk 'NR==4 {print $3}')
    for i in $(seq 0 $(expr $DOMAIN_LIVE_CPU_NUM - 1))
    do
        echo "Pinning $DOMAIN vCPU $i to CPU $(expr $CPUPIN_STRIPE % $AVAILABLE_CPU_NUM)"
        virsh vcpupin $DOMAIN --live --vcpu $i --cpulist $(expr $CPUPIN_STRIPE % $AVAILABLE_CPU_NUM)
        CPUPIN_STRIPE=$(expr $CPUPIN_STRIPE + 1)
        # virsh vcpuinfo $DOMAIN
    done
done
