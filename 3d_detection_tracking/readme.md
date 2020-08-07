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

## Publication
Please cite our paper in your publications if our dataset is used in your research.

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

