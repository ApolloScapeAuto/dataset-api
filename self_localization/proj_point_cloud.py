"""
    Brief: Test renderer
    Author: wangpeng54@baidu.com
    Date: 2018/6/10
"""

from easydict import EasyDict as edict
import cv2
import utils.data as data
import utils.utils as uts

import numpy as np
import renderer.projector as pj


class SelfLocVisualizer(object):
    def __init__(self, args=None, scale=0.4):
        self.dataset = data.ApolloScape(args)
        h, w = self.dataset._data_config['image_size']
        self.image_size = np.uint32(uts.round_prop_to(
            np.float32([h * scale, w * scale])))
        self.shader = {}
        for shader_name in ['vertex', 'fragment', 'geometry']:
            self.shader[shader_name] = './%s/PointLabel.%sshader' % \
                    ('./renderer/shader', shader_name)

    def _to_proj_mat(self, rot, trans):
        """convert 6 dof represenatation to projection matrix
        """
        ext = np.zeros((4, 4), dtype=np.float32)
        ext[:3, :3] = uts.euler_angles_to_rotation_matrix(rot)
        ext[:3, 3] = trans
        ext[3, 3] = 1.0
        ext = np.linalg.inv(ext)
        ext = np.transpose(ext)
        ext = np.float32(ext.flatten())
        return ext

    def _to_proj_intr(self, intr, height, width):
        """convert 4 dim intrinsic to projection matrix
        """
        intrinsic = uts.intrinsic_vec_to_mat(intr, [height, width])
        intr_for_render = np.transpose(intrinsic)
        intr_for_render = intr_for_render.flatten()
        return intr_for_render

    def show_pose(self,  in_case=None):
        """ show an image pose by render point to image
        """
        self._data_config = self.dataset.get_self_local_config(
                in_case.Road_id, in_case.split)
        cloud_name = '%s/%s/pc_sub.pcd' % (self._data_config['cloud_dir'],
                in_case.time_id)
        proj = pj.pyRenderPCD(cloud_name,
                              self.shader['vertex'],
                              self.shader['geometry'],
                              self.shader['fragment'],
                              self.image_size[0],
                              self.image_size[1],
                              in_case.with_label)

        intr = self._to_proj_intr(
                self._data_config['intrinsic'][in_case.camera_name],
                self.image_size[0], self.image_size[1])
        ext = self._to_proj_mat(in_case.pose[:3], in_case.pose[3:])
        label, depth = proj.pyRenderToRGBDepth(intr, ext)

        image_path = '%s/%s/%s/Camera %s/%s.jpg' % (\
                self._data_config['image_dir'],
                in_case.time_id, in_case.record_id,
                in_case.camera_name[-1], in_case.image_name)

        image = cv2.resize(cv2.imread(image_path),
                (self.image_size[1], self.image_size[0]))
        assert not (image is None)

        uts.plot_images({'image': np.uint8(image),
                         'depth': depth,
                         'mask': label},
                         layout=[1, 3])

def test_projection():
    """Test function of verifying the pose and image
    """
    # The image information
    test_case = edict()
    test_case.Road_id = 'Road11'
    test_case.split = 'Train'
    test_case.time_id = 'GZ20180310B'
    test_case.record_id = 'Record001'
    test_case.camera_name = 'Camera_5'
    test_case.image_name = '180310_021218247_Camera_5'
    test_case.pose = np.array([-1.41979, -0.0416934, -1.58829, \
            17.3965, 388.547, 38.8695])
    test_case.with_label = 0

    config = edict()
    # root folder for self localization
    config.data_dir = '../apolloscape/self-localization/'
    config.split = test_case.split
    visualizer = SelfLocVisualizer(config)
    visualizer.show_pose(test_case)


if __name__ == '__main__':
    test_projection()





