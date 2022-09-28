
 * [The 3D Car Instance Understanding Challenge of Apolloscapes Dataset](#the-3d-car-instance-understanding-challenge-of-apolloscapes-dataset)
   * [Dataset Download](#dataset-download)
   
   * [Dataset Structure](#dataset-structure)




# The 3D Car Instance Understanding Challenge of Apolloscapes Dataset

This repository contains the evaluation scripts for the 3d car instance understanding challenge of the ApolloScapes dataset. This large-scale dataset contains a diverse set of stereo video sequences recorded in street scenes from different cities, with high quality annotations of 5000+ frames.

2 · Data Example

http://apolloscape.auto/public/img/scene/datasets-car-instance_1e0382e.png

## Dataset Download

Sample data

[3d_car_instance_sample.tar.gz](https://ad-apolloscape.cdn.bcebos.com/3d_car_instance_sample.tar.gz)

Training data

[3d-car-understanding-train.tar.gz](https://ad-apolloscape.cdn.bcebos.com/3d-car-understanding-train.tar.gz)

Testing data

[3d-car-understanding-test.tar.gz](https://ad-apolloscape.cdn.bcebos.com/3d-car-understanding-test.tar.gz)


## Dataset Structure

The folder structure of the 3d car detection challenge is as follows:
```
{root}/{folder}/{content}/{image_name}{ext}
```

The meaning of the individual elements of `folder` is:
 - `camera`   camera intrinsic parameters.
 - `car_models`   the set of car models, re-saved to python friendly pkl. *Notice the car models in our format (vertices & meshes ) start with index 1 rather than other format like .off starting with 0.*
 - `{split}` the split of car 3d pose dataset, it could be `sample_data`, `Train`, `Test`
 
Elements of `content` under a `{split}` folder includes:
 - `car_poses`   labelled car pose in the image.
 - `images` image set. 
 - `split` training and vlaidation image list. 

Our released official data will have a new folder
 - `ignore_mask` the mask of unlabeled car regions in order to avoid error false positive, *For testing, please prune the detected car inside the ignore mask using our render tool. Otherwise, it will be counted as false positive*. 


## Scripts
There are several scripts included with the dataset in a folder named `scripts`
 - `demo.ipynb`    Demo function for visualization of an labelled image

 - `car_models.py`  central file defining the IDs of all semantic classes and providing mapping between various class properties.
 - `render_car_instances.py`  script for loading image and render image file
 - 'renderer/'      containing scripts of python wrapper for opengl render a car model from a 3d car mesh. We borrow portion of opengl rendering from [Displets](http://www.cvlibs.net/projects/displets/) and change to egl offscreen render context and python api.
 - `install.sh`     installation script of this library. Only tested for Ubuntu.

The scripts can be installed by running install.sh in the bash:
`sudo bash install.sh`

Please download the sample data from 
[apollo 3d car challenges](http://apolloscape.auto/ECCV/challenge.html) with sample data button, and put it under ```../apolloscape/``` 


Then run the following code to show a rendered results:
```bash
python render_car_instances.py --split='sample_data' --image_name='180116_053947113_Camera_5' --data_dir='../apolloscape/3d_car_instance_sample'
```

## Evaluation

We follow similar instance mean AP evalution with the [coco dataset evaluation](https://github.com/cocodataset/cocoapi), while consider thresholds using 3D car simlarity metrics (distance, orientation, shape), for distance and orientation, we use similar metrics of evaluating self-localization, i.e. the Euclidean distance for translation and arccos distance with quaternions representation.

For shape similarity, we consider the reprojection mask similarity by projecting the 3D model to 10 angles and compute the IoU between each pair of models. The similarity we have is ```sim_mat.txt```

For submitting the results, we require paticipants to also contain a estimated car_id which is defined under ```car_models.py``` and also the 6DoF estimated car pose relative to camera. As demonstrated in the ```test_eval_data``` folder.

If you want to have your results evaluated w.r.t car size, please also include an 'area' field for the submitted results by rendering the car on image.
Our final results will based on AP over all the cars same as the coco dataset.

You may run the following code to have a evaluation sample.
```bash
python eval_car_instances.py --test_dir='./test_eval_data/det3d_res' --gt_dir='./test_eval_data/det3d_gt' --res_file='./test_eval_data/res.txt'
```

### Metric formula

We adopt the popularly used mean Avergae Precision for object instance evaluation in 3D similar to [coco detection](http://cocodataset.org/#detection-eval). However instead of using 2D mask IoU for similarity criteria between predicted instances and ground truth to judge a true positive, we propose to used following 3D metrics containing the perspective of *shape* (<img src="/car_instance/tex/6f9bad7347b91ceebebd3ad7e6f6f2d1.svg?invert_in_darkmode&sanitize=true" align=middle width=7.7054801999999905pt height=14.15524440000002pt/>), *3d translation*(<img src="/car_instance/tex/4f4f4e395762a3af4575de74c019ebb5.svg?invert_in_darkmode&sanitize=true" align=middle width=5.936097749999991pt height=20.221802699999984pt/>) and *3d rotation*(<img src="/car_instance/tex/89f2e0d2d24bcf44db73aab8fc03252c.svg?invert_in_darkmode&sanitize=true" align=middle width=7.87295519999999pt height=14.15524440000002pt/>) to judge a true positive.

Specifically, given an estimated 3d car model in an image <img src="/car_instance/tex/36b2583e4d8685215773a8f4cc991656.svg?invert_in_darkmode&sanitize=true" align=middle width=107.66574884999997pt height=24.65753399999998pt/> and ground truth model <img src="/car_instance/tex/282ebdd2ff53dca1412d731c08bec6dc.svg?invert_in_darkmode&sanitize=true" align=middle width=117.63534089999999pt height=24.65753399999998pt/>, we evaluate the three estimates repectively as follows:

For 3d shape, we consider reprojection similarity, by putting the model at a fix location and rendering 10 views by rotating the object. We compute the mean IoU between the two masks rendered from each view. Formally, the metric is defined as,

<img src="/car_instance/tex/e3216a2d9236918d9b114a51a53fc95a.svg?invert_in_darkmode&sanitize=true" align=middle width=272.6026000499999pt height=27.77565449999998pt/>

where <img src="/car_instance/tex/a9a3a4a202d80326bda413b5562d5cd1.svg?invert_in_darkmode&sanitize=true" align=middle width=13.242037049999992pt height=22.465723500000017pt/> is a set of camera views.

For 3d translation and rotation, we follow the same evaluation metric of self-localization [README.md](../self_localization/README.md).

<img src="/car_instance/tex/1a16bf6722735f0218334842c3833b50.svg?invert_in_darkmode&sanitize=true" align=middle width=130.72152555pt height=24.65753399999998pt/>

<img src="/car_instance/tex/3b42802dd2e4ed40ae0918b39904ca2d.svg?invert_in_darkmode&sanitize=true" align=middle width=195.27382379999997pt height=24.65753399999998pt/>

Then, we define a set of 10 thresholds for a true positive prediction from loose criterion to strict criterion:

```
    shapeThrs  - [.5:.05:.95] shape thresholds for $s$
    rotThrs    - [50:  5:  5] rotation thresholds for $r$
    transThrs  - [2.8:.3:0.1] trans thresholds for $t$
```
where the most loose metric ```.5, 50, 2.8``` means shape similarity must <img src="/car_instance/tex/82933ae1b048283d7d52c25038a205e8.svg?invert_in_darkmode&sanitize=true" align=middle width=38.35617554999999pt height=21.18721440000001pt/>, rotation distance must <img src="/car_instance/tex/9dbc26e62bdd6a9004a4e2eac91577e3.svg?invert_in_darkmode&sanitize=true" align=middle width=42.00916004999999pt height=21.18721440000001pt/> and tranlation distance must <img src="/car_instance/tex/ca1c10083b32a6b27b4f70128b09b697.svg?invert_in_darkmode&sanitize=true" align=middle width=52.789274999999996pt height=21.18721440000001pt/>, and the strict metric can be interprated correspondingly.

We use <img src="/car_instance/tex/079669763179631abe6c6725d030fb96.svg?invert_in_darkmode&sanitize=true" align=middle width=78.25920134999998pt height=14.15524440000002pt/> to represent those criteria from loose to strict.


### Rules of ranking

Result benchmark will be:

| Method | AP | AP<img src="/car_instance/tex/f5606b459052f4b8daf6643aa31f3f2a.svg?invert_in_darkmode&sanitize=true" align=middle width=11.46835139999999pt height=14.15524440000002pt/> |  AP<img src="/car_instance/tex/a208b77cb1de63a4427210b05991d250.svg?invert_in_darkmode&sanitize=true" align=middle width=11.46835139999999pt height=14.15524440000002pt/> |  AP<img src="/car_instance/tex/5c71b8d8389a7db46d6f7ca3fe55d85c.svg?invert_in_darkmode&sanitize=true" align=middle width=33.447178049999984pt height=14.15524440000002pt/> | AP<img src="/car_instance/tex/f61e0ba78ad249b2db8b97e556065558.svg?invert_in_darkmode&sanitize=true" align=middle width=44.652151499999995pt height=14.15524440000002pt/> | AP<img src="/car_instance/tex/dd49cdc20271fef88b013ce6bb79b762.svg?invert_in_darkmode&sanitize=true" align=middle width=30.874481549999988pt height=14.15524440000002pt/> | 
| ------ |:------:|:------:|:------:|:------:|:------:|:------:|
| Deepxxx |xx  | xx  | xx | xx |  xx | xx |

Our ranking will determined by the mean AP as usual.


### Submission of data format

```bash
├── test
│   ├── image1.json
│   ├── image2.json
...
```
Here ```image1``` is string  of image name

 - Example format of image1.json

``` bash
[{
"car_id" : int, 
"area": int,
"pose" : [roll,pitch,yaw,x,y,z], 
"score" : float,
}]
...
```

Here``` roll,pitch,yaw,x,y,z``` are ```float32``` numbers, and car_id is int number, which indicates the type of car. "area" can be computed from the rendering code provided by ```render_car_instances.py``` by first rendering an image from the estimated set models and then calculate the area of each instance.



## Publication
Please cite our paper in your publications if our dataset is used in your research.

ApolloCar3D: A Large 3D Car Instance Understanding Benchmark for Autonomous Driving

Xibin Song, Peng Wang, Dingfu Zhou, Rui Zhu, Chenye Guan, Yuchao Dai, Hao Su, Hongdong Li, Ruigang Yang     

CVPR, 2019

```
@InProceedings{Song_2019_CVPR,
author = {Song, Xibin and Wang, Peng and Zhou, Dingfu and Zhu, Rui and Guan, Chenye and Dai, Yuchao and Su, Hao and Li, Hongdong and Yang, Ruigang},
title = {ApolloCar3D: A Large 3D Car Instance Understanding Benchmark for Autonomous Driving},
booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
month = {June},
year = {2019}
} 
```

