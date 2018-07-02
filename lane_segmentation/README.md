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
export PYTHONPATH=$PYTHONPATH:$cur_dir
python evaluation/evalPixelLevelSemanticLabeling.py ./test_eval_data/ ./test_eval_data/pred_list.csv ./test_eval_data/ ./test_eval_data/gt_list.csv
```

More detailed discription of the 

## Contact

Please feel free to contact us with any questions, suggestions or comments:

* www.apollo-scape@baidu.com
