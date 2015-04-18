#!/bin/sh


# Script to add a login to ldap. 
# Not meant for anything beyound casual use
# Author: Rilindo Foster
# Contact:  rilindo.foster@monzell.com
# Date: 09/11/2011

if [ -z $1 ];  then
	echo "addldapuser.sh <username>"
	exit 1
fi

USERNAME=$1

PASSWORD=$1

# Generate a ID between 1000 and 65535. Its okay for home and maybe a small offie. For a medium to large company, you need a bigger number or try something different.

LUID=`echo $[ 1000 + $[ RANDOM % 65535 ]]`

(
cat <<add-user
dn: cn=$USERNAME,ou=Users,dc=shfc,dc=edu,dc=cn
cn: $USERNAME
uid: $USERNAME
sn: $USERNAME
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: top
userPassword: $PASSWORD
uidNumber: $LUID
gidNumber: 501
givenName: $USERNAME
homeDirectory: /home/users/$USERNAME
add-user
) > /root/adduser.ldif

ldapadd -x -w admin -D "cn=admin,dc=shfc,dc=edu,dc=cn" -f /root/adduser.ldif && rm /root/adduser.ldif 

if [ $? -ne "0" ]; then
	echo "Add user failed"
	echo "Please review /root/adduser.ldif and add the account manually"
#else
#	mkdir -p $HOMEDIR/$USERNAME
#	cp -Rv $SKEL $HOMEDIR/$USERNAME
#	chown -Rv $LUID:$LUID $HOMEDIR/$USERNAME
fi
