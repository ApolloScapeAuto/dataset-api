"""
    Brief: Evaluation 6 DOF pose from self localization
    Author: wangpeng54@baidu.com
    Date: 2018/6/10
"""

import os
import numpy as np
import argparse
from collections import OrderedDict
import utils.utils as uts


class PoseEval(object):
    """Evaluation of pose
    """

    def __init__(self, args):
        """ Initializer.
        """
        self.args = args
        self._names = ['median_xyz', 'median_theta']
        self._eval_cameras = ['Camera 5']
        self._offset = []
        self._theta = []
        self._rot_idx = [0, 1, 2]
        self._trans_idx = [3, 4, 5]

    def _checker(self, res_folder, gt_folder):
        """check whether results folder and gt folder has the same dir tree
        """

        def get_scene_files(root_folder, scene_name):
            seq_list = []
            scene_dir = root_folder + scene_name
            tree = [x[0][len(scene_dir):] for x in os.walk(scene_dir)]
            for line in tree:
                if 'Record' in line:
                    for Camera in self._eval_cameras:
                        seq_list.append('%s/%s/%s/%s.txt' % (root_folder, scene_name,
                                                             line, Camera))
            return seq_list

        res_seq_list = OrderedDict({})
        gt_seq_list = OrderedDict({})

        scenes_gt = sorted(os.listdir(gt_folder))
        scenes_res = sorted(os.listdir(res_folder))
        if not self.args.allow_missing:
            if not len(scenes_res) == len(scenes_gt):
                raise ValueError(
                    'Test result scene numbers are not the same as ground truth')

        for scene in scenes_gt:
            gt_seq_list[scene] = sorted(get_scene_files(gt_folder, scene))
            if not (scene in scenes_res):
                continue
            res_seq_list[scene] = sorted(get_scene_files(res_folder, scene))
            if not len(res_seq_list[scene]) == len(gt_seq_list[scene]):
                raise ValueError('Test scene %s seq numbers are not the same as ground truth'
                                 % scene)

        return res_seq_list, gt_seq_list

    def reset(self):
        """ reset the metric
        """
        self._offset = []
        self._theta = []

    def load_pose_file(self, pose_file):
        """ load one result file
        """
        lines = [line.strip().split(' ') for line in open(pose_file)]
        poses = OrderedDict({})
        for line in lines:
            poses[line[0]] = np.array(
                [[np.float32(num) for num in line[1].split(',')]])

        return poses

    def dict_to_array(self, poses_gt, poses):
        """ convert pose dict to np array for faster eval
        """
        res = []
        gt = []
        for key, value in poses_gt.items():
            gt.append(value)
            res.append(poses[key])
        res = np.concatenate(res)
        gt = np.concatenate(gt)
        return gt, res

    def eval(self):
        """ evaluate the results folder
        """
        res_files, gt_files = self._checker(self.args.test_dir,
                                            self.args.gt_dir)
        res_all = OrderedDict({})
        for scene in res_files.keys():
            self.reset()
            for res_file, gt_file in zip(res_files[scene], gt_files[scene]):
                poses = self.load_pose_file(res_file)
                poses_gt = self.load_pose_file(gt_file)
                if not len(poses.items()) == len(poses_gt.items()):
                    raise ValueError('image num of scene %s, seq %s is not \
                               the same as ground truth' % (scene, res_file))

                poses_gt, poses = self.dict_to_array(poses_gt, poses)
                self.update(poses_gt, poses)

            _, values = self.get()
            res_all[scene] = values

        f = open(self.args.res_file, 'w')
        print('%10s: %5s %5s' % ('scene_name', 'xyz', 'rot'))
        for scene in gt_files.keys():
            values = res_all[scene] if scene in res_all else -1 * np.ones(2)
            print('%10s: %5.4f %5.4f' % (scene, values[0], values[1]))
            f.write('%s %.4f,%.4f\n' % (scene, values[0], values[1]))
        f.close()

    def update(self, label, pred):
        """Update metrics.
        """
        pose_x = label[:, self._trans_idx]
        pred_x = pred[:, self._trans_idx]

        pose_q = uts.euler_angles_to_quaternions(label[:, self._rot_idx])
        pred_q = uts.euler_angles_to_quaternions(pred[:, self._rot_idx])

        q1 = pose_q / np.linalg.norm(pose_q, axis=1)[:, None]
        q2 = pred_q / np.linalg.norm(pred_q, axis=1)[:, None]
        diff = abs(np.ravel(1 - np.sum(np.square((q1 - q2)) / 2, axis=1)))
        self._theta.append(2 * np.arccos(diff) * 180 / np.pi)
        self._offset.append(np.ravel(np.linalg.norm(pose_x - pred_x, axis=1)))

    def get(self):
        """Get current state of metrics.
        """
        all_offset = np.concatenate(self._offset)
        all_theta = np.concatenate(self._theta)
        median_offset = np.median(all_offset)
        median_theta = np.median(all_theta)
        values = [median_offset, median_theta]

        return (self._names, values)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Evaluation self localization.')
    parser.add_argument('--test_dir', default='./test_eval_data/Test/',
                        help='the dir of results')
    parser.add_argument('--gt_dir', default='./test_eval_data/Test_gt/',
                        help='the dir of ground truth')
    parser.add_argument('--res_file', default='./test_eval_data/res.txt',
                        help='the dir of ground truth')
    parser.add_argument('--allow_missing', type=uts.str2bool, default='true',
                        help='the dir of ground truth')

    args = parser.parse_args()
    pose_metric = PoseEval(args)
    pose_metric.eval()
