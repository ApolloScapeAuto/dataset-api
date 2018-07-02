"""
    Brief: cython wrapper for renderer
    Author: wangpeng54@baidu.com
    Date: 2018/6/10
"""

from __future__ import division
from libcpp cimport bool
import numpy as np
cimport numpy as np # for np.ndarray


cdef extern from "renderMesh.h":
    void renderMesh(double* FM, int fNum, 
                    double* VM, int vNum, 
                    double* intrinsics, 
                    int height, int width, 
                    float* depth, bool *mask,
                    double linewidth)

DTYPE = np.float64
ctypedef np.float64_t DTYPE_t


def renderMesh_py(np.ndarray[DTYPE_t, ndim=2] vertices,
                  np.ndarray[DTYPE_t, ndim=2] faces,
                  np.ndarray[DTYPE_t, ndim=1] intrinsic,
                  int height, int width, DTYPE_t linewidth):

    cdef int v_num = vertices.shape[0];
    cdef int f_num = faces.shape[0];

    vertices = vertices.transpose().copy()
    faces = faces.transpose().copy()

    cdef np.ndarray[DTYPE_t, ndim=1] color;
    cdef np.ndarray[np.float32_t, ndim=2] depth = np.zeros((height, width), dtype=np.float32);
    cdef np.ndarray[np.uint8_t, ndim=2, cast=True] mask = np.zeros((height, width), dtype=np.uint8);
    cdef bool *mask_bool = <bool*> &mask[0, 0]
    
    renderMesh(&faces[0, 0], f_num,
               &vertices[0, 0], v_num,
               &intrinsic[0],
               height, width,
               &depth[0, 0], 
               mask_bool,
               linewidth)

    depth[mask == 0] = -1.0
    mask = mask[::-1, :]
    depth = depth[::-1, :]
    
    return depth, mask
