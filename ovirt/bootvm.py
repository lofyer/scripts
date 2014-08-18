#!/usr/bin/python
import urllib2
from xml.dom import minidom
import subprocess

engine="192.168.1.200"
username="admin@internal"
password="admin"
vms=["aaa"]
desktops=[]

def AuthUser():
	global engine, username, password

	url = "https://" + engine + "/api/"

	passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
	passman.add_password(None, url, username, password)
	authhandler = urllib2.HTTPBasicAuthHandler(passman)
	opener = urllib2.build_opener(authhandler)
	urllib2.install_opener(opener)

	req = urllib2.Request(url=url)
	res = urllib2.urlopen(req).read()

def StartVm(vm_uuid):
	global engine, username, password
	url = "https://" + engine + "/api/vms/" + vm_uuid + "/start/"

	req = urllib2.Request(url=url, data="<action />", headers={'Content-Type':'application/xml'})
	cmd='curl -k -u %s:%s https://%s/api/vms/%s/start -X POST -d "<action />" -H "Content-type: application/xml"' % (username, password, engine, vm_uuid)
	print vm_uuid
	subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
	#res = urllib2.urlopen(req).read()

def ParseVms(xml):
	global desktops
	doc = minidom.parseString(xml)

	root = doc.documentElement

	for vm in root.getElementsByTagName("vm"):
		desktop = {}
		uuid = vm.getAttribute("id")
		desktop['id'] = uuid

		nameNode = vm.getElementsByTagName("name")[0]
		desktop['name'] = nameNode.childNodes[0].nodeValue

		desktops.append(desktop)
	return desktops

def ListVms():
	global engine, username, password
	url = "http://" + engine + "/api/vms/"
	req = urllib2.Request(url=url)
	res = urllib2.urlopen(req).read()
	return ParseVms(res)
	
AuthUser()
allvms=ListVms()
for vm in allvms:
	if vm["name"] in vms:
		print vm["id"]
		StartVm(vm["id"])
