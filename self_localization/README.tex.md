# The Online Self-localization Challenge of Apolloscape
This repository contains the evaluation scripts for the online self-localization challenge of the ApolloScapes dataset,
Where we extended the dataset with more scenes and 100x large data including recorded videos under different lighting conditions, i.e. morning, noon and night. 
A test dataset for each new scene will be withheld for benchmark. (Notice we will not have point cloud for the very large data due to size of dataset)

Details and download are available at: https://Apolloscape.auto/ECCV/index.html


## Dataset Structure

The dataset has the following structure
```
{root}/{scene_names}/{split}/{data_type}/{record time}/{record id}/{camera id}/{image_name}
```

`scene_names` include a sample scene:
- `Road_01`: which is road id where the dataset is collected.

`split` is the split of the dataset:
- `Train`: include the data for training, including `image, pose, split`.
- `Test`: include the image for testing, including `image` without pose ground truth.

`data_type` includes: 
- `image`: the RGB image from the dataset
- `pose`: the abosolute pose (roll,pitch,yall,x,y,z) of each image related to a map (Notice this is converted from the 4x4 pose matrix from Apolloscape dataset)
- `split`: train val split

`record time`: the time stamp for recorded videos, i.e. BJxxxB is one set of collections at site BJ
`record id`: each sequence, i.e. Recordxxx is a video sequence of the corresponding scene and the images are sorted numerically.

`camera_id`: each scene we provide images recorede by two camera facing front side, e.g. `Camera_5` and `Camera_6`
There is a camera-name in-consistency of the device between the two scene, which will be fixed for the larger dataset later.
The `camera parameters` is consistent with that in other datasets released in https://Apolloscape.auto. ([fx, fy, cx, cy] are also available at [data.py](../data.py)

Here ```split``` include the train and val image names for each scene, where val images are recorded at different period with training images.

`image_name`: the name of the file, images will be ```{timestamp}_{camera id}.jpg```

There is only one pose file (i.e., pose.txt) for each camera and each record. This pose file contains all the extrinsic parameters for all the images of the corresponding camera and record. The format of each line in the pose file is as follows:

```image_name row,pitch,yall,x,y,z```

Similar data structure is described in apolloscape.auto/scene.html, while having the pose saved in a 4x4 matrix, a conversion code from 4x4 matrix to 6 DOF is provided in `utils` of this toolkit.
Later we will also release semantic labels,  and semantic 3d point cloud python toolkit to render 3d point to 2d image for visualizing the semantic points.
You may download the dataset from [self-localization](http://apolloscape.auto/ECCV/challenge.html). The sample data is used for paper 

```
 @inproceedings{wang2018dels,
   title={DeLS-3D: Deep Localization and Segmentation with a 3D Semantic Map},
   author={Wang, Peng and Yang, Ruigang and Cao, Binbin and Xu, Wei and Lin, Yuanqing},
   booktitle={CVPR},
   pages={5860--5869},
   year={2018}
 }
```


## Evaluation
There are several scripts included with the dataset in a folder named `scripts`
 - `eval_pose.py`   Code for evalution pose accuracy based the commonly used eval metric of meidian translation and rotation error.

Code for test evaluation: 
```bash
#!/bin/bash
python eval_pose.py --test_dir='./test_eval_data/pose_res' --gt_dir='./test_eval_data/pose_gt' --res_file='./test_eval_data/res.txt'
```

### Metric formula

For each image, given the predicted rotation $r_i$ and translation $t_i$ of image $i$, and the ground truth $r^*_i$ and $t^*_i$, the metric for evaluation is defined as: 

$e_{translation} = median(\{\|t_i - t^*_i\|_2\}_{i\in\{1, N\}})$

$e_{rotation} = median(\{\arccos(q(r_i) \cdot q(r^*_i)) \}_{i\in\{1, N\}})$

where $q(r_i)$ is the quaternions representation of the Euler angle ```row, pitch, yall```


### Rules of ranking

Result benchmark will be:

| Method | mean | scene1 | scene2 | scene3 | 
| ------ |:------:|:------:|:------:|:------:|
| Deepxxx |xx $m$, xx $^{\circ}$  | xx $m$, xx $^{\circ}$ | xx $m$, xx $^{\circ}$ | xx $m$, xx $^{\circ}$ | 

Our ranking will determined by number of winning metrics from all scenes.


### Submission of data format
Please follow the data format under ```test_eval_data/``` for example. 

The submission structure for test folder is:
```
test/{scene_names}/Test/pose/{record time}/{record id}/{camera id}.txt
```

We only ask for the pose of a single camera, i.e. ```Camera_5``` in this case

- Example dir tree of submitted zip file
```bash
├── test
│   ├── Road11
│   │   ├── Test
│   │   │   ├── BJxxxB
│   │   │   │   ├── Recordxxx
│   │   │   │   │   ├── Camera_5.txt
│   │    ...
│   ├── Road12
│   │   ├── Test
│   │   │   ├── BJxxxB
│   │   │   │   ├── Recordxxx
│   │   │   │   │   ├── Camera_5.txt
...
```

 - Example format of ```{camera id}.txt```
```bash
image_name1 roll,pitch,yaw,x,y,z
image_name2 roll,pitch,yaw,x,y,z
image_name3 roll,pitch,yaw,x,y,z
image_name4 roll,pitch,yaw,x,y,z
image_name5 roll,pitch,yaw,x,y,z
```
Here  ```roll,pitch,yaw,x,y,z``` are ```float32``` numbers


## Contact
Please feel free to contact us, or raise an issue with any questions, suggestions or comments:
* apollo-scape@baidu.com

