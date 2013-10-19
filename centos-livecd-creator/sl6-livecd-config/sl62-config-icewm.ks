#
# sl62-config-icewm.ks
#
# Configures iceWM
#

%post

mkdir -p /etc/icewm

cat > /etc/icewm/menu << EOF
prog xterm xterm xterm -sb
prog rxvt xterm rxvt -bg black -cr green -fg white -C -fn 9x15 -sl 500
prog urxvt xterm urxvt -bg black -cr green -fg white -C -fn 9x15 -sl 500
# prog MC mc xterm -geometry 100x30 -e mc
prog Xfe xfe xfe
separator
prog Emacs emacs emacs
prog XEmacs emacs xemacs
prog NEdit nedit nedit
prog Vim vim xterm -geometry 100x30 -e vim
separator
prog Gftp gftp gftp
prog Firefox firefox firefox
prog Thunderbird thunderbird thunderbird
prog XChat xchat xchat
prog Gaim gaim gaim
separator
prog GPicView gpicview gpicview
prog Gimp gimp gimp
prog OpenOffice soffice soffice
prog GCalcTool gcalctool gcalctool
separator
prog Gparted gparted gparted
prog Ethereal ethereal ethereal
prog NXclient nxclient nxclient
prog Vncviewer vncviewer vncviewer
prog Xcdroast xcdroast xcdroast
prog "Network manager applet" nm-applet nm-applet
prog "Configure display" gnome-display-properties
prog "Configure keyboard" system-config-keyboard system-config-keyboard
#prog system-config-network system-config-network xterm -geometry 100x30 -e system-config-network
prog "Configure firewall" system-config-firewall xterm -e "su - -c system-config-firewall"
prog "Configure date and time" system-config-date system-config-date
prog "Configure services" system-config-services system-config-services
prog "Configure users" system-config-users system-config-users
separator
prog Poweroff poweroff poweroff
prog Reboot reboot reboot
prog "Install to Hard Drive" liveinst liveinst
EOF

%end
