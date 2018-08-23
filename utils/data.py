"""
    Brief: Apollo dataset path and parameters config class
    Author: wangpeng54@baidu.com
    Date: 2018/6/10
"""

import cv2
import numpy as np
import utils as uts


class ApolloScape(object):
    def __init__(self, args=None, scale=1.0, use_stereo=False):
        self._data_dir = './apolloscape/'
        self._args = args
        self._scale = scale
        self._get_data_parameters()
        if use_stereo:
            self._get_stereo_rectify_params()

    def _get_data_parameters(self):
        """get the data configuration of the dataset.
           These parameters are shared across different tasks
        """
        self._data_config = {}
        self._data_config['image_size_raw'] = [2710, 3384]
        # when need to rescale image due to large data
        self._data_config['image_size'] = [int(2710 * self._scale),
                                           int(3384 * self._scale)]

        # fx, fy, cx, cy
        self._data_config['intrinsic'] = {
            'Camera_5': np.array(
                [2304.54786556982, 2305.875668062,
                 1686.23787612802, 1354.98486439791]),
            'Camera_6': np.array(
                [2300.39065314361, 2301.31478860597,
                 1713.21615190657, 1342.91100799715])}

        # normalized intrinsic for handling image resizing
        cam_names = self._data_config['intrinsic'].keys()
        for c_name in cam_names:
            self._data_config['intrinsic'][c_name][[0, 2]] /= \
                self._data_config['image_size_raw'][1]
            self._data_config['intrinsic'][c_name][[1, 3]] /= \
                self._data_config['image_size_raw'][0]

        # relative pose of camera 6 wrt camera 5
        self._data_config['extrinsic'] = {
            'R': np.array([
                [9.96978057e-01, 3.91718762e-02, -6.70849865e-02],
                [-3.93257593e-02, 9.99225970e-01, -9.74686202e-04],
                [6.69948100e-02, 3.60985263e-03, 9.97746748e-01]]),
            'T': np.array([-0.6213358, 0.02198739, -0.01986043])
        }

        # crop margin after stereo rectify for getting the region
        # with stereo matching, however it can remove some valid region
        self._data_config['stereo_crop'] = np.array(
            [1232., 668., 2500., 2716.])
        self._data_config['stereo_crop'][[0, 2]] /= \
            self._data_config['image_size_raw'][0]
        self._data_config['stereo_crop'][[1, 3]] /= \
            self._data_config['image_size_raw'][1]

    def _get_stereo_rectify_params(self):
        """ if using stereo, we need to findout the stereo parameters,
            based on the extrinsic parameters for the two cameras
        """
        camera_names = self._data_config['intrinsic'].keys()
        camera5_mat = uts.intrinsic_vec_to_mat(
            self._data_config['intrinsic']['Camera_5'],
            self._data_config['image_size'])
        camera6_mat = uts.intrinsic_vec_to_mat(
            self._data_config['intrinsic']['Camera_6'],
            self._data_config['image_size'])

        distCoeff = np.zeros(4)
        image_size = (self._data_config['image_size'][1],
                      self._data_config['image_size'][0])

        # compare the two image
        R1, R2, P1, P2, Q, roi1, roi2 = cv2.stereoRectify(
            cameraMatrix1=camera5_mat,
            distCoeffs1=distCoeff,
            cameraMatrix2=camera6_mat,
            distCoeffs2=distCoeff,
            imageSize=image_size,
            R=self._data_config['extrinsic']['R'],
            T=self._data_config['extrinsic']['T'],
            flags=cv2.CALIB_ZERO_DISPARITY,
            alpha=1)

        # for warping image 5
        map1x, map1y = cv2.initUndistortRectifyMap(
            cameraMatrix=camera5_mat,
            distCoeffs=distCoeff,
            R=R1,
            newCameraMatrix=P1,
            size=image_size,
            m1type=cv2.CV_32FC1)

        # for warping image 6
        map2x, map2y = cv2.initUndistortRectifyMap(
            cameraMatrix=camera6_mat,
            distCoeffs=distCoeff,
            R=R2,
            newCameraMatrix=P2,
            size=image_size,
            m1type=cv2.CV_32FC1)

        res = {'Camera_5_rot': R1,
               'Camera_5_intr': P1,
               'Camera_5_mapx': map1x,
               'Camera_5_mapy': map1y,
               'Camera_6_rot': R2,
               'Camera_6_intr': P2,
               'Camera_6_mapx': map2x,
               'Camera_6_mapy': map2y}

        # get new intrinsic and rotation parameters after rectification
        for name in camera_names:
            res[name + '_intr'] = uts.intrinsic_mat_to_vec(res[name + '_intr'])
            res[name + '_intr'][[0, 2]] /= self._data_config['image_size'][1]
            res[name + '_intr'][[1, 3]] /= self._data_config['image_size'][0]
            rect_extr_mat = np.eye(4)
            rect_extr_mat[:3, :3] = res[name + '_rot']
            res[name + '_ext'] = rect_extr_mat

        self._data_config.update(res)

    def stereo_rectify(self, image, camera_name,
                       interpolation=cv2.INTER_LINEAR):
        """ Given an image we rectify this image for stereo matching
        Input:
            image: the inputs image
            camera_name: 'Camera_5' or 'Camera_6' the name of camera where the
                    image is
            interpolation: the method of warping
        Output:
            the rectified image
        """
        image_rect = cv2.remap(image,
                               self._data_config[camera_name + '_mapx'],
                               self._data_config[camera_name + '_mapy'],
                               interpolation)
        return image_rect

    def get_3d_car_config(self):
        """get configuration of the dataset for 3d car understanding
        """
        ROOT = self._data_dir + '3d_car_instance/' if self._args is None else \
            self._args.data_dir
        split = self._args.split if hasattr(
            self._args, 'split') else 'sample_data'

        self._data_config['image_dir'] = ROOT + '%s/images/' % split
        self._data_config['pose_dir'] = ROOT + '%s/car_poses/' % split
        self._data_config['train_list'] = ROOT + '%s/split/train.txt'
        self._data_config['val_list'] = ROOT + '%s/split/val.txt'

        self._data_config['car_model_dir'] = ROOT + 'car_models/'

        return self._data_config

    def get_intrinsic(self, image_name, camera_name=None):
        assert self._data_config
        if camera_name:
            return self._data_config['intrinsic'][camera_name]
        else:
            for name in self._data_config['intrinsic'].keys():
                if name in image_name:
                    return self._data_config['intrinsic'][name]
        raise ValueError('%s has no provided intrinsic' % image_name)


