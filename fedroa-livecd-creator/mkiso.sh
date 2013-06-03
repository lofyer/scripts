#!/bin/bash
livecd-creator --verbose \
--fslabel=Virtfan-Fedora.iso \
--config=my.ks \
-t /home/tmp/tmp \
--cache=/home/tmp \
--cacheonly \
--nocleanup
