#!/bin/bash
rpm2cpio $1|cpio -dimv
