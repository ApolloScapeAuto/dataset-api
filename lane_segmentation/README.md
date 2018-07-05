# The Landmark Detection Challenge of Apolloscapes Dataset

This repository contains the evaluation scripts for the landmark detection challenge of the ApolloScapes dataset. This large-scale dataset contains a diverse set of stereo video sequences recorded in street scenes from different cities, with high quality pixel-level annotations of 16000+ frames.

Details and download are available in [ECCV Challenge Page](http://apolloscape.auto/ECCV/challenge.html) correspondingly.

Please also check [LanemarkDiscription.pdf](./LanemarkDiscription.pdf) for more detailed discriptions.

## Dataset Structure

The folder structure of the landmark detection challenge is as follows:
```
{root}/{type}{road id}/{record id}/{camera id}/{timestamp}_{camera id}{ext}
```

The meaning of the individual elements is:
 - `root`      the root folder of the Apolloscapes dataset.
 - `type`      the type/modality of data, e.g. `ColorImage` and 'Labels'.
 - `road id`   an identifier specifying the road, e.g. road02.
 - `record id` the folder name of a subset of images. Defined by the data collection system. 
 - `camera id` images are grouped by the cameras that capture them. In Apolloscape there are always two cameras: 'Camera 5' and 'Camera 6'. 
 - `timestamp` the time when each image is captured.
 - `ext`       the extension of the file. '.jpg' for RGB images and '.png' for groundtruths.


## Scripts

There are several scripts included with the dataset in a folder named `scripts`
 - `helpers`      helper files that are included by other scripts
 - `evaluation`   validate your approach
 - `thirdParty`   containing scripts from external libraries. We borrow codes from [Cityscapes](https://github.com/mcordts/cityscapesScripts).

Note that all files have a small documentation at the top. Most important files
 - `helpers/laneMarkDetection.py`                    central file defining the IDs of all semantic classes and providing mapping between various class properties.
 - `evaluation/evalPixelLevelSemanticLabeling.py`    script to evaluate pixel-level semantic labeling results on the test set.
 - `install.sh`                                      installation script of this library. Only tested for Ubuntu.

The scripts can be installed by running install.sh in the bash:
`sudo bash install.sh`

This tool is dependent on the evaluation script from cityScape dataset, which is need to pull recursively


## Evaluation

Once you want to test your method on the test set, please run your approach on the provided test images and submit your results at [Apollo Test Server](To be updated):

For semantic labeling, we require the result format to match the format of our label images.
Thus, your code should produce images where each pixel's value corresponds to a class ID as defined in `laneMarkDetection.py`.
Note that our evaluation scripts are included in the scripts folder and can be used to test your approach.
For further details regarding the submission process, please consult our website.

Run the following code for a sample evaluation:
```
cur_dir=`pwd`
export PYTHONPATH=<img src="/lane_segmentation/tex/27a3c5b0259eb4b4eb682b2bc7579295.svg?invert_in_darkmode&sanitize=true" align=middle width=142.10499765pt height=22.465723500000017pt/>cur_dir
python evaluation/evalPixelLevelSemanticLabeling.py ./test_eval_data/ ./test_eval_data/pred_list.csv ./test_eval_data/ ./test_eval_data/gt_list.csv
```

### Metric formula
We adopt the widely used mean IoU metric which is presented in [cityscape metric here](https://www.cityscapes-dataset.com/benchmarks/#scene-labeling-task). 
For each class, given the predicted masks <img src="/lane_segmentation/tex/b48f9a7b2f437d3195f6d31d2bc638a8.svg?invert_in_darkmode&sanitize=true" align=middle width=26.47306529999999pt height=22.465723500000017pt/> and ground truth <img src="/lane_segmentation/tex/f70d22e4badda024297b4d0b7e90867e.svg?invert_in_darkmode&sanitize=true" align=middle width=26.47306529999999pt height=22.63846199999998pt/> of image <img src="/lane_segmentation/tex/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode&sanitize=true" align=middle width=5.663225699999989pt height=21.68300969999999pt/> and class <img src="/lane_segmentation/tex/3e18a4a28fdee1744e5e3f79d13b9ff6.svg?invert_in_darkmode&sanitize=true" align=middle width=7.11380504999999pt height=14.15524440000002pt/>, the metric for evaluation is defined as: 

<img src="/lane_segmentation/tex/9e32ad2f1f8d49b96d0edf3297947e76.svg?invert_in_darkmode&sanitize=true" align=middle width=219.59248409999995pt height=24.65753399999998pt/>
<img src="/lane_segmentation/tex/4f5d8bd520f816a934dafacebed47284.svg?invert_in_darkmode&sanitize=true" align=middle width=145.71317639999998pt height=24.657735299999988pt/>
<img src="/lane_segmentation/tex/c01538506e170770b209ecd9f507d3d3.svg?invert_in_darkmode&sanitize=true" align=middle width=180.46786394999998pt height=24.657735299999988pt/>
<img src="/lane_segmentation/tex/049bc6aef85fb7ffa7a5a5a1cb4ee095.svg?invert_in_darkmode&sanitize=true" align=middle width=186.80901029999998pt height=24.657735299999988pt/>


### Rules of ranking

Result benchmark will be:

| Method | mean iou | lane name 1 | lane name 2 | lane name 3| 
| ------ |:------:|:------:|:------:|:------:|
| Deepxxx |xx  | xx  | xx | xx | 

Our ranking will determined by the mean iou of all lane classes.


### Submission of data format
 - Example dir tree of submitted zip file
```bash
├── test
│   ├── road_name_1
│   │   ├── image_name1.png
│   │   ├── image_name1.png
│   │    ...
│   ├── road_name_2
│   │   ├── image_name1.png
│   │   ├── image_name2.png
```


- Example format of ```image_name1.png```
```bash
1: image_name1.png is a prediction label image, which should have the same name and same size as the testing image. In this image, each pixel encode the class IDs as defined in our labels description. Note that regular ID is used, not the train ID.
2: Each pixel is encoded as ```uint8``` format.
```



## Contact

Please feel free to contact us with any questions, suggestions or comments:

* www.apollo-scape@baidu.com
