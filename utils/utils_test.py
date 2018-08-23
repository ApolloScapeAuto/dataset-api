import utils as uts


def convert_pose_mat_to_6dof_test():
    print('test convert_pose_mat_to_6dof')
    pose_in_file = 'pose.txt'
    pose_out_file = '/tmp/pose_out.txt'
    uts.convert_pose_mat_to_6dof(pose_in_file, pose_out_file)
    lines = [line for line in open(pose_out_file, 'r')]
    lines2 = [line for line in open(pose_in_file, 'r')]
    assert len(lines) == len(lines2)


if __name__ == '__main__':
    convert_pose_mat_to_6dof_test()
    print('test utils pass')
