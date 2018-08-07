#include <math.h>
#include <stdio.h>
#include <iostream>

#include "GL/glew.h"
#include "GL/gl.h"
#include "GL/glu.h"
#include <cassert>
/* #include "GL/glut.h" */

#include <EGL/egl.h>

#define CHECK_GL_ERROR \
{ \
       int e = glGetError(); \
       if (e!=GL_NO_ERROR) \
           fprintf(stderr, "%s:%i ERROR: 0x%x\n", __FILE__, __LINE__, e); \
       assert(e == GL_NO_ERROR); \
}

using namespace std;

class OffscreenGL {
  
public:
  OffscreenGL(int maxHeight, int maxWidth);
  ~OffscreenGL();
  
private:
  static int glutWin;
  static bool glutInitialized;

  EGLDisplay eglDpy;
  GLuint fb;
  GLuint renderTex;
  GLuint depthTex;
};


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

int OffscreenGL::glutWin = -1;
bool OffscreenGL::glutInitialized = false;

OffscreenGL::OffscreenGL(int maxHeight, int maxWidth) {

      // 1. Initialize EGL
      eglDpy = eglGetDisplay(EGL_DEFAULT_DISPLAY);
      EGLint major, minor;
      eglInitialize(eglDpy, &major, &minor);

      // 2. Select an appropriate configuration
      EGLint numConfigs;
      EGLConfig eglCfg;
      eglChooseConfig(eglDpy, configAttribs, &eglCfg, 1, &numConfigs);

      // 3. Create a surface
      EGLSurface eglSurf = eglCreatePbufferSurface(eglDpy, eglCfg, pbufferAttribs);

      // 4. Bind the API
      eglBindAPI(EGL_OPENGL_API);

      // 5. Create a context and make it current
      EGLContext eglCtx = eglCreateContext(
              eglDpy, eglCfg, EGL_NO_CONTEXT, NULL);


      eglMakeCurrent(eglDpy, eglSurf, eglSurf, eglCtx);

      if (glewInit() != GLEW_OK) {
         // GLEW fail would cause segmentation fault return
         fprintf(stderr, "Failed to initialize GLEW\n");
      }

        glGenFramebuffersEXT(1, &fb);
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fb);
        glGenTextures(1, &renderTex);
        glActiveTexture(GL_TEXTURE0);
        glBindTexture(GL_TEXTURE_RECTANGLE_ARB, renderTex);
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE);
        glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        glTexImage2D(GL_TEXTURE_RECTANGLE_ARB, 0, GL_RGB, maxWidth, maxHeight,
                0, GL_RGBA, GL_UNSIGNED_BYTE, 0);
    
        glGenTextures(1, &depthTex);
        glBindTexture(GL_TEXTURE_RECTANGLE_ARB, depthTex);
        glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_DEPTH_TEXTURE_MODE, GL_INTENSITY);
        glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_COMPARE_MODE, GL_COMPARE_R_TO_TEXTURE);
        glTexParameteri(GL_TEXTURE_RECTANGLE_ARB, GL_TEXTURE_COMPARE_FUNC, GL_LEQUAL);
        glTexImage2D(GL_TEXTURE_RECTANGLE_ARB, 0, GL_DEPTH24_STENCIL8, maxWidth, maxHeight, 0, GL_DEPTH_STENCIL, GL_UNSIGNED_INT_24_8, NULL);
        
        glGenFramebuffersEXT(1, &fb);
        glBindFramebufferEXT(GL_FRAMEBUFFER_EXT, fb);
        glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT, GL_COLOR_ATTACHMENT0_EXT, GL_TEXTURE_RECTANGLE_ARB, renderTex, 0);
        glFramebufferTexture2DEXT(GL_FRAMEBUFFER_EXT, GL_DEPTH_STENCIL_ATTACHMENT, GL_TEXTURE_RECTANGLE_ARB, depthTex, 0);
        glDrawBuffer(GL_COLOR_ATTACHMENT0_EXT|GL_DEPTH_ATTACHMENT_EXT);

      /* } else { */
      /*   glutSetWindow(glutWin); */
      /* } */
}

OffscreenGL::~OffscreenGL() {
    eglTerminate(eglDpy);
}

GLuint createDisplayList(double *fM, int fNum, 
                         double *vM, int vNum, 
                         double *cM, unsigned int colorModFactor, 
                         double linewidth = 0, bool coloring = true) {
  
  GLuint theShape;
  int i;
  unsigned int channelCapacity, channelCapacity2;
  double *fp;
  int vIndex, fNum2;
  fNum2 = fNum*2;
  
  channelCapacity = 256 / colorModFactor;
  channelCapacity2 = channelCapacity * channelCapacity;
  
  theShape = glGenLists(1);
  
  glNewList(theShape, GL_COMPILE);
  
  if (linewidth>0.1) {
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE);
    glLineWidth(linewidth);
  }
  
  glBegin(GL_TRIANGLES);
  for (i = 1; i <= fNum; i++) {
    fp = fM + i-1;
    
    vIndex = (int)fp[0] - 1;
    if (coloring)  glColor3ub(cM[vIndex], cM[vIndex + vNum], cM[vIndex + 2*vNum]);
    glVertex3d(vM[vIndex], vM[vIndex + vNum], vM[vIndex + 2*vNum]);
    
    vIndex = (int)fp[fNum] - 1;
    if (coloring)  glColor3ub(cM[vIndex], cM[vIndex + vNum], cM[vIndex + 2*vNum]);
    glVertex3d(vM[vIndex], vM[vIndex + vNum], vM[vIndex + 2*vNum]);
    
    vIndex = (int)fp[fNum2] - 1;
    if (coloring)  glColor3ub(cM[vIndex], cM[vIndex + vNum], cM[vIndex + 2*vNum]);
    glVertex3d(vM[vIndex], vM[vIndex + vNum], vM[vIndex + 2*vNum]);
  }
  glEnd();
  if (linewidth>0.1)
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL);
  glEndList();
    

  return theShape;
}

void cameraSetup(double zNear, double zFar, double *intrinsics, 
                 unsigned int imgHeight, unsigned int imgWidth) {
  
  double viewMat[] = {1, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1};
  double fcv[] = {intrinsics[0], intrinsics[1]};
  double ccv[] = {intrinsics[2], intrinsics[3]};
  
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);
  glEnable(GL_DEPTH_TEST);
  glDisable(GL_TEXTURE_2D);
  
  glMatrixMode(GL_MODELVIEW);
  glLoadMatrixd(viewMat);
  
  double left = - ccv[0] / fcv[0] * zNear;
  double bottom = (ccv[1] - (double)(imgHeight-1)) / fcv[1] * zNear;
  double right = ((double)imgWidth - 1.0 - ccv[0]) / fcv[0] * zNear;
  double top = ccv[1] / fcv[1] * zNear;
  
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  glFrustum(left, right, bottom, top, zNear, zFar);
  glViewport(0, 0, imgWidth, imgHeight);

}

void drawPatchToDepthBuffer(GLuint listName, unsigned char *imageBuffer, 
        float *depthBuffer, bool *maskBuffer,
        unsigned int imgHeight, unsigned int imgWidth, 
        double *zNearFarV, bool coloring = true) {
  
  glCallList(listName);
  glFlush();
  
  // bug fix for Nvidia
  unsigned int paddedWidth = imgWidth % 4;
  if (paddedWidth != 0) paddedWidth = 4 - paddedWidth + imgWidth;
  else                  paddedWidth = imgWidth;
  
  // Read off of the depth buffer
  float *dataBuffer_depth = new float [paddedWidth * imgHeight];
  glReadPixels(0, 0, paddedWidth, imgHeight, GL_DEPTH_COMPONENT, GL_FLOAT, dataBuffer_depth);
  
  // Read off of the color buffer
  GLubyte *dataBuffer_rgb = new GLubyte [3 * paddedWidth * imgHeight];
  if (coloring)
    glReadPixels(0, 0, paddedWidth, imgHeight, GL_RGB, GL_UNSIGNED_BYTE, dataBuffer_rgb);
  
  // reorder the pixel data for the opengl to matlab conversion
  unsigned int ImgIndex = 0;
  unsigned int oglImageIndex = 0;
  
  float n = zNearFarV[0];
  float f = zNearFarV[1];

  for (int j = 0; j < imgWidth; j++) {
    for (int i = 0; i < imgHeight; i++, ImgIndex++) {

      oglImageIndex = (j + (imgHeight-1-i) * paddedWidth);
      float depth = dataBuffer_depth[oglImageIndex];
      
      // render mask: indicating points inside the clipped plane
      maskBuffer[oglImageIndex] = depth<1;
      
      // render depth
      depthBuffer[oglImageIndex] = -f*n/(depth*(f-n)-f);
      
      // render color
      if (coloring) {
        imageBuffer[oglImageIndex] = (unsigned char) dataBuffer_rgb[oglImageIndex*3];
        imageBuffer[oglImageIndex+imgWidth*imgHeight] = (unsigned char) dataBuffer_rgb[oglImageIndex*3+1];
        imageBuffer[oglImageIndex+imgWidth*imgHeight*2] = (unsigned char) dataBuffer_rgb[oglImageIndex*3+2];
      }
    }
  }
  
  delete []dataBuffer_depth;
  delete []dataBuffer_rgb;
}

static void renderDepthMesh(double *FM, int fNum, 
                     double *VM, int vNum, 
                     double *CM, double *intrinsics, 
                     long unsigned int *imgSizeV, double *zNearFarV,
                     unsigned char * imgBuffer, float *depthBuffer, 
                     bool *maskBuffer, 
                     double linewidth = 0, bool coloring = true) {
  cameraSetup(zNearFarV[0], zNearFarV[1], intrinsics, int(imgSizeV[0]), int(imgSizeV[1]));
  GLuint list = createDisplayList(FM, fNum, VM, vNum, CM, 1, linewidth, coloring);
  drawPatchToDepthBuffer(list, imgBuffer, depthBuffer, maskBuffer, imgSizeV[0], imgSizeV[1], zNearFarV, coloring);
  if (list) {
    glDeleteLists(list, 1);
    list = 0;
  }
}


void renderMesh(double *FM, int fNum, 
                double *VM, int vNum, 
                double *intrinsics, 
                int height, int width,
                float *depth, bool *mask,
                double linewidth = 0) {

  // drop the color image render function
  double *CM=0;
  unsigned char* img = 0;

  double znf[] = {+1e10, -1e10};
  
  for (int32_t i=0; i < vNum; i++) {
    double z = VM[2 * vNum + i];
    if (z<znf[0]) znf[0] = z;
    if (z>znf[1]) znf[1] = z;
  }

  // adjust znear/zfar
  znf[0] -= 0.1; // znear
  znf[1] += 0.1; // zfar
  znf[0] = max(znf[0], 0.1);
  znf[1] = max(znf[1], znf[0] + 0.1);
  long unsigned int imgSize[] = {
          (long unsigned int)height, 
          (long unsigned int)width};

  OffscreenGL offscreenGL(imgSize[0], imgSize[1]);
  bool coloring = false;
  if (CM) coloring = true;

  renderDepthMesh(FM, fNum, VM, vNum, CM, intrinsics, 
                  imgSize, znf, img, depth, mask, 
                  linewidth, coloring);
}
