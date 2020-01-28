# Toolkit for [ApolloScape Dataset](http://apolloscape.auto/index.html)

## Introduction
This is a repo of toolkit for ApolloScape Dataset, [CVPR 2019 Workshop on Autonomous Driving Challenge](http://wad.ai/2019/challenge.html) and [ECCV 2018 challenge](http://apolloscape.auto/ECCV/index.html). It includes lanemark segmentation, online self-localization, 3D car instance understanding, Trajectory Prediction, 3D Lidar Object Detection and 3D Lidar Object Tracking and Stereo. Some example videos and images are shown below:

### Stereo estimation:
![](./examples/stereo_depth.png)

### Trajectory Prediction:
![](./examples/trajectory-prediction.gif)

### 3D Lidar Object Detection and Tracking:
![](./examples/3d-tracking.gif)

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

## Publication
The apolloscape open dataset for autonomous driving and its application. [PDF](http://ad-apolloscape.bj.bcebos.com/public%2FApolloScape%20Dataset.pdf)

Huang, Xinyu and Wang, Peng and Cheng, Xinjing and Zhou, Dingfu and Geng, Qichuan and Yang, Ruigang

```
@article{huang2018apolloscape,
  title={The apolloscape open dataset for autonomous driving and its application},
  author={Huang, Xinyu and Wang, Peng and Cheng, Xinjing and Zhou, Dingfu and Geng, Qichuan and Yang, Ruigang},
  journal={arXiv preprint arXiv:1803.06184},
  year={2018}
}
```

TrafficPredict: Trajectory Prediction for Heterogeneous Traffic-Agents. [PDF](https://arxiv.org/abs/1811.02146)
[BibTex](https://ad-apolloscape.cdn.bcebos.com/TrafficPredict/trafficpredict_bibtex.txt) [Website](http://gamma.cs.unc.edu/TPredict/TrafficPredict.html)
Yuexin Ma, Xinge Zhu, Sibo Zhang, Ruigang Yang, Wenping Wang, and Dinesh Manocha.
AAAI(oral), 2019

```
@article{ma2018trafficpredict,
  title={TrafficPredict: Trajectory prediction for heterogeneous traffic-agents},
  author={Ma, Yuexin and Zhu, Xinge and Zhang, Sibo and Yang, Ruigang and Wang, Wenping and Manocha, Dinesh},
  journal={arXiv preprint arXiv:1811.02146},
  year={2018}
}
```

AADS: Augmented autonomous driving simulation using data-driven algorithms
Wei Li, Chengwei Pan, Rong Zhang, Jiaping Ren, Yuexin Ma, Jin Fang, Feilong Yan, Qichuan Geng, Xinyu Huang, Huajun Gong, Weiwei Xu, Guoping Wang, Dinesh Manocha, Ruigang Yang

```
@article{li2019aads,
  title={AADS: Augmented autonomous driving simulation using data-driven algorithms},
  author={Li, Wei and Pan, Chengwei and Zhang, Rong and Ren, Jiaping and Ma, Yuexin and Fang, Jin and Yan, Feilong and Geng, Qichuan and Huang, Xinyu and Gong, Huajun and others},
  journal={arXiv preprint arXiv:1901.07849},
  year={2019}
}
```

