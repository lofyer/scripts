#!/usr/bin/env python

import paramiko
import libvirt
import urllib2

# ssh root@xxx cmd
def ssh_cmd(host_ip, host_rootpass, cmd):
    ssh_c = paramiko.SSHClient()
    ssh_c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_c.connect(host_ip, 22, "root", host_rootpass)
    stdin, stdout, stderr = ssh_c.exec_command(cmd)
    print "stdout: %s\nstderr: %s" % (stdout.readlines(), stderr.readlines())
    ssh_c.close()

# scp file root@xxx:file
def scp(host_ip, host_rootpass, local_file, remote_file):
    t = paramiko.Transport((host_ip,22)) 
    t.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    t.connect(username = "root", password = host_rootpass)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp.get(remote_file, local_file)
    t.close()

# An interactive authentication method
def list_libvirt_networks(host_ip, host_rootpass):
    cmd = "/usr/bin/ovs-node-ctl.py list_networks"
    ssh_cmd(host_ip, host_rootpass, cmd)


def create_libvirt_network(host_ip, host_rootpass, network_name):
    cmd = "/usr/bin/ovs-node-ctl.py create_network %s" % network_name
    ssh_cmd(host_ip, host_rootpass, cmd)

def delete_libvirt_network(host_ip, host_rootpass, network_name):
    cmd = "/usr/bin/ovs-node-ctl.py delete_network %s" % network_name
    ssh_cmd(host_ip, host_rootpass, cmd)
    pass

def check_para():
    pass

# Checkout if network is in use by destroying
def check_libvirt_network_usage(master_ip, network_name):
    cmd = "/usr/bin/ovs-node-ctl.py check_network %s" % network_name
    print ssh_cmd(host_ip, host_rootpass, cmd)

def update_nic_profile(action, bridge_name):
    pass

def setup_dhcp(master_ip, master_rootpass, bridge_name, gateway, dhcp_start, dhcp_end):
    dhcp_conf = """strict-order
pid-file=/var/run/libvirt/network/ovs-%s
conf-file=
except-interface=lo
bind-interfaces
interface=ovs-%s
listen-address=%s
dhcp-range=%s,%s
dhcp-leasefile=/var/lib/libvirt/dnsmasq/ovs-%s.leases
dhcp-lease-max=253
dhcp-no-override
dhcp-hostsfile=/var/lib/libvirt/dnsmasq/ovs-%s.hostsfile
addn-hosts=/var/lib/libvirt/dnsmasq/ovs-%s.addnhosts""" % (bridge_name, bridge_name, gateway, dhcp_start, dhcp_end, bridge_name, bridge_name, bridge_name)
    f_name = "/etc/dnsmasq.d/ovs-%s.conf" % bridge_name
    with open(f_name, 'w') as f:
        f.write(dhcp_conf)
    f.close()
    cmd = "service dnsmasq restart"
    ssh_cmd(master_ip, master_rootpass, cmd)

def del_dhcp(master_ip, master_rootpass, bridge_name):
    cmd = "rm -f /etc/dnsmasq.d/ovs-%s" % bridge_name
    print ssh_cmd(master_ip, master_rootpass, bridge_name)

def add_switch(master_ip, master_rootpass, slave_ip_list, slave_rootpass_list, bridge_name, bridge_ip, bridge_netmask):
    slave_ip_list_c = list(slave_ip_list)
    slave_ip_list_c.insert(0, master_ip)
    slave_rootpass_list_c = list(slave_rootpass_list)
    slave_rootpass_list_c.insert(0, master_rootpass)
    bridge_name = "ovs-" + bridge_name
    for i in range(len(slave_ip_list_c)):
        # exit if it see blank element
        if slave_ip_list_c[i] == '':
            return
        print slave_ip_list_c[i]
        print slave_rootpass_list_c[i]
        # Add ovs-bridge
        cmd = "ovs-vsctl add-br %s" % bridge_name
        print cmd
        ssh_cmd(slave_ip_list_c[i], slave_rootpass_list_c[i], cmd)
    	# Create an ifcfg file, Only master has got an IP
        print "Create network ifcfg"
        if i == 0:
            cmd = 'echo -e "NAME=%s\\nDEVICE=%s\\nONBOOT=yes\\nIPADDR=%s\\nNETMASK=%s" > /etc/sysconfig/network-scripts/ifcfg-%s' % (bridge_name, bridge_name, bridge_ip, bridge_netmask, bridge_name)
        else:
            cmd = 'echo -e "NAME=%s\nDEVICE=%s\nONBOOT=yes" > /etc/sysconfig/network-scripts/ifcfg-%s' % (bridge_name, bridge_name, bridge_name)

        print cmd
        ssh_cmd(slave_ip_list_c[i], slave_rootpass_list_c[i], cmd)

        print "Create libvirt network"
        create_libvirt_network(slave_ip_list_c[i], slave_rootpass_list_c[i], bridge_name)
        # Bring up bridge
        print "Bring up bridge"
        if i == 0:
            cmd = "ifconfig %s %s netmask %s up" % (bridge_name, bridge_ip, bridge_netmask)
        else:
            cmd = "ifconfig %s up" % bridge_name

        print cmd
        ssh_cmd(slave_ip_list_c[i], slave_rootpass_list_c[i], cmd)


def del_switch(master_ip, master_rootpass, slave_ip_list, slave_rootpass_list, bridge_name):
    slave_ip_list_c = list(slave_ip_list)
    slave_ip_list_c.insert(0, master_ip)
    slave_rootpass_list_c = list(slave_rootpass_list)
    slave_rootpass_list_c.insert(0, master_rootpass)
    bridge_name = "ovs-" + bridge_name
    for i in range(len(slave_ip_list)):
        # Exit if it see blank element
        if slave_ip_list_c[i] == '':
            return
        print slave_ip_list_c[i]
        print slave_rootpass_list_c[i]
        # Add ovs-bridge
        cmd = "ovs-vsctl del-br %s" % bridge_name
        print cmd
        ssh_cmd(slave_ip_list_c[i], slave_rootpass_list_c[i], cmd)
    	# Delete all ifcfg-ovs
        print "Delete network ifcfg"
        cmd = 'rm -f /etc/sysconfig/network-scripts/ifcfg-%s' % bridge_name
        print cmd
        ssh_cmd(slave_ip_list_c[i], slave_rootpass_list_c[i], cmd)
        print "Delete libvirt network"
        delete_libvirt_network(slave_ip_list_c[i], slave_rootpass_list_c[i], bridge_name)
    pass

# Add gre tunnel
def add_gre_tunnel(master_ip, master_rootpass,  slave_ip_list, slave_rootpass_list, network_name):
    print "Add gre tunnel"
    if slave_ip_list == [''] or len(slave_ip_list) == 0:
        return 0
    # Add gre tunnel to each host on master
    for host_ip in slave_ip_list:
        cmd = 'ovs-vsctl add-port ovs-%s gre-%s -- set interface gre-%s type=gre options:remote_ip=%s' % (network_name, network_name, network_name, host_ip)
        print cmd
        print ssh_cmd(master_ip, master_rootpass, cmd)
    # Add gre tunnel to master on each host
    for host_ip,host_rootpass in zip(slave_ip_list, slave_rootpass_list):
        cmd = 'ovs-vsctl add-port ovs-%s gre-%s -- set interface gre-%s type=gre options:remote_ip=%s' % (network_name, network_name, network_name, master_ip)
        print cmd
        print ssh_cmd(host_ip, host_rootpass, cmd)
    pass

def del_gre_tunnel(master_ip, master_rootpass, slave_ip_list, slave_rootpass_list, network_name):
    if slave_ip_list == [''] or len(slave_ip_list) == 0:
        return 0
     # Del gre tunnel to each host on master
    cmd = 'ovs-vsctl del-port ovs-%s gre-%s' % (network_name, network_name)
    for host_ip in slave_ip_list:
        print cmd
        print ssh_cmd(master_ip, master_rootpass, cmd)
    # Del gre tunnel to master on each host
    for host_ip,host_rootpass in zip(slave_ip_list, slave_rootpass_list):
        print cmd
        print ssh_cmd(host_ip, host_rootpass, cmd)
    pass

def permit_wan_access(master_ip, master_rootpass, bridge_name ):
    #sysctl -w net.ipv4.ip_forward=1
    cmd = 'echo "net.ipv4.ip_forward=1" > /etc/sysctl.d/ipv4_forward.conf'
    ssh_cmd(master_ip, master_rootpass, cmd)
    cmd = 'sysctl -w net.ipv4.ip_forward=1'
    ssh_cmd(master_ip, master_rootpass, cmd)
    cmd = 'iptables -t nat -A POSTROUTING -o mgmtnet -j MASQUERADE'
    ssh_cmd(master_ip, master_rootpass, cmd)
    cmd = 'service iptables save'
    ssh_cmd(master_ip, master_rootpass, cmd)
    #iptabl
    #iptables XXX MASQUERADE
    #service iptables save
    pass

# Functions for UI

def setup_ovs_network(master_ip, master_rootpass, slave_ip_list, slave_rootpass_list, network_name, gateway, netmask, dhcp_start, dhcp_end):
    #check_para()
    add_switch(master_ip, master_rootpass, slave_ip_list, slave_rootpass_list, network_name, gateway, netmask)
    setup_dhcp(master_ip, master_rootpass, network_name, gateway, dhcp_start, dhcp_end)
    add_gre_tunnel(master_ip, master_rootpass, slave_ip_list, slave_rootpass_list, network_name)
    #update_nic_profile()
    permit_wan_access(master_ip, master_rootpass, network_name)
    pass

def del_ovs_network(master_ip, master_rootpass, slave_ip_list, slave_rootpass_list, network_name):
    #check_libvirt_network_usage(master_ip, network_name)
    #update_nic_profile()
    del_gre_tunnel(master_ip, master_rootpass, slave_ip_list, slave_rootpass_list, network_name)
    del_switch(master_ip, master_rootpass, slave_ip_list, slave_rootpass_list, network_name)
    pass

def update_ovs_network(master_ip, master_rootpass, slave_ip_list, slave_rootpass_list, network_name, gateway, dhcp_start, dhcp_end):
    del_ovs_network(master_ip, master_rootpass, slave_ip_list, slave_rootpass_list, network_name):
    setup_ovs_network(master_ip, master_rootpass, slave_ip_list, slave_rootpass_list, network_name, gateway, netmask, dhcp_start, dhcp_end):
    pass


list_libvirt_networks("192.168.0.120","123456")
setup_ovs_network("192.168.0.119", "123456", ["192.168.0.120"], ["123456"], "network9", "10.10.9.1", "255.255.255.0", "10.10.9.10", "10.10.9.200")
del_ovs_network("192.168.0.223", "123456", [''], [''], "network9")
