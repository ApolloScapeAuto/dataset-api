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

## Formula for evalution
```
    shapeThrs  - [.5:.05:.95] T=10 shape thresholds for evaluation
    rotThrs    - [50:  5:  5] T=10 rot thresholds for evaluation
    transThrs  - [0.1:.3:2.8] T=10 trans thresholds for evaluation
```

We use ```c0, c1, ..., c9``` to represent the criteria from loose to strict
To be updated


## License
For the source code from the renderer and any part we borrow from cocoapi, we follow their license requirements.


## Contact

Please feel free to contact us with any questions, suggestions or comments:
* www.apollo-scape@baidu.com
