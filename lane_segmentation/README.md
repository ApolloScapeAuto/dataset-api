 * [The Lanemark Segmentation Challenge of Apolloscapes Dataset](#the-lanemark-segmentation-challenge-of-apolloscapes-dataset)
      * [Dataset Structure](#dataset-structure)
      * [Download](#download)
      * [Scripts](#scripts)
      * [Evaluation](#evaluation)
         * [Metric formula](#metric-formula)
         * [Rules of ranking](#rules-of-ranking)
         * [Submission of data format](#submission-of-data-format)
      * [Contact](#contact)


# The Lanemark Segmentation Challenge of Apolloscapes Dataset

This repository contains the evaluation scripts for the landmark segmentation challenge of the ApolloScapes dataset. This large-scale dataset contains a diverse set of stereo video sequences recorded in street scenes from different cities, with high quality pixel-level annotations of 110 000+ frames.

Details and download information are available in [ECCV Challenge Page](http://apolloscape.auto/ECCV/challenge.html) correspondingly.

Please also check [LanemarkDiscription.pdf](./LanemarkDiscription.pdf) for more detailed discriptions.

## Dataset Structure

The folder structure of the landmark segmentation challenge is as follows:
```
{root}/{type}_{road id}/{type}/{record id}/{camera id}/{timestamp}_{camera id}{ext}
```

The meaning of the individual elements is:
 - `root`      the root folder of the Apolloscapes dataset.
 - `type`      the type/modality of data, e.g. `ColorImage` and 'Labels'.
 - `road id`   an identifier specifying the road, e.g. road02.
 - `record id` the folder name of a subset of images. Defined by the data collection system. 
 - `camera id` images are grouped by the cameras that capture them. In Apolloscape there are always two cameras: 'Camera 5' and 'Camera 6'. 
 - `timestamp` the time when each image is captured.
 - `ext`       the extension of the file. '.jpg' for RGB images and '.png' for groundtruths.


## Download
We have three set of data release for training and validation of your algorithm. Please check our website for download [link](http://apolloscape.auto/lane_segmentation.html).

## Scripts

The evaluation scripts are released on github [here](https://github.com/ApolloScapeAuto/dataset-api). For lane segmentation, the codes are under */dataset-api/lane_segmentation/*. The structure of the script is described as below: 

 - `helpers`      helper files which include usful information of using our evaluation files
 - `evaluation`   the main file for validating your approach
 - `thirdParty`   containing scripts from external libraries. We borrow some codes from [Cityscapes](https://github.com/mcordts/cityscapesScripts).

Note that all files have a short description at the top. Most important files are listed as below
 - `helpers/laneMarkDetection.py`                    the main file defining the IDs of all lane classes and providing mapping between various class properties.
 - `evaluation/evalPixelLevelSemanticLabeling.py`    script to evaluate pixel-level lane labeling results on the test set.
 - `install.sh`                                      installation script of this library. Only tested for Ubuntu.

The scripts can be installed by running install.sh in the bash:
`sudo bash install.sh`

This tool is dependent on the evaluation script from cityScape dataset, which is will be pulled recursively

## Evaluation

Once you want to test your method on the test set, please run your approach on the provided test images and submit your results at [Apollo Test Server](To be updated):

For lane labeling, we require the result format to match the format of our label images. Thus, your code should produce images where each pixel's value corresponds to a class ID as defined in `laneMarkDetection.py`. Note that our evaluation scripts are included in the scripts folder and can be used to test your approach. For further details regarding the submission process, please consult our website.

Run the following code for a sample evaluation:
```
cur_dir=`pwd`
export PYTHONPATH = \$PYTHONPATH:cur_dir
python evaluation/evalPixelLevelSemanticLabeling.py ./test_eval_data/ ./test_eval_data/pred_list.csv ./test_eval_data/ ./test_eval_data/gt_list.csv
```

### Metric formula

We adopt the widely used mean IoU metric which is presented in [cityscape metric here](https://www.cityscapes-dataset.com/benchmarks/#scene-labeling-task). 
For each class, given the predicted masks <img src="/lane_segmentation/tex/b48f9a7b2f437d3195f6d31d2bc638a8.svg?invert_in_darkmode&sanitize=true" align=middle width=26.47306529999999pt height=22.465723500000017pt/> and ground truth <img src="/lane_segmentation/tex/61d9d0fc3372eb81de31c6e7eed6e705.svg?invert_in_darkmode&sanitize=true" align=middle width=26.47306529999999pt height=22.63846199999998pt/> of image <img src="/lane_segmentation/tex/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode&sanitize=true" align=middle width=5.663225699999989pt height=21.68300969999999pt/> and class <img src="/lane_segmentation/tex/3e18a4a28fdee1744e5e3f79d13b9ff6.svg?invert_in_darkmode&sanitize=true" align=middle width=7.11380504999999pt height=14.15524440000002pt/>, the metric for evaluation is defined as: 

<img src="/lane_segmentation/tex/9e32ad2f1f8d49b96d0edf3297947e76.svg?invert_in_darkmode&sanitize=true" align=middle width=219.59248409999995pt height=24.65753399999998pt/>
<img src="/lane_segmentation/tex/d78dc64ea5382b305ce04f342a772153.svg?invert_in_darkmode&sanitize=true" align=middle width=161.6606904pt height=24.657735299999988pt/>
<img src="/lane_segmentation/tex/9ffe0c7d35f0eea9d3cc2eb25d9d0b09.svg?invert_in_darkmode&sanitize=true" align=middle width=203.72113574999997pt height=24.657735299999988pt/>
<img src="/lane_segmentation/tex/31f245f0af35e32eb71ab12b6bd844d1.svg?invert_in_darkmode&sanitize=true" align=middle width=205.8843336pt height=24.657735299999988pt/>

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

1. image_name1.png is a prediction label image, which should have the same name and same size as the testing image. In this image, each pixel encode the class IDs as defined in our labels description. Note that regular ID is used, not the train ID.

2. Each pixel is encoded as ```uint8``` format.

## Contact

Please feel free to contact us with any questions, suggestions or comments:

* apollo-scape@baidu.com
