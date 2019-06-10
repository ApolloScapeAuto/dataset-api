* [The Trajectory Prediction Challenge of Apolloscape](#the-trajectory-prediction-challenge-of-apolloscape)
   * [Evaluation](#evaluation)
   * [Contact](#contact)
   
# The Trajectory Prediction Challenge of Apolloscapes Dataset

## Introduction
This repository contains the evaluation scripts for the trajectory prediction challenge of the ApolloScapes dataset. Our trajectory dataset consists of camera-based images, LiDAR scanned point clouds, and manually annotated trajectories. It is collected under various lighting conditions and traffic densities in Beijing, China. More specifically, it contains highly complicated traffic flows mixed with vehicles, riders, and pedestrians.

## Dataset download
[trajectory dataset download](http://apolloscape.auto/trajectory.html)


## Evaluation
evaluation.py is the evaluation code. Run the code for a sample evaluation:

```
python evaluation.py --object_file=./test_eval_data/considered_objects.txt --gt_dir=./test_eval_data/prediction_gt.txt --res_file=./test_eval_data/prediction_result.txt
./test_eval_data/considered_objects.txt contains objects we consider when counting the error.
./test_eval_data/prediction_gt.txt is just for testing the code which is not the real ground truth. Please submit your result to the leaderboard to get true error.
./test_eval_data/prediction_result.txt is one example for submitted result.
```

### Submission of data format
Submit your result for online evaluation here: [Submit](http://apolloscape.auto/submit.html)
Leadertboard: [Leaderboard](http://apolloscape.auto/leader_board.html)

## Contact
Please feel free to contact us, or raise an issue with any questions, suggestions or comments:
* apollo-scape@baidu.com
