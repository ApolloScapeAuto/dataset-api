"""
    Brief: Utility functions of evaluation
    Date: 2019/6/1
"""

__all__ = ['cubeOverlap']

import numpy as np
import numba
from numba import cuda
import math

@cuda.jit('(float32[:], float32[:])', device=True, inline=True)
def box2vertex(box, vertex):  # clockwise
    # rot: x->y
    x, y, dx, dy, rot = box
    offsetX, offsetY = dx/2, dy/2
    v = cuda.local.array((8, ), dtype=numba.float32)
    v[0], v[2], v[4], v[6] = -offsetX, -offsetX, offsetX, offsetX
    v[1], v[3], v[5], v[7] = -offsetY, offsetY, offsetY, -offsetY
    cos_r, sin_r = math.cos(rot), math.sin(rot)
    # anticlockwise rotation matrix: [[cosr, -sinr], [sinr, cosr]]
    for xInd, yInd in zip(range(0, 8, 2), range(1, 8, 2)):
        vertex[xInd] = cos_r * v[xInd] - sin_r * v[yInd] + x
        vertex[yInd] = sin_r * v[xInd] + cos_r * v[yInd] + y

@cuda.jit('(float32[:], float32[:])', device=True, inline=True)
def dot(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]

@cuda.jit('(float32[:], float32[:], float32[:], uint8, boolean)', device=True, inline=True)
def vertexInInter(p, q, interV, vertexNum, overlapVertexFlag):
    vec0 = cuda.local.array((2, ), dtype=numba.float32)
    vec1 = cuda.local.array((2, ), dtype=numba.float32)
    vec2 = cuda.local.array((2, ), dtype=numba.float32)
    for pBegin, pEnd in zip(range(0, 8, 2), range(2, 9, 2)):
        p0 = p[pBegin:pEnd]
        q0, q1, q3 = q[0:2], q[2:4], q[6:8]
        vec0[0], vec0[1], vec1[0], vec1[1], vec2[0], vec2[1] = p0[0] - q0[0], p0[1] - q0[1], q1[0] - q0[0], q1[1] - q0[1], q3[0] - q0[0], q3[1] - q0[1]
        norm01, norm11 = dot(vec0, vec1), dot(vec1, vec1)
        norm02, norm22 = dot(vec0, vec2), dot(vec2, vec2)
        if not overlapVertexFlag and (norm01 == 0) + (norm01 == norm11) + (norm02 == 0) + (norm02 == norm22) > 1:  # skip overlap vertex
            continue
        if norm01 >= 0 and norm01 <= norm11 and norm02 >=0 and norm02 <= norm22:
            vxInd = vertexNum * 2
            interV[vxInd], interV[vxInd + 1] = p0
            vertexNum += 1
    return vertexNum

@cuda.jit('(float32[:], float32[:], float32[:])', device=True, inline=True)
def _cross(vec1, p1, p2):
    return vec1[0] * (p2[1] - p1[1]) - (p2[0] - p1[0]) * vec1[1]

@cuda.jit('(float32[:], float32[:])', device=True, inline=True)
def cross(vec1, vec2):
    return vec1[0] * vec2[1] - vec2[0] * vec1[1]

@cuda.jit('(float32[:], float32[:], float32[:], uint8)', device=True, inline=True)
def cuspOnSide(p, q, interV, vertexNum):
    vecp = cuda.local.array((2, ), dtype=numba.float32)
    vecq = cuda.local.array((2, ), dtype=numba.float32)
    for pBegin, pEnd in zip(range(0, 8, 2), range(2, 9, 2)):
        p1Begin = (pBegin + 2) % 8
        p1End = p1Begin + 2
        p0, p1 = p[pBegin:pEnd], p[p1Begin:p1End]
        vecp[0], vecp[1] = p1[0] - p0[0], p1[1] - p0[1]
        for qBegin, qEnd in zip(range(0, 8, 2), range(2, 9, 2)):
            q1Begin = (qBegin + 2) % 8
            q1End = q1Begin + 2
            q0, q1 = q[qBegin:qEnd], q[q1Begin:q1End]
            vecq[0], vecq[1] = q1[0] - q0[0], q1[1] - q0[1]
            if _cross(vecp, p0, q0) * _cross(vecp, p0, q1) >= 0 or _cross(vecq, q0, p0) * _cross(vecq, q0, p1) >= 0:
                continue
            # swap
            a1, b1, c1 = vecp[0], - vecp[1], cross(p0, p1)
            a2, b2, c2 = vecq[0], - vecq[1], cross(q0, q1)
            dh = a1 * b2 - a2 * b1
            dx = a2 * c1 - a1 * c2
            dy = b1 * c2 - b2 * c1
            xInd = vertexNum * 2
            interV[xInd], interV[xInd + 1] = dx / dh, dy / dh
            vertexNum += 1
    return vertexNum

@cuda.jit('(float32[:], uint8)', device=True, inline=True)
def sortVertex(interV, vertexNum):
    center = cuda.local.array((2, ), dtype=numba.float32)
    verIndNum = vertexNum * 2
    sumx, sumy = 0, 0
    for xInd, yInd in zip(range(0, verIndNum, 2), range(1, verIndNum, 2)):
        sumx += interV[xInd]
        sumy += interV[yInd]
    center[0], center[1] = sumx / vertexNum, sumy / vertexNum
    rot = cuda.local.array((3 * 8, ), dtype=numba.float32)
    rotIndNum = vertexNum * 3
    for verBegin, verEnd, rotBegin, rotEnd in zip(range(0, verIndNum, 2), range(2, verIndNum + 1, 2), range(0, rotIndNum, 3), range(3, rotIndNum + 1, 3)):
        p, r = interV[verBegin:verEnd], rot[rotBegin:rotEnd]
        r[0], r[1] = p[0] - center[0], p[1] - center[1]
        r[2] = math.atan2(r[1], r[0])
    for pBegin, pRotBegin in zip(range(2, verIndNum, 2), range(3, rotIndNum, 3)):
        pRot = rot[pRotBegin:pRotBegin + 3]
        for qBegin, qRotBegin in zip(range(pBegin - 2, -1, -2), range(pRotBegin - 3, -1, -3)):
            qRot = rot[qRotBegin:qRotBegin + 3]
            # auti clockwise
            if qRot[2] < pRot[2]:
                break
            if qRot[2] == pRot[2] and dot(qRot[:2], qRot[:2]) < dot(pRot[:2], pRot[:2]):
                break
            # swap
            x, y = interV[qBegin:qBegin + 2]
            interV[qBegin], interV[qBegin + 1] = interV[pBegin:pBegin + 2]
            interV[pBegin], interV[pBegin + 1] = x, y
            pBegin = qBegin
            x, y, t = qRot
            rot[qRotBegin], rot[qRotBegin + 1], rot[qRotBegin + 2] = pRot
            rot[pRotBegin], rot[pRotBegin + 1], rot[pRotBegin + 2] = x, y, t
            pRotBegin = qRotBegin
            pRot = qRot

@cuda.jit('(float32[:], float32[:], float32[:])', device=True, inline=True)
def __cross(p0, p1, p2):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])

@cuda.jit('(float32[:], uint8)', device=True, inline=True)
def calInterArea(interV, vertexNum):
    p0 = interV[0:2]
    area = 0.
    verIndNum = vertexNum * 2
    for p1xInd, p2xInd in zip(range(2, verIndNum - 2, 2), range(4, verIndNum, 2)):
        p1 = interV[p1xInd:p1xInd + 2]
        p2 = interV[p2xInd:p2xInd + 2]
        area += abs(__cross(p0, p1, p2))
    return area * 0.5

@cuda.jit('(float32[:], float32[:], uint8)', device=True, inline=True)
def rotatedCubeOverlap(gt, dt, hAxis):
    # cube to box
    gbox = cuda.local.array((5, ), dtype=numba.float32)
    dbox = cuda.local.array((5, ), dtype=numba.float32)
    tInd = 0
    for ind in range(4):
        tInd += (tInd % 3 == hAxis)
        gbox[ind], dbox[ind] = gt[tInd], dt[tInd]
        tInd += 1
    gbox[-1], dbox[-1] = gt[-1], dt[-1]  # rot
    # box to vertex
    gv = cuda.local.array((8, ), dtype=numba.float32)
    box2vertex(gbox, gv)
    dv = cuda.local.array((8, ), dtype=numba.float32)
    box2vertex(dbox, dv)
    # obtain vertex of intersection area
    interVertex, vertexNum = cuda.local.array((16, ), dtype=numba.float32), numba.uint8(0)
    vertexNum = numba.uint8(vertexInInter(gv, dv, interVertex, vertexNum, True))
    vertexNum = numba.uint8(vertexInInter(dv, gv, interVertex, vertexNum, False))
    vertexNum = numba.uint8(cuspOnSide(gv, dv, interVertex, vertexNum))
    if vertexNum:
        # sort inner points
        sortVertex(interVertex, vertexNum)
        # calculate intersection area
        boxInter = calInterArea(interVertex, vertexNum)
        # calculate intersection volume
        gHoffset, dHoffset = gt[hAxis + 3] / 2, dt[hAxis + 3] / 2
        hInter = max(0, min(gt[hAxis] + gHoffset, dt[hAxis] + dHoffset) - max(gt[hAxis] - gHoffset, dt[hAxis] - dHoffset))
        cubeInter = boxInter * hInter
    else:
        cubeInter = 0.
    return cubeInter
        
@cuda.jit('(float32[:], float32[:], uint8, int8)', device=True, inline=True)
def cubeOverlap_device(gt, dt, hAxis, criterion):
    delta_r = abs(gt[-1] - dt[-1])
    if delta_r % math.pi < 1e-6:  # parallel
        axisInter = cuda.local.array((3, ), dtype=numba.float32)
        for axis in range(3):
            offsetInd = axis + 3
            gOffset, dOffset = gt[offsetInd]/2, dt[offsetInd]/2
            axisInter[axis] = max(0, min(gt[axis] + gOffset, dt[axis] + dOffset) - max(gt[axis] - gOffset, dt[axis] - dOffset))
        cubeInter = axisInter[0] * axisInter[1] * axisInter[2]
    elif (2 * delta_r) % math.pi < 1e-6:  # orthogonal
        axisInter = cuda.local.array((3, ), dtype=numba.float32)
        for axis in range(3):
            gOffset, dOffset = gt[axis+3]/2, dt[3-hAxis-axis+3]/2
            axisInter[axis] = max(0, min(gt[axis] + gOffset, dt[axis] + dOffset) - max(gt[axis] - gOffset, dt[axis] - dOffset))
        cubeInter = axisInter[0] * axisInter[1] * axisInter[2]
    else:  # intersect
        cubeInter = rotatedCubeOverlap(gt, dt, hAxis)
    # overlap criterion
    if criterion == -1:  # intersection volume
        return cubeInter
    elif criterion == 0:  # intersection over union
        gtVolume = gt[3] * gt[4] * gt[5]
        dtVolume = dt[3] * dt[4] * dt[5]
        return cubeInter / (gtVolume + dtVolume - cubeInter)
    elif criterion == 1:  # intersection over groundtruth
        gtVolume = gt[3] * gt[4] * gt[5]
        return cubeInter / gtVolume

@cuda.jit('(uint8[:], uint8[:], uint8, uint8, float32[:], float32[:], float32[:], uint8, int8)', fastmath=False)
def cubeOverlap_kernel(gtNums, dtNums, gtCubeNum, dtCubeNum, gts, dts, overlaps, hAxis, criterion):  # per thread, no return
    # frame
    frameInd = cuda.blockIdx.x
    gtNum = gtNums[frameInd]
    dtNum = dtNums[frameInd]
    
    gtframeDim = gtCubeNum * 7
    gtFrameOffset = frameInd * gtframeDim
    gts = gts[gtFrameOffset:gtFrameOffset + gtframeDim]
    dtframeDim = dtCubeNum * 7
    dtFrameOffset = frameInd * dtframeDim
    dts = dts[dtFrameOffset:dtFrameOffset + dtframeDim]
    overlapDim = gtCubeNum * dtCubeNum
    overlapOffset = frameInd * overlapDim
    overlaps = overlaps[overlapOffset:overlapOffset + overlapDim]
    # gt
    gtInd = cuda.threadIdx.x
    if gtInd >= gtNum:
        return
    gtOffset = gtInd * 7
    gt = gts[gtOffset:gtOffset + 7]
    overlapOffset = gtInd * dtCubeNum
    overlaps = overlaps[overlapOffset:overlapOffset + dtCubeNum]
    for dtInd in range(dtNum):
        # dt
        dtOffset = dtInd * 7
        dt = dts[dtOffset:dtOffset + 7]
        overlaps[dtInd] = cubeOverlap_device(gt, dt, hAxis, criterion)

def cubeOverlap(gtNums, dtNums, gts, dts, hAxis, criterion, gpuId):
    '''
    gtNums: array of #gt with shape (#frame, ), dtype uint8
    dtNums: array of #dt with shape (#frame, ), dtype uint8
    gts: array of gt with shape (#frame, maxGTnum, itemNum), dtype float32
    dts: array of dt with shape (#frame, maxDTnum, itemNum), dtype float32
    hAxis: height axis (uint8)
    criterion: overlap criterion (int8)
    gpuId: device id
    item info: x, y, z, dx, dy, dz, heading
    '''
    assert gtNums.shape == dtNums.shape, 'gtNums {} frames while dtNums {} frames'.format(gtNums.shape, dtNums.shape)
    assert gtNums.dtype == np.uint8, 'gtNums: uint8 expected but {} given'.format(gtNums.dtype)
    assert dtNums.dtype == np.uint8, 'dtNums: uint8 expected but {} given'.format(dtNums.dtype)
    assert gts.shape[0] == dts.shape[0], 'gts {} frames while dts {} frames'.format(gts.shape[0], dts.shape[0])
    assert gts.dtype == np.float32, 'gts: float32 expected but {} given'.format(gts.dtype)
    assert dts.dtype == np.float32, 'dts: float32 expected but {} given'.format(dts.dtype)
    assert gtNums.shape[0] == gts.shape[0], 'gtNums {} frames while gts {} frames'.format(gtNums.shape[0], gts.shape[0])
    
    assert hAxis in set([0, 1, 2]), 'invalid hAxis {}'.format(hAxis)
    hAxis = np.uint8(hAxis)
    assert criterion in set([-1, 0, 1]), 'invalid overlap criterion {}'.format(criterion)
    criterion = np.int8(criterion)
    
    overlaps = np.zeros((gts.shape[0], gts.shape[1], dts.shape[1]), np.float32)
    if not np.all(overlaps.shape):
        return overlaps
    
    assert gts.shape[-1] == 7, 'invalid gt shape {}'.format(gts.shape)
    assert dts.shape[-1] == 7, 'invalid dt shape {}'.format(dts.shape)
    
    device = cuda.select_device(gpuId)
    # if device.id != gpuId:
    #     cuda.close()
    #     device = cuda.select_device(gpuId)
    assert device is None or device.id == gpuId, 'wake up {}th gpu rather than requested {}th gpu'.format(device.id, gpuId)
    
    blocksPerGrid = gts.shape[0]
    threadsPerBlock = gts.shape[1]
    gtCubeNum = np.uint8(gts.shape[1])
    dtCubeNum = np.uint8(dts.shape[1])
    stream = cuda.stream()
    with stream.auto_synchronize():
        gtNumsGPU = cuda.to_device(gtNums, stream)
        dtNumsGPU = cuda.to_device(dtNums, stream)
        gtsGPU = cuda.to_device(gts.reshape(-1), stream)
        dtsGPU = cuda.to_device(dts.reshape(-1), stream)
        overlapsGPU = cuda.to_device(overlaps.reshape(-1), stream)
        cubeOverlap_kernel[blocksPerGrid, threadsPerBlock, stream](gtNumsGPU, dtNumsGPU, gtCubeNum, dtCubeNum, gtsGPU, dtsGPU, overlapsGPU, hAxis, criterion)
        overlapsGPU.copy_to_host(overlaps.reshape(-1), stream)
    return overlaps


if __name__ == '__main__':
    raise Exception('Only for include, not executable on its own.')
    
    '''only for test'''
    # import numpy as np
    # gt = np.array([[[-4.361, 12.652, -0.643, 7.101, 0.898, 2.752, 0]]], dtype=np.float32)
    # dt = np.array([[[-4.361, 12.652, -0.643, 7.101, 0.898, 2.752, 0.001]]], dtype=np.float32)
    # gtNum = np.array([1], dtype=np.uint8)
    # dtNum = np.array([1], dtype=np.uint8)
    # overlaps = cubeOverlap(gtNum, dtNum, gt, dt, 2, 0, 0)
    # print(overlaps)
