#!/bin/bash
import cx_Oracle

con = cx_Oracle.connect('theuser', 'thepass', 'your DB alias on your TNSNAMES.ORA file ')
cur = con.cursor()
if cur.execute('select * from dual'):
    print "finally, it works!!!"
else:
    print "facepalm"
    con.close()
