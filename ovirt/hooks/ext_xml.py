#!/usr/bin/python
"""
Tweak an interface defintion so that its source is forced to be a specified
network. Applied on a per vnic basis, it gets triggered and used by two
different events:
    * before_device_create
    * before_nic_hotplug

This hook can be used to force a VM to use a libvirt network that is managed
outside of ovirt, such as an openvswitch network, or libvirt's default network.
"""


import os
import sys
import traceback
from xml.dom import minidom

import hooking

#ext_string="""
#<interface type='hostdev'>
#  <mac address='9a:eb:fd:22:c4:67'/>
#  <driver name='vfio'/>
#  <source>
#    <address type='pci' domain='0x0000' bus='0x04' slot='0x10' function='0x2'/>
#  </source>
#</interface>
#"""

ext_string="""
<hostdev mode='subsystem' type='pci' managed='yes'>
      <driver name='vfio'/>
      <source>
        <address domain='0x0000' bus='0x04' slot='0x10' function='0x2'/>
      </source>
      <alias name='igbxe'/>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x08' function='0x0' multifunction='on'/>
</hostdev>
"""

def main():
    #newnet = os.environ.get('extnet')
    doc = hooking.read_domxml()
    uuid = doc.getElementsByTagName('uuid')[0]
    UUID = uuid.childNodes[0].nodeValue
    if UUID == "f60cba97-e09f-4515-bdef-a7af3d93e6e5":
        pass
    else:
        return 0
    devices_dom = doc.getElementsByTagName("devices")[0]
    ext_dom = minidom.parseString(ext_string)
    ext_elements = ext_dom.getElementsByTagName("hostdev")[0]
    devices_dom.appendChild(ext_elements)
    hooking.write_domxml(doc)

if __name__ == '__main__':
    try:
        main()
    except:
        hooking.exit_hook('ext_xml hook: [unexpected error]: %s\n' %
                          traceback.format_exc())
