########################################################################
#
#  Mini LiveCD with icewm desktop
#
#  Urs Beyerle, ETHZ
#
########################################################################

part / --size 4096 --fstype ext4

########################################################################
# Include kickstart files
########################################################################

%include sl62-live-base.ks
%include sl62-config-icewm.ks
%include sl62-extra-software.ks
%include sl62-doc.ks


########################################################################
# Packages
########################################################################

%packages
# packages removed from @base
-bind-utils
-ed
-kexec-tools
-system-config-kdump
-libaio
-libhugetlbfs
-microcode_ctl
-psacct
-quota
-autofs
-smartmontools 

# from @fonts
dejavu-fonts-common
dejavu-sans-fonts
dejavu-sans-mono-fonts
dejavu-serif-fonts
fontpackages-filesystem
xorg-x11-fonts-misc

# login manager
gdm

# icewm desktop
@ice-desktop

## mini SL LiveCD specific changes

# packages to remove
-scenery-backgrounds
-xinetd
-smartmontools
-ql2100-firmware
-ql2200-firmware
-ql23xx-firmware
-ql2400-firmware
-ql2500-firmware
-qt3                  
-samba-common
-samba-client               
-samba-winbind-clients     
-selinux-policy           
-nmap                      
-mysql-libs                
-words                     
-openswan                  
-nautilus                  
-smp_utils                 
-system-config-network-tui 

# packages to add
ibus-gtk
thunderbird
firefox
NetworkManager-gnome
#@openafs-client

# install extra software from rpmforge
rxvt-unicode

%end


########################################################################
# Post installation
########################################################################

%post

### save diskspace for MiniLiveCD
### this changes will survive MiniLiveCD install to harddisk !

# remove yumdb - will give a warning that "RPMDB altered outside of yum"
rm -rf /var/lib/yum/yumdb/*

# remove folders/files that use a lot of diskspace 
# and are not really needed for miniLiveCD
find /usr/share/doc/* -maxdepth 0 -type d  | grep -v HTML | while read d; do rm -rf $d; done
rm -rf /usr/share/info
rm -rf /usr/share/vim/vim7*/doc
rm -rf /usr/share/vim/vim7*/lang
find /usr/share/backgrounds -type f  | grep -v default | while read f; do rm -f $f; done

# remove all locale except en
find /usr/share/locale/* -maxdepth 0 -type d         | grep -v /en | while read d; do rm -rf $d; done
find /usr/share/i18n/locales/*  -maxdepth 0 -type f  | grep -v /en | while read d; do rm -rf $d; done

%end
