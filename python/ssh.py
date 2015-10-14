#!/usr/bin/env python
import paramiko
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("lofyer.org",22,"root", "password")
stdin, stdout, stderr = ssh.exec_command("ls /")
print stdout.readlines()
ssh.close()
