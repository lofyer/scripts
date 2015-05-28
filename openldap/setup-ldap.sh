#!/bin/bash
# Setup LDAP server in CentOS

# Install packages
yum install openldap-{servers,clients}

# Configure
echo -e "pidfile /var/run/openldap/slapd.pid\nargsfile /var/run/openldap/slapd.args" >> /etc/openldap/slapd.conf
rm -fr /etc/openldap/slapd.d/*
slaptest -f /etc/openldap/slapd.conf -F /etc/openldap/slapd.d/
gsed -i '/olcAccess/d' /etc/openldap/slapd.d/cn\=config/olcDatabase\=\{0\}config.ldif
echo 'olcAccess: {0}to * by dn.exact=gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth manage by * break' >> /etc/openldap/slapd.d/cn\=config/olcDatabase\=\{0\}config.ldif
chown -R ldap. /etc/openldap/slapd.d/
chmod -R 700  /etc/openldap/slapd.d/
service slapd start
chkconfig slapd on

ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/core.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/cosine.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/nis.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/inetorgperson.ldif
ldapadd -Y EXTERNAL -H ldapi:/// -f ./backend.ldif
ldapadd -x -D cn=admin,dc=example,dc=com -W -f frontend.ldif

# Change openldapphp

