#!/usr/bin/env python
import sys
import libvirt

# Commands list:
# 
# list_networks
#     Return: all libvirt networks
# create_network network_name
#     Return: 0: Success
# delete_network network_name
#     Return: 0: Success
# check_network network_name
#     Return: 0: Clear, 1: In use

USER = "vdsm@ovirt"
PASS = file("/etc/pki/vdsm/keys/libvirt_password").readline().rstrip("\n")

def authcb(credentials, user_data):
    for credential in credentials:
        if credential[0] == libvirt.VIR_CRED_AUTHNAME:
            credential[4] = USER
        elif credential[0] == libvirt.VIR_CRED_PASSPHRASE:
            credential[4] = PASS
    return 0

def check_network(network_name):
    auth = [[libvirt.VIR_CRED_AUTHNAME, libvirt.VIR_CRED_PASSPHRASE], authcb, None]
    uri = "qemu:///system"
    conn = libvirt.openAuth(uri, auth, 0)
    nw = conn.networkLookupByName(network_name)
    if nw.destroy() != 0:
        return 1
    nw.create()
    return 0

def list_networks():
    auth = [[libvirt.VIR_CRED_AUTHNAME, libvirt.VIR_CRED_PASSPHRASE], authcb, None]
    uri = "qemu:///system"
    conn = libvirt.openAuth(uri, auth, 0)
    networks = conn.listNetworks()
    conn.close()
    return networks

def create_network(network_name):
    auth = [[libvirt.VIR_CRED_AUTHNAME, libvirt.VIR_CRED_PASSPHRASE], authcb, None]
    uri = "qemu:///system"
    conn = libvirt.openAuth(uri, auth, 0)
    nw_xml = "<network><name>%s</name><forward mode='bridge'/><bridge name='%s' /><virtualport type='openvswitch'/></network>" % (network_name, network_name)

    try:
        conn.networkDefineXML(nw_xml)
    except Exception as e:
        return "%s: net-define failed." % e

    nw = conn.networkLookupByName(network_name) 

    try:
        nw.create()
    except Exception as e:
        return "%s: net-create failed." % e
    
    nw.setAutostart(1)
    conn.close()
    return 0

def delete_network(network_name):
    auth = [[libvirt.VIR_CRED_AUTHNAME, libvirt.VIR_CRED_PASSPHRASE], authcb, None]
    uri = "qemu:///system"
    conn = libvirt.openAuth(uri, auth, 0)
    nw = conn.networkLookupByName(network_name) 
    if check_network(network_name) == 0:
        nw.destroy()
        nw.undefine()
    return 0

if sys.argv[1] == "list_networks":
    print list_networks()

if sys.argv[1] == "create_network":
    print create_network(sys.argv[2])

if sys.argv[1] == "delete_network":
    print delete_network(sys.argv[2])

if sys.argv[1] == "check_network":
    print check_network(sys.argv[2])
