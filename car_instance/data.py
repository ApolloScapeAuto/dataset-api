
"""
    Brief: Apollo dataset 3d car class
    Author: wangpeng54@baidu.com
    Date: 2018/6/10
"""

import numpy as np


class ApolloScape(object):
    def __init__(self, args=None):
        self._data_config = {}
        self._data_dir = './apolloscape/'
        self._split = 'train'
        self._args = args

    def get_3d_car_config(self):
        """get configuration of the dataset for 3d car understanding
        """
        ROOT = self._data_dir + '3d_car_instance/' if self._args is None else \
            self._args.data_dir
        if hasattr(self._args, 'split'):
            split = self._args.split

        self._data_config['image_dir'] = ROOT + '%s/images/' % split
        self._data_config['pose_dir'] = ROOT + '%s/car_poses/' % split
        self._data_config['train_list'] = ROOT + '%s/split/train.txt'
        self._data_config['val_list'] = ROOT + '%s/split/val.txt'
        self._data_config['image_size'] = [2710, 3384]
        self._data_config['intrinsic'] = {
            'Camera_5': np.array(
                [2304.54786556982, 2305.875668062,
                 1686.23787612802, 1354.98486439791]),
            'Camera_6': np.array(
                [2300.39065314361, 2301.31478860597,
                 1713.21615190657, 1342.91100799715])}

        # normalized intrinsic
        cam_names = self._data_config['intrinsic'].keys()
        for c_name in cam_names:
            self._data_config['intrinsic'][c_name][[0, 2]] /= \
                self._data_config['image_size'][1]
            self._data_config['intrinsic'][c_name][[1, 3]] /= \
                self._data_config['image_size'][0]
        self._data_config['car_model_dir'] = ROOT + 'car_models/'

        return self._data_config

    def get_intrinsic(self, image_name):
        assert self._data_config
        for name in self._data_config['intrinsic'].keys():
            if name in image_name:
                return self._data_config['intrinsic'][name]
        raise ValueError('%s has no provided intrinsic' % image_name)
