#!/bin/bash
rm -fr build *.c *.so
python3 setup.py build_ext --inplace
