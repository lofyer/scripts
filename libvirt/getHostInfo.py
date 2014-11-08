#!/usr/bin/python

import netifaces
import platform
import psutil
import subprocess
import uptime

def getHostInfo():
    '''
    Use hal-get-property ?
    STATIC_INFO                 DYNAMIC_INFO
    Hostname
    Uptime_in_Seconds
    OS_Version
    Kernel_Version
    KVM_Version
    Spice_Version
    RUNNING_VMS
    CPU_Family
    CPU_Type
    CPU_Sockets
    CPU_Cores_per_Socket
    CPU_Threads_per_Core        All_CPU_Usage
    Virtualization
    Physical_Memory_Size        Physical_Memory_Usage
    Swap_Size                   Swap_Usage
    IP_Address
    MAC_Address
    Network_Interfaces
    Network_Interface_Bandwidth 
    Network_Interface_Updown    Network_Usage
    '''

    info = {}

    info["hostname"] = platform.node()
    info["uptime_in_seconds"] = str(uptime.uptime())
    info["os_version"] = platform.platform()
    #OS_Version = platform.linux_distribution()
    info["kernel_version"] = platform.release()
    info["kvm_version"] = subprocess.Popen("rpm -qa|grep qemu-kvm|awk -F 'qemu-kvm-' '{print $2}'",stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read().strip()
    info["spice_version"] = subprocess.Popen("rpm -qa|grep spice-server|awk -F 'spice-server-' '{print $2}'",stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read().strip()
    # TBD
    info["running_vms"] = subprocess.Popen("ps aux|grep qemu|wc -l",stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read().strip()
    info["cpu_family"] = platform.processor()
    info["cpu_type"]= subprocess.Popen("cat /proc/info | grep 'model name' | head -n 1 | awk -F ':' '{print $2}'",stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read().strip()
    info["cpu_sockets"] = subprocess.Popen("lscpu | grep 'Socket(s)' | awk -F ':' '{print $2}'",stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read().strip()
    info["cpu_cores_per_socket"] = subprocess.Popen("lscpu | grep 'per socket' | awk -F ':' '{print $2}'",stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read().strip()
    info["cpu_threads_per_core"] = subprocess.Popen("lscpu | grep 'per core' | awk -F ':' '{print $2}'",stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read().strip()
    info["virtualization"] = subprocess.Popen("lscpu | grep 'Virtualization' | awk -F ':' '{print $2}'",stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read().strip()
    info["all_cpu_usage"] = str(psutil.cpu_percent())
    info["physical_memory_size_in_mb"] = str(psutil.virtual_memory()[0]/1024/1024)
    info["physical_memory_used_in_mb"] = str(psutil.virtual_memory()[0]*psutil.virtual_memory()[2]/1024/1024/100)
    info["swap_size_in_mb"] = str(psutil.swap_memory()[0]/1024/1024)
    info["swap_used_in_mb"] = str(psutil.swap_memory()[1]/1024/1024)
    info["networkinfo"] = {}

    network = {}
    i = 0
    for iface in netifaces.interfaces():
        ifaddress = netifaces.ifaddresses(iface)
        if iface != "lo0": continue
        print iface
        network["name"] = iface
        try:
            network["ip_address"] = ifaddress[2][0]["addr"]
        except:
            network["ip_address"] = "null"
        try:
            network["broadcast"] = ifaddress[2][0]["broadcast"]
        except:
            network["broadcast"] = "null"
        try:
            network["netmask"] = ifaddress[2][0]["netmask"]
        except:
            network["netmask"] = "null"
        try:
            network["mac_address"] = ifaddress[18][0]["addr"]
        except:
            network["mac_address"] = "null"
        try:
            cmd = "ethtool %s 2>/dev/null | grep 'Speed' | awk -F ':' '{print $2}'" % iface
            network["speed"] = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).stdout.read().strip() % iface
        except:
            network["speed"] = "null"
        info["networkinfo"][i] = network
        i = i+1

    #Network_Interface_Bandwidth
    #Network_Interface_Updown
    #Network_Usage
    #info["network"] = networkinfo
    return info

print getHostInfo()
