#!/bin/bash
# Split archives
7z -v4g a my_zip.7z my_folder/

# Hide filename
7z a archive.7z -mhe -pPASSWORD files
