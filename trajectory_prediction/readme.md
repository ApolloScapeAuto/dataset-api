# The Trajectory Prediction Challenge of Apolloscapes Dataset
ApolloScape Trajectory dataset and 3D Lidar Object Detection and Tracking dataset including about 100K image frames, 80k lidar point cloud and 1000km trajectories for urban traffic. The dataset consisting of varying conditions and traffic densities which includes many challenging scenarios where vehicles, bicycles, and pedestrians move among one another. 
[For detail and download](http://apolloscape.auto/trajectory.html)

```
wget https://ad-apolloscape.cdn.bcebos.com/trajectory/prediction_train.zip
wget https://ad-apolloscape.cdn.bcebos.com/trajectory/prediction_test.zip

```

## Introduction
This repository contains the evaluation scripts for the trajectory prediction challenge of the ApolloScapes dataset. Our trajectory dataset consists of camera-based images, LiDAR scanned point clouds, and manually annotated trajectories. It is collected under various lighting conditions and traffic densities in Beijing, China. More specifically, it contains highly complicated traffic flows mixed with vehicles, riders, and pedestrians.

![](../examples/trajectory-prediction.gif)

## Dataset download
[sample_trajectory.zip](https://ad-apolloscape.cdn.bcebos.com/trajectory/sample_trajectory.zip")
[sample_image.zip](https://ad-apolloscape.cdn.bcebos.com/trajectory/sample_image.zip")

[prediction_test.zip](https://ad-apolloscape.cdn.bcebos.com/prediction_data%2Fprediction_test.zip)
[prediction_train.zip](https://ad-apolloscape.cdn.bcebos.com/prediction_data%2Fprediction_train.zip)

## Evaluation
evaluation.py is the evaluation code. Run the code for a sample evaluation:

```
python evaluation.py --object_file=./test_eval_data/considered_objects.txt --gt_dir=./test_eval_data/prediction_gt.txt --res_file=./test_eval_data/prediction_result.txt
./test_eval_data/considered_objects.txt contains objects we consider when counting the error.
./test_eval_data/prediction_gt.txt is just for testing the code which is not the real ground truth. Please submit your result to the leaderboard to get true error.
./test_eval_data/prediction_result.txt is one example for submitted result.
```

## Submission of data format
Submit your result for online evaluation here: [Submit](http://apolloscape.auto/submit.html)

Leaderboard: [Leaderboard](http://apolloscape.auto/leader_board.html)

## Publication
Please cite our paper in your publications if our dataset is used in your research.

TrafficPredict: Trajectory Prediction for Heterogeneous Traffic-Agents. [PDF](https://arxiv.org/abs/1811.02146)
[BibTex](https://ad-apolloscape.cdn.bcebos.com/TrafficPredict/trafficpredict_bibtex.txt) [Website](http://gamma.cs.unc.edu/TPredict/TrafficPredict.html)

Yuexin Ma, Xinge Zhu, Sibo Zhang, Ruigang Yang, Wenping Wang, and Dinesh Manocha.

AAAI(oral), 2019

```
@inproceedings{ma2019trafficpredict,
  title={Trafficpredict: Trajectory prediction for heterogeneous traffic-agents},
  author={Ma, Yuexin and Zhu, Xinge and Zhang, Sibo and Yang, Ruigang and Wang, Wenping and Manocha, Dinesh},
  booktitle={Proceedings of the AAAI Conference on Artificial Intelligence},
  volume={33},
  pages={6120--6127},
  year={2019}
}
```

