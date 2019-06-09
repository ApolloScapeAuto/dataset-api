
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

For each image, given the predicted disparity <img src="/stereo/tex/672a7aeac9254219b9609330a12e55e5.svg?invert_in_darkmode&sanitize=true" align=middle width=13.206862349999989pt height=22.831056599999986pt/> and  the ground truth <img src="/stereo/tex/97f89923e9f24bff9cc59b4e881bc32e.svg?invert_in_darkmode&sanitize=true" align=middle width=15.291158849999992pt height=22.831056599999986pt/>, the metric for evaluation is defined as: 



<img src="/stereo/tex/8c596229026f8693ff0f9f2ede2c4c04.svg?invert_in_darkmode&sanitize=true" align=middle width=299.4934305pt height=43.64887559999999pt/>

Here the <img src="/stereo/tex/e8a05164f5403e1a2b31404dc04cf1d5.svg?invert_in_darkmode&sanitize=true" align=middle width=39.90310334999999pt height=22.831056599999986pt/> can be either foreground (fg), background (bg) or the whole region (merge of fg and bg). <img src="/stereo/tex/f9c4988898e7f532b9f826a75014ed3c.svg?invert_in_darkmode&sanitize=true" align=middle width=14.99998994999999pt height=22.465723500000017pt/> is the number of image


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

