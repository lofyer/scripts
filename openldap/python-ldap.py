#!/usr/bin/env python
import sys,ldap

LDAP_HOST = '192.168.0.88'
LDAP_BASE_DN = 'dc=virtfan,dc=com'
MGR_CRED = 'cn=admin,dc=virtfan,dc=com'
MGR_PASSWD = 'admin'
STOOGE_FILTER = 'o=stooges'


