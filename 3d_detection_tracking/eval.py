#!/home/guanchenye/thirdparty/preda/envs/apolloscape/bin/python
"""
    Brief: Evaluation of 3D Detection/Tracking
    Date: 2019/6/1
"""
# import remoteDebug

import sys
import logging
import argparse
import os
import numpy as np
import functools
import queue
import threading

if sys.version_info[0] < 3:
    raise Exception('Python 3 is required.')

logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName('INFO'))
logger.addHandler(logging.StreamHandler(sys.stdout))

nparray = functools.partial(np.array, dtype=np.float32)
npzeros = functools.partial(np.zeros, dtype=np.float32)
npones = functools.partial(np.ones, dtype=np.float32)

cubeOverlapPoolFlag = False

apolloObjType = {1: 'car', 2: 'car', 3: 'pedestrian', 4: 'cyclist', 5: 'trafficcone', 6: 'others'}
apolloObjTypeNum = len(apolloObjType)
assert apolloObjTypeNum < 256, 'uint8 is invalid for apolloObjTypeNum {}'.format(apolloObjTypeNum)


def parseArgs():
    def _modeType(mode_str):
        mode_str = mode_str.lower()
        assert mode_str in set(['detection', 'tracking']), 'invalid modeType'
        return mode_str
    
    def _dataType(type_str):
        type_str = type_str.lower()
        assert type_str in set(['apollo']), 'invalid dataType'
        return type_str
    
    def _pathType(path_str):
        assert os.path.isdir(path_str), 'invalid dir path'
        return os.path.realpath(os.path.normpath(path_str))
    
    def _objType(type_str):
        type_str = type_str.lower()
        assert type_str in set(['car', 'pedestrian', 'cyclist']), 'invalid objType'
        return type_str
    
    parser = argparse.ArgumentParser(description='3D Detection/Tracking Evaluation.')
    parser.add_argument('--modeType', type=_modeType, default='detection', help='evaluation mode')
    parser.add_argument('--dataType', type=_dataType, default='apollo', help='type of data format')
    parser.add_argument('--gtPath', type=_pathType, help='the dir of ground truth')
    parser.add_argument('--dtPaths', nargs='+', type=_pathType, help='the dir of results')
    parser.add_argument('--evalLists', nargs='+', type=str, default=None, help='list file to evaluate')
    parser.add_argument('--resFiles', nargs='+', type=str, default=None, help='the file to save result')
    parser.add_argument('--objTypes', nargs='+', type=_objType, default=['car', 'pedestrian', 'cyclist'], help='object type to evaluate')
    parser.add_argument('--minIoUs', nargs='+', type=float, default=[0.7, 0.5, 0.5], help='minimum iou for box matching')
    parser.add_argument('--minScores', nargs='+', type=float, default=[-1, -1, -1], help='minimum score to consider')
    parser.add_argument('--typeFilterFlag', action='store_true', help='ignore obj with objType different from target objType')
    parser.add_argument('--apSampleNum', type=int, help='#sample employed when calculating average precision')
    args = parser.parse_args()
    
    if args.gtPath is None:
        args.gtPath = _pathType('../detect/apollo_lab')
    if args.dtPaths is None:
        args.dtPaths = [_pathType('../detect/apollo_res')]
    
    dtpath_num = len(args.dtPaths)
    
    # evalLists
    def _sortEvalList(filepath):
        videoName, frameName = filepath.split('/')
        videoId = int('{}{:02d}'.format(*map(int, videoName.split('_'))))
        frameId = int(os.path.splitext(frameName)[0])
        return (videoId, frameId)
    if args.evalLists is None:
        evalList = list()
        for rootpath, _, filenames in os.walk(args.gtPath):
            for filename in filenames:
                filepath = os.path.join(rootpath, filename).replace(args.gtPath, '')[1:]
                for dtPath in args.dtPaths:
                    dtfilepath = os.path.join(dtPath, filepath)
                    if not os.path.isfile(dtfilepath):
                        open(dtfilepath, 'a').close()
                        logger.info('empty file {} is created'.format(dtfilepath))
                evalList.append(filepath)
        args.evalLists = [evalList]
        evallist_num = 1
    else:
        evallist_num = len(args.evalLists)
        assert evallist_num == 1 or evallist_num == dtpath_num, 'invalid evalLists for {} dtPaths'.format(dtpath_num)
        for evalList in args.evalLists:
            assert os.path.isfile(evalList), 'evalList {} does not exist'.format(evalList)
            with open(evalList, 'r') as f:
                filepaths = f.read().splitlines()
            for filepath in filepaths:
                gtfilepath = os.path.join(args.gtPath, filepath)
                assert os.path.isfile(gtfilepath), 'gt file {} does not exist'.format(gtfilepath)
                for dtPath in args.dtPaths:
                    dtfilepath = os.path.join(dtPath, filepath)
                    assert os.path.join(dtfilepath), 'dt file {} does not exist'.format(dtfilepath)
    for listInd, evalList in enumerate(args.evalLists):
        sortedEvalList = sorted(evalList, key=_sortEvalList, reverse=False)
        args.evalLists[listInd] = sortedEvalList
    if evallist_num == 1:
        args.evalLists = [args.evalLists[0] for _ in range(dtpath_num)]
    
    # resFiles
    if args.resFiles is None:
        defaultResDir = os.path.realpath(os.path.join(os.path.dirname(__file__), 'result'))
        resFileTemplate = ('{}_' * 3)[:-1] + '.txt'
        os.makedirs(defaultResDir, exist_ok=True)
        args.resFiles = list()
        for dtPath in args.dtPaths:
            resFile = resFileTemplate.format(args.modeType, args.dataType, os.path.basename(dtPath))
            args.resFiles.append(os.path.join(defaultResDir, resFile))
    elif len(args.resFiles) == dtpath_num:
        for resFile in args.resFiles:
            os.makedirs(os.path.dirname(resFile), exist_ok=True)
    else:
        raise Exception('invalid resFiles for {} dtPaths'.format(dtpath_num))
    
    objtype_num = len(args.objTypes)
    
    # minIoUs
    miniou_num = len(args.minIoUs)
    for minIoU in args.minIoUs:
        assert minIoU >= 0 and minIoU <= 1, 'invalid minIoU {}'.format(minIoU)
    if miniou_num == 1:
        args.minIoUs = [args.minIoUs[0] for _ in range(objtype_num)]
    else:
        assert miniou_num == objtype_num, 'invalid minIoUs for {} objTypes'.format(objtype_num)
    
    # minScores
    minscore_num = len(args.minScores)
    for minScore in args.minScores:
        assert (minScore >= 0 and minScore <= 1) or minScore == -1, 'invalid minScore {}'.format(minScore)
    if minscore_num == 1:
        args.minScores = [args.minScores[0] for _ in range(objtype_num)]
    else:
        assert minscore_num == objtype_num, 'invalid minScores for {} objTypes'.format(objtype_num)
    
    # typeFilterFlag
    if args.typeFilterFlag:
        args.minIoUs = [[minIoU] for minIoU in args.minIoUs]
    else:
        args.minIoUs = [args.minIoUs]

    # apSampleNum
    if args.modeType != 'detection':
        assert args.apSampleNum is None, 'apSampleNum {} is invalid when modeType {}'.format(args.apSampleNum, args.modeType)
    else:
        assert args.apSampleNum is not None, 'apSampleNum is required when modeType detection'

    return args

def loadData(dirpath, filelist, dataType, objTypes, minScores, objIdFlag, scoreFlag, typeFilterFlag):
    objTypeSet = set(objTypes)

    assert dataType == 'apollo', 'invalid data type for loadData function'
    cubelist_len = objIdFlag + 8 + scoreFlag
    objTypeInd = 0 + objIdFlag
    objItemNum = 10
    
    if typeFilterFlag:
        data = {objType: list() for objType in objTypes}
        cubeNums = {objType: list() for objType in objTypes}
    else:
        data = {'all': list()}
        cubeNums = {'all': list()}
    frameNums = list()
    
    lastVideoId = None
    for filename in filelist:
        videoId = int(''.join(filename.split('/')[0].split('_')))
        if videoId != lastVideoId:
            for objData in data.values():
                objData.append(list())  # video
            lastVideoId = videoId
            frameNums.append(0)
        for objData in data.values():
            objData[-1].append(list())  # frame
        filepath = os.path.join(dirpath, filename)
        with open(filepath, 'r') as f:
            cubeStrs = f.read().splitlines()
        objIds = set()
        for cubeInd, cubeStr in enumerate(cubeStrs):
            cubeList = cubeStr.split(' ')
            assert len(cubeList) == cubelist_len, '{}: invalid cube info for frame {} {}th object'.format(
                'DT' if scoreFlag else 'GT', videoId, filename, cubeInd)
            if objIdFlag:
                objId = int(cubeList[0])
                assert objId not in objIds, '{}: object id {} occurred at lease twice in frame {}: 2nd appearance at {}th line'.format(
                    'DT' if scoreFlag else 'GT', objId, filename, cubeInd)
                objIds.add(objId)
            else:
                objId = -1  # detect objId = -1
            cubeType = apolloObjType[int(cubeList[objTypeInd])]
            if typeFilterFlag:
                if cubeType not in objTypeSet:
                    continue
                if scoreFlag:
                    cubeScore = float(cubeList[-1])
                    if cubeScore < minScores[objTypes.index(cubeType)]:
                        continue
                else:
                    cubeList.append(1.)  # gt score = 1.
                cube = [videoId, objId, *list(map(float, cubeList[objTypeInd + 1:]))]
                data[cubeType][-1][-1].append(cube)  # videoId, objId, x, y, z, dx, dy, dz, heading, score (10 items)
            else:
                if not scoreFlag:
                    cubeList.append(1.)
                cubeTypeInt = objTypes.index(cubeType) if cubeType in objTypes else -1
                cube = [videoId, objId, *list(map(float, cubeList[objTypeInd + 1:])), cubeTypeInt]
                data['all'][-1][-1].append(cube)
        frameNums[-1] += 1
        for objType, objData in data.items():
            cubeNums[objType].append(len(objData[-1][-1]))
            objData[-1][-1] = nparray(sorted(objData[-1][-1], key=lambda cube: cube[0], reverse=False)) if objData[-1][-1] else \
                npzeros((0, objItemNum + (not typeFilterFlag)))
    
    frameNums = np.cumsum(frameNums)
    maxCubeNums = dict()
    for objType, cubeNum in cubeNums.items():
        maxCubeNums[objType] = max(cubeNum)
        assert maxCubeNums[objType] < 256, 'uint8 is invaild for maxCubeNum {}'.format(maxCubeNums[objType])
        cubeNums[objType] = np.array(cubeNum, dtype=np.uint8)
    
    cubeData = dict()
    cubeDataType = dict()
    for objType, objData in data.items():
        cubeData[objType] = - npones((frameNums[-1], maxCubeNums[objType], objItemNum))  # default dtScore = -1
        if not typeFilterFlag:
            cubeDataType[objType] = - np.ones((frameNums[-1], maxCubeNums[objType]), dtype=np.int8)
        else:
            cubeDataType[objType] = None
        frameInd = 0
        for videoData in objData:
            for frameData in videoData:
                cubeData[objType][frameInd, :frameData.shape[0]] = frameData[:, :objItemNum]
                if not typeFilterFlag:
                    cubeDataType[objType][frameInd, :frameData.shape[0]] = frameData[:, objItemNum].astype(np.int8)
                frameInd += 1
    data = cubeData
    data['frameNums'], data['cubeNums'] = frameNums, cubeNums
    data['cubeTypes'] = cubeDataType
    
    return data

def cubeOverlap_thread(inputQueue, resultQueue, hAxis, criterion, gpuId):
    from utils import cubeOverlap
    while not inputQueue.empty():
        try:
            args = inputQueue.get(timeout=5.0)
        except queue.Empty:
            continue
        gtNums, dtNums, gts, dts, threadInd = args
        overlaps = cubeOverlap(gtNums, dtNums, gts, dts, hAxis, criterion, gpuId)
        resultQueue.put([overlaps, threadInd])

def computeOverlap(frameNum, gtNums, dtNums, gts, dts):
    gts = gts[:, :, 2:9]  # x, y, z, dx, dy, dz, heading (7 items)
    dts = dts[:, :, 2:9]
    gpuIds = list(range(len(os.environ['CUDA_VISIBLE_DEVICES'].split(',')))) if os.environ.get('CUDA_VISIBLE_DEVICES') else list(range(8))
    gpuNum = len(gpuIds)
    assert gpuNum, 'no valid gpu for evaluation'
    
    procFrameNum = 500  # about 500 frames per process
    poolFrameNum = procFrameNum * gpuNum
    poolNum = frameNum // poolFrameNum
    _frameNum = frameNum - poolFrameNum * poolNum
    _procFrameNum = (_frameNum + gpuNum - 1) // gpuNum
    __procFrameNum = _frameNum - _procFrameNum * (gpuNum - 1)
    procFrameNums_r = np.cumsum([procFrameNum] * poolNum * gpuNum + [_procFrameNum] * (gpuNum - 1) + [__procFrameNum])
    procFrameNums_l = np.insert(procFrameNums_r, 0, 0)[:-1]
    
    criterion = 0
    hAxis = 2
    
    if cubeOverlapPoolFlag:
        # ctx = multiprocessing.get_context('spawn')
        # pool = ctx.Pool(processes=gpuNum)
        # pool = multiprocessing.pool.ThreadPool(processes=gpuNum)
        # overlaps = pool.map()
        inputQueue = queue.Queue()
        inputQueue.queue = queue.deque([(gtNums[lId:rId], dtNums[lId:rId], gts[lId:rId], dts[lId:rId], threadInd) 
                                        for threadInd, (lId, rId) in enumerate(zip(procFrameNums_l, procFrameNums_r))])
        resultQueue = queue.Queue()
        threads = list()
        for gpuId in gpuIds:
            threads.append(threading.Thread(target=cubeOverlap_thread, args=(inputQueue, resultQueue, hAxis, criterion, gpuId)))
            threads[-1].start()
        for thread in threads:
            thread.join()
        overlaps = list(map(lambda items: items[0], sorted(resultQueue.queue, key=lambda items: items[1], reverse=False)))
    else:
        from utils import cubeOverlap
        overlaps = list()
        for lId, rId in zip(procFrameNums_l, procFrameNums_r):
            overlaps.append(cubeOverlap(gtNums[lId:rId], dtNums[lId:rId], gts[lId:rId], dts[lId:rId], hAxis, criterion, gpuIds[0]))
    
    overlaps = np.vstack(overlaps)
    return overlaps

def assignPair(score, pair):
    if not score.size:
        return np.empty((0,), dtype=np.int8)
    axisInd = np.argmin(pair.shape)
    otherAxis = 1 - axisInd
    axisMin = score.min(axis=otherAxis)
    score = score - np.expand_dims(axisMin, axis=otherAxis)
    axes = list(np.where(score == 0))
    axes[axisInd], indices, counts = np.unique(axes[axisInd], return_index=True, return_counts=True)
    sortInds = np.argsort(counts)
    axes[axisInd], axes[otherAxis] = axes[axisInd][sortInds], axes[otherAxis][indices][sortInds]
    pairNum = (counts == 1).sum()
    pair[axes[0][:pairNum], axes[1][:pairNum]] = 1
    if pairNum == min(pair.shape):
        return pair
    elif pairNum < counts.shape[0]:
        rowInd, colInd = axes[0][pairNum], axes[1][pairNum]
        pair[rowInd, colInd] = 1
        pairNum += 1
    mask = np.ones(score.shape, dtype=np.bool_)
    mask[axes[0][:pairNum]] = False
    mask[:, axes[1][:pairNum]] = False
    subShape = np.array(score.shape, dtype=np.uint8) - pairNum
    subPair = pair[mask].reshape(subShape)
    pair[mask] = assignPair(score[mask].reshape(subShape), subPair).flatten()
    return pair

def seekBijection(gtNums, dtNums, overlaps, dtScores, minIoUs, scoreThreshs, typeFilterFlag, gtTypes, dtTypes):
    # search for one-to-one mapping
    pairs = - np.ones(overlaps.shape, dtype=np.int8)
    if typeFilterFlag:
        minIoU, scoreThresh = minIoUs[0], scoreThreshs[0]
        for gtNum, dtNum, frameOverlaps, dtScore, framePairs in zip(gtNums, dtNums, overlaps, dtScores, pairs):
            dtInds = dtScore >= scoreThresh
            pair = framePairs[:gtNum, dtInds]  # copy
            score = frameOverlaps[:gtNum, dtInds]
            invalidInds = score < max(1e-6, minIoU)
            score[invalidInds] = 0.
            if not score.any():
                continue
            score = 1. - score
            pair.fill(0)
            framePairs[:gtNum, dtInds] = np.multiply(assignPair(score, pair), ~invalidInds)
    else:
        for gtNum, dtNum, frameOverlaps, framePairs, gtType, dtScore, dtType in \
            zip(gtNums, dtNums, overlaps, pairs, gtTypes, dtScores, dtTypes):
            dtInds = np.zeros(dtType.shape, dtype=np.bool_)
            for dtTypeInd, scoreThresh in enumerate(scoreThreshs):
                dtInds = np.logical_or(dtInds, np.logical_and(dtType == dtTypeInd, dtScore >= scoreThresh))
            pair = framePairs[:gtNum, dtInds]
            score = frameOverlaps[:gtNum, dtInds]
            invalidInds = score < 1e-6
            gtInds = np.zeros(gtType.shape, dtype=np.bool_)
            for gtTypeInd, minIoU in enumerate(minIoUs):
                invalidInds = np.logical_or(invalidInds, np.logical_and((gtType[:gtNum] == gtTypeInd)[..., None], score < minIoU))
                gtInds = np.logical_or(gtInds, gtType == gtTypeInd)
            ignoreGTinds = ~gtInds
            score[invalidInds] = 0.
            if not score.any():
                continue
            score = 1. - score
            pair.fill(0)
            framePairs[:gtNum, dtInds] = np.multiply(assignPair(score, pair), ~invalidInds)
            _, ignoreDTinds = np.where(framePairs[ignoreGTinds] == 1)
            framePairs[ignoreGTinds] = -1
            framePairs[:, ignoreDTinds] = -1
    return pairs

def findRecThr(pairs, dtScores, sampleNum, typeFilterFlag, gtTypeNum, gtTypes):
    # score thresholds i.e. recall [ = tp / (tp + fn) = tp / gtNum ] * gtNum (which is scalar)
    scoreThreshs = list()
    if typeFilterFlag:
        frameInds, _, dtTPinds = np.where(pairs == 1)
        scoreThreshs.append(np.sort(dtScores[frameInds, dtTPinds], axis=None, kind='mergesort'))
    else:
        for gtTypeInd in range(gtTypeNum):
            frameInds, _, dtTPinds = np.where(np.logical_and((gtTypes == gtTypeInd)[..., None], pairs == 1))
            scoreThreshs.append(np.sort(dtScores[frameInds, dtTPinds], axis=None, kind='mergesort'))
    thrs = list()
    num = list()
    for scoreThresh in scoreThreshs:
        threshNum = len(scoreThresh)
        typeSampleNum = min(threshNum, sampleNum)
        num.append(typeSampleNum)
        intervalNum = typeSampleNum - 1
        sampleInterval = (threshNum + intervalNum - 1) // intervalNum
        thrs.append(np.append(scoreThresh[:-1][::sampleInterval], scoreThresh[-1]))
    maxSampleNum = max(num)
    recThrs = np.array([[thr[sampleInd] if len(thr) > sampleInd else thr[-1] for thr in thrs] \
        for sampleInd in range(maxSampleNum)], dtype=np.float32)
    return recThrs

def calculMota(frameNums, pairs, gtObjIds, dtObjIds):
    idSwitch = np.zeros(frameNums.shape, dtype=np.int64)
    frameNums = np.insert(frameNums, 0, 0)
    for videoInd, (frameBeginInd, frameEndInd) in enumerate(zip(frameNums[:-1], frameNums[1:])):
        videoPairs = pairs[frameBeginInd:frameEndInd]
        g2dIds = dict()
        for _, gtInd, dtInd in zip(*np.where(videoPairs == 1)):
            if gtInd not in g2dIds:
                g2dIds[gtInd] = dtInd
                continue
            elif g2dIds[gtInd] == dtInd:
                continue
            idSwitch[videoInd] += 1
            g2dIds[gtInd] = dtInd
    fn = (pairs.max(axis=2) == 0).sum()
    fp = (pairs.max(axis=1) == 0).sum()
    ids = idSwitch.sum()
    gtNum = (pairs == 1).sum() + fn
    mota = 1 - (fn + fp + ids) / gtNum
    return mota

def calculPrec(gtNums, dtNums, overlaps, dtScores, minIoUs, recThrs, typeFilterFlag, gtTypes, dtTypes):
    prec = np.zeros(len(recThrs), dtype=np.float32)
    for precInd, recThr in reversed(list(enumerate(recThrs))):
        # one-to-one mapping given score thresholds (recThr)
        pairs = seekBijection(gtNums, dtNums, overlaps, dtScores, minIoUs, recThr, typeFilterFlag, gtTypes, dtTypes)
        # count indicators
        tp = (pairs == 1).sum()
        fp = (pairs.max(axis=1) == 0).sum()
        # calculate precision
        prec[precInd] = tp / (tp + fp)
        prec[precInd] = prec[precInd:].max()
    precs = prec.mean()
    return precs

def evaluate(modeType, dataType, dtPath, evalList, objTypes, minScores, objIdFlag, minIoUs, typeFilterFlag, gts, apSampleNum):
    # load data
    dts = loadData(dtPath, evalList, dataType, objTypes, minScores, objIdFlag, scoreFlag=True, typeFilterFlag=typeFilterFlag)
    frameNums = gts['frameNums']
    assert np.array_equal(frameNums, dts['frameNums']), 'invalid frameNums for dts'
    frameNum = frameNums[-1]
    gtCubeNums, dtCubeNums = gts['cubeNums'], dts['cubeNums']
    gtCubeTypes, dtCubeTypes = gts['cubeTypes'], dts['cubeTypes']
    metrics = list()
    for objType, minIoU in zip(gtCubeNums.keys(), minIoUs):
        gtCubeNum, dtCubeNum = gtCubeNums[objType], dtCubeNums[objType]
        objGTs, objDTs = gts[objType], dts[objType]
        dtScores = objDTs[:, :, -1]
        gtTypeNum = len(minIoU)
        # compute overlap
        overlaps = computeOverlap(frameNum, gtCubeNum, dtCubeNum, objGTs, objDTs)
        # seek bijection between gt and dt
        pairs = seekBijection(gtCubeNum, dtCubeNum, overlaps, dtScores, minIoU, [0.] * gtTypeNum, \
            typeFilterFlag, gtCubeTypes[objType], dtCubeTypes[objType])
        # evaluation core
        if objIdFlag:  # tracking
            # calculate mota
            mota = calculMota(frameNums, pairs, objGTs[:, :, 1], objDTs[:, :, 1])
            metrics.append(mota)
            logger.info('{} @ {}\nMOTA: {:.3f}%'.format(objType, minIoU, mota * 100))
        else:  # detection
            # find score thresholds according to recall
            recThrs = findRecThr(pairs, dtScores, apSampleNum, typeFilterFlag, gtTypeNum, gtCubeTypes[objType])
            # calculate precision
            prec = calculPrec(gtCubeNum, dtCubeNum, overlaps, dtScores, minIoU, recThrs, \
                typeFilterFlag, gtCubeTypes[objType], dtCubeTypes[objType])
            metrics.append(prec)
            logger.info('{} @ {}\nAP: {:.3f}%'.format(objType, minIoU, prec * 100))
    metric = sum(metrics) / len(metrics)
    metricType = 'mMOTA' if objIdFlag else 'mAP'
    logger.info('{} @ {}\n{}: {:.3f}%'.format(str(list(gtCubeNums.keys()))[1:-1], str(minIoUs)[1:-1], metricType, metric * 100))

def main():
    # parse arguments
    args = parseArgs()
    # load ground truth
    objIdFlag = args.modeType == 'tracking'
    gts = loadData(args.gtPath, args.evalLists[0], args.dataType, args.objTypes, args.minScores, objIdFlag, scoreFlag=False, typeFilterFlag=args.typeFilterFlag)
    # evaluation results
    for dtPath, evalList, resFile in zip(args.dtPaths, args.evalLists, args.resFiles):
        if evalList != args.evalLists[0]:
            gts = loadData(args.gtPath, evalList, args.dataType, args.objTypes, args.minScores, objIdFlag, scoreFlag=False, typeFilterFlag=args.typeFilterFlag)
        resFileHandler = logging.FileHandler(resFile)
        logger.addHandler(resFileHandler)
        # evaluation core
        evaluate(args.modeType, args.dataType, dtPath, evalList, args.objTypes, args.minScores, objIdFlag, args.minIoUs, args.typeFilterFlag, gts, args.apSampleNum)
        logger.removeHandler(resFileHandler)


if __name__ == '__main__':
    main()