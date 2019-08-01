# The 3D Lidar Object Detection and Tracking Challenge of Apolloscape Dataset
[For detail and download](http://apolloscape.auto/tracking.html)

## Introduction
Our 3D Lidar object detection and tracking dataset consists of LiDAR scanned point clouds with high quality annotation. It is collected under various lighting conditions and traffic densities in Beijing, China. More specifically, it contains highly complicated traffic flows mixed with vehicles, cyclists, and pedestrians.

![](../examples/3d-tracking.gif)



## Evaluation
eval.py is the evaluation code. Run the code for a sample evaluation:

```
# export NUMBA_ENABLE_CUDASIM=1

# detection
python eval.py --gtPath=apollo_lab_test --dtPath=apollo_res_test --apSampleNum=10 #--typeFilterFlag #2>&1 | tee run.log

# tracking
# python eval.py --modeType=tracking --gtPath=../track/apollo_lab --dtPath=../track/apollo_res --typeFilterFlag
```

## Submission of data format
Submit your result for online evaluation here: [Submit](http://apolloscape.auto/submit.html)

[Leaderboard](http://apolloscape.auto/leader_board.html)


## Contact
Please feel free to contact us, or raise an issue with any questions, suggestions or comments:
* apollo-scape@baidu.com
