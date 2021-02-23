# The 3D Lidar Object Detection and Tracking Challenge of Apolloscape Dataset
Our 3D Lidar object detection and tracking dataset consists of LiDAR scanned point clouds with high quality annotation. It is collected under various lighting conditions and traffic densities in Beijing, China. More specifically, it contains highly complicated traffic flows mixed with vehicles, cyclists, and pedestrians.
The 3D Lidar object detection and tracking benchmark consists of about 53min training sequences and 50min testing sequences. The data is captured at 10 frames per second and labeled at 2 frames per second. We provide all the raw data and labeled data. [Dataset detail and download](http://apolloscape.auto/tracking.html)

CVPR 2019 WAD Challenge on Trajectory Prediction and 3D Perception. [PDF](https://arxiv.org/pdf/2004.05966.pdf) [Website](http://wad.ai/2019/challenge.html)


## Introduction
Our 3D Lidar object detection and tracking dataset consists of LiDAR scanned point clouds with high quality annotation. It is collected under various lighting conditions and traffic densities in Beijing, China. More specifically, it contains highly complicated traffic flows mixed with vehicles, cyclists, and pedestrians.

![](../examples/3d-tracking.gif)


## Dataset download
The trajectory dataset consists of 53min training sequences and 50min testing sequences captured at 2 frames per second.

object counts for cars, bicycles, and pedestrians are as follows (https://arxiv.org/pdf/1811.02146.pdf): 
16.2k, 5.5k, 60.1k

[Apolloscape 3D Dataset download](http://apolloscape.auto/tracking.html)


## Evaluation
eval.py is the evaluation code. Here gtPath is (label) and dtPath is (Your detection/tracking result)

```
# export NUMBA_ENABLE_CUDASIM=1

# detection
python eval.py --gtPath= xx --dtPath= xx  

# tracking
# python eval.py --modeType=tracking --gtPath= xx --dtPath= xx
```

## Format of submission file
Submit your result for online evaluation here: [Submit](http://apolloscape.auto/submit.html)

[Leaderboard](http://apolloscape.auto/leader_board.html)

1) 3D detection

Please submit one detection_result.zip file. In this zip file, you have one folder named detection_result, under this folder, you have multiple subfolders follow the same name in test_pcd, under each subfolder are result txt files of that sequence:

detection_result

├── 9048_2

├── ├── 2.txt

├── ├── 7.txt

...

├── ├── 462.txt

...

├── 9049_1

...

├── 9063_10

...

- Each line in every file contains object_type, position_x, position_y, position_z, object_length, object_width, object_height, heading, score. score indicates confidence in detection results.
- Each file name is frame_id name, which should be same as pcd frame id we provide in test_pcd. Each pcd file should have a corresponding result file. Total test result should be 5400 txt files.
- Please only keep type 1/2/3/4 in your result file. We do evaluation just for Car (type 1 and 2), Pedestrian (type 3) and Cyclist (type 4).

2) 3D tracking

Please submit one tracking_result.zip file. Folder and subfolders structure and file name are same to detection_result, but we need object_id in file.
- Each line in every file contains object_id, object_type, position_x, position_y, position_z, object_length, object_width, object_height, heading, score


## Publication
Please cite our paper in your publications.

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

TrafficPredict: Trajectory Prediction for Heterogeneous Traffic-Agents. [PDF](https://arxiv.org/abs/1811.02146)
[BibTex](https://ad-apolloscape.cdn.bcebos.com/TrafficPredict/trafficpredict_bibtex.txt)

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

