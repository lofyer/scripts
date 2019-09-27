# 1. Partition(Optional)

    [root@localhost]# fdisk /dev/vdb

# 2. Crypt with LUKS 

    [root@localhost]# cryptsetup luksFormat /dev/vdb1

    WARNING!
    This will overwrite data on /dev/vdb1 irrevocably.
    Are you sure? (Type uppercase yes): YES
    Enter passphrase: ***********
    Verify passphrase: ***********

# 3. Unlock the volume

    [root@localhost]# cryptsetup luksOpen /dev/vdb1 encrypted-volume
    Enter passphrase for /dev/vdb1: *********** 

Verify:

    [root@localhost]# ls -l /dev/mapper | grep encrypted-volume
    lrwxrwxrwx. 1 root root       7 Apr 21 23:02 encrypted-volume -> ../dm-2

    [root@localhost]# blkid | grep crypt
    /dev/vdb1: UUID="dc57e3a0-5d47-4dec-857e-89db2fad2f70" TYPE="crypto_LUKS"

# 4. Format the volume

    [root@localhost]# mkfs -t xfs /dev/mapper/encrypted-volume
    [root@localhost]# blkid | grep crypt
    /dev/vdb1: UUID="dc57e3a0-5d47-4dec-857e-89db2fad2f70" TYPE="crypto_LUKS" 
    /dev/mapper/encrypted-volume: UUID="a363d94a-206f-4932-a6e6-7b3b98ad817e" TYPE="xfs"

# 5. Manually mount/unmount the volume

    [root@localhost]# mkdir /mnt/safe_volume
    [root@localhost]# mount /dev/mapper/encrypted-volume /mnt/safe_volume


# 6. Auto-mount the volume

    [root@localhost]# touch /root/safe_volume_key
    [root@localhost]# echo 'secretpassphrase' > /root/safe_volume_key
    [root@localhost]# cryptsetup luksAddKey /dev/vdb1 /root/safe_volume_key
    Enter any passphrase: ***********
    [root@localhost]# chmod 600 /root/safe_volume_key 

    [root@localhost]# vi /etc/crypttab
    encrypted-volume   /dev/vdb1   /root/safe_volume_key

    [root@localhost]# vi /etc/fstab
    /dev/mapper/encrypted-volume   /mnt/safe_volume   xfs   defaults   0   0 

    ## Remove the key
    [root@localhost]# cryptsetup luksRemoveKey /dev/vdb1 /root/safe_volume_key