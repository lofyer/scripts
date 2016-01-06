#!/bin/bash
lspci | grep -i ethernet
lspci -s 04:00.1 -k
modprobe vfio_pci vfio_iommu_type1
modinfo ixgbe; modprobe -r ixgbe; modprobe ixgbe max_vfs=4
lspci -n
echo 0000:04:10.0 > /sys/bus/pci/devices/0000\:04\:10.0/driver/unbind
echo 0000:04:10.1 > /sys/bus/pci/devices/0000\:04\:10.1/driver/unbind
echo 0000:04:10.2 > /sys/bus/pci/devices/0000\:04\:10.2/driver/unbind
echo 0000:04:10.3 > /sys/bus/pci/devices/0000\:04\:10.3/driver/unbind
echo 8086 10ed > /sys/bus/pci/drivers/vfio-pci/new_id
# We need that?
chown qemu.kvm /dev/vfio/{47,48,49,50}
chmod 660 /dev/vfio/{47,48,49,50}
