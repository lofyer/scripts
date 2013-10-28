#!/bin/bash
#yum install ImageMagick
convert back.png -resize 640x480 -colors 14 -depth 16 -normalize -verbose splash.xpm
gzip -9 splash.xpm
#cp splash.xpm.gz /boot/grub/
