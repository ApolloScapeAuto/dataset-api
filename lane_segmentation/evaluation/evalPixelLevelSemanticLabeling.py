#!/usr/bin/python
#
# The evaluation script for pixel-level semantic labeling.
# We use this script to evaluate your approach on the test set.
# You can use the script for your own evaluations.
#
# Please check the description before the "main" method below and set the
# required arguments as needed, such that this script can locate your results.
# If the default implementation of the method works, then it's most likely
# that our evaluation server will be able to process your results as well.
#
# Note that the script is a lot faster, if you enable cython support.
# WARNING: Cython only tested for Ubuntu 64bit OS.
# To enable cython, run
# cd thirdParty/cityscapesScripts && python setup.py build_ext --inplace
#
# To run this script, make sure that your results are images,
# where pixels encode the class IDs as defined in labels.py.
# Note that the regular ID is used, not the train ID.
# Further note that many classes are ignored from evaluation.
# Thus, authors are not expected to predict these classes and all
# pixels with a ground truth label that is ignored are ignored in
# evaluation.

# python imports
from __future__ import print_function
import os
import sys
import argparse

# Cityscapes imports
# For semantic segmentation task, we directly call cityscape functions
from thirdParty.cityscapesScripts.cityscapesscripts.evaluation import evalPixelLevelSemanticLabeling
from thirdParty.cityscapesScripts.cityscapesscripts.evaluation.evalPixelLevelSemanticLabeling import evaluateImgLists
from thirdParty.cityscapesScripts.cityscapesscripts.evaluation.evalPixelLevelSemanticLabeling import args

# Apolloscapes imports
from helpers.laneMarkDetection import labels, name2label, id2label, trainId2label, category2labels
from helpers import common as cm

try:
    from itertools import izip
except ImportError:
    izip = zip

topPath = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(topPath)


# overwrite cityscape variables to reuse their functions for apolloscape
evalPixelLevelSemanticLabeling.labels = labels
evalPixelLevelSemanticLabeling.name2label = name2label
evalPixelLevelSemanticLabeling.id2label = id2label
evalPixelLevelSemanticLabeling.trainId2label = trainId2label
evalPixelLevelSemanticLabeling.category2labels = category2labels

# The current implementation takes four arguments.
#   pred_dir : directory to the prediction images
#   pred_list: path to a list file specifying the relative image locations in
#              pred_dir
#   gt_dir   : directory to the groundtruth images
#   gt_list  : path to a list file specifying the relative image locations in
#              gt_dir


def main():
    global args
    args.evalPixelAccuracy = True

    parser = argparse.ArgumentParser()
    parser.add_argument("pred_dir", metavar='PRED_DIR',
            type=lambda x: cm.isValidDirectory(parser, x),
            help="directory to the predction images")
    parser.add_argument("pred_list", metavar='PRED_FILE',
            type=lambda x: cm.isValidFile(parser, x),
            help="path to a list file specifying the relative image locations in pred_dir")
    parser.add_argument("gt_dir", metavar='GT_DIR',
            type=lambda x: cm.isValidDirectory(parser, x),
            help="directory to the groundtruth images")
    parser.add_argument("gt_list", metavar='GT_FILE',
            type=lambda x: cm.isValidFile(parser, x),
            help="path to a list file specifying the relative image locations in gt_dir")
    argv = parser.parse_args()

    # prediction image list
    with open(argv.pred_list) as f:
        content = f.readlines()
    predictionImgList = [os.path.join(argv.pred_dir, line.strip()) for line in content]
    # groundtruth image list
    with open(argv.gt_list) as f:
        content = f.readlines()
    groundTruthImgList = [os.path.join(argv.gt_dir, line.strip()) for line in content]

    # evaluate
    evaluateImgLists(predictionImgList, groundTruthImgList, args)


# call the main method
if __name__ == "__main__":
    main()
