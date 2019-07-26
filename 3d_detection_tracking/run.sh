#!/bin/bash

source activate apolloscape

# export NUMBA_ENABLE_CUDASIM=1

# tracking
python eval.py --modeType=tracking --gtPath=../track/apollo_lab --dtPath=../track/apollo_res --typeFilterFlag
# detection
# python eval.py --gtPath=apollo_lab_test --dtPath=apollo_res_test --apSampleNum=10 #--typeFilterFlag #2>&1 | tee run.log
