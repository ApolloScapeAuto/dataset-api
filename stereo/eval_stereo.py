"""
    Brief: Evaluate disparity
    Author: wangpeng54@baidu.com
    Date: 2019/6/8
"""

import cv2
import os
import glob
import numpy as np
import argparse
from collections import OrderedDict
import utils.utils as uts
import pdb

class StereoEval(object):
    """Evaluation of pose
    """

    def __init__(self, args):
        """ Initializer.
        """
        self.args = args
        self._names = ['D1_bg', 'D1_fg', 'D1_all']
        self._offset = []
        self.bg_mask_path = args.gt_dir + '/bg_mask/'
        self.fg_mask_path = args.gt_dir + '/fg_mask/'
        self.disparity_path = args.gt_dir + '/disparity/'
        self.res_disparity_path = args.test_dir + '/disparity/'

    def _checker(self):
        """check whether results folder and gt folder has the same dir tree
        """
        res_list = glob.glob(self.res_disparity_path + '*.png')
        self.res_image_names = [os.path.basename(line) for line in res_list]

        gt_list = glob.glob(self.disparity_path + '*.png')
        self.image_names = [os.path.basename(line) for line in gt_list]
        for image_name in self.image_names:
            assert image_name in self.res_image_names, \
                    'image %s is not in presented' % image_name

        return res_list, gt_list

    def reset(self):
        """ reset the metric
        """
        self._err_all = []
        self._err_fg = []
        self._err_bg = []

    def load_disparity(self, file_name):
        disparity = np.float32(cv2.imread(file_name, cv2.IMREAD_UNCHANGED))
        return disparity

    def load_mask(self, file_name):
        if not os.path.exists(file_name):
            raise ValueError('%s not exist' % file_name)
        mask = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
        return mask

    def eval(self):
        """ evaluate the results folder
        """
        res_files, gt_files = self._checker()
        self.reset()
        for res_file, gt_file in zip(res_files, gt_files):
            image_name = os.path.basename(gt_file)[:-4]
            gt_disparity = self.load_disparity(gt_file)
            res_disparity = self.load_disparity(res_file)
            self.update(gt_disparity, res_disparity, image_name)

        names, values = self.get()

        f = open(self.args.res_file, 'w')
        print('%5s %5s %5s' % tuple(names))
        f.write('%5s %5s %5s' % tuple(names))
        print('%5.4f %5.4f %5.4f' % tuple(values))
        f.write('%5.4f %5.4f %5.4f' % tuple(values))
        f.close()

    def update(self, label, pred, image_name):
        """Update metrics.
        """
        fg_mask = self.load_mask('%s/%s.png' % (self.fg_mask_path, image_name))
        bg_mask = self.load_mask('%s/%s.png' % (self.bg_mask_path, image_name))
        valid = fg_mask + bg_mask > 0
        abs_err = np.abs(label - pred) * valid
        err_count = np.logical_and(abs_err > 3.0,  (abs_err / (label + 1e-6) > 0.05))
        err_all = np.sum(err_count) / np.float32(np.sum(valid))
        err_fg = np.sum(err_count * fg_mask) / np.float32(np.sum(fg_mask))
        err_bg = np.sum(err_count * bg_mask) / np.float32(np.sum(bg_mask))

        self._err_all.append(err_all)
        self._err_fg.append(err_fg)
        self._err_bg.append(err_bg)

    def get(self):
        """Get current state of metrics.
        """
        err_all = np.array(self._err_all)
        err_fg = np.array(self._err_fg)
        err_bg = np.array(self._err_bg)
        values = [np.mean(err_fg), np.mean(err_bg), np.mean(err_all)]

        return (self._names, values)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Evaluation stereo output.')
    parser.add_argument('--test_dir', default='./test_eval_data/stereo_res/',
                        help='the dir of results')
    parser.add_argument('--gt_dir', default='./test_eval_data/stereo_gt/',
                        help='the dir of ground truth')
    parser.add_argument('--res_file', default='./test_eval_data/res.txt',
                        help='the dir of ground truth')
    parser.add_argument('--allow_missing', type=uts.str2bool, default='true',
                        help='the dir of ground truth')

    args = parser.parse_args()
    pose_metric = StereoEval(args)
    pose_metric.eval()
