# The Video Inpainting Dataset for Autonomous Driving
[![Depth Guided Video Inpainting for Autonomous Driving](https://res.cloudinary.com/marcomontalbano/image/upload/v1595308220/video_to_markdown/images/youtube--iOIxdQIzjQs-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=iOIxdQIzjQs "Depth Guided Video Inpainting for Autonomous Driving")

## Introduction
Inpainting dataset consists of synchronized Labeled image and LiDAR scanned point clouds. It captured by HESAI Pandora All-in-One Sensing Kit. It is collected under various lighting conditions and traffic densities in Beijing, China.
[Dataset detail and download](http://apolloscape.auto/inpainting.html)

## Dataset download
Please download data at [Apolloscape](http://apolloscape.auto/inpainting.html). The first video inpainting dataset with depth. 

## Data Structure
The folder structure of the inpainting is as follows:

1) xxx-yyy_mask.zip: xxx.aaa.jpg is original image. xxx.aaa.png is labelled mask of cars. 

2) xxx-yyy.zip: Data includes ds_map.ply, global_poses.txt, rel_poses.txt, xxx.aaa_optR.xml. ds_map.ply is dense map build from lidar frames. 

3) lidar_bg.zip: lidar background point cloud in ply format.

## Publication
Please cite our paper in your publications if our dataset is used in your research.

DVI: Depth Guided Video Inpainting for Autonomous Driving.

Miao Liao, Feixiang Lu, Dingfu Zhou, Sibo Zhang, Wei Li, Ruigang Yang.  ECCV 2020. [PDF](https://arxiv.org/pdf/2007.08854.pdf), [Code](https://github.com/sibozhang/Depth-Guided-Inpainting), [Video](https://www.youtube.com/watch?v=iOIxdQIzjQs)

```
@article{liao2020dvi,
  title={DVI: Depth Guided Video Inpainting for Autonomous Driving},
  author={Liao, Miao and Lu, Feixiang and Zhou, Dingfu and Zhang, Sibo and Li, Wei and Yang, Ruigang},
  journal={arXiv preprint arXiv:2007.08854},
  year={2020}
}
```
