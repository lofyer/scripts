#!/bin/bash
echo "Manually change your SELinux to enforcing and targeted"

yum install -y wget git net-tools bind-utils iptables-services bridge-utils bash-completion epel-release
yum localinstall http://mirrors.aliyun.com/epel/7/x86_64/a/ansible1.9-1.9.4-2.el7.noarch.rpm
sed -i -e "s/^enabled=1/enabled=0/" /etc/yum.repos.d/epel.repo
yum -y --enablerepo=epel install ansible pyOpenSSL docker

sed -i "s/^OPTIONS='--selinux-enabled'/OPTIONS='--selinux-enabled --insecure-registry 172.30.0.0/16'/" /etc/sysconfig/docker

# Setup docker storage
cat <<EOF > /etc/sysconfig/docker-storage-setup
DEVS=/dev/vdc
VG=docker-vg
EOF
docker-storage-setup
systemctl enable docker
systemctl stop docker
rm -rf /var/lib/docker/*
systemctl restart docker

ssh-keygen
for host in openshift-master.example.com openshift-node.example.com
do
    ssh-copy-id $host
done

cd ~
git clone https://github.com/openshift/openshift-ansible
cd openshift-ansible
# Check
ansible-playbook playbooks/byo/openshift_facts.yml
# Install
#ansible-playbook playbooks/byo/config.yml
# Uninstall
#ansible-playbook [-i /path/to/file] playbooks/adhoc/uninstall.yml

# Setup Registry

# Setup Route
