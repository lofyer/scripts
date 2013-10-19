########################################################################
#
# sl63-extra-software.ks
#
# Extra software for SL LiveCD
#
########################################################################

repo --name=livecd-extra     --baseurl=http://www.livecd.ethz.ch/download/sl-livecd-extra/6.3/$basearch/

%packages

# install yum-conf-livecd-extra
yum-conf-livecd-extra
livecd-extra-release

# install extra software from rpmforge
gstreamer-ffmpeg

# install extra software from epel
gdisk
gparted
NetworkManager-openvpn
NetworkManager-vpnc
NetworkManager-pptp
vpnc-consoleuser
ntfs-3g
fuse-sshfs
ntfsprogs
dd_rescue
ddrescue
iperf

# install extra software from elrepo
kmod-reiserfs
#kmod-ndiswrapper
reiserfs-utils

# install extra software from adobe
flash-plugin

%end
