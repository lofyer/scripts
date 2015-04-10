#!/usr/bin/env python
from ovirtsdk.api import API
from ovirtsdk.xml import params
from time import sleep
import subprocess
import sys

if len(sys.argv) < 5:
    print "Usage: "
    print "./setup-localdc.py adminpassword ipaddress netmask gateway"
    exit(1)

USERNAME = 'admin@internal'
PASSWORD = sys.argv[1]
URL = 'https://localhost/api'

DC_NAME = 'LocalDC'
CLUSTER_NAME = 'LocalCluster'
CPU_TYPE = 'Intel Conroe Family'
VERSION = params.Version(major='3', minor='4')
# Host info
HOST_NAME = 'IAM_Local'
HOST_ADDRESS = 'localhost'
ROOT_PASSWORD = '123456'
ETH = 'eth0'
# ovirtmgmt info
IP_ADDRESS = sys.argv[2]
IP_NETMASK = sys.argv[3]
IP_GATEWAY = sys.argv[4]
# Data domain
DATA_PATH = '/home/vdsm/data'
DATA_NAME = 'LocalData'
# ISO domain
ISO_PATH = '/home/vdsm/iso'
ISO_NAME = 'LocalISO'

try:
    api = API(URL, username=USERNAME, password=PASSWORD, insecure=True)
except Exception as e:
    print 'Failed to login.\n%s' % str(e)
    exit(1)
def nullifyNic(hostNIC):
    ''' resets nic configuration to enable its reuse
    '''
    hostNIC.network =  params.Network()
    hostNIC.boot_protocol = 'none'
    hostNIC.ip = params.IP(address='', netmask='', gateway='')
    return hostNIC
# Create DC
try:
    if api.datacenters.add(params.DataCenter(name=DC_NAME, storage_type='localfs', version=VERSION)):
        print 'Local Data Center was created successfully'
except Exception as e:
    print 'Failed to create Local Data Center:\n%s' % str(e)

# Create Cluster
try:
    if api.clusters.add(params.Cluster(name=CLUSTER_NAME, cpu=params.CPU(id=CPU_TYPE), data_center=api.datacenters.get(DC_NAME), version=VERSION)):
        print 'Cluster was created successfully'
except Exception as e:
    print 'Failed to create Cluster:\n%s' % str(e)

# Install vdsm, since it will be failed if we put it to livecd
try:
    pass
    #cmd = "tar xf /etc/vdsm-setup/vdsm.tar.gz -C /tmp/vdsm-setup/; mv /etc/yum.repos.d/* /tmp/vdsm-setup/; yum localinstall -y /tmp/vdsm-setup/vdsm/*;rm -fr /tmp/vdsm-setup/vdsm/; mv /tmp/vdsm-setup/*.repo /etc/yum.repos.d/"
    #cmd_out = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).stdout.read()
except Exception as e:
    print 'Failed to install rpm:\n%s' % str(e)
    exit(1)

# Add host
try:
    if api.hosts.add(params.Host(name=HOST_NAME, address=HOST_ADDRESS, cluster=api.clusters.get(CLUSTER_NAME), root_password=ROOT_PASSWORD)):
        sleep(60)
        print 'Host was installed successfully'
except Exception as e:
    print 'Failed to install Host:\n%s' % str(e)

# Add ovirtmgmt to host
try:
    #data_center=api.datacenters.get(DC_NAME),
    #host = api.hosts.get(HOST_NAME),
    #ovirtmgmt = data_center.networks.get(name='ovirtmgmt')
    #eth = host.nics.get(name=ETH)
    print 'Adding ovirtmgmt to host'
    hostNics = api.hosts.get(HOST_NAME).nics
    # sync
    hostNicsParam = hostNics.list()
    for nic in hostNicsParam:
        nic.set_override_configuration(True)
    attachnic = params.HostNIC(network = params.Network(name = 'ovirtmgmt'),
        name = 'eth0',
        boot_protocol = 'static',
        ip = params.IP(
            address = IP_ADDRESS,
            netmask = IP_NETMASK,
            gateway = IP_GATEWAY),
        override_configuration = 1
    )
    hostNics.setupnetworks(params.Action(force = 0,
        check_connectivity = 1,
        host_nics = params.HostNics(host_nic = [ attachnic ])))
    # Active host
    host=api.hosts.get(HOST_NAME)
    host.activate()
    print 'Waiting for host to reach the Up status'
    while api.hosts.get(HOST_NAME).status.state != 'up':
        sleep(10)
    print "Host is up"
except Exception as e:
    print 'Failed to setup network:\n%s' % str(e)

# Add data domain
''' Add iscsi target
    storage = params.Storage(type_='iscsi',
        volume_group=params.VolumeGroup(logical_unit=[params.LogicalUnit(id=LUN_GUID,
        address=STORAGE_ADDRESS,
        port=3260,
        target=TARGET_NAME)])))
'''
sdParams = params.StorageDomain(name=DATA_NAME,
    data_center=api.datacenters.get(DC_NAME),
    storage_format='v3',
    type_='data',
    host=api.hosts.get(HOST_NAME),
    storage = params.Storage(type_='localfs', path=DATA_PATH))

try:
    if api.storagedomains.add(sdParams):
        print 'Local Storage Domain was created successfully'
except Exception as e:
    print 'Failed to create Local Storage Domain:\n%s' % str(e)
    exit(1)

#try:
#    if api.datacenters.get(name=DC_NAME).storagedomains.add(api.storagedomains.get(name=STORAGE_NAME)):
#        print 'Local Storage Domain was attached successfully'
#except Exception as e:
#    print 'Failed to attach Local Storage Domain:\n%s' % str(e)

# Add iso domain
isoParams = params.StorageDomain(name=ISO_NAME,
    data_center=api.datacenters.get(DC_NAME),
    type_='iso',
    host=api.hosts.get(HOST_NAME),
    storage = params.Storage(type_='localfs',
        path=ISO_PATH))

try:
    if api.storagedomains.add(isoParams):
        print 'ISO Domain was created/imported successfully'
    #if api.datacenters.get(DC_NAME).storagedomains.add(api.storagedomains.get(ISO_NAME)):
    #    print 'ISO Domain was created and attached successfully'
    # if api.datacenters.get(DC_NAME).storagedomains.get(ISO_NAME).activate():
    #    print 'ISO Domain was activated successfully'
except Exception as e:
    print 'Failed to add ISO domain:\n%s' % str(e)
    exit(1)
