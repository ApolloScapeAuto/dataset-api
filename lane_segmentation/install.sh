#!/bin/bash
# make sure pip and setuptools are available on your system

pip install -r requirements.txt
curr_dir=`pwd`
<<<<<<< 49d5b0ccba1081bb6fe0abb57fb6c311e165dbe7

=======
>>>>>>> updated version zdf
cd thirdParty/cityscapesScripts/
if [ -f "__init__.py" ]; then
    rm __init__.py
fi
python setup.py build_ext --inplace
touch __init__.py
cd $curr_dir
