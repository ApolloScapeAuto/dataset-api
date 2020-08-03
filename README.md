# Toolkit for [ApolloScape Dataset](http://apolloscape.auto/index.html)

## Introduction
This is a repo of toolkit for ApolloScape Dataset, [CVPR 2019 Workshop on Autonomous Driving Challenge](http://wad.ai/2019/challenge.html) and [ECCV 2018 challenge](http://apolloscape.auto/ECCV/index.html). It includes Trajectory Prediction, 3D Lidar Object Detection and 3D Lidar Object Tracking, lanemark segmentation, online self-localization, 3D car instance understanding, Stereo, and Inpainting Dataset. Some example videos and images are shown below:

### Trajectory Prediction:
![](./examples/trajectory-prediction.gif)

### 3D Lidar Object Detection and Tracking:
![](./examples/3d-tracking.gif)

### Video Inpainting:
![](./examples/inpainting.gif)
[![Depth Guided Video Inpainting for Autonomous Driving](https://res.cloudinary.com/marcomontalbano/image/upload/v1595308220/video_to_markdown/images/youtube--iOIxdQIzjQs-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=iOIxdQIzjQs "Depth Guided Video Inpainting for Autonomous Driving")

### Stereo estimation:
![](./examples/stereo_depth.png)

### Lanemark segmentation:
![](./examples/lanemark-segmentation.gif)

### Online self-localization:
![](./examples/self-localization.gif)

### 3D car instance understanding:
![](./examples/3d-car-instance.png)

### Data Download
```
wget https://ad-apolloscape.cdn.bcebos.com/road01_ins.tar.gz 
or
wget https://ad-apolloscape.bj.bcebos.com/road01_ins.tar.gz

wget https://ad-apolloscape.cdn.bcebos.com/trajectory/prediction_train.zip
```

Run 
```bash
pip install -r requirements.txt
source source.rc
```
to include necessary packages and current path in to PYTHONPATH to use several util functions.

Please goto each subfolder for detailed information about the data structure, evaluation criterias and some demo code to visualize the dataset.

## Citation

DVI: Depth Guided Video Inpainting for Autonomous Driving.

Miao Liao, Feixiang Lu, Dingfu Zhou, Sibo Zhang, Wei Li, Ruigang Yang.  ECCV 2020. [PDF](https://arxiv.org/pdf/2007.08854.pdf), [Video](https://www.youtube.com/watch?v=iOIxdQIzjQs)

```
@article{liao2020dvi,
  title={DVI: Depth Guided Video Inpainting for Autonomous Driving},
  author={Liao, Miao and Lu, Feixiang and Zhou, Dingfu and Zhang, Sibo and Li, Wei and Yang, Ruigang},
  journal={arXiv preprint arXiv:2007.08854},
  year={2020}
}
```

TrafficPredict: Trajectory Prediction for Heterogeneous Traffic-Agents. [PDF](https://arxiv.org/abs/1811.02146), [Website](http://gamma.cs.unc.edu/TPredict/TrafficPredict.html), [Trajectory Dataset](http://apolloscape.auto/trajectory.html), [3D Perception Dataset](http://apolloscape.auto/tracking.html), [Video](https://www.youtube.com/watch?v=dST6NDxEMU8)


Yuexin Ma, Xinge Zhu, Sibo Zhang, Ruigang Yang, Wenping Wang, and Dinesh Manocha. AAAI(oral), 2019

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

The apolloscape open dataset for autonomous driving and its application. [PDF](https://arxiv.org/pdf/1803.06184.pdf)

Huang, Xinyu and Wang, Peng and Cheng, Xinjing and Zhou, Dingfu and Geng, Qichuan and Yang, Ruigang

```
@article{wang2019apolloscape,
  title={The apolloscape open dataset for autonomous driving and its application},
  author={Wang, Peng and Huang, Xinyu and Cheng, Xinjing and Zhou, Dingfu and Geng, Qichuan and Yang, Ruigang},
  journal={IEEE transactions on pattern analysis and machine intelligence},
  year={2019},
  publisher={IEEE}
}
```

CVPR 2019 WAD Challenge on Trajectory Prediction and 3D Perception. [PDF](https://arxiv.org/pdf/2004.05966.pdf), [Website](http://wad.ai/2019/challenge.html)
```
@article{zhang2020cvpr,
  title={CVPR 2019 WAD Challenge on Trajectory Prediction and 3D Perception},
  author={Zhang, Sibo and Ma, Yuexin and Yang, Ruigang and Li, Xin and Zhu, Yanliang and Qian, Deheng and Yang, Zetong and Zhang, Wenjing and Liu, Yuanpei},
  journal={arXiv preprint arXiv:2004.05966},
  year={2020}
}
```
