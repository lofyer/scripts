#!/usr/bin/env python
import platform
import psutil

def getHostInfo():
    '''
    Use hal-get-property ?
    STATIC_INFO                 DYNAMIC_INFO
    Hostname
    OS_Version
    Kernel_Version
    KVM_Version
    SPICE_Version
    RUNNING_VMS
    CPU_Family
    CPU_Type
    CPU_Sockets
    CPU_Cores
    CPU_Cores_per_Socket
    CPU_Threads_per_Core        All_CPU_Usage
    Physical_Memory_Size        Physical_Memory_Usage
    Swap_Size                   Swap_Usage
    IP_Address
    MAC_Address
    Network_Interfaces
    Network_Interface_Bandwidth Network_Usage
    Network_Interface_Updown    Network_Usage
    '''
    return 0

print getHostInfo()
