# The Trajectory Prediction Challenge of Apolloscapes Dataset
ApolloScape Trajectory dataset and 3D Lidar Object Detection and Tracking dataset including about 100K image frames, 80k lidar point cloud and 1000km trajectories for urban traffic. The dataset consisting of varying conditions and traffic densities which includes many challenging scenarios where vehicles, bicycles, and pedestrians move among one another. 
[Dataset detail and download](http://apolloscape.auto/trajectory.html)

[![Depth Guided Video Inpainting for Autonomous Driving](https://res.cloudinary.com/marcomontalbano/image/upload/v1595308447/video_to_markdown/images/youtube--dST6NDxEMU8-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=dST6NDxEMU8 "Depth Guided Video Inpainting for Autonomous Driving")

CVPR 2019 WAD Challenge on Trajectory Prediction and 3D Perception. [PDF](https://arxiv.org/pdf/2004.05966.pdf) [Website](http://wad.ai/2019/challenge.html)


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

CVPR 2019 WAD Challenge on Trajectory Prediction and 3D Perception. [PDF](https://arxiv.org/pdf/2004.05966.pdf)
[BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:FM7KYweYqXIJ:scholar.google.com/&output=citation&scisdr=CgXjlNWZEK_chmykD1s:AAGBfm0AAAAAXpihF1tMiyTTew20m4a1LnPyWo9u5cbl&scisig=AAGBfm0AAAAAXpihF_RACGUoa0RN86NWhguFI1Z2YqmE&scisf=4&ct=citation&cd=-1&hl=en)

```
@article{zhang2020cvpr,
  title={CVPR 2019 WAD Challenge on Trajectory Prediction and 3D Perception},
  author={Zhang, Sibo and Ma, Yuexin and Yang, Ruigang and Li, Xin and Zhu, Yanliang and Qian, Deheng and Yang, Zetong and Zhang, Wenjing and Liu, Yuanpei},
  journal={arXiv preprint arXiv:2004.05966},
  year={2020}
}
```

## Dataset Q & A

Q1. Does the dataset include synchronized RGB data?

We have not labeled the image data. Current challenge is just based on the trajectory data.

Q2. Is the trajectory of the ego vehicle also included?

No, the data does not contain the trajectory of the ego vehicle.

Q3. How are these world coordinates generated?

We use the relative positions from LiDAR and the GPS of the ego vehicle to compute the locations of other traffic-agents in the world coordinate system.

Q4. What are the relationships among different files in the training dataset?

They are captured in different period and they are independent.

Q5. What is the meaning of the data in each row of sample_trajectory?

Each line is the info for one traffic-agent in one frame. 
The info for each line is in order by the following:
timestamp, id, width, length, type, position_x, position_y,  velocity_x, velocity_y.

Q6. Why is the number of frames in each file in prediction_train different, instead of 60 s * 2 fps = 120 frames? If prediction_test.txt is a 50 min sequence, why is the total number of frames not 50 min * 2 fps = 6000 frames? 

The number of frames is different because we have cleaned the data for those time without any objects or very few objects.

Q7. What is the specific physical meaning of the frame ID in the dataset? What does the numbers in the name of each file in prediction_train.zip represent?
Frame_id: timestamp 
Number in File_name: not useful, came from original data
