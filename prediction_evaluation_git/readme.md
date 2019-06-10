# Toolkit for ApolloScape Dataset 

## Introduction
This is a repo of toolkit for dataset of [ApolloScape CVPR 2019 Workshop on Autonomous Driving Challenge](http://wad.ai/). It include three tasks, **Trajectory Prediction, 3D Lidar Object Detection and 3D Lidar Object Tracking**, also it includes toolkit for lanemark segmentation, online self-localization, 3D car instance understanding. Some example videos and images are shown below:

evaluation.py is the evaluation code. Run the code for a sample evaluation:
python?evaluation.py?--object_file=./test_eval_data/considered_objects.txt --gt_dir=./test_eval_data/prediction_gt.txt --res_file=./test_eval_data/prediction_result.txt

Run 
```
./test_eval_data/considered_objects.txt contains objects we consider when counting the error.
./test_eval_data/prediction_gt.txt is just for testing the code which is not the real ground truth. Please submit your result to the leaderboard to get true error.
./test_eval_data/prediction_result.txt is one example for submitted result.
```


