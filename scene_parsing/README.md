
 * [The Scene Parsing of Apolloscapes Dataset](#scene-parsing-dataset)
   * [Dataset Download](#dataset-download)
   

# Scene Parsing Dataset

This repository contains the evaluation scripts for the Scene Parsing of the ApolloScapes dataset. The whole dataset will include RGB videos with high resolution image sequences and per pixel annotation, survey-grade dense 3D points with semantic segmentation.

1 · Introduction

Scene parsing aims to assign a class (semantic) label for each pixel in an image, or each point in a point cloud. It is one of the most comprehensive analyses of a 2D/3D scene. Given the rise of autonomous driving, environmental perception is expected to be a key enabling technical piece. The ApolloScape dataset provided by Baidu, Inc. will include RGB videos with high resolution images and per pixel annotation, survey- grade dense 3D points with semantic segmentation, stereoscopic video, and panoramic images.

We equipped a mid-size SUV with high resolution cameras and a Riegl acquisition system. Our dataset is collected in different cities under various traffic conditions. The number of moving objects, such as vehicles and pedestrians, averages from tens to over one hundred. Moreover, each image is tagged with high-accuracy pose information at cm accuracy and the static background point cloud has mm relative accuracy. We expect our new dataset can deeply benefit various autonomous driving related applications that include but not limited to 2D/3D scene understanding, localization, transfer learning, and driving simulation.

[Demo](http://ad-apolloscape.bj.bcebos.com/video%2Fvideo_demo.webm)

2 · Summary of Scence Parsing Dataset

Image frames in our dataset are collected every one meter by our acquisition system with resolution 3384 x 2710. It is expected that the released dataset will include 200K image frames with corresponding pixel-level annotations and pose information. Instance-level annotations are available for a subset of the dataset. Depth maps for static background will also be provided.

As of March 8, 2018, we have released the first part of the dataset that contains 74555 video frames and their pixel-level and instance-level annotations.On March 21, 2018, we added the second part of the data set, including 43592 depth images for static background of road01_ins and road02_ins.On April 03, 2018，the Scene Parsing data set cumulatively provides 146,997 frames with corresponding pixel-level annotations and pose information，depth maps for static background.

The dataset is divided into three subsets for training, validation and testing respectively. The semantic annotations for testing images are not provided. All the pixels in the ground truth annotations for testing images are labeled as 255. The files that contain image lists of training, validation, and testing subsets will be provided soon.

3 · Class Definitions

We annotate 25 different labels covered by five groups. The following table gives the details of these labels. There are two IDs, class ID and train ID, assigned to each pixel. The train ID is the one used for training and can be modified as needed. The value 255 indicates the ignoring labels that currently are not evaluated during the testing phase. The class ID is used to represent the label in ground truth labels. More details including color assignment can be found in label_apollo.py in [utilities.tar.gz](https://ad-apolloscape.cdn.bcebos.com/public/utilities.tar.gz). During the submission, however, please make sure to use the class IDs.

category	Class	Class ID	train ID	Description
Others	others	0	255	
rover	1	255	
Sky	sky	17	0	
movable object	car	33	1	
car_groups	161	1	
motorbicycle	34	2	
motorbicycle_group	162	2	
bicycle	35	3	
bicycle_group	163	3	
person	36	4	
person_group	164	4	
rider	37	5	person on motorcycle,bicycle or tricycle
rider_group	165	5	person on motorcycle,bicycle or tricycle
truck	38	6	
truck_group	166	6	
bus	39	7	
bus_group	167	7	
tricycle	40	8	three-wheeled vehicles,motorized, or human-powered
tricycle_group	168	8	three-wheeled vehicles,motorized, or human-powered
flat	road	49	9	
siderwalk	50	10	
Road obstacles	traffic_cone	65	11	movable and cone-shaped markers
road_pile	66	12	fixed with many different shapes
fence	67	13	
Roadside objects	traffic_light	81	14	
void	pole	82	15	
traffic_sign	83	16	
wall	84	17	
dustbin	85	18	
billboard	86	19	
Building	building	97	20	
bridge	98	255	
tunnel	99	255	
overpass	100	255	
Natural	vegatation	113	21	
Unlabeled	unlabeled	255	255	other unlabeled objects

4 · Data Example

Color Label

![image](https://user-images.githubusercontent.com/13900043/190005406-ba1551ac-6566-4fd9-9893-d640608b7524.png)


Depth Image

![image](https://user-images.githubusercontent.com/13900043/190005421-c525e1fd-56f1-46d0-8dd2-52fe30b5eda8.png)


# Dataset Download
5 · Dataset Download

Instance-level & Pixel-level labels

_ins means labels contains both pixel-level and instance-level labels, _seg means labels contains pixel-level labels only.

[road01_ins](https://ad-apolloscape.cdn.bcebos.com/road01_ins.tar.gz)
[road02_ins](https://ad-apolloscape.cdn.bcebos.com/road02_ins.tar.gz)
[road03_ins](https://ad-apolloscape.cdn.bcebos.com/road03_ins.tar.gz)
[road04_ins](https://ad-apolloscape.cdn.bcebos.com/road04_ins.tar.gz)

[road02_seg](https://ad-apolloscape.cdn.bcebos.com/road02_seg.tar.gz)
[road03_seg](https://ad-apolloscape.cdn.bcebos.com/road03_seg.tar.gz)
[road04_seg](https://ad-apolloscape.cdn.bcebos.com/road04_seg.tar.gz)

Pixel-level LaneLine labels

We annotate 28 different lane markings that currentlyare not available in existing open datasets. The ApolloScape Dataset for Autonomous Driving give detailed information of these lane markings

[road02_ins_lane](https://ad-apolloscape.cdn.bcebos.com/road02_ins_lane.tar.gz)
[road03_ins_lane](https://ad-apolloscape.cdn.bcebos.com/road03_ins_lane.tar.gz)


Depth images

[road01_ins_depth](https://ad-apolloscape.cdn.bcebos.com/road01_ins_depth.tar.gz)
[road02_ins_depth](https://ad-apolloscape.cdn.bcebos.com/road02_ins_depth.tar.gz)
[road03_ins_depth](https://ad-apolloscape.cdn.bcebos.com/road03_ins_depth.tar.gz)
[road04_ins_depth](https://ad-apolloscape.cdn.bcebos.com/road04_ins_depth.tar.gz)

[road02_seg_depth](https://ad-apolloscape.cdn.bcebos.com/road02_seg_depth.tar.gz)
[road03_seg_depth](https://ad-apolloscape.cdn.bcebos.com/road03_seg_depth.tar.gz)
[road04_seg_depth](https://ad-apolloscape.cdn.bcebos.com/road04_seg_depth.tar.gz)

Note: All photos can only be used for educational purpose by individuals or organizations. Commercial use or other violations of copyright law are not permitted.

Image lists

Uploaded the [Image lists](https://ad-apolloscape.cdn.bcebos.com/public/image_lists.tar.gz) for training, validation, and testing for road01_ins, road02_ins, and road03_ins.

6 · Dataset Structure

Folder structure of the dataset

{root} / {type} / {road id} _ {level} / {record id} / {camera id} / {timestamp} _ {camera id} {ext}

root: the root folder defined by users.

type: there are three data types in current release, i.e., ColorImage, Label, and Pose.

road id: the road id, e.g., road001, road002.

level: two different levels, seg means labels contains pixel-level labels only, ins means labels contains both pixel-level and instance-level labels.

record id: the record is, e.g., Record001, Record002. Each record contains up to few thousands images.

camera id: two front cameras are used in our acquisition system, i.e., Camera 5 and Camera 6.

timestamp: the first part of the image name.

camera id: the second part of the image name.

ext: the extension of the file. .jpg for color image, _bin.png for label image, .json for the polygon list of instance-level labels, and _instanceIds.png for instance-level labels.

There is only one pose file (i.e., pose.txt) for each camera and each record. This pose file contains all the extrinsic parameters for all the images of the corresponding camera and record. The format of each line in the pose file is as follows:

r00 r01 r02 t0 r10 r11 r12 t1 r20 r21 r22 t2 0 0 0 1 image_name

The cameras have been well calibrated and undistorted. The intrinsic parameters of cameras can found in camera_intrinsics.txt in the [utilities.tar.gz](https://ad-apolloscape.cdn.bcebos.com/public/utilities.tar.gz).

Depth image format:

In the depth image, the depth value is save as unsigned short int format. It can be easily read in OpenCV as:

cv::Mat depth_u16 = cv::imread ( depth_path, CV_LOAD_IMAGE_ANYDEPTH);

The absolute depth value in meter can be obtained as

double depth_value = depth_u16.at(row, col) / 200.00;

7 · Evaluation Tasks

Given 3D annotations, 2D pixel and instance-level annotations, background depth maps, camera pose information, a number of tasks could be defined. In current release, we mainly focus on the 2D image parsing task. We would like to add more tasks in near future.

We have provided three evaluation metrics for single image parsing and video parsing. More details about the evaluation metrics can be found in our paper.We are organizing 2018 CVPR Workshop on Autonomous Driving Challenge, more details to be announced soon.

8 · Publication

Please cite our paper in your publications if our dataset is used in your research.
Xinyu Huang, Xinjing Cheng, Qichuan Geng, Binbin Cao, Dingfu Zhou, Peng Wang, Yuanqing Lin, and Ruigang Yang, The ApolloScape Dataset for Autonomous Driving, arXiv: 1803.06184, 2018
[PDF](http://ad-apolloscape.bj.bcebos.com/public%2FApolloScape%20Dataset.pdf) [BibTex](http://ad-apolloscape.bj.bcebos.com/public%2FBibTex.txt)



