#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import cgi, os, sys
import subprocess as sub

def GetgAppDataPath(module):
    path = os.path.join('./', module)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

try:
    form = cgi.FieldStorage()
    uuid = form.getfirst("uuid", "")
    huuid = form.getfirst("remaining", "")
    if uuid and huuid :
       open(os.path.join(GetgAppDataPath("txt") ), 'wb').write(remaining)
       message = "上传成功，请稍后到ISO存储域中查看并刷新。"
    else:
       message = '没有上传文件'
except Exception as e:
    message = e
    

print """\
Content-Type: text/html\n
%s
"""% (message,)
