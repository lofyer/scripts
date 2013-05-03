#!/bin/bash
genkernel --menuconfig --kernel-config="$PWD/.config" --kerneldir="$PWD" --no-clean --no-mrproper --ramdisk-modules  all
