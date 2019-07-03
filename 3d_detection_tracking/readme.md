# The 3D Lidar Object Detection and Tracking Challenge of Apolloscape Dataset
[For detail and download](http://apolloscape.auto/tracking.html)

## Introduction
Our 3D Lidar object detection and tracking dataset consists of LiDAR scanned point clouds with high quality annotation. It is collected under various lighting conditions and traffic densities in Beijing, China. More specifically, it contains highly complicated traffic flows mixed with vehicles, cyclists, and pedestrians.

![](../examples/3d-tracking.gif)



## Evaluation
eval.py is the evaluation code. Run the code for a sample evaluation:

```
source activate apolloscape

# export NUMBA_ENABLE_CUDASIM=1
# export CUDA_VISIBLE_DEVICES=4
# export CUDA_VISIBLE_DEVICES=4,5,6,7

# tracking
python eval.py --modeType=tracking --gtPath=../track/apollo_lab --dtPath=../track/apollo_res --typeFilterFlag
# detection
# python eval.py --gtPath=apollo_lab_test --dtPath=apollo_res_test --apSampleNum=10 #--typeFilterFlag #2>&1 | tee run.log
```

## Submission of data format
Submit your result for online evaluation here: [Submit](http://apolloscape.auto/submit.html)

[Leaderboard](http://apolloscape.auto/leader_board.html)

## Publication
TrafficPredict: Trajectory Prediction for Heterogeneous Traffic-Agents. [PDF](https://arxiv.org/abs/1811.02146)
[BibTex](https://ad-apolloscape.cdn.bcebos.com/TrafficPredict/trafficpredict_bibtex.txt)

Yuexin Ma, Xinge Zhu, Sibo Zhang, Ruigang Yang, Wenping Wang, and Dinesh Manocha.

AAAI(oral), 2019

```
@article{ma2018trafficpredict,
  title={TrafficPredict: Trajectory prediction for heterogeneous traffic-agents},
  author={Ma, Yuexin and Zhu, Xinge and Zhang, Sibo and Yang, Ruigang and Wang, Wenping and Manocha, Dinesh},
  journal={arXiv preprint arXiv:1811.02146},
  year={2018}
}
```

## Contact
Please feel free to contact us, or raise an issue with any questions, suggestions or comments:
* apollo-scape@baidu.com
