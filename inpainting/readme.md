# The Video Inpainting Dataset for Autonomous Driving
[![Depth Guided Video Inpainting for Autonomous Driving](https://res.cloudinary.com/marcomontalbano/image/upload/v1595308220/video_to_markdown/images/youtube--iOIxdQIzjQs-c05b58ac6eb4c4700831b2b3070cd403.jpg)](https://www.youtube.com/watch?v=iOIxdQIzjQs "Depth Guided Video Inpainting for Autonomous Driving")

## Introduction
Inpainting dataset consists of synchronized Labeled image and LiDAR scanned point clouds. It captured by HESAI Pandora All-in-One Sensing Kit. It is collected under various lighting conditions and traffic densities in Beijing, China.
[Dataset detail and download](http://apolloscape.auto/inpainting.html)

## Dataset download
Please download data at [Apolloscape](http://apolloscape.auto/inpainting.html). The first video inpainting dataset with depth. 

[mask_and_image_0.zip](https://ad-apolloscape.cdn.bcebos.com/inpainting%2F1534313570-1534313579_mask.zip)
[data_0.zip](https://ad-apolloscape.cdn.bcebos.com/inpainting%2F1534313570-1534313579.zip)
[lidar_bg_0.zip](https://ad-apolloscape.cdn.bcebos.com/inpainting%2F1534313570-1534313579_lidar_bg.zip)

[mask_and_image_1.zip](https://ad-apolloscape.cdn.bcebos.com/inpainting%2F1534313592-1534313595_mask.zip)
[data_1.zip](https://ad-apolloscape.cdn.bcebos.com/inpainting%2F1534313592-1534313595.zip)
[lidar_bg_1.zip](https://ad-apolloscape.cdn.bcebos.com/inpainting%2F1534313592-1534313595_lidar_bg.zip)

[mask_and_image_2.zip](https://ad-apolloscape.cdn.bcebos.com/inpainting%2F1534313648-1534313656_mask.zip)
[data_2.zip](https://ad-apolloscape.cdn.bcebos.com/inpainting%2F1534313648-1534313656.zip)
[lidar_bg_2.zip](https://ad-apolloscape.cdn.bcebos.com/inpainting%2F1534313648-1534313656_lidar_bg.zip)

[mask_and_image_3.zip](https://ad-apolloscape.cdn.bcebos.com/inpainting%2F1534313856-1534313869_mask.zip)
[data_3.zip](https://ad-apolloscape.cdn.bcebos.com/inpainting%2F1534313856-1534313869.zip)
[lidar_bg_3.zip](https://ad-apolloscape.cdn.bcebos.com/inpainting%2F1534313856-1534313869_lidar_bg.zip)


## Data Structure
The folder structure of the inpainting is as follows:

1) xxx-yyy_mask.zip: xxx.aaa.jpg is original image. xxx.aaa.png is labelled mask of cars. 

2) xxx-yyy.zip: Data includes ds_map.ply, global_poses.txt, rel_poses.txt, xxx.aaa_optR.xml. ds_map.ply is dense map build from lidar frames. 

3) lidar_bg.zip: lidar background point cloud in ply format.

## Publication
Please cite our paper in your publications.

DVI: Depth Guided Video Inpainting for Autonomous Driving.

Miao Liao, Feixiang Lu, Dingfu Zhou, Sibo Zhang, Wei Li, Ruigang Yang.  ECCV 2020. [PDF](https://arxiv.org/pdf/2007.08854.pdf), [Webpage](https://sites.google.com/view/sibozhang/dvi), [Inpainting Dataset](http://apolloscape.auto/inpainting.html), [Video](https://www.youtube.com/watch?v=iOIxdQIzjQs), [Presentation](https://youtu.be/_pcqH1illCU)

```
@inproceedings{liao2020dvi,
  title={DVI: Depth Guided Video Inpainting for Autonomous Driving},
  author={Liao, Miao and Lu, Feixiang and Zhou, Dingfu and Zhang, Sibo and Li, Wei and Yang, Ruigang},
  booktitle={European Conference on Computer Vision},
  pages={1--17},
  year={2020},
  organization={Springer}
}
```
