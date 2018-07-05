# The 3D Car Instance Understanding Challenge of Apolloscapes Dataset

This repository contains the evaluation scripts for the 3d car instance understanding challenge of the ApolloScapes dataset. This large-scale dataset contains a diverse set of stereo video sequences recorded in street scenes from different cities, with high quality annotations of 5000+ frames.

Details and download are available at: https://Apolloscape.auto/ECCV/index.html


## Dataset Structure
You may download the dataset from [apollo 3d car challenges](http://apolloscape.auto/ECCV/challenge.html)

The folder structure of the 3d car detection challenge is as follows:
```
{root}/{folder}/{image_name}{ext}
```

The meaning of the individual elements is:
 - `camera`   camera intrinsic parameters.
 - `car_models`   the set of car models, re-saved to python friendly pkl.
 - `car_poses`   labelled car pose in the image.
 - `images` image set. 
 - `split` training and vlaidation image list. 


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
python render_car_instances.py --image_name='./test_example/pose_res' --data_dir='../apolloscape/3d_car_instance_sample'
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

We adopt the popularly used mean Avergae Precision for object instance evaluation in 3D similar to [coco detection](http://cocodataset.org/#detection-eval). However instead of using 2D mask IoU for similarity criteria between predicted instances and ground truth to judge a true positive, we propose to used following 3D metrics containing the perspective of *shape* ($s$), *3d translation*($t$) and *3d rotation*($r$) to judge a true positive.

Specifically, given an estimated 3d car model in an image $C_{i}=\{s_i, t_i, r_i\}$ and ground truth model $C_{i}^* = \{s_i^*, t_i^*, r_i^*\}$, we evaluate the three estimates repectively as follows:

For 3d shape, we consider reprojection similarity, by putting the model at a fix location and rendering 10 views by rotating the object. We compute the mean IoU between the two masks rendered from each view. Formally, the metric is defined as,

$c_{shape} = \frac{1}{|V|}\sum_{v\in V}IoU(P(s_i), P(s_i^*))_v$

where $V$ is a set of camera views.

For 3d translation and rotation, we follow the same evaluation metric of self-localization, please check [README.md](../self_localization/README.md) for detailed formula.

Then, we define a set of 10 thresholds for a true positive prediction from loose criterion to strict criterion:

```
    shapeThrs  - [.5:.05:.95] shape thresholds for $s$
    rotThrs    - [50:  5:  5] rotation thresholds for $r$
    transThrs  - [2.8:.3:0.1] trans thresholds for $t$
```
where the most loose metric ```.5, 50, 2.8``` means shape similarity must $> 0.5$, rotation distance must $<50 \circ$ and tranlation distance must $<2.8 m$, and the strict metric can be interprated correspondingly.

We use $c_0, c_1, ..., c_9$ to represent those criteria from loose to strict.


### Rules of ranking

Result benchmark will be:

| Method | AP | AP$_{c_0}$ |  AP$_{c_3}$ |  AP$_{small}$ | AP$_{median}$ | AP$_{large}$ | 
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


## License
For the source code from the renderer and any part we borrow from cocoapi, we follow their license requirements.


## Contact

Please feel free to contact us with any questions, suggestions or comments:
* www.apollo-scape@baidu.com
