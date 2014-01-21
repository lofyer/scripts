#!/bin/bash
# This is gentoo quick install scripts, except fdisk
mkdir /install
mount /dev/sdb2 /install
cd /install
wget stage3
tar xjpf stage3

mkdir boot
mount /dev/sdb1 /boot

cd usr
wget portage
tar xjpf portage

cd /install
mount /dev/sdb5 home
mount -o bind /dev dev
mount -o bind /sys sys
mount -o bind /proc proc
cp -L /etc/resolv.conf etc/resolv.conf

chroot /install

cat > /install/setup.sh << EOF
source /etc/profile
echo "127.0.0.1 rex.lofyer.org rex localhost localhost.localdomain" > /etc/hosts
echo 'HOSTNAME="rex"' > /etc/hostname
cat >> /etc/portage/make.conf << EOF_MAKE
GENTOO_MIRRORS=""
FETCH_COMMAND=""
RESUME_COMMAND=""
LINGUAS="zh_CN"
EOF_MAKE
EOF
