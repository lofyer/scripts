lang en_US.UTF-8
keyboard us
timezone US/Eastern
auth --useshadow --enablemd5
selinux --enforcing
firewall --disabled

repo --name=a-base    --baseurl=http://mirror.centos.org/centos/5/os/$basearch
repo --name=a-updates --baseurl=http://mirror.centos.org/centos/5/updates/$basearch
#repo --name=a-extras  --baseurl=http://mirror.centos.org/centos/5/extras/$basearch
repo --name=a-live    --baseurl=http://www.nanotechnologies.qc.ca/propos/linux/centos-live/$basearch/live

%packages
bash
kernel
syslinux
passwd
policycoreutils
chkconfig
authconfig
rootfiles
comps-extras
xkeyboard-config
