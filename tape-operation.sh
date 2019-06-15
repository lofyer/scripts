#!/bin/bash
# Change initiator name
cat cat /etc/iscsi/initiatorname.iscsi

# iSCSI discover
iscsiadm -m discovery --type sendtargets --portal 172.32.1.119

# iSCSI login
iscsiadm -m node --login

# Without rewind
export TAPE=/dev/nst0
# With rewind
#export TAPE=/dev/st0

# Show generic name of changer sch0
lsscsi -g
mtx -f /dev/sg3 inquiry
# Push the first tape to the drive
mtx -f /dev/sg4 first

# Check tape status
mt status

# Load tape to drive
mt load

# Rewind the tape
mt rewind

# Backup files or folders to tape
tar cf - file_to_backup_1 -P | pv -s $(du -sb file_to_backup_1 | awk '{print $1}') > $TAPE
tar cf - file_to_backup_2 -P | pv -s $(du -sb file_to_backup_2 | awk '{print $1}') > $TAPE

# List tar 1
tar tvf $TAPE

# List tar 2
mt fsf
tar tvf $TAPE

# Restore files or folders from tape
mt rewind
tar xvf /dev/st0 -C file_directory 
mt fsf
tar xvf /dev/st0 -C file_directory 

# Backup filesystem to tape
dump -0auqb 64 -f $TAPE /dev/sda1

# Restore filesystem from tape
restore -Cyf /dev/nst0 -b 64 -s $counter

# Erase tape
mt erase

# Unload the tape
mt offline/eject

# iSCSI logout
iscsiadm --mode node --logoutall=all
