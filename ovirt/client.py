#!/usr/bin/python
import wx
import os
import sys
import json
import httplib
import threading
import subprocess
import logging
import time
import inspect
import urllib
import urllib2
import commands
from datetime import datetime
from xml.dom import minidom

from base64 import b32encode, b32decode

# Configuration file should include:
# VIRTUAL_KEYBOARD=True/False
#     If set to True, the virtual keyboard will be shown. User for the case of touch screen.
# ENGINE_IP=xxx.xxx.xxx.xxx
# USER_NAME=xxx

platform = sys.platform
if platform == 'win32':
    cfile = os.getcwd() + '\\vclient.conf'
    lfile = os.getcwd() + '\\vclient.log'
    cafile = 'ca.crt'
    #viewer = "VirtViewer\\bin\\remote-viewer"
else:		#linux2
    cdir = os.path.dirname(os.path.realpath(inspect.getfile(inspect.currentframe())))
    cfile = cdir + '/vclient.conf'
    lfile = cdir + '/vclient.log'
    cafile = 'ca.crt'
    #viewer = "remote-viewer"
viewer = None
spicec = None
logger = None
vkbd = 'False'
showmenu = 'True'
autologin = 'False'
autoconnect = 'False'
engine = ''
username = ''
password = ''
desktops = []

ldialog = None
virtkeyboard = None
desktopframe = None
curfocus = None
curdialog = None


def encrypt(msg):
    return b32encode(msg)

def decrypt(msg):
    return b32decode(msg)


def FetchCA():
    global engine, logger
    logger.info('Fetching Certification...')
    url = "https://" + engine + "/ca.crt"
    req = urllib2.Request(url=url)
    res = urllib2.urlopen(req).read()
    ca = open(cafile, "w" )
    ca.write(res)
    ca.close()


def AuthUser():
    global engine, username, password, logger
    logger.info('Authenticating User...')

    url = "https://" + engine + "/api/"

    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, url, username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)

    req = urllib2.Request(url=url)
    res = urllib2.urlopen(req).read()


def ParseVms(xml):
    global desktops, logger
    doc = minidom.parseString(xml)

    root = doc.documentElement

    desktops = []
    for vm in root.getElementsByTagName("vm"):
        desktop = {}
        uuid = vm.getAttribute("id")
        desktop['id'] = uuid

        nameNode = vm.getElementsByTagName("name")[0]
        desktop['name'] = nameNode.childNodes[0].nodeValue

        memoryNode = vm.getElementsByTagName("memory")[0]
        desktop['memory'] = memoryNode.childNodes[0].nodeValue

        statusNode = vm.getElementsByTagName("status")[0]
        stateNode = statusNode.getElementsByTagName("state")[0]
        desktop['status'] = stateNode.childNodes[0].nodeValue

        displayNode = vm.getElementsByTagName("display")[0]
        typeNode = displayNode.getElementsByTagName("type")[0]
        desktop['type'] = typeNode.childNodes[0].nodeValue
        try:
            portNode = displayNode.getElementsByTagName("port")[0]
            desktop['port'] = portNode.childNodes[0].nodeValue
        except Exception, e:
            desktop['port'] = ''
        try:
            sportNode = displayNode.getElementsByTagName("secure_port")[0]
            desktop['sport'] = sportNode.childNodes[0].nodeValue
        except Exception, e:
            desktop['sport'] = ''

        try:
            hostNode = vm.getElementsByTagName("host")[0]
            host_id = hostNode.getAttribute("id")
            desktop['host'] = host_id
        except Exception, e:
            desktop['host'] = ''
        desktops.append(desktop)
    logger.info(desktops)
    return desktops


def ListVms():
    global engine, username, password
    url = "https://" + engine + "/api/vms/"

    #passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    #passman.add_password(None, url, username, password)
    #authhandler = urllib2.HTTPBasicAuthHandler(passman)
    #opener = urllib2.build_opener(authhandler)
    #urllib2.install_opener(opener)

    req = urllib2.Request(url=url, headers={'filter': 'true'})
    #req = urllib2.Request(url=url)
    res = urllib2.urlopen(req).read()
    return ParseVms(res)


def StartVm(vm_uuid):
    global engine, username, password
    url = "https://" + engine + "/api/vms/" + vm_uuid + "/start/"

    #passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    #passman.add_password(None, url, username, password)
    #authhandler = urllib2.HTTPBasicAuthHandler(passman)
    #opener = urllib2.build_opener(authhandler)
    #urllib2.install_opener(opener)

    req = urllib2.Request(url=url, data="<action />", headers={'Content-Type': 'application/xml'})
    res = urllib2.urlopen(req).read()


def StopVm(vm_uuid):
    global engine, username, password
    url = "https://" + engine + "/api/vms/" + vm_uuid + "/stop/"

    #passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    #passman.add_password(None, url, username, password)
    #authhandler = urllib2.HTTPBasicAuthHandler(passman)
    #opener = urllib2.build_opener(authhandler)
    #urllib2.install_opener(opener)

    req = urllib2.Request(url=url, data="<action />", headers={'Content-Type': 'application/xml'})
    res = urllib2.urlopen(req).read()


def ParseTicket(xml):
    doc = minidom.parseString(xml)

    root = doc.documentElement
    ticketNode = root.getElementsByTagName("ticket")[0]
    valueNode = ticketNode.getElementsByTagName("value")[0]
    return valueNode.childNodes[0].nodeValue


def SetTicket(vm_uuid):
    global engine, username, password
    url = "https://" + engine + "/api/vms/" + vm_uuid + "/ticket/"

    #passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    #passman.add_password(None, url, username, password)
    #authhandler = urllib2.HTTPBasicAuthHandler(passman)
    #opener = urllib2.build_opener(authhandler)
    #urllib2.install_opener(opener)

    req = urllib2.Request(url=url, data="<action><ticket><expiry>120</expiry></ticket></action>", headers={'Content-Type': 'application/xml'})
    res = urllib2.urlopen(req).read()
    return ParseTicket(res)


def ParseHostSubject(xml):
    doc = minidom.parseString(xml)

    root = doc.documentElement
    #certificateNode = root.getElementsByTagName("certificate")[0]
    #subjectNode = ticketNode.getElementsByTagName("subject")[0]
    displayNode = root.getElementsByTagName("display")[0]
    certificateNode = displayNode.getElementsByTagName("certificate")[0]
    subjectNode = certificateNode.getElementsByTagName("subject")[0]
    return subjectNode.childNodes[0].nodeValue


def ParseHost(xml):
    doc = minidom.parseString(xml)

    root = doc.documentElement
    #certificateNode = root.getElementsByTagName("certificate")[0]
    #subjectNode = ticketNode.getElementsByTagName("subject")[0]
    displayNode = root.getElementsByTagName("display")[0]
    addressNode = displayNode.getElementsByTagName("address")[0]
    return addressNode.childNodes[0].nodeValue


#def GetHostSubject(host_uuid):
def GetHostSubject(vm_uuid):
    global engine, username, password
    #url = "https://" + engine + "/api/hosts/" + host_uuid + "/"		#Can also get from VM's detailed information (aoqingy)
    url = "https://" + engine + "/api/vms/" + vm_uuid + "/"

    req = urllib2.Request(url=url)
    res = urllib2.urlopen(req).read()
    return ParseHostSubject(res)


def GetHost(vm_uuid):
    global engine, username, password
    #url = "https://" + engine + "/api/hosts/" + host_uuid + "/"                #Can also get from VM's detailed information (aoqingy)
    url = "https://" + engine + "/api/vms/" + vm_uuid + "/"

    req = urllib2.Request(url=url)
    res = urllib2.urlopen(req).read()
    return ParseHost(res)


#def report(line):
#    global logger
#    logger.info(line)


def RemoteViewerConnect(host, port, sport, ticket, subject):
    global logger, viewer, spicec, cafile
    logger.info('Preparing to connect to port %s and secure port %s on host %s' % (host, port, sport))
    platform = sys.platform
    if platform == 'win32':
        #cmd = 'lib\spicec.exe -h %s -p %s -w %s -f' % (host, port, password)
        if viewer != None:
            if port != '':
                cmd = '%s --spice-ca-file="%s" --spice-host-subject="%s" "spice://%s/?port=%s&tls-port=%s&password=%s"' % (viewer, cafile, subject, host, port, sport, ticket)
            else:
                cmd = '%s --spice-ca-file="%s" --spice-host-subject="%s" "spice://%s/?tls-port=%s&password=%s"' % (viewer, cafile, subject, host, sport, ticket)
        else:
            if port != '':
                cmd = '%s --ca-file "%s" --host-subject "%s" -h %s -p %s -s %s -w %s' % (spicec, cafile, subject, host, port, sport, ticket)
            else:
                cmd = '%s --ca-file "%s" --host-subject "%s" -h %s -s %s -w %s' % (spicec, cafile, subject, host, sport, ticket)
        logger.info(cmd)
        os.system(cmd)
    if platform == 'linux2':
        #cmd = ['remote-viewer', '--spice-ca-file=%s' % cafile, '--spice-host-subject="%s"' % subject, '"spice://%s/?port=%s&tls-port=%s&password=%s"' % (host, port, sport, ticket)]
        if viewer != None:
            if port != '':
                cmd = '%s --spice-ca-file="%s" --spice-host-subject="%s" "spice://%s/?port=%s&tls-port=%s&password=%s"' % (viewer, cafile, subject, host, port, sport, ticket)
            else:
                cmd = '%s --spice-ca-file="%s" --spice-host-subject="%s" "spice://%s/?tls-port=%s&password=%s"' % (viewer, cafile, subject, host, sport, ticket)
        else:
            if port != '':
                cmd = '%s --ca-file "%s" --host-subject "%s" -h %s -p %s -s %s -w %s' % (spicec, cafile, subject, host, port, sport, ticket)
            else:
                cmd = '%s --ca-file "%s" --host-subject "%s" -h %s -s %s -w %s' % (spicec, cafile, subject, host, sport, ticket)
        logger.info(cmd)
        status, output = commands.getstatusoutput(cmd)
        logger.info(output)
        #logger.info(cmd)
        #proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #for line in proc.stdout:
        #    wx.CallAfter(report, line)


def ConnectVm(vm_uuid, port, sport):
    ticket = SetTicket(vm_uuid)
    host = GetHost(vm_uuid)
    subject = GetHostSubject(vm_uuid)
    #thread = threading.Thread(target=RemoteViewerConnect, args=(host, port, sport, ticket, subject, ))
    #thread.setDaemon(True)
    #thread.start()
    RemoteViewerConnect(host, port, sport, ticket, subject)
    

def LoadConfig():
    global vkbd, showmenu, engine, username, password, autologin, autoconnect, viewer, spicec, logger
    try:
        logger.info('Preparing to load the configuration file...')
        f = file(cfile, 'r')
        for line in f.read().split('\n'):
            try:
                k, v = line.split('=', 1)
                if k == 'VIRTUAL_KEYBOARD' and v != '':
                    vkbd = v
                if k == 'SHOW_MENU' and v != '':
                    showmenu = v
                if k == 'ENGINE_IP' and v != '':
                    engine = v
                if k == 'USER_NAME':
                    username = v.decode('utf-8')
                if k == 'PASSWORD':
                    password = decrypt(v)
                if k == 'AUTO_LOGIN':
                    autologin = v
                if k == 'AUTO_CONNECT':
                    autoconnect = v
                if k == "REMOTE_VIEWER" and v != '':
                    viewer = v.strip("\"'")
                if k == "SPICEC" and v != '':
                    spicec = v.strip("\"'")
            except Exception, e:
                pass
        f.close()
        logger.info('vkbd=%s, engine=%s, username=%s, password=%s, autologin=%s, autoconnect=%s' % (vkbd, engine, username, password, autologin, autoconnect))
    except Exception, e:
        logger.info('Fail to parse the configuration file: %s' % str(e))


def SaveConfig():
    global  vkbd, showmenu, engine, username, password, autologin, autoconnect, viewer, spicec, logger
    try:
        logger.info('Preparing to save the configuration file...')
        f = file(cfile, 'w')
        f.write("VIRTUAL_KEYBOARD=%s\n" % vkbd)
        f.write("SHOW_MENU=%s\n" % showmenu)
        if viewer != None:
            f.write("REMOTE_VIEWER=%s\n" % viewer)
        if spicec != None:
            f.write("SPICEC=%s\n" % spicec)
        f.write("ENGINE_IP=%s\n" % engine)
        f.write("USER_NAME=%s\n" % username.encode('utf-8'))
        f.write("PASSWORD=%s\n" % encrypt(password))
        f.write("AUTO_LOGIN=%s\n" % autologin)
        f.write("AUTO_CONNECT=%s\n" % autoconnect)
        f.close()
    except Exception, e:
        logger.info(str(e))
        pass


def InitLog():
    global lfile, logger
    logger = logging.getLogger()
    hdlr = logging.FileHandler(lfile)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)


class LoginDialog(wx.Dialog):
    def __init__(self, parent, id, title, size=(600,480), pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE | wx.TAB_TRAVERSAL, useMetal=False):
        global ldialog
        ldialog = self

        global engine, username, password, logger
        logger.info('Initializing login dialog...')
        wx.Dialog.__init__(self, parent, id, title, size=size, style=style)
        self.Bind(wx.EVT_CLOSE, self.OnExit)

        logger.info('Creating components...')
        vbox = wx.BoxSizer(wx.VERTICAL)

        logger.info('Adding prompting message...')
        self.prompt = wx.StaticText(self, -1, 'Please input engine address, user name and\nlogin password.', size=(300, 40))
        #font = wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL)
        #self.prompt.SetFont(font)
        #logger.info(self.prompt.GetFont().GetFamilyString())
        #logger.info(self.prompt.GetFont().GetStyleString())
        #logger.info(self.prompt.GetFont().GetPointSize())
        vbox.Add(self.prompt, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        logger.info('Adding engine label and textctrl...')
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        slabel = wx.StaticText(self,  -1, 'Engine', size=(70, 20))
        hbox.Add(slabel, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.etext = wx.TextCtrl(self, -1, engine, size=(80, -1), style=0)
        self.etext.Bind(wx.EVT_TEXT, self.OnEngine)
        self.etext.Bind(wx.EVT_SET_FOCUS, self.OnEngineEnter)
        self.etext.SetFocus()
        hbox.Add(self.etext, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(hbox, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        logger.info('Adding username label and textctrl...')
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        #if action == 'CONNECT':
        #    self.ulabel = wx.StaticText(self, -1, 'Port', size=(70, 20))
        #else:
        #    self.uplabel = wx.StaticText(self, -1, 'Username', size=(70, 20))
        self.ulabel = wx.StaticText(self, -1, 'Username', size=(70, 20))
        hbox.Add(self.ulabel, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.utext = wx.TextCtrl(self, -1, username, size=(80, -1), style=0)
        self.utext.Bind(wx.EVT_TEXT, self.OnUsername)
        self.utext.Bind(wx.EVT_SET_FOCUS, self.OnUsernameEnter)
        hbox.Add(self.utext, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(hbox, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        logger.info('Adding password label and textctrl...')
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        plabel = wx.StaticText(self, -1, 'Password', size=(70, 20))
        hbox.Add(plabel, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        self.ptext = wx.TextCtrl(self, -1, "", size=(80, -1), style=wx.TE_PASSWORD)
        self.ptext.Bind(wx.EVT_TEXT, self.OnPassword)
        self.ptext.Bind(wx.EVT_SET_FOCUS, self.OnPasswordEnter)
        hbox.Add(self.ptext, 1, wx.ALIGN_CENTER | wx.ALL, 5)
        vbox.Add(hbox, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        #hbox = wx.BoxSizer(wx.HORIZONTAL)
        #self.abox = wx.CheckBox(self, -1, "Automatically Connect", wx.DefaultPosition, (300, 20))
        #if auto == 'True':
        #    self.abox.SetValue(True)
        #else:
        #    self.abox.SetValue(False)
        #self.abox.Bind(wx.EVT_CHECKBOX, self.OnAbox)
        #self.abox.Bind(wx.EVT_SET_FOCUS, self.OnAutoEnter)
        #hbox.Add(self.abox, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        #vbox.Add(hbox, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)

        #logger.info('Adding seperator line...')
        #vbox.Add(wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL), 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 2)

        logger.info('Adding status message...')
        self.message = wx.StaticText(self, -1, '', size=(300, 20))
        vbox.Add(self.message, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        logger.info('Adding OK button...')
        #hbox = wx.BoxSizer()
        okId = wx.NewId()
        self.okbutton = wx.Button(self, okId, 'OK', wx.DefaultPosition, (150, 32), 0)
        self.Bind(wx.EVT_BUTTON, self.OnOK, id=okId)
        self.okbutton.Bind(wx.EVT_SET_FOCUS, self.OnOKEnter)
        #hbox.Add(self.okbutton, 1, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER, 0)
        vbox.Add(self.okbutton, 0, wx.ALIGN_CENTER | wx.ALL, 2)

        self.SetSizer(vbox)
        vbox.Fit(self)
        self.Centre()

    def OnEngineEnter(self, event):
        global virtkeyboard, curfocus, curdialog
        if virtkeyboard is not None:
            virtkeyboard.Show()
        self.Raise()
        curfocus = self.etext
        curdialog = self

    def OnUsernameEnter(self, event):
        global virtkeyboard, curfocus, curdialog
        if virtkeyboard is not None:
            virtkeyboard.Show()
        self.Raise()
        curfocus = self.utext
        curdialog = self

    def OnPasswordEnter(self, event):
        global virtkeyboard, curfocus, curdialog
        if virtkeyboard is not None:
            virtkeyboard.Show()
        self.Raise()
        curfocus = self.ptext
        curdialog = self

    #def OnAutoEnter(self, event):
    #    global virtkeyboard, curfocus, curdialog
    #    if virtkeyboard is not None:
    #        virtkeyboard.Show(False)
    #    curfocus = self.abox
    #    curdialog = self

    def OnOKEnter(self, event):
        global virtkeyboard, curfocus, curdialog
        if virtkeyboard is not None:
            virtkeyboard.Show(False)
        curfocus = self.okbutton
        curdialog = self

    def OnEngine(self, event):
        global engine
        engine = event.GetString()


    def OnUsername(self, event):
        global username
        username = event.GetString()


    def OnPassword(self, event):
        global password
        password = event.GetString()

    def OnAbox(self, event):
        global auto
        auto = self.abox.GetValue()

    def OnOK(self, event):
        global logger
        logger.info('Login in to the virtualization engine as the specified user...')
        if not self.ValidateEngine():
            self.message.SetLabel('Engine Address Invalid!')
            self.message.SetForegroundColour((255, 0, 0))
            return
        if not self.ValidateUsername():
            self.message.SetLabel('User Authentication Failed!')
            self.message.SetForegroundColour((255, 0, 0))
            return
        self.message.SetLabel('')
        self.message.SetForegroundColour((0, 0, 0))
        SaveConfig()	#Save parameters in configuration file
        #self.EndModal(wx.ID_OK)
        self.Show(False)			#Hide the login dialog
        global desktopframe
        count = desktopframe.RefreshDesktops()	#Show the desktop frame
        desktopframe.Show(True)

    def ValidateEngine(self):
        #try:
        #    global engine
        #    addr = engine.strip().split('.')
        #except AttributeError:
        #    return False
        #try:
        #    #if not (len(addr) == 4 and all(int(octet) < 256 for octet in addr)):
        #    if not len(addr) >= 0:
        #        return False
        #except ValueError:
        #    return False
        try:
            FetchCA()
        except Exception, e:
            return False

        return True

    def ValidateUsername(self):
        try:
            global engine, username, password
            AuthUser()
            return True
        except Exception, e:
            logger.info('ValidateUsername: %s' % str(e))
            return False

    def OnExit(self, event):
        logger.info('Exiting...')
        global desktopframe
        desktopframe.Destroy()


class VirtKeyboard(wx.Frame):
  
    def __init__(self, parent, title):
        global virtkeyboard
        virtkeyboard = self
        #width, dummy = wx.DisplaySize()
        width = 900
        bwidth = width / 12
        bheight = bwidth * 4 / 5
        height = (bheight * 3) / 2 * 2
        platform = sys.platform
        if platform == 'win32':
            super(VirtKeyboard, self).__init__(parent, title=title, size=(width, height), style=wx.STAY_ON_TOP | wx.BORDER_NONE)
        else:          #linux2
            super(VirtKeyboard, self).__init__(parent, title=title, size=(width, height), style=wx.STAY_ON_TOP | wx.FRAME_TOOL_WINDOW | wx.FRAME_FLOAT_ON_PARENT | wx.BORDER_NONE)

        self.mode = 0
        self.position = 'top'

        #width = 996
        #height = 192
        #bwidth = (width - 0) / 12
        #bheight = (height - 0) / 3
 
        #New panel0
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        id_button_0_0 = wx.NewId()
        self.button_0_0 = wx.Button(self, id_button_0_0, 'ABC', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_0_0, id=id_button_0_0)
        hbox.Add(self.button_0_0, 0, wx.CENTER | wx.ALL, 0)

        id_button_0_1 = wx.NewId()
        self.button_0_1 = wx.Button(self, id_button_0_1, 'q', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_0_1, id=id_button_0_1)
        hbox.Add(self.button_0_1, 0, wx.CENTER | wx.ALL, 0)

        id_button_0_2 = wx.NewId()
        self.button_0_2 = wx.Button(self, id_button_0_2, 'w', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_0_2, id=id_button_0_2)
        hbox.Add(self.button_0_2, 0, wx.CENTER | wx.ALL, 0)

        id_button_0_3 = wx.NewId()
        self.button_0_3 = wx.Button(self, id_button_0_3, 'e', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_0_3, id=id_button_0_3)
        hbox.Add(self.button_0_3, 0, wx.CENTER | wx.ALL, 0)

        id_button_0_4 = wx.NewId()
        self.button_0_4 = wx.Button(self, id_button_0_4, 'r', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_0_4, id=id_button_0_4)
        hbox.Add(self.button_0_4, 0, wx.CENTER | wx.ALL, 0)

        id_button_0_5 = wx.NewId()
        self.button_0_5 = wx.Button(self, id_button_0_5, 't', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_0_5, id=id_button_0_5)
        hbox.Add(self.button_0_5, 0, wx.CENTER | wx.ALL, 0)

        id_button_0_6 = wx.NewId()
        self.button_0_6 = wx.Button(self, id_button_0_6, 'y', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_0_6, id=id_button_0_6)
        hbox.Add(self.button_0_6, 0, wx.CENTER | wx.ALL, 0)

        id_button_0_7 = wx.NewId()
        self.button_0_7 = wx.Button(self, id_button_0_7, 'u', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_0_7, id=id_button_0_7)
        hbox.Add(self.button_0_7, 0, wx.CENTER | wx.ALL, 0)

        id_button_0_8 = wx.NewId()
        self.button_0_8 = wx.Button(self, id_button_0_8, 'i', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_0_8, id=id_button_0_8)
        hbox.Add(self.button_0_8, 0, wx.CENTER | wx.ALL, 0)

        id_button_0_9 = wx.NewId()
        self.button_0_9 = wx.Button(self, id_button_0_9, 'o', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_0_9, id=id_button_0_9)
        hbox.Add(self.button_0_9, 0, wx.CENTER | wx.ALL, 0)

        id_button_0_A = wx.NewId()
        self.button_0_A = wx.Button(self, id_button_0_A, 'p', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_0_A, id=id_button_0_A)
        hbox.Add(self.button_0_A, 0, wx.CENTER | wx.ALL, 0)

        id_button_0_B = wx.NewId()
        self.button_0_B = wx.Button(self, id_button_0_B, 'BACK', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_0_B, id=id_button_0_B)
        hbox.Add(self.button_0_B, 0, wx.CENTER | wx.ALL, 0)

        vbox.Add(hbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        #New panel1
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        static_0 = wx.StaticText(self, -1, '', wx.DefaultPosition, (bwidth/2, bheight), 0)
        hbox.Add(static_0, 0, wx.CENTER | wx.ALL | wx.ALL, 0)

        id_button_1_0 = wx.NewId()
        self.button_1_0 = wx.Button(self, id_button_1_0, ',', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_1_0, id=id_button_1_0)
        hbox.Add(self.button_1_0, 0, wx.CENTER | wx.ALL, 0)

        id_button_1_1 = wx.NewId()
        self.button_1_1 = wx.Button(self, id_button_1_1, 'a', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_1_1, id=id_button_1_1)
        hbox.Add(self.button_1_1, 0, wx.CENTER | wx.ALL, 0)

        id_button_1_2 = wx.NewId()
        self.button_1_2 = wx.Button(self, id_button_1_2, 's', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_1_2, id=id_button_1_2)
        hbox.Add(self.button_1_2, 0, wx.CENTER | wx.ALL, 0)

        id_button_1_3 = wx.NewId()
        self.button_1_3 = wx.Button(self, id_button_1_3, 'd', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_1_3, id=id_button_1_3)
        hbox.Add(self.button_1_3, 0, wx.CENTER | wx.ALL, 0)

        id_button_1_4 = wx.NewId()
        self.button_1_4 = wx.Button(self, id_button_1_4, 'f', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_1_4, id=id_button_1_4)
        hbox.Add(self.button_1_4, 0, wx.CENTER | wx.ALL, 0)

        id_button_1_5 = wx.NewId()
        self.button_1_5 = wx.Button(self, id_button_1_5, 'g', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_1_5, id=id_button_1_5)
        hbox.Add(self.button_1_5, 0, wx.CENTER | wx.ALL, 0)

        id_button_1_6 = wx.NewId()
        self.button_1_6 = wx.Button(self, id_button_1_6, 'h', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_1_6, id=id_button_1_6)
        hbox.Add(self.button_1_6, 0, wx.CENTER | wx.ALL, 0)

        id_button_1_7 = wx.NewId()
        self.button_1_7 = wx.Button(self, id_button_1_7, 'j', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_1_7, id=id_button_1_7)
        hbox.Add(self.button_1_7, 0, wx.CENTER | wx.ALL, 0)

        id_button_1_8 = wx.NewId()
        self.button_1_8 = wx.Button(self, id_button_1_8, 'k', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_1_8, id=id_button_1_8)
        hbox.Add(self.button_1_8, 0, wx.CENTER | wx.ALL, 0)

        id_button_1_9 = wx.NewId()
        self.button_1_9 = wx.Button(self, id_button_1_9, 'l', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_1_9, id=id_button_1_9)
        hbox.Add(self.button_1_9, 0, wx.CENTER | wx.ALL, 0)

        id_button_1_A = wx.NewId()
        self.button_1_A = wx.Button(self, id_button_1_A, ':', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_1_A, id=id_button_1_A)
        hbox.Add(self.button_1_A, 0, wx.CENTER | wx.ALL, 0)

        static_1 = wx.StaticText(self, -1, '', size=(bwidth/2, bheight))
        hbox.Add(static_1, 0, wx.CENTER | wx.ALL, 0)

        vbox.Add(hbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        #New panel2
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        id_button_2_0 = wx.NewId()
        self.button_2_0 = wx.Button(self, id_button_2_0, 'TAB', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_2_0, id=id_button_2_0)
        hbox.Add(self.button_2_0, 0, wx.CENTER | wx.ALL, 0)

        id_button_2_1 = wx.NewId()
        self.button_2_1 = wx.Button(self, id_button_2_1, '.', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_2_1, id=id_button_2_1)
        hbox.Add(self.button_2_1, 0, wx.CENTER | wx.ALL, 0)

        id_button_2_2 = wx.NewId()
        self.button_2_2 = wx.Button(self, id_button_2_2, 'z', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_2_2, id=id_button_2_2)
        hbox.Add(self.button_2_2, 0, wx.CENTER | wx.ALL, 0)

        id_button_2_3 = wx.NewId()
        self.button_2_3 = wx.Button(self, id_button_2_3, 'x', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_2_3, id=id_button_2_3)
        hbox.Add(self.button_2_3, 0, wx.CENTER | wx.ALL, 0)

        id_button_2_4 = wx.NewId()
        self.button_2_4 = wx.Button(self, id_button_2_4, 'c', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_2_4, id=id_button_2_4)
        hbox.Add(self.button_2_4, 0, wx.CENTER | wx.ALL, 0)

        id_button_2_5 = wx.NewId()
        self.button_2_5 = wx.Button(self, id_button_2_5, 'v', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_2_5, id=id_button_2_5)
        hbox.Add(self.button_2_5, 0, wx.CENTER | wx.ALL, 0)

        id_button_2_6 = wx.NewId()
        self.button_2_6 = wx.Button(self, id_button_2_6, 'b', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_2_6, id=id_button_2_6)
        hbox.Add(self.button_2_6, 0, wx.CENTER | wx.ALL, 0)

        id_button_2_7 = wx.NewId()
        self.button_2_7 = wx.Button(self, id_button_2_7, 'n', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_2_7, id=id_button_2_7)
        hbox.Add(self.button_2_7, 0, wx.CENTER | wx.ALL, 0)

        id_button_2_8 = wx.NewId()
        self.button_2_8 = wx.Button(self, id_button_2_8, 'm', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_2_8, id=id_button_2_8)
        hbox.Add(self.button_2_8, 0, wx.CENTER | wx.ALL, 0)

        id_button_2_9 = wx.NewId()
        self.button_2_9 = wx.Button(self, id_button_2_9, '_', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_2_9, id=id_button_2_9)
        hbox.Add(self.button_2_9, 0, wx.CENTER | wx.ALL, 0)

        id_button_2_A = wx.NewId()
        self.button_2_A = wx.Button(self, id_button_2_A, '', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_2_A, id=id_button_2_A)
        hbox.Add(self.button_2_A, 0, wx.CENTER | wx.ALL, 0)

        id_button_2_B = wx.NewId()
        self.button_2_B = wx.Button(self, id_button_2_B, 'BOTTOM', wx.DefaultPosition, (bwidth, bheight), 0)
        self.Bind(wx.EVT_BUTTON, self.OnButton_2_B, id=id_button_2_B)
        hbox.Add(self.button_2_B, 0, wx.CENTER | wx.ALL, 0)

        vbox.Add(hbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        panel.SetSizer(vbox)
        panel.Layout()
        self.RefreshPosition()

    def RefreshLabel(self):
        if self.mode == 0:
            self.button_0_0.SetLabel('ABC')
            self.button_0_1.SetLabel('q')
            self.button_0_2.SetLabel('w')
            self.button_0_3.SetLabel('e')
            self.button_0_4.SetLabel('r')
            self.button_0_5.SetLabel('t')
            self.button_0_6.SetLabel('y')
            self.button_0_7.SetLabel('u')
            self.button_0_8.SetLabel('i')
            self.button_0_9.SetLabel('o')
            self.button_0_A.SetLabel('p')
            #self.button_0_B.SetLabel('BACKSPACE')
            self.button_1_0.SetLabel(',')
            self.button_1_1.SetLabel('a')
            self.button_1_2.SetLabel('s')
            self.button_1_3.SetLabel('d')
            self.button_1_4.SetLabel('f')
            self.button_1_5.SetLabel('g')
            self.button_1_6.SetLabel('h')
            self.button_1_7.SetLabel('j')
            self.button_1_8.SetLabel('k')
            self.button_1_9.SetLabel('l')
            self.button_1_A.SetLabel(':')
            #self.button_2_0.SetLabel('RELOCATE')
            self.button_2_1.SetLabel('.')
            self.button_2_2.SetLabel('z')
            self.button_2_3.SetLabel('x')
            self.button_2_4.SetLabel('c')
            self.button_2_5.SetLabel('v')
            self.button_2_6.SetLabel('b')
            self.button_2_7.SetLabel('n')
            self.button_2_8.SetLabel('m')
            self.button_2_9.SetLabel('_')
            self.button_2_A.SetLabel('')
        elif self.mode == 1:
            self.button_0_0.SetLabel('012')
            self.button_0_1.SetLabel('Q')
            self.button_0_2.SetLabel('W')
            self.button_0_3.SetLabel('E')
            self.button_0_4.SetLabel('R')
            self.button_0_5.SetLabel('T')
            self.button_0_6.SetLabel('Y')
            self.button_0_7.SetLabel('U')
            self.button_0_8.SetLabel('I')
            self.button_0_9.SetLabel('O')
            self.button_0_A.SetLabel('P')
            #self.button_0_B.SetLabel('BACKSPACE')
            self.button_1_0.SetLabel(',')
            self.button_1_1.SetLabel('A')
            self.button_1_2.SetLabel('S')
            self.button_1_3.SetLabel('D')
            self.button_1_4.SetLabel('F')
            self.button_1_5.SetLabel('G')
            self.button_1_6.SetLabel('H')
            self.button_1_7.SetLabel('J')
            self.button_1_8.SetLabel('K')
            self.button_1_9.SetLabel('L')
            self.button_1_A.SetLabel(':')
            #self.button_2_0.SetLabel('RELOCATE')
            self.button_2_1.SetLabel('.')
            self.button_2_2.SetLabel('Z')
            self.button_2_3.SetLabel('X')
            self.button_2_4.SetLabel('C')
            self.button_2_5.SetLabel('V')
            self.button_2_6.SetLabel('B')
            self.button_2_7.SetLabel('N')
            self.button_2_8.SetLabel('M')
            self.button_2_9.SetLabel('_')
            self.button_2_A.SetLabel('')
        elif self.mode == 2:
            self.button_0_0.SetLabel('abc')
            self.button_0_1.SetLabel('1')
            self.button_0_2.SetLabel('2')
            self.button_0_3.SetLabel('3')
            self.button_0_4.SetLabel('4')
            self.button_0_5.SetLabel('5')
            self.button_0_6.SetLabel('6')
            self.button_0_7.SetLabel('7')
            self.button_0_8.SetLabel('8')
            self.button_0_9.SetLabel('9')
            self.button_0_A.SetLabel('0')
            #self.button_0_B.SetLabel('BACKSPACE')
            self.button_1_0.SetLabel(',')
            self.button_1_1.SetLabel('(')
            self.button_1_2.SetLabel(')')
            self.button_1_3.SetLabel('+')
            self.button_1_4.SetLabel('-')
            self.button_1_5.SetLabel('=')
            self.button_1_6.SetLabel('\'')
            self.button_1_7.SetLabel('\"')
            self.button_1_8.SetLabel('/')
            self.button_1_9.SetLabel('\\')
            self.button_1_A.SetLabel(':')
            #self.button_2_0.SetLabel('RELOCATE')
            self.button_2_1.SetLabel('.')
            self.button_2_2.SetLabel('!')
            self.button_2_3.SetLabel('?')
            self.button_2_4.SetLabel('@')
            self.button_2_5.SetLabel('#')
            self.button_2_6.SetLabel('$')
            self.button_2_7.SetLabel('%')
            self.button_2_8.SetLabel('*')
            self.button_2_9.SetLabel('_')
            self.button_2_A.SetLabel('')
        else:
            raise Exception('Unexpected mode!')

    def OnButton_0_0(self, event):
        if self.mode == 0:
            self.mode = 1
        elif self.mode == 1:
            self.mode = 2
        elif self.mode == 2:
            self.mode = 0
        else:
            raise Exception('Unexpected mode!')
        self.RefreshLabel()

    def CharInput(self, char):
        global curfocus, ldialog
        if curfocus in [ldialog.sbutton, ldialog.okbutton]:
            return
        value = curfocus.GetValue()
        length = curfocus.GetLastPosition()
        current = curfocus.GetInsertionPoint()
        start, end = curfocus.GetSelection()
        if start == end:
            curfocus.SetValue(value[0:current] + char + value[current:length])
            curfocus.SetInsertionPoint(current+1)
        else:
            curfocus.SetValue(value[0:start] + char + value[end:length])
            curfocus.SetSelection(start, start)
            curfocus.SetInsertionPoint(start+1)
        curdialog.Raise()

    def OnButton_0_1(self, event):
        if self.mode == 0: self.CharInput('q')
        elif self.mode == 1: self.CharInput('Q')
        elif self.mode == 2: self.CharInput('1')
        else: raise Exception('Unexpected mode!')

    def OnButton_0_2(self, event):
        if self.mode == 0: self.CharInput('w')
        elif self.mode == 1: self.CharInput('W')
        elif self.mode == 2: self.CharInput('2')
        else: raise Exception('Unexpected mode!')

    def OnButton_0_3(self, event):
        if self.mode == 0: self.CharInput('e')
        elif self.mode == 1: self.CharInput('E')
        elif self.mode == 2: self.CharInput('3')
        else: raise Exception('Unexpected mode!')

    def OnButton_0_4(self, event):
        if self.mode == 0: self.CharInput('r')
        elif self.mode == 1: self.CharInput('R')
        elif self.mode == 2: self.CharInput('4')
        else: raise Exception('Unexpected mode!')

    def OnButton_0_5(self, event):
        if self.mode == 0: self.CharInput('t')
        elif self.mode == 1: self.CharInput('T')
        elif self.mode == 2: self.CharInput('5')
        else: raise Exception('Unexpected mode!')

    def OnButton_0_6(self, event):
        if self.mode == 0: self.CharInput('y')
        elif self.mode == 1: self.CharInput('Y')
        elif self.mode == 2: self.CharInput('6')
        else: raise Exception('Unexpected mode!')

    def OnButton_0_7(self, event):
        if self.mode == 0: self.CharInput('u')
        elif self.mode == 1: self.CharInput('U')
        elif self.mode == 2: self.CharInput('7')
        else: raise Exception('Unexpected mode!')

    def OnButton_0_8(self, event):
        if self.mode == 0: self.CharInput('i')
        elif self.mode == 1: self.CharInput('I')
        elif self.mode == 2: self.CharInput('8')
        else: raise Exception('Unexpected mode!')

    def OnButton_0_9(self, event):
        if self.mode == 0: self.CharInput('o')
        elif self.mode == 1: self.CharInput('O')
        elif self.mode == 2: self.CharInput('9')
        else: raise Exception('Unexpected mode!')

    def OnButton_0_A(self, event):
        if self.mode == 0: self.CharInput('p')
        elif self.mode == 1: self.CharInput('P')
        elif self.mode == 2: self.CharInput('0')
        else: raise Exception('Unexpected mode!')

    def OnButton_0_B(self, event):
        global curfocus, ldialog
        if curfocus in [ldialog.okbutton]:
            return
        value = curfocus.GetValue()
        length = curfocus.GetLastPosition()
        current = curfocus.GetInsertionPoint()
        start, end = curfocus.GetSelection()
        if start == end:
            if current > 0:
                curfocus.SetValue(value[0:current-1] + value[current:length])
                curfocus.SetInsertionPoint(current-1)
        else:
            curfocus.SetValue(value[0:start] + value[end:length])
            curfocus.SetSelection(start, start)
            curfocus.SetInsertionPoint(start)
        curdialog.Raise()

    def OnButton_1_0(self, event):
        self.CharInput(',')

    def OnButton_1_1(self, event):
        if self.mode == 0: self.CharInput('a')
        elif self.mode == 1: self.CharInput('A')
        elif self.mode == 2: self.CharInput('(')
        else: raise Exception('Unexpected mode!')

    def OnButton_1_2(self, event):
        if self.mode == 0: self.CharInput('s')
        elif self.mode == 1: self.CharInput('S')
        elif self.mode == 2: self.CharInput(')')
        else: raise Exception('Unexpected mode!')

    def OnButton_1_3(self, event):
        if self.mode == 0: self.CharInput('d')
        elif self.mode == 1: self.CharInput('D')
        elif self.mode == 2: self.CharInput('+')
        else: raise Exception('Unexpected mode!')

    def OnButton_1_4(self, event):
        if self.mode == 0: self.CharInput('f')
        elif self.mode == 1: self.CharInput('F')
        elif self.mode == 2: self.CharInput('-')
        else: raise Exception('Unexpected mode!')

    def OnButton_1_5(self, event):
        if self.mode == 0: self.CharInput('g')
        elif self.mode == 1: self.CharInput('G')
        elif self.mode == 2: self.CharInput('=')
        else: raise Exception('Unexpected mode!')

    def OnButton_1_6(self, event):
        if self.mode == 0: self.CharInput('h')
        elif self.mode == 1: self.CharInput('H')
        elif self.mode == 2: self.CharInput('\'')
        else: raise Exception('Unexpected mode!')

    def OnButton_1_7(self, event):
        if self.mode == 0: self.CharInput('j')
        elif self.mode == 1: self.CharInput('J')
        elif self.mode == 2: self.CharInput('\"')
        else: raise Exception('Unexpected mode!')

    def OnButton_1_8(self, event):
        if self.mode == 0: self.CharInput('k')
        elif self.mode == 1: self.CharInput('K')
        elif self.mode == 2: self.CharInput('/')
        else: raise Exception('Unexpected mode!')

    def OnButton_1_9(self, event):
        if self.mode == 0: self.CharInput('l')
        elif self.mode == 1: self.CharInput('L')
        elif self.mode == 2: self.CharInput('\\')
        else: raise Exception('Unexpected mode!')

    def OnButton_1_A(self, event):
        self.CharInput(':')

    def RefreshPosition(self):
        dw, dh = wx.DisplaySize()
        w, h = self.GetSize()
        if self.position == 'top':
            x = (dw - w) / 2
            y = 0
        elif self.position == 'bottom':
            x = (dw - w) / 2
            y = dh - h
        #elif self.position == 'left':
        #    x = 0
        #    y = (dh - h) / 2
        #elif self.position == 'right':
        #    x = dw - w
        #    y = (dh - h) / 2
        else:
            raise Exception('Unexpected location!')
        self.SetPosition((x, y))

    def OnButton_2_0(self, event):
        global curfocus, curdialog, ldialog
        if curfocus == ldialog.etext:
            ldialog.utext.SetFocus()
        elif curfocus == ldialog.utext:
            ldialog.ptext.SetFocus()
        elif curfocus == ldialog.ptext:
            ldialog.abox.SetFocus()
        #elif curfocus == ldialog.abox:
        #    ldialog.sbutton.SetFocus()
        #elif curfocus == ldialog.sbutton:
        #    ldialog.okbutton.SetFocus()
        elif curfocus == ldialog.okbutton:
            ldialog.etext.SetFocus()
        else:
            raise Exception('Unexpected focus!')
        curdialog.Raise()

    def OnButton_2_1(self, event):
        self.CharInput('.')

    def OnButton_2_2(self, event):
        if self.mode == 0: self.CharInput('z')
        elif self.mode == 1: self.CharInput('Z')
        elif self.mode == 2: self.CharInput('!')
        else: raise Exception('Unexpected mode!')

    def OnButton_2_3(self, event):
        if self.mode == 0: self.CharInput('x')
        elif self.mode == 1: self.CharInput('X')
        elif self.mode == 2: self.CharInput('?')
        else: raise Exception('Unexpected mode!')

    def OnButton_2_4(self, event):
        if self.mode == 0: self.CharInput('c')
        elif self.mode == 1: self.CharInput('C')
        elif self.mode == 2: self.CharInput('@')
        else: raise Exception('Unexpected mode!')

    def OnButton_2_5(self, event):
        if self.mode == 0: self.CharInput('v')
        elif self.mode == 1: self.CharInput('V')
        elif self.mode == 2: self.CharInput('#')
        else: raise Exception('Unexpected mode!')

    def OnButton_2_6(self, event):
        if self.mode == 0: self.CharInput('b')
        elif self.mode == 1: self.CharInput('B')
        elif self.mode == 2: self.CharInput('$')
        else: raise Exception('Unexpected mode!')

    def OnButton_2_7(self, event):
        if self.mode == 0: self.CharInput('n')
        elif self.mode == 1: self.CharInput('N')
        elif self.mode == 2: self.CharInput('%')
        else: raise Exception('Unexpected mode!')

    def OnButton_2_8(self, event):
        if self.mode == 0: self.CharInput('m')
        elif self.mode == 1: self.CharInput('M')
        elif self.mode == 2: self.CharInput('*')
        else: raise Exception('Unexpected mode!')

    def OnButton_2_9(self, event):
        self.CharInput('_')

    def OnButton_2_A(self, event):
        self.CharInput(' ')

    def OnButton_2_B(self, event):
        if self.position == 'bottom':
            self.position = 'top'
            self.button_2_B.SetLabel('BOTTOM')
        elif self.position == 'top':
            self.position = 'bottom'
            self.button_2_B.SetLabel('TOP')
        else:
            raise Exception('Unexpected location!')
        self.RefreshPosition()


class DesktopList(wx.ListCtrl):
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=(800, 570), style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        self.InsertColumn(0, "Name")
        self.InsertColumn(1, "Type")
        self.InsertColumn(2, "Status")

        self.SetColumnWidth(0, 280)
        self.SetColumnWidth(1, 250)
        self.SetColumnWidth(2, 250)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnClick)
        platform = sys.platform
        if platform == 'win32':
            self.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)
        else:          #linux2
            self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)

    def OnClick(self, event):
        global desktopframe
        desktopframe.RefreshMenu()

    def OnRightClick(self, event):
        self.startId = wx.NewId()
        self.stopId = wx.NewId()
        self.connectId = wx.NewId()

        self.Bind(wx.EVT_MENU, self.OnStart, id=self.startId)
        self.Bind(wx.EVT_MENU, self.OnStop, id=self.stopId)
        self.Bind(wx.EVT_MENU, self.OnConnect, id=self.connectId)

        menu = wx.Menu()
        menu.Append(self.startId, "Start")
        menu.Append(self.stopId, "Stop")
        menu.Append(self.connectId, "Connect")

        desktop = desktops[self.GetFirstSelected()]
        #Consider VM display type
        if desktop['status'] in ['up', 'powering_up']:
            menu.Enable(self.startId, False)
            menu.Enable(self.stopId, True)
            menu.Enable(self.connectId, True)
        elif desktop['status'] in ['down']:
            menu.Enable(self.startId, True)
            menu.Enable(self.stopId, False)
            menu.Enable(self.connectId, False)
        else:
            menu.Enable(self.startId, False)
            menu.Enable(self.stopId, False)
            menu.Enable(self.connectId, False)
        if desktop['type'] not in ['spice']:
            menu.Enable(self.startId, False)
            menu.Enable(self.stopId, False)
            menu.Enable(self.connectId, False)

        self.PopupMenu(menu)
        menu.Destroy()

    def OnStart(self, event):
        global logger
        desktop = desktops[self.GetFirstSelected()]
        logger.info('Starting %s' % desktop['name'])
        StartVm(desktop['id'])

    def OnStop(self, event):
        global logger
        desktop = desktops[self.GetFirstSelected()]
        logger.info('Stopping %s' % desktop['name'])
        StopVm(desktop['id'])

    def OnConnect(self, event):
        global logger
        desktop = desktops[self.GetFirstSelected()]
        logger.info('Connecting to %s' % desktop['name'])
        ConnectVm(desktop['id'], desktop['port'], desktop['sport'])

    def Populate(self):
        global desktops, logger
        for desktop in desktops:
            try:
                index = self.InsertStringItem(sys.maxint, desktop['name'])
                self.SetStringItem(index, 1, desktop['type'])
                self.SetStringItem(index, 2, desktop['status'])
            except Exception, e:
                logger.info('Failed to add desktop %s to the list!' % desktop['name'])
                pass
        self.First()

    def Clear(self):
        self.DeleteAllItems()

    def First(self):
        global logger
        logger.info('First()')
        count = self.GetItemCount()
        if count == 0:
            return
        current = self.GetFirstSelected()
        logger.info('count:%s, current=%s' % (count, current))
        if current != -1:
            self.Select(current, False)
        self.Select(0, True)
        current = self.GetFirstSelected()
        logger.info('count:%s, current=%s' % (count, current))

    def Down(self):
        global logger
        logger.info('Down()')
        count = self.GetItemCount()
        if count == 0:
            return
        current = self.GetFirstSelected()
        if current == -1:
            return
        logger.info('count:%s, current=%s' % (count, current))
        if current < count-1:
            self.Select(current, False)
            self.Select(current+1, True)
        current = self.GetFirstSelected()
        logger.info('count:%s, current=%s' % (count, current))

    def PageDown(self):
        global logger
        logger.info('PageDown()')
        count = self.GetItemCount()
        if count == 0:
            return
        current = self.GetFirstSelected()
        if current == -1:
            return
        logger.info('count:%s, current=%s' % (count, current))
        if current < count-10:
            self.Select(current, False)
            self.Select(current+10, True)
            return
        if current < count-1:
            self.Select(current, False)
            self.Select(count-1, True)
        current = self.GetFirstSelected()
        logger.info('count:%s, current=%s' % (count, current))

    def PageUp(self):
        global logger
        logger.info('PageUp()')
        count = self.GetItemCount()
        if count == 0:
            return
        current = self.GetFirstSelected()
        if current == -1:
            return
        logger.info('count:%s, current=%s' % (count, current))
        if current > 10:
            self.Select(current, False)
            self.Select(current-10, True)
            return
        if current > 0:
            self.Select(current, False)
            self.Select(0, True)
        current = self.GetFirstSelected()
        logger.info('count:%s, current=%s' % (count, current))


    def Up(self):
        global logger
        logger.info('Up()')
        count = self.GetItemCount()
        if count == 0:
            return
        current = self.GetFirstSelected()
        if current == -1:
            return
        logger.info('count:%s, current=%s' % (count, current))
        if current > 0:
            self.Select(current, False)
            self.Select(current-1, True)
        current = self.GetFirstSelected()
        logger.info('count:%s, current=%s' % (count, current))


    def Last(self):
        global logger
        logger.info('Last()')
        count = self.GetItemCount()
        if count == 0:
            return
        current = self.GetFirstSelected()
        logger.info('count:%s, current=%s' % (count, current))
        if current != -1:
            self.Select(current, False)
        self.Select(count-1, True)
        current = self.GetFirstSelected()
        logger.info('count:%s, current=%s' % (count, current))


class DesktopFrame(wx.Frame):
    def __init__(self, title, config=None, log=None):
        global desktopframe, ldialog, desktops, autologin, autoconnect, logger
        desktopframe = self

        global cfile, lfile
        if config is not None:
            cfile = config

        if log is not None:
            lfile = log

        InitLog()
        LoadConfig()

        wx.Frame.__init__(self, None, title=title, size=(800,600), style=0)	#(wx.CAPTION | wx.CLOSE_BOX))

        #self.CreateStatusBar()

        if showmenu == 'True':
            logger.info('Building menu bar...')
            appmenu = wx.Menu()
            menuRefreshList = appmenu.Append(wx.NewId(), "Refresh List", "Refresh the desktop list assign to me")
            menuLoginAgain = appmenu.Append(wx.NewId(), "Login Again", "Login with a different account")
            appmenu.AppendSeparator()
            menuExit = appmenu.Append(wx.NewId(), "Exit", "Exit from this client.")

            selmenu = wx.Menu()
            self.menuFirst = selmenu.Append(wx.NewId(), "First", "Go to the first desktop")
            self.menuDown = selmenu.Append(wx.NewId(), "Down", "Go to the next desktop")
            self.menuPageDown = selmenu.Append(wx.NewId(), "Page Down", "Go to the next batch desktop")
            self.menuPageUp = selmenu.Append(wx.NewId(), "Page Up", "Go to the previous batch desktop")
            self.menuUp = selmenu.Append(wx.NewId(), "Up", "Go to the previous desktop")
            self.menuLast = selmenu.Append(wx.NewId(), "Last", "Go to the last desktop")

            actmenu = wx.Menu()
            self.menuStart = actmenu.Append(wx.NewId(), "Start", "Start this desktop")
            self.menuStop = actmenu.Append(wx.NewId(), "Stop", "Stop this desktop")
            self.menuConnect = actmenu.Append(wx.NewId(), "Connect", "Connect to this desktop")

            hlpmenu = wx.Menu()
            self.menuAbout = hlpmenu.Append(wx.NewId(), "About", "About me")

            menubar = wx.MenuBar()
            menubar.Append(appmenu, "Application")
            menubar.Append(selmenu, "Selection")
            menubar.Append(actmenu, "Activity")
            menubar.Append(hlpmenu, "Help")
            self.SetMenuBar(menubar)

            self.Bind(wx.EVT_MENU, self.OnRefreshList, menuRefreshList)
            self.Bind(wx.EVT_MENU, self.OnLoginAgain, menuLoginAgain)
            self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

            self.Bind(wx.EVT_MENU, self.OnFirst, self.menuFirst)
            self.Bind(wx.EVT_MENU, self.OnDown, self.menuDown)
            self.Bind(wx.EVT_MENU, self.OnPageDown, self.menuPageDown)
            self.Bind(wx.EVT_MENU, self.OnPageUp, self.menuPageUp)
            self.Bind(wx.EVT_MENU, self.OnUp, self.menuUp)
            self.Bind(wx.EVT_MENU, self.OnLast, self.menuLast)

            self.Bind(wx.EVT_MENU, self.OnStart, self.menuStart)
            self.Bind(wx.EVT_MENU, self.OnStop, self.menuStop)
            self.Bind(wx.EVT_MENU, self.OnConnect, self.menuConnect)

            self.Bind(wx.EVT_MENU, self.OnAbout, self.menuAbout)

        logger.info('Building accelerator...')
        aRefreshListId = wx.NewId()
        aLoginAgainId = wx.NewId()
        aExitId = wx.NewId()
        aFirstId = wx.NewId()
        aDownId = wx.NewId()
        aPageDownId = wx.NewId()
        aPageUpId = wx.NewId()
        aUpId = wx.NewId()
        aLastId = wx.NewId()
        aStartId = wx.NewId()
        aStopId = wx.NewId()
        aConnectId = wx.NewId()
        aAboutId = wx.NewId()
        self.Bind(wx.EVT_MENU, self.OnRefreshList, id=aRefreshListId)
        self.Bind(wx.EVT_MENU, self.OnLoginAgain, id=aLoginAgainId)
        self.Bind(wx.EVT_MENU, self.OnExit, id=aExitId)
        self.Bind(wx.EVT_MENU, self.OnFirst, id=aFirstId)
        self.Bind(wx.EVT_MENU, self.OnDown, id=aDownId)
        self.Bind(wx.EVT_MENU, self.OnPageDown, id=aPageDownId)
        self.Bind(wx.EVT_MENU, self.OnPageUp, id=aPageUpId)
        self.Bind(wx.EVT_MENU, self.OnUp, id=aUpId)
        self.Bind(wx.EVT_MENU, self.OnLast, id=aLastId)
        self.Bind(wx.EVT_MENU, self.OnStart, id=aStartId)
        self.Bind(wx.EVT_MENU, self.OnStop, id=aStopId)
        self.Bind(wx.EVT_MENU, self.OnConnect, id=aConnectId)
        self.Bind(wx.EVT_MENU, self.OnAbout, id=aAboutId)
        atable = wx.AcceleratorTable([(wx.ACCEL_NORMAL, wx.WXK_F5, aRefreshListId),	#F5
                                      (wx.ACCEL_CTRL, wx.WXK_ESCAPE, aLoginAgainId),	#CTRL-ESC
                                      (wx.ACCEL_CTRL, ord('X'), aExitId),		#CTRL-X
                                      (wx.ACCEL_NORMAL, wx.WXK_HOME, aFirstId),		#HOME
                                      (wx.ACCEL_NORMAL, wx.WXK_DOWN, aDownId),		#DOWN
                                      (wx.ACCEL_NORMAL, wx.WXK_PAGEDOWN, aPageDownId),	#PAGEDOWN
                                      (wx.ACCEL_NORMAL, wx.WXK_PAGEUP, aPageUpId),	#PAGEUP
                                      (wx.ACCEL_NORMAL, wx.WXK_UP, aUpId),		#UP
                                      (wx.ACCEL_NORMAL, wx.WXK_END, aLastId),		#END
                                      (wx.ACCEL_NORMAL, wx.WXK_RETURN, aConnectId),     #ENTER
                                      (wx.ACCEL_CTRL, wx.WXK_RETURN, aConnectId),	#ENTER
                                      (wx.ACCEL_CTRL, wx.WXK_UP, aStartId),             #CTRL-UP
                                      (wx.ACCEL_CTRL, wx.WXK_DOWN, aStopId),            #CTRL_DOWN
                                      (wx.ACCEL_CTRL, ord('A'), aAboutId)               #CTRL-A
                                     ])
        self.SetAcceleratorTable(atable)

        #panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        logger.info('Creating desktop list...')
        self.dlist = DesktopList(self, wx.NewId(), style=wx.LC_REPORT | wx.BORDER_NONE | wx.LC_SINGLE_SEL)
        self.dlist.SetFocus()
        #self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnConnect, self.dlist)
        vbox.Add(self.dlist, 1, wx.EXPAND)
        self.SetSizer(vbox)
        self.SetAutoLayout(True)
        self.Centre()

        global vkbd
        if vkbd == 'True':
            virtkeyboard = VirtKeyboard(None, title='VirtKeyboard')

        ldialog = LoginDialog(None, wx.ID_ANY, 'Login')
        logger.info('LoginDialog constructed, but autologin=%s' % autologin)
        if autologin == 'True':
            #The following logic is similar to OnOK in LoginDialog
            logger.info('Auto login...')
            try:
                FetchCA()
                AuthUser()
                count = self.RefreshDesktops()
                if autoconnect == 'True' and count == 1:
                    logger.info('Auto connect...')
                    desktop = desktops[0]
                    if desktops[0]['status'] in ['up', 'powering_up']:
                        logger.info('Connecting to %s' % desktop['name'])
                        ConnectVm(desktop['id'], desktop['port'], desktop['sport'])
                        self.Destroy()
                        #if ldialog:
                        #    ldialog.Destroy()
                        #self.Close(True)
                    else:
                        self.Show(True)
                else:
                    self.Show(True)
            except Exception, e:
                ldialog.Show()
        else:
            ldialog.Show()

    def RefreshMenu(self):
        global desktops, showmenu
        if showmenu == 'False':
            return
        current = self.dlist.GetFirstSelected()
        total = self.dlist.GetItemCount()
        if current == total-1:
            self.menuLast.Enable(False)
            self.menuDown.Enable(False)
            self.menuPageDown.Enable(False)
            self.menuFirst.Enable(True)
            self.menuUp.Enable(True)
            self.menuPageUp.Enable(True)
        elif current == 0:
            self.menuLast.Enable(True)
            self.menuDown.Enable(True)
            self.menuPageDown.Enable(True)
            self.menuFirst.Enable(False)
            self.menuUp.Enable(False)
            self.menuPageUp.Enable(False)
        else:
            self.menuLast.Enable(True)
            self.menuDown.Enable(True)
            self.menuPageDown.Enable(True)
            self.menuFirst.Enable(True)
            self.menuUp.Enable(True)
            self.menuPageUp.Enable(True)

        if current == -1:
            self.menuStart.Enable(False)
            self.menuStop.Enable(False)
            self.menuConnect.Enable(False)
        desktop = desktops[current]
        if desktop['status'] in ['up', 'powering_up']:
            self.menuStart.Enable(False)
            self.menuStop.Enable(True)
            self.menuConnect.Enable(True)
        elif desktop['status'] in ['down']:
            self.menuStart.Enable(True)
            self.menuStop.Enable(False)
            self.menuConnect.Enable(False)
        else:
            self.menuStart.Enable(False)
            self.menuStop.Enable(False)
            self.menuConnect.Enable(False)
        if desktop['type'] not in ['spice']:
            self.menuStart.Enable(False)
            self.menuStop.Enable(False)
            self.menuConnect.Enable(False)

    def Destroy(self):
        global ldialog, virtkeyboard
        if ldialog:
            ldialog.Destroy()
        if virtkeyboard:
            virtkeyboard.Close(True)
        self.Close(True)

    def OnExit(self, event):
        self.Destroy()

    def OnAbout(self, event):
        about = wx.MessageDialog(None, 'Dedicated for Virtfan Virtualization Platform, this virtualization client (version 2.6) can be used to list, start, stop and connect to desktops assigned to any specified user.\nAccelerator keys are as follows:\nRefreshList\tF5\nLogin Again\tCTRL-ESC\nExit\t\tCTRL-X\nFirst\t\tHOME\nDown\t\tDOWN\nPage Down\tPGDN\nPage Up\tPGUP\nUp\t\tUP\nLast\t\tEND\nStart\t\tCTRL-UP\nStop\t\tCTRL-DOWN\nConnect\tCTRL-ENTER\nAbout\t\tCTRL-A', 'About me', wx.OK | wx.ICON_INFORMATION)
        about.ShowModal() 
        
    def RetrieveDesktops(self):
        global desktops, logger
        try:
            desktops = sorted(ListVms(), key=lambda k:k['name'])
            return len(desktops)
        except Exception, e:
            logger.info('RetrieveDesktops: %s' % str(e))
            return 0

    def RefreshDesktops(self):
        self.dlist.Clear()
        count = self.RetrieveDesktops()
        self.dlist.Populate()
        return count

    def OnRefreshList(self, event):
        self.RefreshDesktops()

    def OnLoginAgain(self, event):
        self.Show(False)
        global ldialog
        if ldialog is None:
            ldialog = LoginDialog(None, wx.ID_ANY, 'Login')
        ldialog.utext.SetFocus()
        ldialog.Show()

    def OnFirst(self, event):
        self.dlist.First()
        self.RefreshMenu()

    def OnDown(self, event):
        self.dlist.Down()
        self.RefreshMenu()

    def OnPageDown(self, event):
        self.dlist.PageDown()
        self.RefreshMenu()

    def OnPageUp(self, event):
        self.dlist.PageUp()
        self.RefreshMenu()

    def OnUp(self, event):
        self.dlist.Up()
        self.RefreshMenu()

    def OnLast(self, event):
        self.dlist.Last()
        self.RefreshMenu()

    def OnStart(self, event):
        global desktops, logger
        desktop = desktops[self.dlist.GetFirstSelected()]
        logger.info('Starting %s' % desktop['name'])
        StartVm(desktop['id'])

    def OnStop(self, event):
        global desktops, logger
        desktop = desktops[self.dlist.GetFirstSelected()]
        logger.info('Stopping %s' % desktop['name'])
        StopVm(desktop['id'])

    def OnConnect(self, event):
        global desktops, logger
        desktop = desktops[self.dlist.GetFirstSelected()]
        logger.info('Connecting to %s' % desktop['name'])
        ConnectVm(desktop['id'], desktop['port'], desktop['sport'])


if __name__=='__main__':
    app = wx.App(redirect=False)   # Error messages go to popup window
    #app = wx.App(True)
    desktopframe = DesktopFrame("Virtfan Virtualization Desktop Client")
    app.MainLoop()

