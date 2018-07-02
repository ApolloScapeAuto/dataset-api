"""
    Brief: Compute similarity metrics for evaluation
    Author: wangpeng54@baidu.com
    Date: 2018/6/20
"""

import numpy as np
import utils as uts


def pose_similarity(dt, gt, shape_sim_mat):
    """compute pose similarity in terms of shape, translation and rotation
    Input:
        dt: np.ndarray detection [N x 7] first 6 dims are roll, pitch, yaw, x, y, z
        gt: save with dt

    Output:
        sim_shape: similarity based on shape eval
        dis_trans: distance based on translation eval
        dis_rot:   dis.. based on rotation eval
    """
    dt_num = len(dt)
    gt_num = len(gt)
    car_num = shape_sim_mat.shape[0]

    dt_car_id = np.uint32(dt[:, -1])
    gt_car_id = np.uint32(gt[:, -1])

    idx = np.tile(dt_car_id[:, None], (1, gt_num)).flatten() * car_num + \
            np.tile(gt_car_id[None, :], (dt_num, 1)).flatten()
    sims_shape = shape_sim_mat.flatten()[idx]
    sims_shape = np.reshape(sims_shape, [dt_num, gt_num])


    # translation similarity
    dt_car_trans = dt[:, 3:-1]
    gt_car_trans = gt[:, 3:-1]
    dis_trans = np.linalg.norm(np.tile(dt_car_trans[:, None, :], [1, gt_num, 1]) - \
            np.tile(gt_car_trans[None, :, :], [dt_num, 1, 1]), axis=2)

    # rotation similarity
    dt_car_rot = uts.euler_angles_to_quaternions(dt[:, :3])
    gt_car_rot = uts.euler_angles_to_quaternions(gt[:, :3])
    q1 = dt_car_rot / np.linalg.norm(dt_car_rot, axis=1)[:, None]
    q2 = gt_car_rot / np.linalg.norm(gt_car_rot, axis=1)[:, None]


    # diff = abs(np.matmul(q1, np.transpose(q2)))
    diff = abs(1 - np.sum(np.square(np.tile(q1[:, None, :], [1, gt_num, 1]) - \
            np.tile(q2[None, :, :], [dt_num, 1, 1])), axis=2) / 2.0)
    dis_rot = 2 * np.arccos(diff) * 180 / np.pi

    return sims_shape, dis_trans, dis_rot



def IOU(mask1, mask2):
    """ compute the intersection of union of two logical inputs
    Input:
        mask1: the first mask
        mask2: the second mask
    """

    inter = np.logical_and(mask1 > 0, mask2 > 0)
    union = np.logical_or(mask1 > 0, mask2 > 0)
    if np.sum(inter) == 0:
        return 0.

    return np.float32(np.sum(inter)) / np.float32(np.sum(union))





if __name__ == '__main__':
    shape_sim_mat = np.loadtxt('./test_eval_data/sim_mat.txt')
    fake_gt = []
    fake_dt = []
    sim_shape, sim_trans, sim_rot = pose_similarity(fake_dt, fake_gt, shape_sim_mat)


