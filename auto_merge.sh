#!/bin/bash
BEGIN_DATE=`date`
subject="Automerge conflict detected"
from="AutoMerge@gitserver.com"
recipients="user0@gmail.com,user1@gmail.com"
 
echo "Begin merge at $BEGIN_DATE" >> /mnt/automerge.log;
# Need pull first
GIT_UPDATE=`su git -c 'cd /home/git/src.git; git pull'`
# Need pull first
if [ -d /mnt/src ]
then
    GIT_CD=`su git -c 'cd /mnt/src'`;
else
    GIT_CLONE=`su git -c 'cd /mnt/; git clone /home/git/src.git'`;
fi
GIT_PULL=`su git -c 'cd /mnt/src/; git checkout master;git pull'`
# Merge master to test1
GIT_MERGE=`su git -c 'cd /mnt/src; git checkout test1; git pull origin master; git push origin test1'`
echo -e "Pulling now...n"
# Test if CONFLICT exist
if [[ "$GIT_MERGE" == *CONFLICT* ]]
    then
        echo "CONFLICT detected!" >> /mnt/automerge.log;
        # Send a mail here
        mail="subject:$subjectnfrom:$fromn$GIT_MERGEn$BEGIN_DATE"
        echo -e $mail | sendmail "$recipients"
        # It'll be better if you delete current src and clone a new one
        RM_CLONE_CMD=`su git -c 'cd /mnt; rm -rf src'`
        exit 1
    else
        # No conflict, checkout master
        GIT_CMD=`su git -c 'cd /mnt/src; git checkout master'`
        END_DATE=`date`
        echo "Merge succeed at $END_DATE" >> /mnt/automerge.log;
        exit 0
fi
