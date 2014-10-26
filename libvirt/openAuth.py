#!/usr/bin/python
import libvirt

URI = "qemu+ssh://root@192.168.2.110/system"
USER = "root"
PASS = "123456"

def authcb(credentials, user_data):
    for credential in credentials:
        if credential[0] == libvirt.VIR_CRED_AUTHNAME:
            credential[4] = USER
        elif credential[0] == libvirt.VIR_CRED_PASSPHRASE:
            credential[4] = PASS
    return 0
auth = [[libvirt.VIR_CRED_AUTHNAME, libvirt.VIR_CRED_PASSPHRASE], authcb, None]
conn = libvirt.openAuth(URI, auth, 0)
print conn.getCapabilities()
