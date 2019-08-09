#!/bin/bash

# detection
python eval.py --gtPath=apollo_lab_test --dtPath=apollo_res_test --apSampleNum=10 #--typeFilterFlag #2>&1 | tee run.log

# tracking
# python eval.py --modeType=tracking --gtPath=../track/apollo_lab --dtPath=../track/apollo_res --typeFilterFlag

