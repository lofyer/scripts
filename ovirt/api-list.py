#!/usr/bin/python
import os
import sys
#import httplib
#import threading
#import subprocess
#import logging
#import time
#import inspect
#import urllib
import urllib2
from xmltodict import parse
#import commands
#from datetime import datetime
from xml.dom import minidom

from base64 import b32encode, b32decode

from logger import logger


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# Configuration file should include:
# VIRTUAL_KEYBOARD=True/False
#     If set to True, the virtual keyboard will be shown. User for the case of touch screen.
# ENGINE_IP=xxx.xxx.xxx.xxx
# USER_NAME=xxx

#platform = sys.platform
#if platform == 'win32':
#    cfile = os.getcwd() + '\\vclient.conf'
#    lfile = os.getcwd() + '\\vclient.log'
#    cafile = 'ca.crt'
#    #viewer = "VirtViewer\\bin\\remote-viewer"
#else:		#linux2
#    cdir = os.path.dirname(os.path.realpath(inspect.getfile(inspect.currentframe())))
#    cfile = cdir + '/vclient.conf'
#    lfile = cdir + '/vclient.log'
#    cafile = 'ca.crt'
#    #viewer = "remote-viewer"
#viewer = None
#spicec = None
cafile = os.path.join(BASE_DIR, "ca.crt")
#vkbd = 'False'
#showmenu = 'True'
#autologin = 'False'
#autoconnect = 'False'
engine = '192.168.0.223'
username = 'admin@internal'
password = 'admin'
desktops = []

#ldialog = None
#virtkeyboard = None
#desktopframe = None
#curfocus = None
#curdialog = None


def encrypt(msg):
    return b32encode(msg)

def decrypt(msg):
    return b32decode(msg)


RETRY_COUNT = 3
def sendRequestToEngine(url, method=None, data=None, headers=None):
    count = 0
    while (count < RETRY_COUNT):
        print("Sending request (%s) to: %s..." % (str(count), url))
        try:
            passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
            passman.add_password(None, url, username, password)
            authhandler = urllib2.HTTPBasicAuthHandler(passman)
            opener = urllib2.build_opener(authhandler)
            urllib2.install_opener(opener)

            if data:
                if headers:
                    request = urllib2.Request(url=url, data=data, headers=headers)
                else:
                    request = urllib2.Request(url=url, data=data)
            else:
                if headers:
                    request = urllib2.Request(url=url, headers=headers)
                else:
                    request = urllib2.Request(url=url)

            if method:
                request.get_method = lambda: method

            response = urllib2.urlopen(request).read()
            return response
        except Exception, e:
            count = count + 1
            #logger.info(str(e))
            print str(e)
        #time.sleep(1)
    if count == RETRY_COUNT:
        raise Exception("Sending request failed!")


def FetchCA():
    logger.info('Fetching Certification...')
    url = "https://" + engine + "/ca.crt"
    req = urllib2.Request(url=url)
    res = urllib2.urlopen(req).read()
    ca = open(cafile, "w" )
    ca.write(res)
    ca.close()


def AuthUser():
    logger.info('Authenticating User...')

    url = "https://" + engine + "/api/"

    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)

    req = urllib2.Request(url=url)
    res = urllib2.urlopen(req).read()


#################################################################
#
# Listing resources
#
#################################################################
def getDataCenters():
    url = "https://" + engine + "/api/datacenters/"
    response = sendRequestToEngine(url=url, headers={'filter':'true'})
    return parse(response)


def getClusters():
    url = "https://" + engine + "/api/clusters/"
    response = sendRequestToEngine(url=url, headers={'filter':'true'})
    return parse(response)


def getNetworks():
    url = "https://" + engine + "/api/networks/"
    response = sendRequestToEngine(url=url, headers={'filter':'true'})
    return parse(response)


def getStorageDomains():
    url = "https://" + engine + "/api/storagedomains/"
    response = sendRequestToEngine(url=url, headers={'filter':'true'})
    return parse(response)


def getHosts():
    url = "https://" + engine + "/api/hosts/"
    response = sendRequestToEngine(url=url, headers={'filter':'true'})
    return parse(response)


def getVms():
    url = "https://" + engine + "/api/vms/"
    response = sendRequestToEngine(url=url, headers={'filter':'false'})
    return parse(response)


def getTemplates():
    url = "https://" + engine + "/api/templates/"
    response = sendRequestToEngine(url=url, headers={'filter':'true'})
    return parse(response)


def getVmpools():
    url = "https://" + engine + "/api/vmpools/"
    response = sendRequestToEngine(url=url, headers={'filter':'true'})
    return parse(response)


def getDomains():
    url = "https://" + engine + "/api/domains/"
    response = sendRequestToEngine(url=url, headers={'filter':'true'})
    return parse(response)


def getGroups():
    url = "https://" + engine + "/api/groups/"
    response = sendRequestToEngine(url=url, headers={'filter':'true'})
    return parse(response)


def getUsers():
    url = "https://" + engine + "/api/users/"
    response = sendRequestToEngine(url=url, headers={'filter':'true'})
    return parse(response)


def getTags():
    url = "https://" + engine + "/api/tags/"
    response = sendRequestToEngine(url=url, headers={'filter':'true'})
    return parse(response)


def getRoles():
    url = "https://" + engine + "/api/roles/"
    response = sendRequestToEngine(url=url)
    return parse(response)


#################################################################
#
# Getting specific resource
#
#################################################################
def getDataCenter(datacenter_id):
    url = "https://" + engine + "/api/datacenters/" + datacenter_id
    response = sendRequestToEngine(url=url)
    return parse(response)


def getDataCenterStorageDomains(datacenter_id):
    url = "https://" + engine + "/api/datacenters/" + datacenter_id + '/storagedomains/'
    response = sendRequestToEngine(url=url)
    return parse(response)


def getDataCenterClusters(datacenter_id):
    url = "https://" + engine + "/api/datacenters/" + datacenter_id + '/clusters/'
    response = sendRequestToEngine(url=url)
    return parse(response)


def getDataCenterNetworks(datacenter_id):
    url = "https://" + engine + "/api/datacenters/" + datacenter_id + '/networks/'
    response = sendRequestToEngine(url=url)
    return parse(response)


def getDataCenterPermissions(datacenter_id):
    url = "https://" + engine + "/api/datacenters/" + datacenter_id + '/permissions/'
    response = sendRequestToEngine(url=url)
    return parse(response)


def getDataCenterQuotas(datacenter_id):
    url = "https://" + engine + "/api/datacenters/" + datacenter_id + '/quotas/'
    response = sendRequestToEngine(url=url)
    return parse(response)


def getDataCenterIscsiBonds(datacenter_id):
    url = "https://" + engine + "/api/datacenters/" + datacenter_id + '/iscsibonds/'
    response = sendRequestToEngine(url=url)
    return parse(response)


def getDataCenterQoss(datacenter_id):
    url = "https://" + engine + "/api/datacenters/" + datacenter_id + '/qoss/'
    response = sendRequestToEngine(url=url)
    return parse(response)


def getCluster(cluster_id):
    url = "https://" + engine + "/api/clusters/" + cluster_id
    response = sendRequestToEngine(url=url)
    return parse(response)


def getClusterNetworks(cluster_id):
    url = "https://" + engine + "/api/clusters/" + cluster_id + "/networks/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getClusterPermissions(cluster_id):
    url = "https://" + engine + "/api/clusters/" + cluster_id + "/permissions/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getClusterGlusterVolumes(cluster_id):
    url = "https://" + engine + "/api/clusters/" + cluster_id + "/glustervolumes/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getClusterGlusterHooks(cluster_id):
    url = "https://" + engine + "/api/clusters/" + cluster_id + "/glusterhooks/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getClusterAffinityGroups(cluster_id):
    url = "https://" + engine + "/api/clusters/" + cluster_id + "/affinitygroups/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getClusterCpuProfiles(cluster_id):
    url = "https://" + engine + "/api/clusters/" + cluster_id + "/cpuprofiles/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getNetwork(network_id):
    url = "https://" + engine + "/api/networks/" + network_id
    response = sendRequestToEngine(url=url)
    return parse(response)


def getNetworkPermissions(network_id):
    url = "https://" + engine + "/api/networks/" + network_id + "/permissions/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getNetworkVnicProfiles(network_id):
    url = "https://" + engine + "/api/networks/" + network_id + "/vnicprofiles/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getNetworkLabels(network_id):
    url = "https://" + engine + "/api/networks/" + network_id + "/labels/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getStorageDomain(storagedomain_id):
    url = "https://" + engine + "/api/storagedomains/" + storagedomain_id
    response = sendRequestToEngine(url=url)
    return parse(response)


def getStorageDomain(storagedomain_id):
    url = "https://" + engine + "/api/storagedomains/" + storagedomain_id
    response = sendRequestToEngine(url=url)
    return parse(response)


def getStorageDomainPermissions(storagedomain_id):
    url = "https://" + engine + "/api/storagedomains/" + storagedomain_id + "/permissions/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getStorageDomainDisks(storagedomain_id):
    url = "https://" + engine + "/api/storagedomains/" + storagedomain_id + "/disks/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getStorageDomainStorageConnections(storagedomain_id):
    url = "https://" + engine + "/api/storagedomains/" + storagedomain_id + "/storageconnections/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getStorageDomainDiskSnapshots(storagedomain_id):
    url = "https://" + engine + "/api/storagedomains/" + storagedomain_id + "/disksnapshots/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getStorageDomainDiskProfiles(storagedomain_id):
    url = "https://" + engine + "/api/storagedomains/" + storagedomain_id + "/diskprofiles/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getIsoStorageDomainFiles(storagedomain_id):
    url = "https://" + engine + "/api/storagedomains/" + storagedomain_id + "/files/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getHost(host_id):
    url = "https://" + engine + "/api/hosts/" + host_id
    response = sendRequestToEngine(url=url)
    return parse(response)


def getHostStorage(host_id):
    url = "https://" + engine + "/api/hosts/" + host_id + "/storage/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getHostNics(host_id):
    url = "https://" + engine + "/api/hosts/" + host_id + "/nics/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getHostNumanodes(host_id):
    url = "https://" + engine + "/api/hosts/" + host_id + "/numanodes/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getHostTags(host_id):
    url = "https://" + engine + "/api/hosts/" + host_id + "/tags/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getHostPermissions(host_id):
    url = "https://" + engine + "/api/hosts/" + host_id + "/permissions/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getHostStatistics(host_id):
    url = "https://" + engine + "/api/hosts/" + host_id + "/statistics/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVm(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmApplications(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/applications/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmDisks(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/disks/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmNics(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/nics/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmNumanodes(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/numanodes/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmCdroms(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/cdroms/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmSnapshots(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/snapshots/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmTags(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/tags/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmPermissions(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/permissions/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmStatistics(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/statistics/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmReportedDevices(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/reporteddevices/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmWatchDogs(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/watchdogs/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmSessions(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/sessions/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmDiskStatistics(vm_id, disk_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/disks/" + disk_id + "/statistics/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmNicStatistics(vm_id, nic_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/nics/" + nic_id + "/statistics/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getTemplate(template_id):
    url = "https://" + engine + "/api/templates/" + template_id
    response = sendRequestToEngine(url=url)
    return parse(response)


def getTemplateDisks(template_id):
    url = "https://" + engine + "/api/templates/" + template_id + "/disks/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getTemplateNics(template_id):
    url = "https://" + engine + "/api/templates/" + template_id + "/nics/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getTemplateCdroms(template_id):
    url = "https://" + engine + "/api/templates/" + template_id + "/cdroms/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getTemplateTags(template_id):
    url = "https://" + engine + "/api/templates/" + template_id + "/tags/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getTemplatePermissions(template_id):
    url = "https://" + engine + "/api/templates/" + template_id + "/permissions/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getTemplateWatchDogs(template_id):
    url = "https://" + engine + "/api/templates/" + template_id + "/watchdogs/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmpool(vmpool_id):
    url = "https://" + engine + "/api/vmpools/" + vmpool_id
    response = sendRequestToEngine(url=url)
    return parse(response)


def getVmpoolPermissions(vmpool_id):
    url = "https://" + engine + "/api/vmpools/" + vmpool_id + "/permissions/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getDomain(domain_id):
    url = "https://" + engine + "/api/domains/" + domain_id
    response = sendRequestToEngine(url=url)
    return parse(response)


def getDomainUsers(domain_id):
    url = "https://" + engine + "/api/domains/" + domain_id + "/users/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getDomainGroups(domain_id):
    url = "https://" + engine + "/api/domains/" + domain_id + "/groups/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getGroup(group_id):
    url = "https://" + engine + "/api/groups/" + group_id
    response = sendRequestToEngine(url=url)
    return parse(response)


def getGroupPermissions(group_id):
    url = "https://" + engine + "/api/groups/" + group_id + "/permissions/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getGroupRoles(group_id):
    url = "https://" + engine + "/api/groups/" + group_id + "/roles/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getGroupTags(group_id):
    url = "https://" + engine + "/api/groups/" + group_id + "/tags/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getUser(user_id):
    url = "https://" + engine + "/api/users/" + user_id
    response = sendRequestToEngine(url=url)
    return parse(response)


def getUserPermissions(user_id):
    url = "https://" + engine + "/api/users/" + user_id + "/permissions/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getUserRoles(user_id):
    url = "https://" + engine + "/api/users/" + user_id + "/roles/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getUserTags(user_id):
    url = "https://" + engine + "/api/users/" + user_id + "/tags/"
    response = sendRequestToEngine(url=url)
    return parse(response)


def getTag(tag_id):
    url = "https://" + engine + "/api/tags/" + tag_id
    response = sendRequestToEngine(url=url)
    return parse(response)


def getRole(role_id):
    url = "https://" + engine + "/api/roles/" + role_id
    response = sendRequestToEngine(url=url)
    return parse(response)


def getRolePermits(role_id):
    url = "https://" + engine + "/api/roles/" + role_id + "/permits/"
    response = sendRequestToEngine(url=url)
    return parse(response)


#################################################################
#
# Data Center Update Logic
#
#################################################################
def createDataCenter(name, storage_type, version):
    url = "https://" + engine + "/api/datacenters/"
    response = sendRequestToEngine(url=url, data="<data_center><name>%s</name><storage_type>%s</storage_type><version minor='%s' major='%s'/></data_center>" % (name, storage_type, version['minor'], version['major']), headers={'Content-Type': 'application/xml'})
    return parse(response)


def updateDataCenterName(datacenter_id, name):
    url = "https://" + engine + "/api/datacenters/" + datacenter_id
    response = sendRequestToEngine(url=url, method='PUT', data="<data_center><name>%s</name></data_center>" % description, headers={'Content-Type': 'application/xml'})
    return parse(response)

    
def updateDataCenterDescription(datacenter_id, description):
    url = "https://" + engine + "/api/datacenters/" + datacenter_id
    response = sendRequestToEngine(url=url, method='PUT', data="<data_center><description>%s</description></data_center>" % description, headers={'Content-Type': 'application/xml'})
    return parse(response)


def removeDataCenter(datacenter_id):
    url = "https://" + engine + "/api/datacenters/" + datacenter_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


def attachDataCenterStorageDomain(datacenter_id, storagedomain_id):
    url = "https://" + engine + "/api/datacenters/" + datacenter_id + "/storagedomains/"
    response = sendRequestToEngine(url=url, data="<storage_domain id='%s' />" % storagedomain_id, headers={'Content-Type': 'application/xml'})
    return parse(response)



def activateDataCenterStorageDomain(datacenter_id, storagedomain_id):
    url = "https://" + engine + "/api/datacenters/" + datacenter_id + "/storagedomains/" + storagedomain_id + "/activate/"
    response = sendRequestToEngine(url=url, data="<action />", headers={'Content-Type': 'application/xml'})
    return parse(response)


def deactivateDataCenterStorageDomain(datacenter_id, storagedomain_id):
    url = "https://" + engine + "/api/datacenters/" + datacenter_id + "/storagedomains/" + storagedomain_id + "/deactivate/"
    response = sendRequestToEngine(url=url, data="<action />", headers={'Content-Type': 'application/xml'})
    return parse(response)


#################################################################
#
# Cluster Update Logic
#
#################################################################
def createCluster(name, cpu_id, datacenter_id):
    url = "https://" + engine + "/api/clusters/"
    response = sendRequestToEngine(url=url, data="<cluster><name>%s</name><cpu id='%s' /><data_center id='%s' /></cluster>" % (name, cpu_id, datacenter_id), headers={'Content-Type': 'application/xml'})
    return parse(response)


def updateClusterName(cluster_id, name):
    url = "https://" + engine + "/api/clusters/" + cluster_id
    response = sendRequestToEngine(url=url, method='PUT', data="<cluster><name>%s</name></cluster>" % description, headers={'Content-Type': 'application/xml'})
    return parse(response)


def updateClusterDescription(cluster_id, description):
    url = "https://" + engine + "/api/clusters/" + cluster_id
    response = sendRequestToEngine(url=url, method='PUT', data="<cluster><description>%s</description></cluster>" % description, headers={'Content-Type': 'application/xml'})
    return parse(response)


def removeCluster(cluster_id):
    url = "https://" + engine + "/api/clusters/" + cluster_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


def associateClusterNetwork(cluster_id, network_id):
    url = "https://" + engine + "/api/clusters/" + cluster_id + "/networks/"
    response = sendRequestToEngine(url=url, data="<network><name>%s</name></network>" % name, headers={'Content-Type': 'application/xml'})
    return parse(response)


def removeClusterNetwork(cluster_id, network_id):
    url = "https://" + engine + "/api/clusters/" + cluster_id + "/networks/" + network_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


#################################################################
#
# Network Update Logic
#
#################################################################
def createNetwork(name, datacenter_id):
    url = "https://" + engine + "/api/networks/"
    response = sendRequestToEngine(url=url, data="<network><name>%s</name><data_center id=%s /></network>" % (name, datacenter_id), headers={'Content-Type': 'application/xml'})
    return parse(response)


def updateNetworkName(network_id, name):
    url = "https://" + engine + "/api/networks/" + network_id
    response = sendRequestToEngine(url=url, method='PUT', data="<network><name>%s</name></network>" % name, headers={'Content-Type': 'application/xml'})
    return parse(response)


def updateNetworkDescription(network_id, description):
    url = "https://" + engine + "/api/networks/" + network_id
    response = sendRequestToEngine(url=url, method='PUT', data="<network><description>%s</description></network>" % description, headers={'Content-Type': 'application/xml'})
    return parse(response)


def removeNetwork(network_id):
    url = "https://" + engine + "/api/networks/" + network_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


#################################################################
#
# Storage Domain Update Logic
#
#################################################################
def createStorageDomain(name, storagedomain_type, host_id, storage_type, storage_params):
    url = "https://" + engine + "/api/storagedomains/"
    if storage_type == 'nfs':
        data = "<storage_domain><name>%s</name><type>%s</type><host id='%s' /><storage><type>%s</type><address>%s</address><path>%s</path></storage></storage_domain>" % (name, storagedomain_type, host_id, storage_type, storage_params['address'], storage_params['path'])
    elif storage_type == 'localfs':
        data = "<storage_domain><name>%s</name><type>%s</type><host id='%s' /><storage><type>%s</type><path>%s</path></storage></storage_domain>" % (name, storagedomain_type, host_id, storage_type, storage_params['path'])
    elif storage_type == 'iscsi':
        data = ""			#To handle (aoqingy)
    else:
        raise Exception('Invalid storage type!')

    response = sendRequestToEngine(url=url, data=data, headers={'Content-Type': 'application/xml'})
    return parse(response)


def updateStorageDomainName(storagedomain_id, name):
    url = "https://" + engine + "/api/storagedomains/" + storagedomain_id
    response = sendRequestToEngine(url=url, method='PUT', data="<storage_domain><name>%s</name></storage_domain>" % name, headers={'Content-Type': 'application/xml'})
    return parse(response)


def removeStorageDomain(storagedomain_id):
    url = "https://" + engine + "/api/storagedomains/" + storagedomain_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


def importExportStorageDomainVm(storagedomain_id):		#To think (aoqingy)
    pass


def importExportStorageDomainTemplate(storagedomain_id):	#To think (aoqingy)
    pass


def removeExportStorageDomainVm(storagedomain_id, vm_id):
    url = "https://" + engine + "/api/storagedomains/" + storagedomain_id + "/vms/" + template_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


def removeExportStorageDomainTemplate(storagedomain_id, template_id):
    url = "https://" + engine + "/api/storagedomains/" + storagedomain_id + "/templates/" + template_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


#################################################################
#
# Host Update Logic
#
#################################################################
def createHost(name, address, root_password):
    url = "https://" + engine + "/api/hosts/"
    response = sendRequestToEngine(url=url, data="<host><name>%s</name><address>%s</address><root_password>%s</root_password></host>", headers={'Content-Type': 'application/xml'})
    return parse(response)


def updateHostName(host_id, name):
    url = "https://" + engine + "/api/hosts/" + host_id
    response = sendRequestToEngine(url=url, method='PUT', data="<host><name>%s</name></host>" % name, headers={'Content-Type': 'application/xml'})
    return parse(response)


def removeHost(host_id):
    url = "https://" + engine + "/api/hosts/" + host_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


def activateHost(host_id):
    url = "https://" + engine + "/api/hosts/" + host_id + "/activate/"
    response = sendRequestToEngine(url=url, data="<action />", headers={'Content-Type': 'application/xml'})
    return parse(response)


def deactivateHost(host_id):
    url = "https://" + engine + "/api/hosts/" + host_id + "/deactivate/"
    response = sendRequestToEngine(url=url, data="<action />", headers={'Content-Type': 'application/xml'})
    return parse(response)


def approveHost(host_id):
    url = "https://" + engine + "/api/hosts/" + host_id + "/approve/"
    response = sendRequestToEngine(url=url, data="<action />", headers={'Content-Type': 'application/xml'})
    return parse(response)


def commitHostNetworkConfig(host_id):
    url = "https://" + engine + "/api/hosts/" + host_id + "/commitnetconfig/"
    response = sendRequestToEngine(url=url, data="<action />", headers={'Content-Type': 'application/xml'})
    return parse(response)


def fenceHost(host_id, fence_type):
    url = "https://" + engine + "/api/hosts/" + host_id + "/fence/"
    response = sendRequestToEngine(url=url, data="<action><fence_type>%s</fence_type></action>" % fence_type, headers={'Content-Type': 'application/xml'})
    return parse(response)


def attachHostNics(host_id, network_id):		#nics_id or network_id (aoqingy)
    url = "https://" + engine + "/api/hosts/" + host_id + "/nics/" + network_id + "/attach/"
    response = sendRequestToEngine(url=url, data="<action><network id='%s'></action>" % fence_type, headers={'Content-Type': 'application/xml'})
    return parse(response)


def detachHostNics(host_id, network_id):                #nics_id or network_id (aoqingy)
    url = "https://" + engine + "/api/hosts/" + host_id + "/nics/" + network_id + "/detach/"
    response = sendRequestToEngine(url=url, data="<action><network id='%s'></action>" % fence_type, headers={'Content-Type': 'application/xml'})
    return parse(response)


def addHostTag(host_id, tag_name):
    url = "https://" + engine + "/api/hosts/" + host_id + "/tags/"
    response = sendRequestToEngine(url=url, data="<tag><name>%s</name></tag>" % tag_name, headers={'Content-Type': 'application/xml'})
    return parse(response)


def removeHostTag(host_id, tag_id):
    url = "https://" + engine + "/api/hosts/" + host_id + "/tags/" + tag_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


#################################################################
#
# Vm Update Logic
#
#################################################################
def createVm(name, template_id, cluster_id):
    url = "https://" + engine + "/api/vms/"
    response = sendRequestToEngine(url=url, data="<vm><name>%s</name><cluster><id>%s</id></cluster><template><id>%s</id></template></vm>" % (name, cluster_id, template_id), headers={'Content-Type': 'application/xml'})
    return parse(response)


def updateVmMemory(vm_id, memory):
    url = "https://" + engine + "/api/vms/" + vm_id
    response = sendRequestToEngine(url=url, method='PUT', data="<vm><memory>%s</memory></vm>" % memory, headers={'Content-Type': 'application/xml'})
    return parse(response)


def removeVm(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


def startVm(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/start/"
    response = sendRequestToEngine(url=url, data="<action />", headers={'Content-Type': 'application/xml'})
    return parse(response)


def stopVm(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/stop/"
    response = sendRequestToEngine(url=url, data="<action />", headers={'Content-Type': 'application/xml'})
    return parse(response)


def shutdownVm(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/shutdown/"
    response = sendRequestToEngine(url=url, data="<action />", headers={'Content-Type': 'application/xml'})
    return parse(response)


def suspendVm(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/suspend/"
    response = sendRequestToEngine(url=url, data="<action />", headers={'Content-Type': 'application/xml'})
    return parse(response)


def migrateVm(vm_id, host_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/migrate/"
    if host_id:
        data = "<action><host id='%s'/></action>" % host_id
    else:
        data = "<action />"
    response = sendRequestToEngine(url=url, data=data, headers={'Content-Type': 'application/xml'})
    return parse(response)


def setVmTicket(vm_id, timeout):
    url = "https://" + engine + "/api/vms/" + vm_id + "/ticket/"
    response = sendRequestToEngine(url=url, data="<action><ticket><expiry>%s</expiry></ticket></action>" % str(timeout), headers={'Content-Type': 'application/xml'})
    return parse(response)


def exportVm(vm_id):
    pass


def addVmDisk(vm_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/disks/"
    response = sendRequestToEngine(url=url, data="<disk><size>%s</size></disk>" % str(timeout), headers={'Content-Type': 'application/xml'})
    return parse(response)


def addVmNics(vm_id, network_id):
    pass


def updateVmNics():
    pass


def removeVmNics():
    pass


def changeVmCdrom(vm_id, cdrom_id, file_id, online=False):
    url = "https://" + engine + "/api/vms/" + vm_id + "/cdroms/" + cdrom_id
    if online:
        url += "?current"
    response = sendRequestToEngine(url=url, method="PUT", data="<cdrom><file id='%s' /></cdrom>" % file_id, headers={'Content-Type': 'application/xml'})
    return parse(response)


def addVmSnapshot(vm_id, description):
    url = "https://" + engine + "/api/vms/" + vm_id + "/snapshots/"
    response = sendRequestToEngine(url=url, data="<snapshot><description>%s</description></snapshot>" % description, headers={'Content-Type': 'application/xml'})
    return parse(response)


def previewVmSnapshot(vm_id, snapshot_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/snapshots/" + snapshot_id		#+ "/prev/"? (aoqingy)
    response = sendRequestToEngine(url=url, data="<action />" % description, headers={'Content-Type': 'application/xml'})
    return parse(response)


def restoreVmSnapshot(vm_id, snapshot_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/snapshots/" + snapshot_id + "/restore/"
    response = sendRequestToEngine(url=url, data="<action />" % description, headers={'Content-Type': 'application/xml'})
    return parse(response)


def addVmTag(vm_id, tag_name):
    url = "https://" + engine + "/api/vms/" + vm_id + "/tags/"
    response = sendRequestToEngine(url=url, data="<tag><name>%s</name></tag>" % tag_name, headers={'Content-Type': 'application/xml'})
    return parse(response)


def removeVmTag(vm_id, tag_id):
    url = "https://" + engine + "/api/vms/" + vm_id + "/tags/" + tag_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


#################################################################
#
# Template Update Logic
#
#################################################################
def createTemplate(name, vm_id):
    url = "https://" + engine + "/api/templates/"
    response = sendRequestToEngine(url=url, data="<template><name>%s</name><vm id='%s' /></template>" % (name, vm_id), headers={'Content-Type': 'application/xml'})
    return parse(response)


def updateTemplateMemory(template_id, memory):
    url = "https://" + engine + "/api/templates/" + template_id
    response = sendRequestToEngine(url=url, method='PUT', data="<template><memory>%s</memory></template>" % memory, headers={'Content-Type': 'application/xml'})
    return parse(response)


def removeTemplate(template_id):
    url = "https://" + engine + "/api/templates/" + template_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


def exportTemplate(template_id):
    pass


def addTemplateTag(template_id, tag_name):
    url = "https://" + engine + "/api/templates/" + template_id + "/tags/"
    response = sendRequestToEngine(url=url, data="<tag><name>%s</name></tag>" % tag_name, headers={'Content-Type': 'application/xml'})
    return parse(response)


def removeTemplateTag(template_id, tag_id):
    url = "https://" + engine + "/api/templates/" + template_id + "/tags/" + tag_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


#################################################################
#
# Vm Pool Update Logic
#
#################################################################
def createVmpool(name, template_id, cluster_id):
    url = "https://" + engine + "/api/vmpools/"
    response = sendRequestToEngine(url=url, data="<vmpool><name>%s</name><cluster id='%s' href='/api/clusters/%s'/><template id='%s' href='/api/templates/%s'/></vmpool>" % (name, cluster_id, cluster_id, template_id, template_id), headers={'Content-Type': 'application/xml'})		#Do we need href? (aoqingy)
    return parse(response)


def updateVmpoolSize(vmpool_id, size):
    url = "https://" + engine + "/api/vmpools/" + vmpool_id
    response = sendRequestToEngine(url=url, method='PUT', data="<vmpool><size>%s</size></vmpool>" % size, headers={'Content-Type': 'application/xml'})
    return parse(response)


def removeVmpool(vmpool_id):
    url = "https://" + engine + "/api/vmpools/" + vmpool_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


#################################################################
#
# Domain Update Logic
#
#################################################################
#Domain is not updatable?


#################################################################
#
# Group Update Logic
#
#################################################################
#Group is not updatable?

def addGroupTag(group_id, tag_name):
    url = "https://" + engine + "/api/groups/" + group_id + "/tags/"
    response = sendRequestToEngine(url=url, data="<tag><name>%s</name></tag>" % tag_name, headers={'Content-Type': 'application/xml'})
    return parse(response)


def removeGroupTag(group_id, tag_id):
    url = "https://" + engine + "/api/groups/" + group_id + "/tags/" + tag_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)

#################################################################
#
# User Update Logic
#
#################################################################
#User is not updatable?

def addUserTag(user_id, tag_name):
    url = "https://" + engine + "/api/users/" + user_id + "/tags/"
    response = sendRequestToEngine(url=url, data="<tag><name>%s</name></tag>" % tag_name, headers={'Content-Type': 'application/xml'})
    return parse(response)


def removeUserTag(user_id, tag_id):
    url = "https://" + engine + "/api/users/" + user_id + "/tags/" + tag_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


#################################################################
#
# Role Update Logic
#
#################################################################
def createRole(name, administrative, initial_permits):
    url = "https://" + engine + "/api/roles/"
    data = "<role><name>%s</name><administrative>%s</administrative><permits>"
    for permit in initial_permits:
        data += "<permit id='%s' />" % permit
    data += "</permits></role>"
    response = sendRequestToEngine(url=url, data=data, headers={'Content-Type': 'application/xml'})
    return parse(response)


def updateRoleDescription(role_id, description):
    url = "https://" + engine + "/api/roles/" + role_id
    response = sendRequestToEngine(url=url, method='PUT', data="<role><description>%s</description></role>" % description, headers={'Content-Type': 'application/xml'})
    return parse(response)


def removeRole(role_id):
    url = "https://" + engine + "/api/roles/" + role_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


def assignRolePermit(role_id, permit_id):
    url = "https://" + engine + "/api/roles/" + role_id + "/permits/"
    response = sendRequestToEngine(url=url, data="<permit id='%s' />" % permit_id, headers={'Content-Type': 'application/xml'})
    return parse(response)


def reclaimRolePermit(role_id, permit_id):
    url = "https://" + engine + "/api/roles/" + role_id + "/permits/" + permit_id
    response = sendRequestToEngine(url=url, method='DELETE')
    return parse(response)


#################################################################
#
# Tag Update Logic
#
#################################################################
#Tag hierarchy? (aoqingy)

def CreateISODomain():
    pass


def CreateDataDomain():
    pass


def CreateExportDomain():
    pass


def SetupNetwork():
    pass


def GetDisplayProtocol():
    pass


def ChangeDisplayProtocol():
    pass


if __name__ == "__main__":
    #FetchCA()
    #AuthUser()
    #print ListTemplates()
    #vms =getVms()
    #print len(vms['vms']['vm'])
    #print vms['vms']['vm'][0]['name']
    #print len(vms['vms']['vm'][0]['actions']['link'])
    #print vms['vm']['@id']
    #print StartVm("251dfc39-4623-4860-99cd-1a519a755cdd")
    #print StopVm("251dfc39-4623-4860-99cd-1a519a755cdd")
    #print getDataCenters()
    #print createDataCenter('test', 'nfs', {'major':'3', 'minor':'0'})
    #print setDataCenterDescription('38979bb8-f28b-4f1f-9dac-8e1681a248fc', 'hhhhhhhh')
    #print removeDataCenter('38979bb8-f28b-4f1f-9dac-8e1681a248fc')
    #print getDataCenters()
    #print getTemplates()
    #print getClusters()
    #print createVm("aoaoao", "00000000-0000-0000-0000-000000000000", "00000001-0001-0001-0001-000000000203")
    #print getDataCenters()
    #print getDataCenter("00000002-0002-0002-0002-000000000116")
    #print getVms()
    #print getVm("0b1996bd-b5ad-4f03-b2f7-7f37bb5c9e35")
    #print getVms()
    #for vm in getVms()['vms']['vm']:
    #    print vm['@id']
    #print getClusterNetworks('00000001-0001-0001-0001-000000000203')
    #print getClusterpermissions('00000001-0001-0001-0001-000000000203')
    #print getClustercpuprofiles('00000001-0001-0001-0001-000000000203')
    print getNetworkpermissions('8551d62e-9284-483c-9362-0bc3d77817a9')

