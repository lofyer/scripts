#!/bin/bash
# I will be a service running at level 3

# disable selinux, or I'll not be able to refer libraries in the chroot env.
setenforce 0
INSTALL_ROOT=/install
INSTALL_BOOT=/install/boot
CHROOT_NET=chroot_net.sh
CHROOT_HOSTNAME=chroot_hostname.sh
CHROOT_ROOTPW=chroot_rootpw.sh
CHROOT_MISC=chroot_misc.sh
CHROOT_BOOTLOADER=chroot_bootloader.sh
# change STATUS to 1 before apply to the system
HD_STATUS=1
NET_STATUS=1
HOSTNAME_STATUS=1
ROOTPW_STATUS=1
MISC_STATUS=1
KVM_SUPPORT=false
# global var
ip=""
hostname=""
rootpw=""
use_dev=""
use_dev_mapper=""
use_dev_serial=""

# Test ipv4
is_valid_ipv4 () {
    local address=${1}
    local result=1
    if [[ "$address" =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        oldIFS="$IFS"
        IFS='.'
        ip=($address)
        IFS="$oldIFS"
        [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 \
            && ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
        result=$?
    fi
    echo $result
}

# ALL ENRTIES HERE

# get available hard drive.
set_hd () {
	devs_name=$(hal-find-by-capability --capability storage)
	let ALL_DEV_NUM=0
	all_dev=""
	all_dev_size=""

	for i in $devs_name
	do
		#echo $i
		#echo $(hal-get-property --udi $i --key storage.drive_type)
		if [[ "$(hal-get-property --udi $i --key storage.drive_type)" == "disk" ]]
		then
			all_dev="$all_dev $(hal-get-property --udi $i --key block.device)"
			all_dev_size="$all_dev_size $(hal-get-property --udi $i --key storage.size)"
			all_dev_mapper="$all_dev_mapper $(ls /dev/mapper | grep "$(hal-get-property --udi $i --key storage.serial)$")"
			all_dev_serial="$all_dev_serial $(hal-get-property --udi $i --key storage.serial)"
			let ALL_DEV_NUM+=1
		fi
	done

	if [[ $ALL_DEV_NUM == "0" ]]
	then
		echo -e "No hard drive found."
		return
	fi
	#echo "all_dev: "$all_dev
	#echo "all_dev_size: "$all_dev_size
	declare -a ALL_DEV=($all_dev)
	declare -a ALL_DEV_SIZE=($all_dev_size)
	declare -a ALL_DEV_MAPPER=($all_dev_mapper)
	declare -a ALL_DEV_SERIAL=($all_dev_serial)

	while true
	do
		echo -en '\E[37;32m'"\033[1mHard Drive Configuration - Select on which disk to install\n\033[0m"
		for ((i=1;i<=$(($ALL_DEV_NUM));i++))
		do
			echo -e "$i) Hard Drive: ${ALL_DEV[i-1]}    Size(MB): $((${ALL_DEV_SIZE[i-1]}/1024/1024))"
		done
		echo -e "$i) Exit"
		read -p "Select which hard drive to install: " answer_hd
		case $answer_hd in
			[1-$(($ALL_DEV_NUM))]) echo $(($answer_hd-1));;
			$i) return;;
			*) continue;;
		esac
		use_dev=${ALL_DEV[$(($answer_hd-1))]}
		use_dev_size=${ALL_DEV_SIZE[$(($answer_hd-1))]}
		use_dev_mapper=${ALL_DEV_MAPPER[$(($answer_hd-1))]}
		use_dev_serial=${ALL_DEV_SERIAL[$(($answer_hd-1))]}
		use_dev_size_MB=$(($use_dev_size/1024/1024))
		break
	done
# enough space?
# partion op.
	echo -en '\E[37;32m'"\033[1mHard Drive Configuration - Partion\n\033[0m"
	echo -e "Partion table:\n"$use_dev"1\t/boot\t200M"
	echo -e "Partion table:\n"$use_dev"2\tswap\t8192M"
	echo -e "Partion table:\n"$use_dev"3\t/\t"$(($use_dev_size_MB-200-8192))"M"
	read -p "Confirm?[N]" answer
	case $answer in
		[yY]) ;;
		*) return;;
	esac
	echo "Partioning..."
# Use /dev/sdX
	if [[ $use_dev_mapper == "" ]]
	then
		dd if=/dev/zero of=$use_dev bs=1024k count=1
		echo "mklabel"
		parted "$use_dev" -s "mklabel msdos"
		parted "$use_dev" -s "mkpart primary 0M 200M"
		parted "$use_dev" -s "mkpart primary 200M 8192M"
		parted "$use_dev" -s "mkpart primary 8392M -1"
		parted "$use_dev" -s "set 1 boot on"
# kpartx or partprobe here to sync partion label
		partprobe
		sleep 1
		mkfs.ext3 $use_dev"1"
# swap, no need to swapon
		mkswap $use_dev"2"
		mkfs.ext3 $use_dev"3"
		tune2fs -i 0 -c 0 $use_dev"1"
		tune2fs -i 0 -c 0 $use_dev"3"
		mkdir $INSTALL_ROOT
		mount -t ext3 $use_dev"3" $INSTALL_ROOT
		mkdir $INSTALL_BOOT
		mount -t ext3 $use_dev"1" $INSTALL_BOOT
		read -p "Mount done." -n 1
	else
# I use msdos label here, if gpt - along with gtpsync
		#dd if=/dev/zero of=$use_dev_mapper bs=1024k count=1
		echo "mklabel"
		parted "/dev/mapper/$use_dev_mapper" -s "mklabel msdos"
		parted "/dev/mapper/$use_dev_mapper" -s "mkpart primary 0M 200M"
		parted "/dev/mapper/$use_dev_mapper" -s "mkpart primary 200M 8192M"
		parted "/dev/mapper/$use_dev_mapper" -s "mkpart primary 8392M -1"
		parted "/dev/mapper/$use_dev_mapper" -s "set 1 boot on"
# kpartx or partprobe here to sync partion label
		partprobe
		sleep 1
		mkfs.ext3 "/dev/mapper/"$use_dev_mapper"p1"
# swap, no need to swapon
		mkswap "/dev/mapper/"$use_dev_mapper"p2"
		mkfs.ext3 "/dev/mapper/"$use_dev_mapper"p3"
		tune2fs -i 0 -c 0 "/dev/mapper/"$use_dev_mapper"p1"
		tune2fs -i 0 -c 0 "/dev/mapper/"$use_dev_mapper"p3"
		mkdir $INSTALL_ROOT
		mount -t ext3 "/dev/mapper/"$use_dev_mapper"p3" $INSTALL_ROOT
		mkdir $INSTALL_BOOT
		mount -t ext3 "/dev/mapper/"$use_dev_mapper"p1" $INSTALL_BOOT
		read -p "Mount done." -n 1
	fi
	HDSTATUS=$?
# unsquashfs here
	echo "Copying squashfs"
	cp /dev/.initramfs/live/LiveOS/squashfs.img $INSTALL_ROOT
	unsquashfs -d $INSTALL_ROOT/squashfs-root $INSTALL_ROOT/squashfs.img
	mkdir $INSTALL_ROOT/tmp-root
	mount -o loop $INSTALL_ROOT/squashfs-root/LiveOS/ext*.img $INSTALL_ROOT/tmp-root
	cp -arf $INSTALL_ROOT/tmp-root/boot/* $INSTALL_ROOT/boot
	cp -arf $INSTALL_ROOT/tmp-root/bin $INSTALL_ROOT/tmp-root/cgroup $INSTALL_ROOT/tmp-root/dev $INSTALL_ROOT/tmp-root/etc $INSTALL_ROOT/tmp-root/home $INSTALL_ROOT/tmp-root/lib* $INSTALL_ROOT/tmp-root/m* $INSTALL_ROOT/tmp-root/net $INSTALL_ROOT/tmp-root/opt $INSTALL_ROOT/tmp-root/proc $INSTALL_ROOT/tmp-root/r* $INSTALL_ROOT/tmp-root/s* $INSTALL_ROOT/tmp-root/tmp $INSTALL_ROOT/tmp-root/usr $INSTALL_ROOT/tmp-root/var $INSTALL_ROOT/
	sync
	read -p "Unsquashfs done." -n 1
	mount -o bind /dev $INSTALL_ROOT/dev
	mount -o bind /sys $INSTALL_ROOT/sys
	mount -o bind /proc $INSTALL_ROOT/proc
	if [[ $HDSTATUS == "1" ]]
	then
		echo -en '\E[37;31m'"\033[1mPartion failed. Press any key to continue.\n\033[0m"
		read -n 1
		return
	fi
	
	echo -en '\E[37;32m'"\033[1m\nDone. Press any key to continue.\n\033[0m"
	read -n 1
	return
}

set_ip (){
	if [[ $HD_STATUS == "1" ]]
	then
		echo -e "You should configure hard drive first.\n"
		read -n 1
		return
	fi
	echo -en '\E[37;32m'"\033[1mSelect which interface to be used:\n\033[0m"
	echo ""
	let ETH_NUM=0
	NICS=""
	udi_list=$(hal-find-by-capability --capability net.80203)
	if [ -n "$udi_list" ]; then
		for d in $udi_list; do
			if [[ ! "$(hal-get-property --udi $d --key net.physical_device)" =~ computer ]]; then
				NICS="$NICS $(hal-get-property --udi "$d" --key net.interface)"
				let ETH_NUM=$ETH_NUM+1
			fi
		done
	fi
	declare -a IFACE=($NICS)
	while true
	do
		for (( i=1;i<=$ETH_NUM;i++ ))
		do
	    	echo "$i) Interface: ${IFACE[$(($i-1))]}"
		done
		echo -e "$i) Exit"
		read which_iface_plus_one
		let which_iface=$which_iface_plus_one-1
		echo ""
		case $which_iface_plus_one in
			[1-$ETH_NUM]) echo -e "Setting ${IFACE[$which_iface]}\n";break;;
			$i) return;;
			*) echo -e "You should pick up an interface.";continue;;
		esac
	done
	
	while true
	do
		read -p "Input IP address: " ip
		if [[ $(is_valid_ipv4 $ip) == 1 ]]
			then 
				echo "Invalid ip!";continue
			else
				break
		fi
	done
	while true
	do
		read -p "Input netmask[255.255.255.0]: " netmask
		if [[ $netmask == "" ]]
			then netmask="255.255.255.0"
		fi
		if [[ $(is_valid_ipv4 $netmask) == 1 ]]
			then 
				echo "Invalid netmask!";continue
			else
				break
		fi
	done
	while true
	do
		read -p "Input gateway address: " gateway
		if [[ $(is_valid_ipv4 $gateway) == 1 ]]
			then 
				echo "Invalid gateway address!";continue
			else
				break
		fi
	done
	while true
	do
		read -p "Input dns address, if none, just press Enter: " dns
		if [[ $dns == "" ]]
		then
			break
		fi
		if [[ $(is_valid_ipv4 $gateway) == 1 ]]
		then 
			echo "Invalid dns address!";continue
		else
			break
		fi
	done
	echo -e "Here's you network configuration\nIP: $ip\nGATEWAY: $gateway\nNETMASK: $netmask\nDNS: $dns\n"
	cat > /etc/sysconfig/network-scripts/ifcfg-${IFACE[$which_iface]}<< EOF_IFCFG
DEVICE=${IFACE[$which_iface]}
ONBOOT=yes
IPADDR=$ip
NETMASK=$netmask
GATEWAY=$gateway
DNS1=$dns
EOF_IFCFG
	chkconfig NetworkManager off
	chkconfig network on
	service NetworkManager stop
	service network restart

	ping -c 1 -w 4 -I ${IFACE[$which_iface]} $gateway
	if [[ $? == "1" ]]
	then
		echo "${IFACE[$which_iface]} seems to be wrongly configured, continue?[N]"
   	 	read  -n 1 answer_iface_fail
		echo ""
	    case $answer_iface_fail in
   	 	    [yY]) continue;;
   	     	* ) rm /etc/sysconfig/network-scripts/ifcfg-${IFACE[$which_iface]};set_ip;return;;
	    esac
	fi
# chroot execute CHROOT_NET
	cp -L /etc/sysconfig/network-scripts/ifcfg-${IFACE[$which_iface]} $INSTALL_ROOT/etc/sysconfig/network-scripts/ifcfg-${IFACE[$which_iface]}
	cat > $INSTALL_ROOT/$CHROOT_NET << EOF_CHROOT_NET
chkconfig NetworkManager off
chkconfig network on
#service NetworkManager stop
#service network restart
EOF_CHROOT_NET
	chmod +x $INSTALL_ROOT/$CHROOT_NET
	chroot $INSTALL_ROOT /bin/bash $CHROOT_NET
	echo -en '\E[37;32m'"\033[1m\nDone. Press any key to continue.\n\033[0m"
	read -n 1
	NET_STATUS=0
	clear
	return
}

set_hostname () {
	if [[ $ip == "" ]]
	then
		echo "You should set IP first."
		read -n 1
		return ;
	fi
	local answer
	while true
	do
		read -p "Input hostname you want to set[engine.mycloud.org]: " hostname
		if [[ $hostname == "" ]]
			then
				hostname="engine.mycloud.org"
				break
		fi
		echo -e "Is $hostname right?[Y]"
		read -n 1 answer 
		echo ""
		case $answer in
   			[nN] ) continue;;
	   		* ) break;;
		esac
	done
	# Set hostname
	hostname $hostname
	sed -i '/$ip/d' /etc/hosts
	echo $ip $(hostname)
	cat >> /etc/hosts << EOF_HOSTS
$ip $(hostname)
EOF_HOSTS
	if [[ $hostname == $(hostname -f) ]]
	then
		echo -en '\E[37;32m'"\033[1mSet hostname success!\n\033[0m"
		HOSTNAME_STATUS=0
		read -n 1
		return 0
	else
		echo -en '\E[37;32m'"\033[1mSet hostname failed!\n\033[0m"
		read -n 1
		return 1
	fi
}

# set OS password
set_ospasswd () {
	while true
    do
        read  -p "OS root password: " rootpw
        read  -p "Confirm password: " rootpwc
        if [[ $rootpw == $rootpwc ]] && { [[ $rootpw != "" ]] && [[ ${#rootpw} -gt "5" ]]; }
        then
            break
        else
			echo -en '\E[37;31m'"\033[1m\nInvalid password, do it again.\n\033[0m"
            continue
        fi
    done
	echo -en '\E[37;32m'"\033[1m\nDone. Press any key to continue.\n\033[0m"
	ROOTPW_STATUS=0
	read -n 1
	clear
	return
}

# misc configuration, like allinone? admin password?
# since no interactive interface is allowed, we should detect kvm_support in advance
set_misc () {
	if [[ $HD_STATUS == "1" || $HOSTNAME_STATUS == "1" || $ROOTPW_STATUS == "1" ]]
	then
		echo -e "You should configure hard drive, hostname and root password at first."
		read -n 1
		return
	fi
	grepvmx=$(grep --color "vmx" /proc/cpuinfo)
    let kvm_intel=$?
    grepsvm=$(grep --color "svm" /proc/cpuinfo)
    let kvm_amd=$?
    let kvm_checksum=$kvm_intel*1+$kvm_amd*3
    #echo "kvm check sum" $kvm_checksum
    case $kvm_checksum in
        4) echo -e "\nThis CPU does not support KVM.\nNo vdsm will be installed on this host";KVM_SUPPORT=false;;
        3) modprobe kvm;modprobe kvm-intel;KVM_SUPPORT=true;;
        1) modprobe kvm;modprobe kvm-amd;KVM_SUPPORT=true;;
        *) ;;
    esac
	while [[ $KVM_SUPPORT == true ]] 
	do
		read -p "Configure vdsm on this host (all-in-one)?[Y] " answer_vdsm
		case $answer_vdsm in
			[nN]) echo "I will not configure vdsm on this host.";VDSM=true;break;;
			*) echo "VDSM will be set on this host.";VDSM=false;break;;
		esac
	done

	while true
    do
        read -s -p "Engine admin password: " adminpass
        echo ""
        read -s -p "Confirm password: " adminpassc
        if [[ $adminpass == $adminpassc && $adminpass != "" ]]
        then
            break;
        else
            echo -e "\nInvalid password."
            continue
        fi
    done

	echo -en '\E[37;32m'"\033[1m\nDone. Press any key to continue.\n\033[0m"
	read -n 1
	clear
	MISC_STATUS=0
	return
}

begin_install () {
	if [[ $(($HD_STATUS+$NET_STATUS+$HOSTNAME_STATUS+$MISC_STATUS)) -gt "0" ]]
	then
		echo "You should configure all the 1-5 items at first."
		read -n 1
		clear;return
	fi

# chroot execute CHROOT_HOSTNAME
	cat > $INSTALL_ROOT/$CHROOT_HOSTNAME << EOF_CHROOT_HOSTNAME
	hostname $hostname
	sed -i '/$ip/d' /etc/hosts
EOF_CHROOT_HOSTNAME

	chmod +x $INSTALL_ROOT/$CHROOT_HOSTNAME
	chroot $INSTALL_ROOT /bin/bash $CHROOT_HOSTNAME

	cat >> $INSTALL_ROOT/etc/hosts << EOF_HOSTS
$ip $(hostname)
EOF_HOSTS

# chroot execute CHROOT_ROOTPW
	cat > $INSTALL_ROOT/$CHROOT_ROOTPW << EOF_CHROOT_ROOTPW
echo -e "root:$rootpw" | chpasswd
EOF_CHROOT_ROOTPW
	chmod +x $INSTALL_ROOT/$CHROOT_ROOTPW
	chroot $INSTALL_ROOT /bin/bash $CHROOT_ROOTPW

# chroot execute CHROOT_MISC
	if [[ $KVM_SUPPORT == true && $VDSM == true ]]
	then
		cat > $INSTALL_ROOT/tmp/engine-setup.answer << EOF_ANSWER
[environment:default]
OSETUP_RPMDISTRO/enableUpgrade=bool:False
OVESETUP_CORE/engineStop=none:None
OVESETUP_DIALOG/confirmSettings=bool:True
OVESETUP_DB/database=str:engine
OVESETUP_DB/fixDbViolations=none:None
OVESETUP_DB/secured=bool:False
OVESETUP_DB/securedHostValidation=bool:False
OVESETUP_DB/host=str:localhost
OVESETUP_DB/user=str:engine
OVESETUP_DB/password=str:virtfan
OVESETUP_DB/port=int:5432
OVESETUP_SYSTEM/nfsConfigEnabled=bool:True
OVESETUP_PKI/organization=str:$(dnsdomainname)
OVESETUP_CONFIG/isoDomainName=str:ISO_DOMAIN
OVESETUP_CONFIG/isoDomainMountPoint=str:/virtfan/iso
OVESETUP_CONFIG/adminPassword=str:$adminpass
OVESETUP_CONFIG/applicationMode=str:virt
OVESETUP_CONFIG/firewallManager=str:None
OVESETUP_CONFIG/websocketProxyConfig=none:None
OVESETUP_CONFIG/fqdn=str:$(hostname)
OVESETUP_CONFIG/storageType=str:nfs
OVESETUP_PROVISIONING/postgresProvisioningEnabled=bool:True
OVESETUP_APACHE/configureRootRedirection=bool:True
OVESETUP_APACHE/configureSsl=bool:True
OSETUP_RPMDISTRO/requireRollback=none:None
OSETUP_RPMDISTRO/enableUpgrade=none:None
OVESETUP_AIO/configure=bool:True
OVESETUP_AIO/storageDomainDir=str:/virtfan/images
OVESETUP_AIO/rootPassword=str:$rootpw
OVESETUP_AIO/storageDomainName=str:LocalStorage
EOF_ANSWER
	else
		cat > $INSTALL_ROOT/tmp/engine-setup.answer << EOF_ANSWER
# action=setup
[environment:default]
OVESETUP_CORE/engineStop=none:None
OVESETUP_DIALOG/confirmSettings=bool:True
OVESETUP_DB/database=str:engine
OVESETUP_DB/fixDbViolations=none:None
OVESETUP_DB/secured=bool:False
OVESETUP_DB/host=str:localhost
OVESETUP_DB/user=str:engine
OVESETUP_DB/securedHostValidation=bool:False
OVESETUP_DB/password=str:virtfan
OVESETUP_DB/port=int:5432
OVESETUP_SYSTEM/nfsConfigEnabled=bool:True
OVESETUP_SYSTEM/memCheckEnabled=bool:False
OVESETUP_PKI/organization=str:$(dnsdomainname)
OVESETUP_CONFIG/isoDomainName=str:ISO_DOMAIN
OVESETUP_CONFIG/isoDomainMountPoint=str:/virtfan/iso
OVESETUP_CONFIG/adminPassword=str:admin
OVESETUP_CONFIG/applicationMode=str:virt
OVESETUP_CONFIG/firewallManager=none:None
OVESETUP_CONFIG/websocketProxyConfig=none:None
OVESETUP_CONFIG/fqdn=str:$(hostname)
OVESETUP_CONFIG/storageType=str:nfs
OVESETUP_PROVISIONING/postgresProvisioningEnabled=bool:True
OVESETUP_APACHE/configureRootRedirection=bool:True
OVESETUP_APACHE/configureSsl=bool:True
OVESETUP_AIO/configure=none:None
OVESETUP_AIO/storageDomainDir=none:None
EOF_ANSWER
	fi

	cat > $INSTALL_ROOT/$CHROOT_MISC << EOF_CHROOT_MISC
echo "yes" | engine-setup --offline --config=/tmp/engine-setup.answer
EOF_CHROOT_MISC
	chmod +x $INSTALL_ROOT/$CHROOT_MISC
	chroot $INSTALL_ROOT /bin/bash $CHROOT_MISC

# install bootloader, from oVirt-node or make a new one?
# mix them..
# USE UUID INSTEAD OF /dev/sdX
	root_uuid=""
	part_id=$(find /dev/disk/by-id/* -name "*uuid*" -name "*$use_dev_serial*" -name "*part3*")
	for i in $(find /dev/disk/by-uuid/*)
	do
		if [[ $(readlink $i) == $(readlink $part_id) ]]
		then
			root_uuid=$i
			break
		fi
	done

	cat > $INSTALL_ROOT/$CHROOT_BOOTLOADER << EOF_CHROOT_BOOTLOADER
grep -v rootfs /proc/mounts > /etc/mtab
	if [[ $use_dev_mapper == "" ]]
	then
		#echo "(hd0) $use_dev" > /boot/grub/device.map
		grub-install $use_dev
	else
		echo "(hd0) /dev/mapper/$use_dev_mapper" > /boot/grub/device.map
		grub-install /dev/mapper/$use_dev_mapper
	fi
#	grub --device-map=$INSTALL_BOOT/grub/device.map << EOF
#root (hd0,0)
#setup --prefix=/grub (hd0)
#EOF
	mkinitrd /boot/initramfs-\$(uname -r) \$(uname -r)
	cat > /boot/grub/grub.conf << EOF_GRUB
timeout=5
title Virtfan Engine
	root (hd0,0)
	kernel /vmlinuz-\$(uname -r) root=$root_uuid elevator=deadline
	initrd /initramfs-\$(uname -r)
EOF_GRUB
EOF_CHROOT_BOOTLOADER
	chmod +x $INSTALL_ROOT/$CHROOT_BOOTLOADER
	chroot $INSTALL_ROOT /bin/bash $CHROOT_BOOTLOADER

# after work
sed -i 's/SELINUX=enforcing/SELINUX=permissive/' $INSTALL_ROOT/etc/selinux/config
	rm $CHROOT_NET
	rm $CHROOT_HOSTNAME
	rm $CHROOT_ROOTPW
	rm $CHROOT_MISC
	rm $CHROOT_SETUP
	rm $CHROOT_BOOTLOADER

	umount $INSTALL_ROOT/tmp-root/
	umount $INSTALL_ROOT/squashfs-root/
	rm -fr $INSTALL_ROOT/tmp-root $INSTALL_ROOT/squashfs-root

	umount $INSTALL_ROOT/proc
	umount $INSTALL_ROOT/sys
	umount $INSTALL_ROOT/dev
	umount $INSTALL_ROOT/boot
	umount $INSTALL_ROOT
	sync;sync;sync;sync;reboot
}

# main

reset
# disable ^C ^D
trap '' 2 20
echo -en '\E[37;32m'"\033[1mWelcome to Virtfan installation, select an item below to configure the engine.\n\033[0m"

while true
do
	echo -en '\E[37;32m'"\033[1mMain menu\n\033[0m"
	echo -e "1) Configure Hard Drive\t2) Configure Network"
	echo -e "3) Configure Hostname\t4) OS Root Password"
	echo -e "5) Misc Configuration\t6) Install and Reboot"
	echo -e "7) Return to Shell"
	read -p "Choice: " answer_main
		case $answer_main in
			1) clear;echo -en '\E[37;32m'"\033[1mHard Drive Configuration\n\033[0m";set_hd;clear;continue;;
			2) clear;echo -en '\E[37;32m'"\033[1mNetwork Configuration\n\033[0m";set_ip;clear;continue;;
			3) clear;echo -en '\E[37;32m'"\033[1mHostname Configuration\n\033[0m";set_hostname;clear;continue;;
			4) clear;echo -en '\E[37;32m'"\033[1mSet Root Password\n\033[0m";set_ospasswd;clear;continue;;
			5) clear;echo -en '\E[37;32m'"\033[1mMisc Configuration\n\033[0m";set_misc;clear;continue;;
			6) clear;echo -en '\E[37;32m'"\033[1mInstall to Hard Drive\n\033[0m";begin_install;clear;continue;;
			7) bash;clear;continue;;
			*) echo -e "Input a number from 1 to 7";continue;;
		esac
done
