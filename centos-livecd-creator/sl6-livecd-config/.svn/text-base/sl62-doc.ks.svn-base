########################################################################
#
# sl62-doc.ks
#
# Create /usr/share/doc/HTML/index.html 
# A short documentation for Scientific Linux Live CD/DVD
#
########################################################################

%post

# get SL release version and date
version=$( grep -o [0-9].[0-9] /etc/redhat-release )
date=$( date "+%A, %d-%B-%Y" )

# get SL logo
cp /usr/share/doc/sl-release-notes-$version/images/sl-logo-96.png /usr/share/doc/HTML/sl-logo-96.png
if [ ! -e /usr/share/doc/HTML/sl-logo-96.png ]; then
   wget --timeout=20 http://131.225.111.32/documentation/graphics/logo/sl-logo-96.png -O /usr/share/doc/HTML/sl-logo-96.png
fi
if [ ! -e /usr/share/doc/HTML/sl-logo-96.png ]; then
   wget --timeout=20 http://129.132.221.163/sl-logo-96.png -O /usr/share/doc/HTML/sl-logo-96.png
fi

cat > /usr/share/doc/HTML/index.html << EOF
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title>Scientific Linux ${version} Live</title>
<style type="text/css" media="all">@import "layout.css";</style>
</head>
<body>
<center>
<img SRC='sl-logo-96.png' ALT='SL-Logo'><br><br>
<h1>Welcome to Scientific Linux ${version} Live</h1>
</center>
<p>The <b>Scientific Linux Live CD/DVD</b> is a bootable CD/DVD that runs Linux directly from
CD/DVD without installing. It is based on <a href="https://www.scientificlinux.org/"> Scientific Linux</a> (SL),
which is recompiled from <a href="http://www.redhat.com/software/rhel/">RedHat Enterprise Linux</a> (RHEL) sources.<br>
The Live CD/DVD has a read-write rootfs and squashfs provides on-the-fly decompression that allows to store 
2 GB software on a normal CD-ROM. It can be installed on hard disk or usb drive with persistent changes.
The Live CD/DVDs were built using the <a href="http://fedoraproject.org/wiki/FedoraLiveCD">Fedora LiveCD Tools</a>.</p>
<p>For more information visit the <a href="http://www.livecd.ethz.ch/">Scientific Linux Live Homepage</a>.</p>
<p align=right>Last modified: ${date} by Urs Beyerle</p>
</body>
</html>
EOF

cat > /usr/share/doc/HTML/layout.css << EOF
body {
        margin:10px;
        padding:10px;
        font-family:verdana, arial, helvetica, sans-serif;
        color:#333;
        background-color:white;
        }
h1 {
        margin:5px 5px 15px 0px;
        padding:0px;
        font-size:24px;
        line-height:24px;
        font-weight:900;
        color:#333;
        }
p {
        font:12px/20px verdana, arial, helvetica, sans-serif;
        margin:0px 0px 14px 0px;
        padding:3px;
        }
li {
        font:12px/20px verdana, arial, helvetica, sans-serif;
        margin:0px 0px 0px 0px;
        padding:0px;
        }
a {
        color:#09c;
        font-size:12px;
        text-decoration:none;
        font-weight:600;
        font-family:verdana, arial, helvetica, sans-serif;
        }
a:link {color:#05a;}
a:visited {color:#058;}
a:hover {background-color:#eee;}
EOF

%end
