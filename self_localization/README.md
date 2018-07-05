# The Online Self-localization Challenge of Apolloscapes Dataset
This repository contains the evaluation scripts for the online self-localization challenge of the ApolloScapes dataset,
Where we extended the dataset with more scenes and 100x large data including recorded videos under different lighting conditions, i.e. morning, noon and night. 
A test dataset for each new scene will be withheld for benchmark. (Notice we will not have point cloud for the very large data due to size of dataset)

Details and download are available at: https://Apolloscape.auto/ECCV/index.html


## Dataset Structure
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

`scene_names` include a sample scene:
- `Road_01`: which is a small dataset with 2242 train/756 val images recorded in the same scene

`data_type` includes: 
- `image`: the RGB image from the dataset
- `pose`: the abosolute pose (roll,pitch,yall,x,y,z) of each image related to a map (Notice this is converted from the 4x4 pose matrix from Apolloscape dataset)
- `camera_params`: the intrinsic parameter of the camera
- `split`: the train val split used in the paper

`sequence_id`, each sequence, i.e. Recordxxx is a video sequence of the corresponding scene and the images are sorted numerically.

`camera_id`, each scene we provide images recorede by two camera facing front side. 
- `zpark`: `Camera_1` and `Camera_2`
There is a camera-name in-consistency of the device between the two scene, which will be fixed for the larger dataset later.

Here ```split``` include the train and val image names for each scene, where val images are recorded at different period with training images.

Similar data structure is described in apolloscape.auto/scene.html, while having the pose saved in a 4x4 matrix, a conversion code from 4x4 matrix to 6 DOF is provided in `utils` of this toolkit.

Later we will also release semantic labels,  and semantic 3d point cloud python toolkit to render 3d point to 2d image for visualizing the semantic points.


## Evaluation
There are several scripts included with the dataset in a folder named `scripts`
 - `eval_pose.py`   Code for evalution pose accuracy based the commonly used eval metric of meidian translation and rotation error.

Code for test evaluation: 

```bash
#!/bin/bash
python eval_pose.py --test_dir='./test_eval_data/pose_res' --gt_dir='./test_eval_data/pose_gt' --res_file='./test_eval_data/res.txt'
```

### Metric formula

For each image, given the predicted rotation <img src="/self_localization/tex/3cf87ea38a615ed99e0232f8ed9431fe.svg?invert_in_darkmode&sanitize=true" align=middle width=12.067218899999991pt height=14.15524440000002pt/> and translation <img src="/self_localization/tex/02ab12d0013b89c8edc7f0f2662fa7a9.svg?invert_in_darkmode&sanitize=true" align=middle width=10.58699729999999pt height=20.221802699999984pt/> of image <img src="/self_localization/tex/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode&sanitize=true" align=middle width=5.663225699999989pt height=21.68300969999999pt/>, and the ground truth <img src="/self_localization/tex/8baf725662988147b566a34101b2f41d.svg?invert_in_darkmode&sanitize=true" align=middle width=14.608149599999992pt height=22.63846199999998pt/> and <img src="/self_localization/tex/794f29f339ded8d1f520558a6fdd129e.svg?invert_in_darkmode&sanitize=true" align=middle width=12.671292149999989pt height=22.63846199999998pt/>, the metric for evaluation is defined as: 

<img src="/self_localization/tex/d971509386ccce477d1a00716f36feb0.svg?invert_in_darkmode&sanitize=true" align=middle width=293.44066125pt height=24.65753399999998pt/>

<img src="/self_localization/tex/49eac0005f2f37ca6142906d9eeb396e.svg?invert_in_darkmode&sanitize=true" align=middle width=364.9800231pt height=24.65753399999998pt/>

where <img src="/self_localization/tex/dbc3312b32770329001dc37e78afdd3a.svg?invert_in_darkmode&sanitize=true" align=middle width=33.60263774999999pt height=24.65753399999998pt/> is the quaternions representation of the Euler angle ```row, pitch, yall```


### Rules of ranking

Result benchmark will be:

| Method | mean | scene1 | scene2 | scene3 | 
| ------ |:------:|:------:|:------:|:------:|
| Deepxxx |xx <img src="/self_localization/tex/0e51a2dede42189d77627c4d742822c3.svg?invert_in_darkmode&sanitize=true" align=middle width=14.433101099999991pt height=14.15524440000002pt/>, xx <img src="/self_localization/tex/a17fe79641dc49ee31882d6a409221dc.svg?invert_in_darkmode&sanitize=true" align=middle width=6.735194399999992pt height=22.63850490000001pt/>  | xx <img src="/self_localization/tex/0e51a2dede42189d77627c4d742822c3.svg?invert_in_darkmode&sanitize=true" align=middle width=14.433101099999991pt height=14.15524440000002pt/>, xx <img src="/self_localization/tex/a17fe79641dc49ee31882d6a409221dc.svg?invert_in_darkmode&sanitize=true" align=middle width=6.735194399999992pt height=22.63850490000001pt/> | xx <img src="/self_localization/tex/0e51a2dede42189d77627c4d742822c3.svg?invert_in_darkmode&sanitize=true" align=middle width=14.433101099999991pt height=14.15524440000002pt/>, xx <img src="/self_localization/tex/a17fe79641dc49ee31882d6a409221dc.svg?invert_in_darkmode&sanitize=true" align=middle width=6.735194399999992pt height=22.63850490000001pt/> | xx <img src="/self_localization/tex/0e51a2dede42189d77627c4d742822c3.svg?invert_in_darkmode&sanitize=true" align=middle width=14.433101099999991pt height=14.15524440000002pt/>, xx <img src="/self_localization/tex/a17fe79641dc49ee31882d6a409221dc.svg?invert_in_darkmode&sanitize=true" align=middle width=6.735194399999992pt height=22.63850490000001pt/> | 

Our ranking will determined by number of winning metrics from all scenes.


### Submission of data format
Please follow the data format under ```test_eval_data/``` for example. 

- Example dir tree of submitted zip file
```bash
├── test
│   ├── scene1
│   │   ├── sequence1.txt
│   │   ├── sequence2.txt
│   │    ...
│   ├── scene2
│   │   ├── sequence1.txt
│   │   ├── sequence2.txt
...
```

 - Example format of ```sequence1.txt```
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
* www.apollo-scape@baidu.com

