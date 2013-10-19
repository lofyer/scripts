########################################################################
#
# sl63-live-base.ks
#
# Defines the basics for all kickstarts of sl63-live
# Kickstarts including this template can override these settings
#
########################################################################

lang en_US.UTF-8
keyboard us
timezone US/Eastern
auth --useshadow --enablemd5
selinux --enforcing
firewall --enabled --service=mdns

# SL repositories
repo --name=base      --baseurl=http://ftp.scientificlinux.org/linux/scientific/6.3/$basearch/os/
repo --name=security  --baseurl=http://ftp.scientificlinux.org/linux/scientific/6.3/$basearch/updates/security/

# or use a mirror close to you
#repo --name=base      --baseurl=http://mirror.switch.ch/ftp/mirror/scientificlinux/6.3/$basearch/os/
#repo --name=security  --baseurl=http://mirror.switch.ch/ftp/mirror/scientificlinux/6.3/$basearch/updates/security/

# fastbugs is disabled
#repo --name=fastbugs  --baseurl=http://ftp.scientificlinux.org/linux/scientific/6.3/$basearch/updates/fastbugs/

xconfig --startxonboot
services --enabled=NetworkManager --disabled=network,sshd


########################################################################
#
# Basic software packages
#
########################################################################

%packages
syslinux
kernel

# basic software groups
@base
# package added to @base
squashfs-tools
@core
@graphical-admin-tools
@network-file-system-client
@network-tools
@x11

# remote-desktop-clients
rdesktop
tsclient

# other usefull packages
busybox
mailx
memtest86+
livecd-tools
fuse
wpa_supplicant
dracut-network
yum-plugin-fastestmirror

# livecd bits to set up the livecd and be able to install
anaconda
device-mapper-multipath
isomd5sum

%end


########################################################################
#
#  LiveCD post install in chroot 
#
########################################################################
%post

#***********************************************************************
# Create LiveCD configuration file and LiveCD functions
#***********************************************************************

cat > /etc/livesys.conf << 'EOF_livesysconf'
#--------------------------------------------------------------------
# Configuration file for LiveCD
#--------------------------------------------------------------------

# default LiveCD user
LIVECD_DEF_USER="liveuser"

# delay in seconds before auto login
LOGIN_DELAY=15

# Services which are off (not running) on the LiveCD
SERVICES_OFF="mdmonitor setroubleshoot auditd crond atd readahead_early \
              readahead_later kdump microcode_ctl openct pcscd postfix  \
	      yum-updatesd"

# Services which should be on, but are not on per default
SERVICES_ON=""

EOF_livesysconf


cat > /etc/init.d/livesys.functions << 'EOF_livesysfunctions'
#--------------------------------------------------------------------
# livesys functions
#--------------------------------------------------------------------

# egrep_o is a replacement for "egrep -o". It prints only the last matching text
egrep_o() {
   cat | egrep "$1" | sed -r "s/.*($1).*/\\1/"
}

# boot parameter
cmdline_parameter() {
   CMDLINE=/proc/cmdline
   cat "$CMDLINE" | egrep_o "(^|[[:space:]]+)$1(\$|=|[[:space:]]+)" | egrep_o "$1"
}

# boot parameter value
cmdline_value()
{
   CMDLINE=/proc/cmdline
   cat "$CMDLINE" | egrep_o "(^|[[:space:]]+)$1=([^[:space:]]+)" | egrep_o "=.*" | cut -b 2- | tail -n 1
}

exists() {
    which $1 >/dev/null 2>&1 || return
    $*
}

EOF_livesysfunctions


#***********************************************************************
# Create /root/post-install
# Must change "$" to "\$" and "`" to "\`" to avoid shell quoting
#***********************************************************************

cat > /root/post-install << EOF_post
#!/bin/bash

#***********************************************************************
# Create the livesys init script - /etc/rc.d/init.d/livesys
#***********************************************************************

echo "Creating the livesys init script - livesys"

cat > /etc/rc.d/init.d/livesys << EOF_initscript
#!/bin/bash
#
# live: Init script for live image
#
# chkconfig: 345 00 99
# description: Init script for live image.

. /etc/init.d/functions
. /etc/livesys.conf
. /etc/init.d/livesys.functions

# exit if not running from LiveCD
if [ ! "\\\$( cmdline_parameter liveimg )" ] || [ "\\\$1" != "start" ]; then
    exit 0
fi

[ -e /.liveimg-configured ] && configdone=1

touch /.liveimg-configured

### read boot parameters out of /proc/cmdline

# hostname
hostname=\\\$( cmdline_value hostname )

# afs cell
CELL=\\\$( cmdline_value cell )

# services to turn on / off
SERVICEON=\\\$( cmdline_value serviceon )
SERVICEOFF=\\\$( cmdline_value serviceoff )

# cups server
CUPS=\\\$( cmdline_value cups )

# password
PW=\\\$( cmdline_value pw )
[ ! \\\$PW ] && PW=\\\$( cmdline_value passwd )

# set livecd user
LIVECD_USER=\\\$( cmdline_value user )
[ ! "\\\$LIVECD_USER" ] && LIVECD_USER=\\\$LIVECD_DEF_USER


### mount live image
if [ -b \\\`readlink -f /dev/live\\\` ]; then
   mkdir -p /mnt/live
   mount -o ro /dev/live /mnt/live 2>/dev/null || mount /dev/live /mnt/live
fi

livedir=\\\$( cmdline_value live_dir )
[ ! "\\\$livedir" ] && livedir="LiveOS"

### enable swaps unless requested otherwise
swaps=\\\`blkid -t TYPE=swap -o device\\\`
if [ ! "\\\$( cmdline_parameter noswap )" ] && [ -n "\\\$swaps" ] ; then
  for s in \\\$swaps ; do
    action "Enabling swap partition \\\$s" swapon \\\$s
  done
fi
if [ ! "\\\$( cmdline_parameter noswap )" ] && [ -f /mnt/live/\\\${livedir}/swap.img ] ; then
  action "Enabling swap file" swapon /mnt/live/\\\${livedir}/swap.img
fi

### functions for persisten Home 
mountPersistentHome() {
  # support label/uuid
  if [ "\\\${homedev##LABEL=}" != "\\\${homedev}" -o "\\\${homedev##UUID=}" != "\\\${homedev}" ]; then
    homedev=\\\`/sbin/blkid -o device -t "\\\$homedev"\\\`
  fi

  # if we're given a file rather than a blockdev, loopback it
  if [ "\\\${homedev##mtd}" != "\\\${homedev}" ]; then
    # mtd devs don't have a block device but get magic-mounted with -t jffs2
    mountopts="-t jffs2"
  elif [ ! -b "\\\$homedev" ]; then
    loopdev=\\\`losetup -f\\\`
    if [ "\\\${homedev##/mnt/live}" != "\\\${homedev}" ]; then
      action "Remounting live store r/w" mount -o remount,rw /mnt/live
    fi
    losetup \\\$loopdev \\\$homedev
    homedev=\\\$loopdev
  fi

  # if it's encrypted, we need to unlock it
  if [ "\\\$(/sbin/blkid -s TYPE -o value \\\$homedev 2>/dev/null)" = "crypto_LUKS" ]; then
    echo
    echo "Setting up encrypted /home device"
    plymouth ask-for-password --command="cryptsetup luksOpen \\\$homedev EncHome"
    homedev=/dev/mapper/EncHome
  fi

  # and finally do the mount
  mount \\\$mountopts \\\$homedev /home
  # if we have /home under what's passed for persistent home, then
  # we should make that the real /home.  useful for mtd device on olpc
  if [ -d /home/home ]; then mount --bind /home/home /home ; fi
  [ -x /sbin/restorecon ] && /sbin/restorecon /home
  if [ -d /home/\\\$LIVECD_USER ]; then USERADDARGS="-M" ; fi
}

findPersistentHome() {
  for arg in \\\`cat /proc/cmdline\\\` ; do
    if [ "\\\${arg##persistenthome=}" != "\\\${arg}" ]; then
      homedev=\\\${arg##persistenthome=}
      return
    fi
  done
}

if strstr "\\\`cat /proc/cmdline\\\`" persistenthome= ; then
  findPersistentHome
elif [ -e /mnt/live/\\\${livedir}/home.img ]; then
  homedev=/mnt/live/\\\${livedir}/home.img
fi

### if we have a persistent /home, then we want to go ahead and mount it
if ! strstr "\\\`cat /proc/cmdline\\\`" nopersistenthome && [ -n "\\\$homedev" ] ; then
  action "Mounting persistent /home" mountPersistentHome
fi

### make it so that we don't do writing to the overlay for things which
### are just tmpdirs/caches
mount -t tmpfs -o mode=0755 varcacheyum /var/cache/yum
mount -t tmpfs tmp /tmp
mount -t tmpfs vartmp /var/tmp
[ -x /sbin/restorecon ] && /sbin/restorecon /var/cache/yum /tmp /var/tmp >/dev/null 2>&1

### set afs cell if given by boot parameter
if [ "\\\$CELL" ]; then
    [ -e /usr/vice/etc/ThisCell ] && echo \\\$CELL > /usr/vice/etc/ThisCell
fi

### set cups server
if [ "\\\$CUPS" ]; then
    if [ -e /etc/cups/client.conf ]; then
        sed -i "s|.*ServerName .*|ServerName  \\\$CUPS|" /etc/cups/client.conf
        grep -q ServerName /etc/cups/client.conf || echo "ServerName  \\\$CUPS" >> /etc/cups/client.conf 
    fi
fi

### set the LiveCD hostname
[ ! "\\\$hostname" ] && hostname="livecd.localdomain"
sed -i -e "s|HOSTNAME=.*|HOSTNAME=\\\$hostname|g" /etc/sysconfig/network
/bin/hostname \\\$hostname

#-----------------------------------------------------------------------
# EXIT here if LiveCD has already been configured         
# happens if you start the LiveCD with persistent changes 
#-----------------------------------------------------------------------

[ "\\\$configdone" ] && exit 0

### turn off services, which are not useful on LiveCD, to preserve resources
if [ "\\\$SERVICES_OFF" ]; then
    for service in \\\$SERVICES_OFF ; do
        [ -f /etc/init.d/\\\$service ] && chkconfig \\\$service off 2>/dev/null
    done
fi

### turn on services, which are off by default
if [ "\\\$SERVICES_ON" ]; then
    for service in \\\$SERVICES_ON ; do
        [ -f /etc/init.d/\\\$service ] && chkconfig \\\$service ofn  2>/dev/null
    done
fi

### services off, from command line parameter (turn it off once again)
if [ "\\\$SERVICEOFF" ]; then
    for service in \\\$( echo "\\\$SERVICEOFF" | tr ':' ' ' ); do
        [ -f /etc/init.d/\\\$service ] && chkconfig \\\$service off 2>/dev/null
    done
fi

# services on, from command line parameter (turn it ofn once again)
if [ "\\\$SERVICEON" ]; then
    for service in \\\$( echo "\\\$SERVICEON" | tr ':' ' ' ); do
        [ -f /etc/init.d/\\\$service ] && chkconfig \\\$service on  2>/dev/null
    done
fi

### fix various bugs and issues
# unmute sound card
exists alsaunmute 0 2> /dev/null

# turn off firstboot for livecd boots
echo "RUN_FIRSTBOOT=NO" > /etc/sysconfig/firstboot

# start afs with option -memcache (gets a kernel panic on some system - do not use it for the moment)
# [ -e /etc/sysconfig/afs ] && sed -i "s|^OPTIONS=.*|OPTIONS=\"-memcache\"|" /etc/sysconfig/afs

# Stopgap fix for RH #217966; should be fixed in HAL instead
touch /media/.hal-mtab

### create the LiveCD default user
# add default user with no password
/usr/sbin/useradd -c "LiveCD default user" \\\$LIVECD_USER
/usr/bin/passwd -d \\\$LIVECD_USER > /dev/null
# give default user sudo privileges
# echo "\\\$LIVECD_USER     ALL=(ALL)     NOPASSWD: ALL" >> /etc/sudoers

### set password
if [ "\\\$PW" ]; then
    echo \\\$PW | passwd --stdin root >/dev/null
    echo \\\$PW | passwd --stdin \\\$LIVECD_USER >/dev/null
fi

### enable auto-login
if [ ! "\\\$( cmdline_parameter noautologin )" ]; then
    cat >> /etc/gdm/custom.conf << FOE
[daemon]
TimedLoginEnable=true
TimedLogin=LIVECD_USER
TimedLoginDelay=\\\$LOGIN_DELAY
FOE
    sed -i "s|LIVECD_USER|\\\$LIVECD_USER|" /etc/gdm/custom.conf
fi

### add keyboard and display configuration utilities to the desktop
mkdir -p /home/\\\$LIVECD_USER/Desktop >/dev/null
cp /usr/share/applications/gnome-keyboard.desktop           /home/\\\$LIVECD_USER/Desktop/
cp /usr/share/applications/gnome-display-properties.desktop /home/\\\$LIVECD_USER/Desktop/

### disable screensaver locking
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t bool   /apps/gnome-screensaver/lock_enabled "false" >/dev/null

### don't do packagekit checking by default
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t int /apps/gnome-packagekit/update-icon/frequency_get_updates "0" >/dev/null
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t string /apps/gnome-packagekit/update-icon/frequency_get_updates never >/dev/null
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t string /apps/gnome-packagekit/update-icon/frequency_get_upgrades never >/dev/null
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t string /apps/gnome-packagekit/update-icon/frequency_refresh_cache never >/dev/null
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t bool /apps/gnome-packagekit/update-icon/notify_available false >/dev/null
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t bool /apps/gnome-packagekit/update-icon/notify_distro_upgrades false >/dev/null
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t bool /apps/gnome-packagekit/enable_check_firmware false >/dev/null
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t bool /apps/gnome-packagekit/enable_check_hardware false >/dev/null
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t bool /apps/gnome-packagekit/enable_codec_helper false >/dev/null
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t bool /apps/gnome-packagekit/enable_font_helper false >/dev/null
gconftool-2 --direct --config-source=xml:readwrite:/etc/gconf/gconf.xml.defaults -s -t bool /apps/gnome-packagekit/enable_mime_type_helper false >/dev/null

### start system-config-firewall with su 
#  (bugfix: system-config-firewall does not work when root has no password)
sed -i "s|^Exec=.*|Exec=su - -c /usr/bin/system-config-firewall|" /usr/share/applications/system-config-firewall.desktop
sed -i "s|^Terminal=.*|Terminal=true|"                            /usr/share/applications/system-config-firewall.desktop

### don't use prelink on a running live image
sed -i 's/PRELINKING=yes/PRELINKING=no/' /etc/sysconfig/prelink &>/dev/null


###-----------------------------------------------------------------------
# detecting disk partitions and logical volumes (disabled by default)
# use boot parameter automount to enable it
###-----------------------------------------------------------------------

CreateDesktopIconHD()
{
cat > /home/\\\$LIVECD_USER/Desktop/Local\ hard\ drives.desktop << EOF_HDicon
[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Link
Name=Local hard drives
Name[en_US]=Local hard drives
Name[fr_CA]=Disques durs locaux
URL=/mnt/disc
Icon=/usr/share/icons/gnome/32x32/devices/gnome-dev-harddisk.png
EOF_HDicon

chmod 755 /home/\\\$LIVECD_USER/Desktop/Local\ hard\ drives.desktop
}

CreateDesktopIconLVM()
{
mkdir -p /home/\\\$LIVECD_USER/Desktop >/dev/null

cat > /home/\\\$LIVECD_USER/Desktop/Local\ logical\ volumes.desktop << EOF_LVMicon
[Desktop Entry]
Encoding=UTF-8
Version=1.0
Type=Link
Name=Local logical volumes
Name[en_US]=Local logical volumes
Name[fr_CA]=Volumes logiques locaux
URL=/mnt/lvm
Icon=/usr/share/icons/gnome/32x32/devices/gnome-dev-harddisk.png
EOF_LVMicon

chmod 755 /home/\\\$LIVECD_USER/Desktop/Local\ logical\ volumes.desktop
}

# mount disk partitions if 'automount' is given as a boot option
if [ "\\\$( cmdline_parameter automount )" ]; then
	MOUNTOPTION="rw"
	HARD_DISKS=\\\`egrep "[sh]d.\\\$" /proc/partitions | tr -s ' ' | sed 's/^  *//' | cut -d' ' -f4\\\`

	echo "Mounting hard disk partitions... "
	for DISK in \\\$HARD_DISKS; do
	    # Get the device and system info from fdisk (but only for fat and linux partitions).
	    FDISK_INFO=\\\`fdisk -l /dev/\\\$DISK | tr [A-Z] [a-z] | egrep "fat|linux" | egrep -v "swap|extended|lvm" | sed 's/*//' | tr -s ' ' | tr ' ' ':' | cut -d':' -f1,6-\\\`
	    for FDISK_ENTRY in \\\$FDISK_INFO; do
		PARTITION=\\\`echo \\\$FDISK_ENTRY | cut -d':' -f1\\\`
		MOUNTPOINT="/mnt/disc/\\\${PARTITION##/dev/}"
		mkdir -p \\\$MOUNTPOINT
		MOUNTED=FALSE

		# get the partition type
		case \\\`echo \\\$FDISK_ENTRY | cut -d':' -f2-\\\` in
		*fat*) 
		    FSTYPES="vfat"
		    EXTRAOPTIONS=",uid=500";;
		*)
		    FSTYPES="ext4 ext3 ext2"
		    EXTRAOPTIONS="";;
		esac

		# try to mount the partition
		for FSTYPE in \\\$FSTYPES; do
		    if mount -o "\\\${MOUNTOPTION}\\\${EXTRAOPTIONS}" -t \\\$FSTYPE \\\$PARTITION \\\$MOUNTPOINT &>/dev/null; then
			echo "\\\$PARTITION \\\$MOUNTPOINT \\\$FSTYPE noauto,\\\${MOUNTOPTION}\\\${EXTRAOPTIONS} 0 0" >> /etc/fstab
			echo -n "\\\$PARTITION "
			MOUNTED=TRUE
			CreateDesktopIconHD
		    fi
		done
		[ \\\$MOUNTED = "FALSE" ] && rmdir \\\$MOUNTPOINT
	    done
	done
	echo
fi

# mount logical volumes if 'automount' is given as a boot option
if [ "\\\$( cmdline_parameter automount )" ]; then
        MOUNTOPTION="rw"
	FSTYPES="ext4 ext3 ext2"
	echo "Scanning for logical volumes..."
	if ! lvm vgscan 2>&1 | grep "No volume groups"; then
	    echo "Activating logical volumes ..."
	    modprobe dm_mod >/dev/null
	    lvm vgchange -ay
	    LOGICAL_VOLUMES=\\\`lvm lvdisplay -c | sed "s/^  *//" | cut -d: -f1\\\`
	    if [ ! -z "\\\$LOGICAL_VOLUMES" ]; then
		echo "Making device nodes ..."
		lvm vgmknodes
		echo -n "Mounting logical volumes ... "
		for VOLUME_NAME in \\\$LOGICAL_VOLUMES; do
		    VG_NAME=\\\`echo \\\$VOLUME_NAME | cut -d/ -f3\\\`
		    LV_NAME=\\\`echo \\\$VOLUME_NAME | cut -d/ -f4\\\`
		    MOUNTPOINT="/mnt/lvm/\\\${VG_NAME}-\\\${LV_NAME}"
		    mkdir -p \\\$MOUNTPOINT

		    MOUNTED=FALSE
		    for FSTYPE in \\\$FSTYPES; do
			if mount -o \\\$MOUNTOPTION -t \\\$FSTYPE \\\$VOLUME_NAME \\\$MOUNTPOINT &>/dev/null; then
			    echo "\\\$VOLUME_NAME \\\$MOUNTPOINT \\\$FSTYPE defaults,\\\${MOUNTOPTION} 0 0" >> /etc/fstab
			    echo -n "\\\$VOLUME_NAME "
			    MOUNTED=TRUE
			    CreateDesktopIconLVM
			    break
			fi
		    done
		    [ \\\$MOUNTED = FALSE ] && rmdir \\\$MOUNTPOINT
		done
		echo

	    else
		echo "No logical volumes found"
	    fi
	fi
fi

### give back ownership to the default user
chown -R \\\$LIVECD_USER:\\\$LIVECD_USER /home/\\\$LIVECD_USER

EOF_initscript
#***********************************************************************
# End of livesys script
#***********************************************************************


#***********************************************************************
# Create the livesys init script - /etc/rc.d/init.d/livesys-late
#***********************************************************************

echo "Creating the livesys init script - livesys-late"

cat > /etc/rc.d/init.d/livesys-late << EOF_lateinitscript
#!/bin/bash
#
# live: Late init script for live image
#
# chkconfig: 345 99 01
# description: Late init script for live image.

. /etc/init.d/functions
. /etc/livesys.conf
. /etc/init.d/livesys.functions

# exit if not running from LiveCD
if [ ! "\\\$( cmdline_parameter liveimg )" ] || [ "\\\$1" != "start" ]; then
    exit 0
fi

touch /.liveimg-late-configured

# read boot parameters out of /proc/cmdline
ks=\\\$( cmdline_value ks )
xdriver=\\\$( cmdline_value xdriver )
kb=\\\$( cmdline_value kb )

# if liveinst or textinst is given, start anaconda
if [ "\\\$( cmdline_parameter liveinst )" ]; then
   plymouth --quit
   /usr/sbin/liveinst \\\$ks
   /sbin/reboot
fi
if [ "\\\$( cmdline_parameter textinst )" ] ; then
   plymouth --quit
   /usr/sbin/liveinst --text \\\$ks
   /sbin/reboot
fi

# configure X, allowing user to override xdriver 
# (does not work in SL6 with xorg 7.4)
# if [ -n "\\\$xdriver" ]; then
#   cat > /etc/X11/xorg.conf.d/00-xdriver.conf <<FOE
# Section "Device"
#        Identifier      "Videocard0"
#        Driver          "\\\$xdriver"
# EndSection
# FOE
# fi

# configure X, allowing user to override xdriver
# (does not work in SL6 because system-config-display is missing)
if [ -n "\\\$xdriver" ]; then
   exists system-config-display --noui --reconfig --set-depth=24 \\\$xdriver
fi

# configure keyboard
# (does not work in SL6 because system-config-keyboard is missing)
if [ "\\\$kb" ]; then
    exists system-config-keyboard --noui \\\$kb 
fi


EOF_lateinitscript
#***********************************************************************
# End of livesys-late script
#***********************************************************************


#***********************************************************************
# Create /sbin/halt.local
#***********************************************************************

echo "Creating /sbin/halt.local"

cat > /sbin/halt.local << EOF_haltlocal
#!/bin/bash
#
# Ejects LiveCD/DVD, if boot parameter eject is given 
#

. /etc/init.d/functions
. /etc/livesys.conf
. /etc/init.d/livesys.functions

# exit if not running from LiveCD
if [ ! "\\\$( cmdline_parameter liveimg )" ]; then
    exit 0
fi
if [ "\\\$( cmdline_parameter eject )" ]; then
    echo "Eject CD/DVD ..."
    /usr/sbin/eject -p -m \\\$(readlink -f /dev/live) >/dev/null 2>&1
fi

EOF_haltlocal
#***********************************************************************
# End of /sbin/halt.local script
#***********************************************************************
chmod 755 /sbin/halt.local


#***********************************************************************
# Configure the LiveCD
# Everything configured here will survive LiveCD install to harddisk !
#***********************************************************************

echo "Configure the LiveCD"

chmod 755 /etc/rc.d/init.d/livesys
/sbin/restorecon /etc/rc.d/init.d/livesys
/sbin/chkconfig --add livesys

chmod 755 /etc/rc.d/init.d/livesys-late
/sbin/restorecon /etc/rc.d/init.d/livesys-late
/sbin/chkconfig --add livesys-late

# go ahead and pre-make the man -k cache (#455968)
/usr/sbin/makewhatis -w

# save a little bit of space at least...
rm -f /var/lib/rpm/__db*
rm -f /boot/initrd*
rm -f /boot/initramfs*
# make sure there aren't core files lying around
rm -f /core*

# convince readahead not to collect
rm -f /.readahead_collect
touch /var/lib/readahead/early.sorted

# workaround clock syncing on shutdown that we don't want (#297421)
sed -i -e 's/hwclock/no-such-hwclock/g' /etc/rc.d/init.d/halt

# import RPM GPG keys
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-sl6
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-dawson
rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-sl
#rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-adobe-linux
#rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-atrpms
#rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-elrepo.org
#rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6
#rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-rpmforge-dag
#rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-rpmforge-fabian

# evolution is in the gnome launch panel (bad workaround to start thunderbird instead)
[ ! -e /usr/bin/evolution ] && ln -s /usr/bin/thunderbird /usr/bin/evolution

# clean up yum
yum clean all

# workaround avahi segfault (#279301)
touch /etc/resolv.conf
/sbin/restorecon /etc/resolv.conf

# create locate db
/etc/cron.daily/mlocate.cron

# list kernel just for debugging
rpm -q kernel

EOF_post

# run post-install script
/bin/bash -x /root/post-install 2>&1 | tee /root/post-install.log

%end


########################################################################
#
#  LiveCD post no chroot install 
#
########################################################################
%post --nochroot

#***********************************************************************
# Create /root/postnochroot-install
# Must change "$" to "\$" and "`" to "\`" to avoid shell quoting
#***********************************************************************

cat > /root/postnochroot-install << EOF_postnochroot
#!/bin/bash

# Copy licensing information
cp $INSTALL_ROOT/usr/share/doc/*-release-*/GPL $LIVE_ROOT/GPL

# customize boot menu entries
grep -B4 'menu default'            \$LIVE_ROOT/isolinux/isolinux.cfg > \$LIVE_ROOT/isolinux/default.txt
grep -B3 'xdriver=vesa nomodeset'  \$LIVE_ROOT/isolinux/isolinux.cfg > \$LIVE_ROOT/isolinux/basicvideo.txt
grep -A3 'label check0'            \$LIVE_ROOT/isolinux/isolinux.cfg > \$LIVE_ROOT/isolinux/check.txt
grep -A2 'label memtest'           \$LIVE_ROOT/isolinux/isolinux.cfg > \$LIVE_ROOT/isolinux/memtest.txt
grep -A2 'label local'             \$LIVE_ROOT/isolinux/isolinux.cfg > \$LIVE_ROOT/isolinux/localboot.txt

sed "s/label linux0/label linuxtext0/"   \$LIVE_ROOT/isolinux/default.txt > \$LIVE_ROOT/isolinux/textboot.txt
sed -i "s/Boot/Boot (Text Mode)/"                                           \$LIVE_ROOT/isolinux/textboot.txt
sed -i "s/liveimg/liveimg 3/"                                               \$LIVE_ROOT/isolinux/textboot.txt
sed -i "/menu default/d"                                                    \$LIVE_ROOT/isolinux/textboot.txt

sed "s/label linux0/label install0/"     \$LIVE_ROOT/isolinux/default.txt > \$LIVE_ROOT/isolinux/install.txt
sed -i "s/Boot/Install/"                                                    \$LIVE_ROOT/isolinux/install.txt
sed -i "s/liveimg/liveimg liveinst noswap/"                                 \$LIVE_ROOT/isolinux/install.txt
sed -i "s/ quiet / /"                                                       \$LIVE_ROOT/isolinux/install.txt
sed -i "s/ rhgb / /"                                                        \$LIVE_ROOT/isolinux/install.txt
sed -i "/menu default/d"                                                    \$LIVE_ROOT/isolinux/install.txt

sed "s/label linux0/label textinstall0/" \$LIVE_ROOT/isolinux/default.txt > \$LIVE_ROOT/isolinux/textinstall.txt
sed -i "s/Boot/Install (Text Mode)/"                                        \$LIVE_ROOT/isolinux/textinstall.txt
sed -i "s/liveimg/liveimg textinst noswap/"                                 \$LIVE_ROOT/isolinux/textinstall.txt
sed -i "s/ quiet / /"                                                       \$LIVE_ROOT/isolinux/textinstall.txt
sed -i "s/ rhgb / /"                                                        \$LIVE_ROOT/isolinux/textinstall.txt
sed -i "/menu default/d"                                                    \$LIVE_ROOT/isolinux/textinstall.txt

cat \$LIVE_ROOT/isolinux/default.txt \$LIVE_ROOT/isolinux/basicvideo.txt \$LIVE_ROOT/isolinux/check.txt \$LIVE_ROOT/isolinux/memtest.txt \$LIVE_ROOT/isolinux/localboot.txt > \$LIVE_ROOT/isolinux/current.txt

diff \$LIVE_ROOT/isolinux/isolinux.cfg \$LIVE_ROOT/isolinux/current.txt | sed '/^[0-9][0-9]*/d; s/^. //; /^---$/d' > \$LIVE_ROOT/isolinux/cleaned.txt

cat \$LIVE_ROOT/isolinux/cleaned.txt      \
    \$LIVE_ROOT/isolinux/default.txt      \
    \$LIVE_ROOT/isolinux/textboot.txt     \
    \$LIVE_ROOT/isolinux/basicvideo.txt   \
    \$LIVE_ROOT/isolinux/check.txt        \
    \$LIVE_ROOT/isolinux/install.txt      \
    \$LIVE_ROOT/isolinux/textinstall.txt  \
    \$LIVE_ROOT/isolinux/memtest.txt      \
    \$LIVE_ROOT/isolinux/localboot.txt > \$LIVE_ROOT/isolinux/isolinux.cfg
rm -f \$LIVE_ROOT/isolinux/*.txt

EOF_postnochroot

# run postnochroot-install script
/bin/bash -x /root/postnochroot-install 2>&1 | tee /root/postnochroot-install.log

%end

