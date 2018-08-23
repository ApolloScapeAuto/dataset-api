"""
    Brief: Utility functions of apolloscape tool kit
    Author: wangpeng54@baidu.com
    Date: 2018/6/10
"""

import numpy as np
import math


def euler_angles_to_quaternions(angle):
    """Convert euler angels to quaternions representation.
    Input:
        angle: n x 3 matrix, each row is [roll, pitch, yaw]
    Output:
        q: n x 4 matrix, each row is corresponding quaternion.
    """

    in_dim = np.ndim(angle)
    if in_dim == 1:
        angle = angle[None, :]

    n = angle.shape[0]
    roll, pitch, yaw = angle[:, 0], angle[:, 1], angle[:, 2]
    q = np.zeros((n, 4))

    cy = np.cos(yaw * 0.5)
    sy = np.sin(yaw * 0.5)
    cr = np.cos(roll * 0.5)
    sr = np.sin(roll * 0.5)
    cp = np.cos(pitch * 0.5)
    sp = np.sin(pitch * 0.5)

    q[:, 0] = cy * cr * cp + sy * sr * sp
    q[:, 1] = cy * sr * cp - sy * cr * sp
    q[:, 2] = cy * cr * sp + sy * sr * cp
    q[:, 3] = sy * cr * cp - cy * sr * sp

    return q


def intrinsic_mat_to_vec(K):
    """Convert a 3x3 intrinsic vector to a 4 dim intrinsic
       matrix
    """
    return np.array([K[0, 0], K[1, 1], K[0, 2], K[1, 2]])


def intrinsic_vec_to_mat(intrinsic, shape=None):
    """Convert a 4 dim intrinsic vector to a 3x3 intrinsic
       matrix
    """
    if shape is None:
        shape = [1, 1]

    K = np.zeros((3, 3), dtype=np.float32)
    K[0, 0] = intrinsic[0] * shape[1]
    K[1, 1] = intrinsic[1] * shape[0]
    K[0, 2] = intrinsic[2] * shape[1]
    K[1, 2] = intrinsic[3] * shape[0]
    K[2, 2] = 1.0

    return K


def round_prop_to(num, base=4.):
    """round a number to integer while being propotion to
       a given base number
    """
    return np.ceil(num / base) * base


def euler_angles_to_rotation_matrix(angle, is_dir=False):
    """Convert euler angels to quaternions.
    Input:
        angle: [roll, pitch, yaw]
        is_dir: whether just use the 2d direction on a map
    """
    roll, pitch, yaw = angle[0], angle[1], angle[2]

    rollMatrix = np.matrix([
        [1, 0, 0],
        [0, math.cos(roll), -math.sin(roll)],
        [0, math.sin(roll), math.cos(roll)]])

    pitchMatrix = np.matrix([
        [math.cos(pitch), 0, math.sin(pitch)],
        [0, 1, 0],
        [-math.sin(pitch), 0, math.cos(pitch)]])

    yawMatrix = np.matrix([
        [math.cos(yaw), -math.sin(yaw), 0],
        [math.sin(yaw), math.cos(yaw), 0],
        [0, 0, 1]])

    R = yawMatrix * pitchMatrix * rollMatrix
    R = np.array(R)

    if is_dir:
        R = R[:, 2]

    return R


def rotation_matrix_to_euler_angles(R, check=True):
    """Convert rotation matrix to euler angles
    Input:
        R: 3 x 3 rotation matrix
        check: whether Check if a matrix is a valid
            rotation matrix.
    Output:
        euler angle [x/roll, y/pitch, z/yaw]
    """

    def isRotationMatrix(R):
        Rt = np.transpose(R)
        shouldBeIdentity = np.dot(Rt, R)
        I = np.identity(3, dtype=R.dtype)
        n = np.linalg.norm(I - shouldBeIdentity)
        return n < 1e-6

    if check:
        assert(isRotationMatrix(R))

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])
    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])

    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])


def convert_pose_mat_to_6dof(pose_file_in, pose_file_out):
    """Convert a pose file with 4x4 pose mat to 6 dof [xyz, rot]
    representation.
    Input:
        pose_file_in: a pose file with each line a 4x4 pose mat
        pose_file_out: output file save the converted results
    """

    poses = [line for line in open(pose_file_in)]
    output_motion = np.zeros((len(poses), 6))
    f = open(pose_file_out, 'w')
    for i, line in enumerate(poses):
        nums = line.split(' ')
        mat = [np.float32(num.strip()) for num in nums[:-1]]
        image_name = nums[-1].strip()
        mat = np.array(mat).reshape((4, 4))

        xyz = mat[:3, 3]
        rpy = rotation_matrix_to_euler_angles(mat[:3, :3])
        output_motion = np.hstack((xyz, rpy)).flatten()
        out_str = '%s %s\n' % (image_name, np.array2string(output_motion,
                  separator=',',
                  formatter={'float_kind': lambda x: "%.7f" % x})[1:-1])

        f.write(out_str)
    f.close()

    return output_motion


def trans_vec_to_mat(rot, trans, dim=4):
    """ project vetices based on extrinsic parameters to 3x4 matrix
    """
    mat = euler_angles_to_rotation_matrix(rot)
    mat = np.hstack([mat, trans.reshape((3, 1))])
    if dim == 4:
        mat = np.vstack([mat, np.array([0, 0, 0, 1])])

    return mat


def project(pose, scale, vertices):
    """ transform the vertices of a 3D car model based on labelled pose
    Input:
        pose: 0-3 rotation, 4-6 translation
        scale: the scale at each axis of the car
        vertices: the vertices position
    """

    if np.ndim(pose) == 1:
        mat = trans_vec_to_mat(pose[:3], pose[3:])
    elif np.ndim(pose) == 2:
        mat = pose

    vertices = vertices * scale
    p_num = vertices.shape[0]

    points = vertices.copy()
    points = np.hstack([points, np.ones((p_num, 1))])
    points = np.matmul(points, mat.transpose())

    return points[:, :3]


def crop_image(image, crop_in):
    """crop an image by given image
    Input:
        image: h x w or h x w x c image
        crop_in: a normalized crop
    """
    # crop must be a normalized crop
    crop = crop_in.copy()
    assert np.max(np.array(crop)) < 1.0
    h, w = image.shape[:2]
    crop[[0, 2]] *= h
    crop[[1, 3]] *= w
    crop = np.uint32(crop)

    if np.ndim(image) == 2:
        cropped_img = image[crop[0]:crop[2], crop[1]:crop[3]]
    elif np.ndim(image) == 3:
        cropped_img = image[crop[0]:crop[2], crop[1]:crop[3], :]
    else:
        raise ValueError('not support image dim > 3')

    return cropped_img


def plot_images(images,
                layout=[2, 2],
                fig_size=10,
                save_fig=False,
                fig_name=None):
    """Plot a dictionary of images:
    Input:
        images: dictionary {'image', image}
        layout: the subplot layout of output
        fig_size: size of figure
        save_fig: bool, whether save the plot images
        fig_name: if save_fig, then provide a name to save
    """

    import matplotlib.pyplot as plt
    import matplotlib.pylab as pylab

    plt.figure(figsize=(10, 5))
    pylab.rcParams['figure.figsize'] = fig_size, fig_size / 2
    Keys = images.keys()
    for iimg, name in enumerate(Keys):
        assert len(images[name].shape) >= 2

    for iimg, name in enumerate(Keys):
        s = plt.subplot(layout[0], layout[1], iimg + 1)
        plt.imshow(images[name])

        s.set_xticklabels([])
        s.set_yticklabels([])
        s.set_title(name)
        s.yaxis.set_ticks_position('none')
        s.xaxis.set_ticks_position('none')

    plt.tight_layout()
    if save_fig:
        pylab.savefig(fig_name)
    else:
        plt.show()


def str2bool(conf_str):
    """tool for converting str to bool for python argparser
    Inputs:
        conf_str: 'str' indicating a boolean value.
    """
    if conf_str.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif conf_str.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ValueError('Boolean value expected.')


if __name__ == '__main__':
    pass
