### Instruction for renderer
The renderer is used for render depth map/label map(if available) from dense semantic point clouds based on opengl and shader. 
The renderer is used for the paper:

```
 @inproceedings{wang2018dels,
   title={DeLS-3D: Deep Localization and Segmentation with a 3D Semantic Map},
   author={Wang, Peng and Yang, Ruigang and Cao, Binbin and Xu, Wei and Lin, Yuanqing},
   booktitle={CVPR},
   pages={5860--5869},
   year={2018}
 }
```

Dependency: `python-tk libeigen3-dev libglfw-dev libgles2-mesa-dev libglew-dev libboost-all-dev libpcl-all`

Tested with Ubuntu 14.04 and Python 2.7, nvidia diver 375.26. We use `pcl-1.8` For other versions, we haven't tested it. 


```bash
#!/bin/bash
python test_projector.py'
```
