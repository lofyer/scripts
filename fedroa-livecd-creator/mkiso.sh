#!/bin/bash
livecd-creator --verbose \
--fslabel=Virtfan-Fedora-0706 \
--config=/usr/share/spin-kickstarts/fedora-livecd-desktop.ks \
--cache=/home/tmp \
--cacheonly
#--nocleanup
