#!/usr/bin/env python
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("lofyer.org",22,"root", "password")
stdin, stdout, stderr = ssh.exec_command("ls /")
print stdout.readlines()
ssh.close()

t = paramiko.Transport((“主机”,”端口”))
t.connect(username = “用户名”, password = “口令”)
sftp = paramiko.SFTPClient.from_transport(t)
remotepath=’/var/log/system.log’
localpath=’/tmp/system.log’
sftp.get(remotepath, localpath)
t.close()

t = paramiko.Transport((“主机”,”端口”))
t.connect(username = “用户名”, password = “口令”)
sftp = paramiko.SFTPClient.from_transport(t)
remotepath=’/var/log/system.log’
localpath=’/tmp/system.log’
sftp.put(localpath,remotepath)
t.close()
