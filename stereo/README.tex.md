
# The Stereo Challenge of Apolloscape
This repository contains the evaluation scripts for the stereo challenge of the ApolloScapes dataset,
A test dataset for each new scene will be withheld for benchmark. (Notice we will not have point cloud for the very large data due to size of dataset)

[Details and download](http://apolloscape.auto/stereo.html) of data from different roads are available.

We extend the dataset from combination of 3D scanner and human labelled 3D car instance for depth generation.

## Dataset Structure

The dataset has the following structure
```
{split}/{data_type}/{image_name}
```
data_type:
- fg_mask: foreground mask
- bg_mask: background mask
- disparity: the ground truth disparity

## Evaluation

Code for test evaluation: 
```bash
#!/bin/bash
python eval_stereo.py 
```

### Metric formula

For each image, given the predicted disparity $d_i$ and  the ground truth $d^*_i$, the metric for evaluation is defined as: 



$d1_{mask} = \frac{\sum_{i \in mask_j}(\|d_{ij} - d^*_{ij}\|)}{|mask_j}

Here the $mask$ can be either foreground (fg), background (bg) or the whole region (merge of fg and bg). $N$ is the number of image


### Rules of ranking

Result benchmark will be:

| Method | D1_fg | D1_bg | D1_all | 
| ------ |:------:|:------:|:------:|
| Deepxxx |xx  | xx  | xx | xx | 



### Submission of data format
To be updated

## Contact
Please feel free to contact us, or raise an issue with any questions, suggestions or comments:
* apollo-scape@baidu.com

