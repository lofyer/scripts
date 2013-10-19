########################################################################
#
#  LiveCD with NONPAE kernel from elrepo-kernel
#
#  Urs Beyerle, ETHZ
#
########################################################################

########################################################################
# Add elrepo-kernel repo
########################################################################
repo --name=elrepo-kernel  --baseurl=http://elrepo.org/linux/kernel/el6/$basearch/

%packages
########################################################################
# Add packages
########################################################################
kernel-lt-NONPAE
kernel-lt-firmware
yum-conf-elrepo
# for LiveDVD add kernel-lt-devel and kernel-lt-headers
# kernel-lt-devel 
# kernel-lt-headers

########################################################################
# Remove packages
########################################################################
-kernel-firmware
-kernel
-kernel-headers
-kernel-devel
# kmod for kernel-lt not provided by elrepo
-kmod-*
%end

########################################################################
# Enable elrepo-kernel - disable elrepo 
########################################################################
%post
# enable elrepo-kernel
sed -i '/^\[elrepo-kernel\]/,/^enabled/ {  s/^enabled=.*/enabled=1/ }' /etc/yum.repos.d/elrepo.repo
# disable elrepo, because elrepo-release-6-5.el6.elrepo requires kernel = 2.6.32 
sed -i '/^\[elrepo\]/,/^enabled/ {  s/^enabled=.*/enabled=0/ }'        /etc/yum.repos.d/elrepo.repo
%end

