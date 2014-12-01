#!/usr/bin/env python

def get_instance_cpu_usage(vm):
    import libvirt
    conn = libvirt.open("qemu:///system")
    vm_conn = conn.lookupByName(vm)
    if infos[0] == 1:
        vm_cpu_state_a = vm_conn.getCPUStats(0,0)[0]
        vm_cpu_state_b = vm_conn.getCPUStats(0,0)[0]
        vm_cpu_usage = str(float(vm_cpu_state_b["vcpu_time"]-vm_cpu_state_a["vcpu_time"])/float(vm_cpu_state_b["cpu_time"]-vm_cpu_state_a["cpu_time"])*100)
    else:
        vm_cpu_usage = "0"
    return vm_cpu_usage
