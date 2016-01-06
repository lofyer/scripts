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
import xml.dom

import hooking


def main():
    try:
        doc = hooking.read_domxml()
        sound = doc.getElementsByTagName('sound')[0]
        sound.setAttribute('model','ac97')
        hooking.write_domxml(doc)
    except Exception as e:
        pass


if __name__ == '__main__':
    try:
        main()
    except:
        hooking.exit_hook('extnet hook: [unexpected error]: %s\n' %
                          traceback.format_exc())
