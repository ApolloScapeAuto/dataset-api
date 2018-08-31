//-------------------------------------------------------------------
// Institute of Deep-Learning, BaiDu, China 
// Author: {wangpeng54, chenxinjing}@baidu.com,
// Date: 2018/8/30
//-------------------------------------------------------------------

#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <cstdlib>
#include <string>
#include <vector>
#include <map>
#include <fstream>
#include <iostream>
#include <algorithm>
#include <iomanip> 

// Include GLEW
#include <GL/glew.h>
#include <GL/freeglut.h>
#include <FreeImage.h>

// Include GLM
#define GLM_FORCE_RADIANS
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtx/euler_angles.hpp>
#include <glm/gtc/type_ptr.hpp>

#include <pcl/point_cloud.h>
#include <pcl/common/common.h>
#include <pcl/common/transforms.h>
#include <pcl/console/parse.h>
#include <pcl/console/print.h>
#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>
#include <pcl/io/ply_io.h>
#include <EGL/egl.h>

using namespace std;

static const EGLint configAttribs[] = {
          EGL_SURFACE_TYPE, EGL_PBUFFER_BIT,
          EGL_BLUE_SIZE, 8,
          EGL_GREEN_SIZE, 8,
          EGL_RED_SIZE, 8,
          EGL_DEPTH_SIZE, 8,
          EGL_RENDERABLE_TYPE, EGL_OPENGL_BIT,
          EGL_NONE
};    

static const int pbufferWidth = 9;
static const int pbufferHeight = 9;
static const EGLint pbufferAttribs[] = {
    EGL_WIDTH, pbufferWidth,
    EGL_HEIGHT, pbufferHeight,
    EGL_NONE,
};

class RenderPCD {
private:
	vector<glm::vec3> vertices; //get the vertices 
	vector<int> labels; //get the label of each vertice
    Eigen::Vector4f centroid;
    EGLDisplay eglDpy;
	GLuint programID; // used for store shaders

	GLuint VertexArrayID;
	GLuint vertexbuffer; //vertex
	GLuint labelbuffer;

	GLuint MatrixID;
	GLuint ViewMatrixID;
	GLuint ModelMatrixID;
	GLuint ProjectionMatrixID;
	GLuint QuadsizeID;//get the handle for quadsize

	GLuint FramebufferID;
	GLuint depthrenderbuffer;
	GLuint colorrenderbuffer;
    
	static const float Z_far = 300; // farest dis
	static const float Z_near = 0.01; // closest dis
	static const float quadsize = 0.025f; //quadsize

public:
	char * readPath;
	char * VertexShader;
	char * GemoShader;
	char * FragShader;
	int Win_width, Win_height;
    bool with_label;

    RenderPCD(char * pcd_path, 
              char * vertex_path, 
              char * geo_path, 
              char * frag_path,
              int height, 
              int width,
              bool w_label);
	~RenderPCD();

	void InitializeOpenGL();
	void InitializePointInput();

	// offscreen render
	void RenderToRGBDepth(float *Intrinsic, 
                          float *Extrinsic, 
                          unsigned char *image,
                          unsigned short *depth);

	int SelectPoints(const set<int> &rm_labels,
            const char  *output_path, const char * path);

	void WriteClassSpecPCD(const set<int> &keep_labels) {};
	GLuint LoadAllShaders(
            const char * vertex_file_path, 
            const char * geometry_file_path, 
            const char * fragment_file_path);

	bool loadPCDorPLYWithLabel(const char * path, 
            std::vector<glm::vec3> & out_vertices, 
            std::vector<int> & vertices_label);
	bool loadPCDorPLY(const char * path, 
            std::vector<glm::vec3> & out_vertices, 
            std::vector<int> & vertices_label);

};


