#!/bin/bash
sudo find /private/var/folders/ \( -name com.apple.dock.iconcache -or -name com.apple.iconservices \) -exec rm -rfv {} \;
sudo rm -rf /Library/Caches/com.apple.iconservices.store;
killall Dock
killall Finder
