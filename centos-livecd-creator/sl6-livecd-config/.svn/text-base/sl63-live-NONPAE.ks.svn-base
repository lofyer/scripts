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
kernel-ml-NONPAE
kernel-ml-firmware
yum-conf-elrepo
# for LiveDVD add kernel-ml-devel and kernel-ml-headers
# kernel-ml-devel 
# kernel-ml-headers

########################################################################
# Remove packages
########################################################################
-kernel-firmware
-kernel
-kernel-headers
-kernel-devel
# kmod for kernel-ml not provided by elrepo
-kmod-*
%end

########################################################################
# Enable elrepo-kernel
########################################################################
%post
sed -i '/^\[elrepo-kernel\]/,/^enabled/ {  s/^enabled=.*/enabled=1/ }' /etc/yum.repos.d/elrepo.repo
%end

