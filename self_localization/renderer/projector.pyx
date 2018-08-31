# distutils: sources = PointRender.cpp
from libcpp cimport bool

cdef extern from "PointRender.h":
    cdef cppclass RenderPCD:
        RenderPCD(char*, char*, char*, char*, int, int, bool) except +

        void InitializeOpenGL()

        void InitializePointInput()

        void RenderToRGBDepth(float* Intrinsic, 
                         float* Extrinsic, 
                         unsigned char* image,
                         unsigned short* depth)

import numpy as np
cimport numpy as np

cdef class pyRenderPCD:
    # hold a C++ instance which we're wrapping
    cdef RenderPCD *thisptr      
    cdef int height
    cdef int width
    cdef bool with_label

    def __cinit__(self, 
                 pcd_path,
                 vertex_path, 
                 gemo_path,
                 frag_path,
                 int height,
                 int width,
                 int with_label=1):
        """Renderer of a semantic label map and depth map from
        a large point cloud
        Inputs:
            pcd_path: the labeled point cloud 
            vertex_path: the vertex shader
            geo_path: the geometric shader
            frag_path: the fragment shader 
            height, width: image size to be rendered
            with_label: whether point cloud has been labelled

        """
        cdef char* p1 = <bytes>pcd_path;
        cdef char* p2 = <bytes>vertex_path;
        cdef char* p3 = <bytes>gemo_path;
        cdef char* p4 = <bytes>frag_path;

        self.height = height
        self.width = width
        self.with_label = <bool>with_label
        self.thisptr = new RenderPCD(p1, p2, p3, p4,
                                     height, width, 
                                     self.with_label)
        self.thisptr.InitializeOpenGL()
        self.thisptr.InitializePointInput()

    def __dealloc__(self):
        del self.thisptr

    def pyRenderToRGBDepth(self,
                np.ndarray[np.float32_t, ndim=1] Intrinsic, 
                np.ndarray[np.float32_t, ndim=1] Extrinsic):
        """Intrinsic and Extrinsic of camera for rendering
        Inputs:
            Intrinsic: 3x4 matrix 
            Extrinsic: 4x4 matrix with [0, 0, 0, 1] as last row
        Outputs:
            Colored label image and a depth map
        """

        cdef np.ndarray[np.uint8_t, ndim=1] image = np.zeros(
                self.height * self.width * 4, dtype=np.uint8)
        cdef np.ndarray[np.uint16_t, ndim=1] depth = np.zeros(
                self.height * self.width, dtype=np.uint16)

        self.thisptr.RenderToRGBDepth(&Intrinsic[0], &Extrinsic[0],
                &image[0], &depth[0])
        
        cdef np.ndarray[np.uint8_t, ndim=3] image_out = \
                image.reshape((self.height, self.width, 4))
        cdef np.ndarray[np.float32_t, ndim=2] depth_out = \
                np.array(depth.reshape((self.height, self.width)), dtype=np.float32)
        image_out = image_out[::-1, :, :3]
        depth_out = depth_out / 200.0
        depth_out = depth_out[::-1, :]

        return image_out, depth_out


