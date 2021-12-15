
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

## Dataset download
Training data

[stereo_train_1](https://ad-apolloscape.cdn.bcebos.com/stereo/stereo_train_1.zip)
[stereo_train_2](https://ad-apolloscape.cdn.bcebos.com/stereo/stereo_train_2.zip)
[stereo_train_3](https://ad-apolloscape.cdn.bcebos.com/stereo/stereo_train_3.zip)


Testing data

[stereo_test](https://ad-apolloscape.cdn.bcebos.com/stereo/stereo_test.zip)



## Evaluation

Code for test evaluation: 
```bash
#!/bin/bash
python eval_stereo.py 
```

### Metric formula

For each image, given the predicted disparity <img src="/stereo/tex/672a7aeac9254219b9609330a12e55e5.svg?invert_in_darkmode&sanitize=true" align=middle width=13.206862349999989pt height=22.831056599999986pt/> and  the ground truth <img src="/stereo/tex/97f89923e9f24bff9cc59b4e881bc32e.svg?invert_in_darkmode&sanitize=true" align=middle width=15.291158849999992pt height=22.831056599999986pt/>, the metric for evaluation is defined as: 



<img src="/stereo/tex/33c80dceffc6d9989c32674479e736c9.svg?invert_in_darkmode&sanitize=true" align=middle width=293.54594775pt height=43.64887559999999pt/>

Here the <img src="/stereo/tex/e8a05164f5403e1a2b31404dc04cf1d5.svg?invert_in_darkmode&sanitize=true" align=middle width=39.90310334999999pt height=22.831056599999986pt/> can be either foreground (fg), background (bg) or the whole region (merge of fg and bg). <img src="/stereo/tex/f9c4988898e7f532b9f826a75014ed3c.svg?invert_in_darkmode&sanitize=true" align=middle width=14.99998994999999pt height=22.465723500000017pt/> is the number of image


### Rules of ranking

Result benchmark will be:

| Method | D1_fg | D1_bg | D1_all | 
| ------ |:------:|:------:|:------:|
| Deepxxx |xx  | xx  | xx | xx | 



### Submission of data format
```
{split}/{data_type}/{image_name}
```
data_type:
- disparity: the estimated disparity


## Publication
Please cite our paper in your publications.

DVI: Depth Guided Video Inpainting for Autonomous Driving. Miao Liao, Feixiang Lu, Dingfu Zhou, Sibo Zhang, Wei Li, Ruigang Yang. [PDF](https://arxiv.org/pdf/2007.08854.pdf), [Code](https://github.com/sibozhang/Depth-Guided-Inpainting), [Video](https://www.youtube.com/watch?v=iOIxdQIzjQs), [Presentation](https://www.youtube.com/watch?v=_pcqH1illCU&t=3s&ab_channel=SiboZhang)

ECCV 2020.

```
@article{liao2020dvi,
  title={DVI: Depth Guided Video Inpainting for Autonomous Driving},
  author={Liao, Miao and Lu, Feixiang and Zhou, Dingfu and Zhang, Sibo and Li, Wei and Yang, Ruigang},
  journal={arXiv preprint arXiv:2007.08854},
  year={2020}
}
```

