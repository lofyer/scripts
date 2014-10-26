#!/usr/bin/env python
import libvirt

#URI = "qemu+ssh://root@192.168.2.110/system"
#DEST_URI = "qemu+ssh://root@192.168.2.111/system"
URI = "qemu+tcp://192.168.2.110/system"
DEST_URI = "qemu+tcp://192.168.2.111/system"
#USER = "root"
#PASS = "123456"

def authcb(credentials, user_data):
    for credential in credentials:
        if credential[0] == libvirt.VIR_CRED_AUTHNAME:
            credential[4] = USER
        elif credential[0] == libvirt.VIR_CRED_PASSPHRASE:
            credential[4] = PASS
    return 0

#def auth_domain():
    #auth = [[libvirt.VIR_CRED_AUTHNAME, libvirt.VIR_CRED_PASSPHRASE], authcb, None]
    #conn = libvirt.openAuth(URI, auth, 0)
    #dest_conn = libvirt.openAuth(URI, auth, 0)

def start_demo_doamin():
    f = open('a.xml', 'r')
    return 1

def migrate_domain(domain_name):
    try:
        #auth_domain()
        conn = libvirt.open(URI)
        dest_conn = libvirt.open(DEST_URI)
        dest_vm = conn.lookupByName(domain_name)
        dest_vm.migrate(dest_conn, 1, domain_name, None, 0)
        #dest_domain.migrate(dest_conn, 1, domain_name, 'tcp://192.168.2.110', 0)
    except Exception,e:
        print e
        return 1
    return 0

if __name__ == '__main__':
    print migrate_domain('myvm')
