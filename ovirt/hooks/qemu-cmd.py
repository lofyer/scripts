#!/usr/bin/python
import os
import sys
import hooking
import traceback
import json
import shutil

def addQemuNs(domXML):
    domain = domXML.getElementsByTagName('domain')[0]
    domain.setAttribute('xmlns:qemu',
                        'http://libvirt.org/schemas/domain/qemu/1.0')


def injectQemuCmdLine(domXML, qc):
    domain = domXML.getElementsByTagName('domain')[0]
    qctag = domXML.createElement('qemu:commandline')

    for cmd in qc:
        qatag = domXML.createElement('qemu:arg')
        qatag.setAttribute('value', cmd)

        qctag.appendChild(qatag)

    domain.appendChild(qctag)

domxml = hooking.read_domxml()
cur_vm_uuid = domxml.getElementsByTagName('uuid')[0].firstChild.nodeValue

UUID = "asdbcdef"

if cur_vm_uuid == UUID:
    # USB
    # vendroid = "1bc0"
    # productid = "1234"
    # params = '["-device","usb-host,vendorid=%s,productid=%s"]' % (vendorid,productid)
    # GPU
    # video_param = "pci-assign,host=%s" % video_id
    # audio_param = "pci-assign,host=%s" % audio_id
    # params = '["-boot","menu=on","-device","%s","-device","%s"]' % (video_param, audio_param)
    # VFIO SR-IOV ETHERNET
    params = '["-net","none","-device","vfio-pci,host=81:10.0"]'
    os.environ.__setitem__("qemu_cmdline",params)
else:
    sys.exit(0)

if 'qemu_cmdline' in os.environ:
    try:
        domxml = hooking.read_domxml()

        qemu_cmdline = json.loads(os.environ['qemu_cmdline'])
        addQemuNs(domxml)
        injectQemuCmdLine(domxml, qemu_cmdline)

        hooking.write_domxml(domxml)
    except:
        sys.stderr.write('qemu_cmdline: [unexpected error]: %s\n'
                         % traceback.format_exc())
        sys.exit(2)
