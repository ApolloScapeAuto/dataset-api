'''
Evaluation code for trajectory prediction.

We record the objects in the last frame of every sequence in test dataset as considered objects, which is stored in considered_objects.txt.
We compare the error between your predicted locations in the next 3s(six positions) and the ground truth for these considered objects.

To run this script, make sure that your results are in required format.
'''

import os
import argparse
import numpy as np


def evaluation(frame_data_result, frame_data_gt, consider_peds):

    # defined length of predicted trajectory
    predict_len = 6
    # the counter for testing sequences
    sequence_count = 0
    # weighted coefficient for vehicles, pedestrians, bicyclists respectively
    vehicle_coe = 0.2
    pedestrian_coe = 0.58
    bicycle_coe = 0.22
    # error for missing considered objects
    miss_error = 100
    # record displacement error for three types of objects
    vehicle_error = []
    pedestrian_error = []
    bicycle_error = []
    # record final displacement error for three types of objects
    vehicle_final_error = []
    pedestrian_final_error = []
    bicycle_final_error = []

    for i in range(0, len(frame_data_result) - predict_len + 1, predict_len):
        current_consider_ped = consider_peds[sequence_count]
        sequence_count = sequence_count + 1
        for j in range(i, i + predict_len):
            for ped_gt in frame_data_gt[j]:
                if current_consider_ped.count(int(ped_gt[0])):
                    # ignore unknown objects
                    if ped_gt[1] == 5:
                        continue
                    # error will be large if missing considered objects
                    error = miss_error
                    for ped_res in frame_data_result[j]:
                        if int(ped_res[0]) == int(ped_gt[0]):
                            error = distance([ped_gt[2], ped_gt[3]], [ped_res[2], ped_res[3]])
                            break
                    # distribute the error to different types of objects
                    if ped_gt[1] == 1 or ped_gt[1] == 2:
                        vehicle_error.append(error)
                        if j == i + predict_len - 1:
                            vehicle_final_error.append(error)
                    elif ped_gt[1] == 3:
                        pedestrian_error.append(error)
                        if j == i + predict_len - 1:
                            pedestrian_final_error.append(error)
                    elif ped_gt[1] == 4:
                        bicycle_error.append(error)
                        if j == i + predict_len - 1:
                            bicycle_final_error.append(error)



    # the mean error for objects
    vehicle_mean_error = sum(vehicle_error) / len(vehicle_error)
    pedestrian_mean_error = sum(pedestrian_error) / len(pedestrian_error)
    bicycle_mean_error = sum(bicycle_error) / len(bicycle_error)
    # the final error for objects
    vehicle_final_error = sum(vehicle_final_error) / len(vehicle_final_error)
    pedestrian_final_error = sum(pedestrian_final_error) / len(pedestrian_final_error)
    bicycle_final_error = sum(bicycle_final_error) / len(bicycle_final_error)
    # weighted sum of mean error
    WSADE = vehicle_mean_error * vehicle_coe + pedestrian_mean_error * pedestrian_coe + bicycle_mean_error * bicycle_coe
    # weighted sum of final error
    WSFDE = vehicle_final_error * vehicle_coe + pedestrian_final_error * pedestrian_coe + bicycle_final_error * bicycle_coe

    print('WSADE:', WSADE)
    print('ADEv, ADEp, ADEb:', vehicle_mean_error, pedestrian_mean_error, bicycle_mean_error)
    print('WSFDE:', WSFDE)
    print('FDEv, FDEp, FDEb:',vehicle_final_error, pedestrian_final_error, bicycle_final_error)

    return (WSADE, vehicle_mean_error, pedestrian_mean_error, bicycle_mean_error,
            WSFDE, vehicle_final_error, pedestrian_final_error, bicycle_final_error)


def readConsiderObjects(filename):
    print('Load file: ', filename)

    # load considered objects of each sequence
    consider_peds = []
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break

            curLine = lines.strip().split(" ")
            intLine = map(int, curLine)
            consider_peds.append(intLine)

    return consider_peds


def readTrajectory(filename):

    print('Load file: ',filename)
    raw_data = []
    # load all the data in the file
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()
            if not lines:
                break
            timestamp, id, type, x, y = [float(i) for i in lines.split()]
            raw_data.append((timestamp, id, type, x, y))

    # get frame list
    frameList = []
    for i in range(len(raw_data)):
        if frameList.count(raw_data[i][0]) == 0:
            frameList.append(raw_data[i][0])

    counter = 0
    frame_data = []
    for ind, frame in enumerate(frameList):
        pedsInFrame = []
        # Extract all pedestrians in current frame
        for r in range(counter, len(raw_data)):
            row = raw_data[r]

            if raw_data[r][0] == frame:
                pedsInFrame.append([row[1], row[2], row[3], row[4]])
                counter += 1
            else:
                break

        frame_data.append(pedsInFrame)

    return frame_data


def distance(pos1, pos2):
    # Euclidean distance
    return np.sqrt(pow(pos1[0]-pos2[0], 2) + pow(pos1[1]-pos2[1], 2))


def main():
    parser = argparse.ArgumentParser(
        description='Evaluation self localization.')

    parser.add_argument('--gt_dir', default='./test_eval_data/prediction_gt.txt',
                        help='the dir of ground truth')
    parser.add_argument('--object_file', default='./test_eval_data/considered_objects.txt',
                        help='the dir of considered objects')
    parser.add_argument('--res_file', default='./test_eval_data/prediction_result.txt',
                        help='the dir of results')

    args = parser.parse_args()
    # load results
    file_result = args.res_file
    frame_data_result = readTrajectory(file_result)
    # load ground truth
    file_gt = args.gt_dir
    frame_data_gt = readTrajectory(file_gt)
    # load considered objects
    file_consider_objects = args.object_file
    consider_peds = readConsiderObjects(file_consider_objects)
    # Do evaluation
    evaluation(frame_data_result, frame_data_gt, consider_peds)


if __name__ == '__main__':

    main()



