#!/bin/bash
# make sure pip and setuptools are available on your system

cd renderer/
python setup.py build_ext --inplace
curr_dir=`pwd`
cd $curr_dir
