#!/bin/bash
DATE=$(date)
cmd=$(service tomcat7 status)
if [[ $? != 0 ]]
then
    service tomcat7 restart
    echo "$DATE restart tomcat7." >> /tmp/check_alive.log
fi
