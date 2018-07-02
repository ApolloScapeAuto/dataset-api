#!/bin/bash
# make sure pip and setuptools are available on your system

curr_dir=`pwd`
cd thirdParty/cityscapesScripts/
if [ -f "__init__.py" ]; then
    rm __init__.py
fi
python setup.py build_ext --inplace
touch __init__.py
cd $curr_dir
