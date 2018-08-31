//-------------------------------------------------------------------
// Institute of Deep-Learning, BaiDu, China
// Author: {wangpeng54, chenxinjing}@baidu.com,
// Date: 2018/8/30
//-------------------------------------------------------------------

#include "PointRender.h"

RenderPCD::RenderPCD(char *pcd_path, char *vertex_path, char *geo_path,
                     char *frag_path, int height, int width, bool w_label) {

  readPath = pcd_path;
  VertexShader = vertex_path;
  GemoShader = geo_path;
  FragShader = frag_path;
  Win_height = height;
  Win_width = width;
  with_label = w_label;

}

void RenderPCD::InitializeOpenGL() // some initialize here
{
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
  EGLContext eglCtx = eglCreateContext(eglDpy, eglCfg, EGL_NO_CONTEXT, NULL);
  eglMakeCurrent(eglDpy, eglSurf, eglSurf, eglCtx);

  glewExperimental = true; // Needed for core profile
  if (glewInit() != GLEW_OK) {
    fprintf(stderr, "Failed to initialize GLEW\n");
    getchar();
  }

  glClearColor(1.0f, 1.0f, 1.0f, 1.0f); // background color
  glClearDepth(1.0f);                   // for darak depth
  glEnable(GL_DEPTH_TEST);              // Enable depth test
  glDepthFunc(GL_LESS); // Accept fragment if it closer to the camera than the
                        // former one
  glEnable(GL_CULL_FACE);

  GLuint VertexArrayID;
  glGenVertexArrays(1, &VertexArrayID);
  glBindVertexArray(VertexArrayID);

  // Create and compile our GLSL program from the shaders  compiler shader
  programID = RenderPCD::LoadAllShaders(VertexShader, GemoShader, FragShader);

  // get the handle for quadsize
  // Get a handle for our "MVP" uniform
  MatrixID = glGetUniformLocation(programID, "MVP");
  ViewMatrixID = glGetUniformLocation(programID, "V");
  ModelMatrixID = glGetUniformLocation(programID, "M");
  ProjectionMatrixID = glGetUniformLocation(programID, "P");
  QuadsizeID = glGetUniformLocation(programID, "Quadsize");

  // FBO offscreen
  glGenFramebuffers(1, &FramebufferID);
  glBindFramebuffer(GL_FRAMEBUFFER, FramebufferID);

  // Depth buffer
  glGenRenderbuffers(1, &depthrenderbuffer);
  glBindRenderbuffer(GL_RENDERBUFFER, depthrenderbuffer);
  glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, Win_width,
                        Win_height);
  // attach depthbuffer image to FBO
  glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT,
                            GL_RENDERBUFFER, depthrenderbuffer);

  // Color buffer
  glGenRenderbuffersEXT(1, &colorrenderbuffer);
  glBindRenderbufferEXT(GL_RENDERBUFFER_EXT, colorrenderbuffer);
  glRenderbufferStorageEXT(GL_RENDERBUFFER_EXT, GL_RGBA8, Win_width,
                           Win_height);
  // attach colorbuffer image to FBO
  glFramebufferRenderbufferEXT(GL_FRAMEBUFFER_EXT, GL_COLOR_ATTACHMENT0,
                               GL_RENDERBUFFER_EXT, colorrenderbuffer);

  // check if the frame buffer is completed or not~
  if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE) {
    std::cout << "ERROR: Framebuffer is not completed" << std::endl;
  } else {
    std::cout << "completed" << std::endl;
  }

  glViewport(0, 0, Win_width, Win_height);
  glUseProgram(programID);
}

void RenderPCD::InitializePointInput() // get the vertices
{
  if (with_label)
    RenderPCD::loadPCDorPLYWithLabel(readPath, vertices, labels);
  else
    RenderPCD::loadPCDorPLY(readPath, vertices, labels);

  // Load it into a VBO
  glGenBuffers(1, &vertexbuffer);
  glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);
  glBufferData(GL_ARRAY_BUFFER, vertices.size() * sizeof(glm::vec3),
               &vertices[0], GL_STATIC_DRAW);

  glGenBuffers(1, &labelbuffer);
  glBindBuffer(GL_ARRAY_BUFFER, labelbuffer);
  glBufferData(GL_ARRAY_BUFFER, labels.size() * sizeof(int), &labels[0],
               GL_STATIC_DRAW);
}

// select data points with specific label in the point clouds
// make point clound point  LABEL
int RenderPCD::SelectPoints(const set<int> &rm_labels, const char *output_path,
                            const char *path) {
  pcl::PointCloud<pcl::PointXYZL>::Ptr cloud(
      new pcl::PointCloud<pcl::PointXYZL>);
  printf("Loading pcd %s...\n", path);
  // read PCD if not exist return -1
  if (pcl::io::loadPCDFile<pcl::PointXYZL>(path, *cloud) == -1) 
  {
    PCL_ERROR("Couldn't read file test_pcd.pcd \n"); // terminate the error
    return (-1);
  }
  std::cout << "Loaded " << cloud->points.size() << " data points from file "
            << std::endl;

  cout << "remove not want classes" << endl;
  pcl::PointCloud<pcl::PointXYZL>::Ptr cloud_v2(
      new pcl::PointCloud<pcl::PointXYZL>);
  cloud_v2->height = 1;
  cloud_v2->width = 0;
  cloud_v2->is_dense = true;

  int label;
  for (unsigned int i = 0; i < cloud->points.size(); i++) {
    label = cloud->points[i].label; // GET THE LABEL FROM xyzl
    if (rm_labels.find(label) == rm_labels.end()) {
      cloud_v2->points.push_back(cloud->points[i]);
      cloud_v2->width = cloud_v2->width + 1;
    }
  }
  pcl::io::savePCDFile<pcl::PointXYZL>(output_path, *cloud_v2, true);
  printf("saved to %s \n", output_path);

  return 1;
}

// render a 3d label map to a semantic map and a depth image
void RenderPCD::RenderToRGBDepth(float *Intrinsic, float *Extrinsic,
                                 unsigned char *image, unsigned short *depth) {

  // Clear the screen  color and depth
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

  // Intrinsic
  glm::mat4 ProjectionMatrix = glm::mat4(0.0f);
  ProjectionMatrix[0][0] = 2.0 * Intrinsic[0] / Win_width;
  ProjectionMatrix[1][1] = 2.0 * Intrinsic[4] / Win_height;
  ProjectionMatrix[2][0] = (Win_width - 2.0 * Intrinsic[6]) / Win_width;
  ProjectionMatrix[2][1] = -(Win_height - 2.0 * Intrinsic[7]) / Win_height;
  ProjectionMatrix[2][2] = -(Z_far + Z_near) / (Z_far - Z_near);
  ProjectionMatrix[2][3] = -1.0;
  ProjectionMatrix[3][2] = -2.0 * Z_far * Z_near / (Z_far - Z_near);

  glm::mat4 ViewMatrix = glm::make_mat4(Extrinsic);
  for (int i = 0; i < 4; i++) // other coordinate systems
    for (int j = 1; j <= 2; j++) {
      ViewMatrix[i][j] = -ViewMatrix[i][j];
    }

  glm::mat4 ModelMatrix = glm::mat4(1.0f);
  glm::mat4 MVP = ProjectionMatrix * ViewMatrix * ModelMatrix;

  // Send our transformation to the currently bound shader,
  // in the "MVP" uniform
  glUniformMatrix4fv(MatrixID, 1, GL_FALSE, &MVP[0][0]);
  glUniformMatrix4fv(ModelMatrixID, 1, GL_FALSE, &ModelMatrix[0][0]);
  glUniformMatrix4fv(ViewMatrixID, 1, GL_FALSE, &ViewMatrix[0][0]);
  glUniformMatrix4fv(ProjectionMatrixID, 1, GL_FALSE, &ProjectionMatrix[0][0]);
  glUniform1f(QuadsizeID, quadsize);

  // 1st attribute buffer : vertices
  glEnableVertexAttribArray(0);
  glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer);
  glVertexAttribPointer(0,        // attribute
                        3,        // size
                        GL_FLOAT, // type
                        GL_FALSE, // normalized
                        0,        // stride
                        (void *)0 // array buffer offset
                        );

  // for the label input
  glEnableVertexAttribArray(1);
  glBindBuffer(GL_ARRAY_BUFFER, labelbuffer);
  glVertexAttribPointer(1,        // attribute
                        1,        // size
                        GL_FLOAT, // type
                        GL_FALSE, // normalized
                        0,        // stride
                        (void *)0 // array buffer offset
                        );

  // Draw the Arrays
  glDrawArrays(GL_POINTS, 0, vertices.size());
  glDisableVertexAttribArray(0);
  glDisableVertexAttribArray(1);

  /* Interface for Copy to image*/
  glReadPixels(0, 0, Win_width, Win_height, GL_BGRA_EXT, GL_UNSIGNED_BYTE,
               image); // get the BRG_EXT part

  // depth buffer
  GLfloat *zbuffer = new GLfloat[Win_height * Win_width];
  glReadPixels(0, 0, Win_width, Win_height, GL_DEPTH_COMPONENT, GL_FLOAT,
               zbuffer); /// get the depth buffer

  float *zbufferfloat =
      new float[Win_height * Win_width]; // from int to actual distance

  // quantize depth
  for (int i = 0; i < Win_height * Win_width; i++) {
    zbufferfloat[i] = 2.0 * zbuffer[i] - 1.0;
    zbufferfloat[i] = (2.0 * Z_far * Z_near) /
                      (Z_far + Z_near - zbufferfloat[i] * (Z_far - Z_near));

    if (zbufferfloat[i] > Z_far) {
      zbufferfloat[i] = Z_far;
    } else if (zbufferfloat[i] < Z_near) {
      zbufferfloat[i] = Z_near;
    }
    zbufferfloat[i] = zbufferfloat[i] * 200.0;
  }
  for (int j = 0; j < Win_height * Win_width; j++)
    depth[j] = zbufferfloat[j];

  delete[] zbufferfloat;
  delete[] zbuffer;
}

// loader all three shaders
GLuint RenderPCD::LoadAllShaders(const char *vertex_file_path,
                                 const char *geometry_file_path,
                                 const char *fragment_file_path) {
  // Create the shaders
  GLuint VertexShaderID = glCreateShader(GL_VERTEX_SHADER);
  GLuint GeometryShaderID = glCreateShader(GL_GEOMETRY_SHADER);
  GLuint FragmentShaderID = glCreateShader(GL_FRAGMENT_SHADER);

  // Read the Vertex Shader code from the file
  std::string VertexShaderCode;
  std::ifstream VertexShaderStream(vertex_file_path, std::ios::in);
  if (VertexShaderStream.is_open()) {
    std::string Line = "";
    while (getline(VertexShaderStream, Line))
      VertexShaderCode += "\n" + Line;
    VertexShaderStream.close();
  } else {
    printf("Impossible to open %s. Are you in the right directory ? Don't "
           "forget to read the FAQ !\n",
           vertex_file_path);
    getchar();
    return 0;
  }

  // Read the geometry Shader code from the file
  std::string GeometryShaderCode;
  std::ifstream GeometryShaderStream(geometry_file_path, std::ios::in);
  if (GeometryShaderStream.is_open()) {
    std::string Line = "";
    while (getline(GeometryShaderStream, Line))
      GeometryShaderCode += "\n" + Line;
    GeometryShaderStream.close();
  } else {
    printf("Impossible to open %s. Are you in the right directory ? Don't "
           "forget to read the FAQ !\n",
           geometry_file_path);
    getchar();
    return 0;
  }

  // Read the Fragment Shader code from the file
  std::string FragmentShaderCode;
  std::ifstream FragmentShaderStream(fragment_file_path, std::ios::in);
  if (FragmentShaderStream.is_open()) {
    std::string Line = "";
    while (getline(FragmentShaderStream, Line))
      FragmentShaderCode += "\n" + Line;
    FragmentShaderStream.close();
  }

  GLint Result = GL_FALSE;
  int InfoLogLength;

  // Compile Vertex Shader
  printf("Compiling shader : %s\n", vertex_file_path);
  char const *VertexSourcePointer = VertexShaderCode.c_str();
  glShaderSource(VertexShaderID, 1, &VertexSourcePointer, NULL);
  glCompileShader(VertexShaderID);

  // Check Vertex Shader
  glGetShaderiv(VertexShaderID, GL_COMPILE_STATUS, &Result);
  glGetShaderiv(VertexShaderID, GL_INFO_LOG_LENGTH, &InfoLogLength);
  if (InfoLogLength > 0) {
    std::vector<char> VertexShaderErrorMessage(InfoLogLength + 1);
    glGetShaderInfoLog(VertexShaderID, InfoLogLength, NULL,
                       &VertexShaderErrorMessage[0]);
    printf("%s\n", &VertexShaderErrorMessage[0]);
  }

  // Compile Geometry Shader
  printf("Compiling shader : %s\n", geometry_file_path);
  char const *GeometrySourcePointer = GeometryShaderCode.c_str();
  glShaderSource(GeometryShaderID, 1, &GeometrySourcePointer, NULL);
  glCompileShader(GeometryShaderID);

  // Check Geometry Shader
  glGetShaderiv(GeometryShaderID, GL_COMPILE_STATUS, &Result);
  glGetShaderiv(GeometryShaderID, GL_INFO_LOG_LENGTH, &InfoLogLength);
  if (InfoLogLength > 0) {
    std::vector<char> GeometryShaderErrorMessage(InfoLogLength + 1);
    glGetShaderInfoLog(VertexShaderID, InfoLogLength, NULL,
                       &GeometryShaderErrorMessage[0]);
    printf("%s\n", &GeometryShaderErrorMessage[0]);
  }

  // Compile Fragment Shader
  printf("Compiling shader : %s\n", fragment_file_path);
  char const *FragmentSourcePointer = FragmentShaderCode.c_str();
  glShaderSource(FragmentShaderID, 1, &FragmentSourcePointer, NULL);
  glCompileShader(FragmentShaderID);

  // Check Fragment Shader
  glGetShaderiv(FragmentShaderID, GL_COMPILE_STATUS, &Result);
  glGetShaderiv(FragmentShaderID, GL_INFO_LOG_LENGTH, &InfoLogLength);
  if (InfoLogLength > 0) {
    std::vector<char> FragmentShaderErrorMessage(InfoLogLength + 1);
    glGetShaderInfoLog(FragmentShaderID, InfoLogLength, NULL,
                       &FragmentShaderErrorMessage[0]);
    printf("%s\n", &FragmentShaderErrorMessage[0]);
  }

  // Link the program
  printf("Linking program\n");
  GLuint ProgramID = glCreateProgram();
  glAttachShader(ProgramID, VertexShaderID);
  glAttachShader(ProgramID, GeometryShaderID);
  glAttachShader(ProgramID, FragmentShaderID);
  glLinkProgram(ProgramID);

  // Check the program
  glGetProgramiv(ProgramID, GL_LINK_STATUS, &Result);
  glGetProgramiv(ProgramID, GL_INFO_LOG_LENGTH, &InfoLogLength);
  if (InfoLogLength > 0) {
    std::vector<char> ProgramErrorMessage(InfoLogLength + 1);
    glGetProgramInfoLog(ProgramID, InfoLogLength, NULL,
                        &ProgramErrorMessage[0]);
    printf("%s\n", &ProgramErrorMessage[0]);
  }

  glDetachShader(ProgramID, VertexShaderID);
  glDetachShader(ProgramID, GeometryShaderID);
  glDetachShader(ProgramID, FragmentShaderID);

  glDeleteShader(VertexShaderID);
  glDeleteShader(GeometryShaderID);
  glDeleteShader(FragmentShaderID);

  return ProgramID;
}

//Load a pcd file without semantic label
bool RenderPCD::loadPCDorPLY(const char *path,
                             std::vector<glm::vec3> &out_vertices,
                             std::vector<int> &vertices_label) {

  int pathlen = strlen(path);

  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud(new pcl::PointCloud<pcl::PointXYZ>);
  if (path[pathlen - 1] == 'y') {
    printf("Loading PLY %s...\n", path);

    if (pcl::io::loadPLYFile<pcl::PointXYZ>(path, *cloud) == -1) // read PCD
    {
      PCL_ERROR("Couldn't read file %s \n", path); // terminate the error
      return (-1);
    }
    std::cout << "Loaded " << cloud->points.size() << " data points from file "
              << std::endl;
  } else if (path[pathlen - 1] == 'd') {
    printf("Loading pcd %s...\n", path);
    // read PCD if not exist return -1
    if (pcl::io::loadPCDFile<pcl::PointXYZ>(path, *cloud) == -1) 
    {
      PCL_ERROR("Couldn't read file \n"); // terminate the error
      return (-1);
    }
    std::cout << "Loaded " << cloud->points.size() << " data points from file "
              << std::endl;
  } else {
    std::cout << "Not a PLY or PCD model" << std::endl;
    PCL_ERROR("Couldn't read this file\n"); // terminate the error
    return (-1);
  }

  for (unsigned int i = 0; i < cloud->points.size(); i++) {
    glm::vec3 vertex;
    vertex.x = cloud->points[i].x;
    vertex.y = cloud->points[i].y;
    vertex.z = cloud->points[i].z;
    int labelout;
    labelout = 0; // GET THE LABEL FROM xyzl
    out_vertices.push_back(vertex);
    vertices_label.push_back(labelout); // push back
  }
  return true;
}

//Load a pcd file with semantic label
bool RenderPCD::loadPCDorPLYWithLabel(const char *path,
                                      std::vector<glm::vec3> &out_vertices,
                                      std::vector<int> &vertices_label) {

  int pathlen = strlen(path);
  // make point clound point  LABEL

  pcl::PointCloud<pcl::PointXYZL>::Ptr cloud(
      new pcl::PointCloud<pcl::PointXYZL>);
  if (path[pathlen - 1] == 'y') {
    printf("Loading PLY With label %s...\n", path);
    if (pcl::io::loadPLYFile<pcl::PointXYZL>(path, *cloud) == -1) // read PCD
    {
      PCL_ERROR("Couldn't read file %s \n", path); // terminate the error
      return (-1);
    }
    std::cout << "Loaded " << cloud->points.size() << " data points from file "
              << std::endl;
  } else if (path[pathlen - 1] == 'd') {
    printf("Loading pcd With label %s...\n", path);
    // read PCD if not exist return -1
    if (pcl::io::loadPCDFile<pcl::PointXYZL>(path, *cloud) == -1){
      PCL_ERROR("Couldn't read file \n"); // terminate the error
      return (-1);
    }
    std::cout << "Loaded " << cloud->points.size() << " data points from file "
              << std::endl;
  } else {
    std::cout << "Not a PLY or PCD model" << std::endl;
    PCL_ERROR("Couldn't read this file\n"); // terminate the error
    return (-1);
  }

  for (unsigned int i = 0; i < cloud->points.size(); i++) {
    glm::vec3 vertex;
    vertex.x = cloud->points[i].x;
    vertex.y = cloud->points[i].y;
    vertex.z = cloud->points[i].z;

    int labelout;
    labelout = cloud->points[i].label; // GET THE LABEL FROM xyzl
    out_vertices.push_back(vertex);
    vertices_label.push_back(labelout); // push back
  }
  return true;
}

RenderPCD::~RenderPCD() {
  glDeleteBuffers(1, &vertexbuffer);
  glDeleteBuffers(1, &labelbuffer);
  glDeleteProgram(programID);
  glDeleteVertexArrays(1, &VertexArrayID);

  glDeleteFramebuffers(1, &FramebufferID);
  glDeleteRenderbuffers(1, &depthrenderbuffer);
  glDeleteRenderbuffers(1, &colorrenderbuffer);

  eglTerminate(eglDpy);
}
