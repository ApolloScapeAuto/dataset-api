# The 3D Lidar Object Detection and Tracking Challenge of Apolloscape Dataset
[For detail and download](http://apolloscape.auto/tracking.html)
CVPR 2019 WAD Challenge on Trajectory Prediction and 3D Perception. [PDF](https://arxiv.org/pdf/2004.05966.pdf)

## Introduction
Our 3D Lidar object detection and tracking dataset consists of LiDAR scanned point clouds with high quality annotation. It is collected under various lighting conditions and traffic densities in Beijing, China. More specifically, it contains highly complicated traffic flows mixed with vehicles, cyclists, and pedestrians.

![](../examples/3d-tracking.gif)

## Evaluation
eval.py is the evaluation code. Run the code for a sample evaluation:

```
# export NUMBA_ENABLE_CUDASIM=1

# detection
python eval.py --gtPath=apollo_lab_test --dtPath=apollo_res_test --apSampleNum=10 #--typeFilterFlag #2>&1 | tee run.log

# tracking
# python eval.py --modeType=tracking --gtPath=../track/apollo_lab --dtPath=../track/apollo_res --typeFilterFlag
```

## Submission of data format
Submit your result for online evaluation here: [Submit](http://apolloscape.auto/submit.html)

[Leaderboard](http://apolloscape.auto/leader_board.html)

## Publication
Please cite our paper in your publications if our dataset is used in your research.

TrafficPredict: Trajectory Prediction for Heterogeneous Traffic-Agents. [PDF](https://arxiv.org/abs/1811.02146)
[BibTex](https://ad-apolloscape.cdn.bcebos.com/TrafficPredict/trafficpredict_bibtex.txt)

Yuexin Ma, Xinge Zhu, Sibo Zhang, Ruigang Yang, Wenping Wang, and Dinesh Manocha.

AAAI(oral), 2019

```
@inproceedings{ma2019trafficpredict,
  title={Trafficpredict: Trajectory prediction for heterogeneous traffic-agents},
  author={Ma, Yuexin and Zhu, Xinge and Zhang, Sibo and Yang, Ruigang and Wang, Wenping and Manocha, Dinesh},
  booktitle={Proceedings of the AAAI Conference on Artificial Intelligence},
  volume={33},
  pages={6120--6127},
  year={2019}
}
```

CVPR 2019 WAD Challenge on Trajectory Prediction and 3D Perception. [PDF](https://arxiv.org/pdf/2004.05966.pdf)
[BibTex](https://scholar.googleusercontent.com/scholar.bib?q=info:FM7KYweYqXIJ:scholar.google.com/&output=citation&scisdr=CgXjlNWZEK_chmykD1s:AAGBfm0AAAAAXpihF1tMiyTTew20m4a1LnPyWo9u5cbl&scisig=AAGBfm0AAAAAXpihF_RACGUoa0RN86NWhguFI1Z2YqmE&scisf=4&ct=citation&cd=-1&hl=en)

```
@article{zhang2020cvpr,
  title={CVPR 2019 WAD Challenge on Trajectory Prediction and 3D Perception},
  author={Zhang, Sibo and Ma, Yuexin and Yang, Ruigang and Li, Xin and Zhu, Yanliang and Qian, Deheng and Yang, Zetong and Zhang, Wenjing and Liu, Yuanpei},
  journal={arXiv preprint arXiv:2004.05966},
  year={2020}
}
```

