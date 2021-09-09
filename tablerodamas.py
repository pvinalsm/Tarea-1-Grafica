# coding=utf-8
"""Dibujo del cuadrado basico utilizando EBO (e indices) y clases, equivalente a ex_quad_pro"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import grafica.easy_shaders as es
import grafica.basic_shapes as bs
from grafica.gpu_shape import GPUShape, SIZE_IN_BYTES
from data import Q

# We will use 32 bits data, so floats and integers have 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4


# A class to store the application control
class Controller:
    fillPolygon = True


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):

    if action != glfw.PRESS:
        return
    
    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)

    else:
        print('Unknown key')



def createFondo():
    # Defining locations and colors for each vertex of the shape
    #####################################
    
    vertexData = np.array([
    #   positions        colors
        -1, -1, 0,  1.0, 1.0, 1.0,
         1, -1, 0,  1.0, 1.0, 1.0,
         1,  1, 0,  1.0, 1.0, 1.0,
        -1,  1, 0,  1.0, 1.0, 1.0
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    size = len(indices)
    return bs.Shape(vertexData, indices)



def createQuads():
        # Defining locations and colors for each vertex of the shape
    #####################################
    
    vertexData = np.array([
    #   positions          colors
    #   primera fila
        -1.0,  0.75, 0.0,  0.0, 0.0, 0.0,
        -0.75, 0.75, 0.0,  0.0, 0.0, 0.0,
        -0.75, 1.0,  0.0,  0.0, 0.0, 0.0,
        -1.0,  1.0,  0.0,  0.0, 0.0, 0.0,

        -0.5,  0.75, 0.0,  0.0, 0.0, 0.0,
        -0.25, 0.75, 0.0,  0.0, 0.0, 0.0,
        -0.25, 1.0,  0.0,  0.0, 0.0, 0.0,
        -0.5,  1.0,  0.0,  0.0, 0.0, 0.0,

         0.0,  0.75, 0.0,  0.0, 0.0, 0.0,
         0.25, 0.75, 0.0,  0.0, 0.0, 0.0,
         0.25, 1.0,  0.0,  0.0, 0.0, 0.0,
         0.0,  1.0,  0.0,  0.0, 0.0, 0.0,

         0.5,  0.75, 0.0,  0.0, 0.0, 0.0,
         0.75, 0.75, 0.0,  0.0, 0.0, 0.0,
         0.75, 1.0,  0.0,  0.0, 0.0, 0.0,
         0.5,  1.0,  0.0,  0.0, 0.0, 0.0,

    #   segunda fila
        -0.75, 0.5,  0.0,  0.0, 0.0, 0.0,
        -0.5,  0.5,  0.0,  0.0, 0.0, 0.0,
        -0.5,  0.75, 0.0,  0.0, 0.0, 0.0,
        -0.75, 0.75, 0.0,  0.0, 0.0, 0.0,

        -0.25, 0.5,  0.0,  0.0, 0.0, 0.0,
        -0.0,  0.5,  0.0,  0.0, 0.0, 0.0,
        -0.0,  0.75, 0.0,  0.0, 0.0, 0.0,
        -0.25, 0.75, 0.0,  0.0, 0.0, 0.0,

         0.25, 0.5,  0.0,  0.0, 0.0, 0.0,
         0.5,  0.5,  0.0,  0.0, 0.0, 0.0,
         0.5,  0.75, 0.0,  0.0, 0.0, 0.0,
         0.25, 0.75, 0.0,  0.0, 0.0, 0.0,

         0.75, 0.5,  0.0,  0.0, 0.0, 0.0,
         1.0,  0.5,  0.0,  0.0, 0.0, 0.0,
         1.0,  0.75, 0.0,  0.0, 0.0, 0.0,
         0.75, 0.75, 0.0,  0.0, 0.0, 0.0,

    #   tercera fila
        -1.0,  0.25, 0.0,  0.0, 0.0, 0.0,
        -0.75, 0.25, 0.0,  0.0, 0.0, 0.0,
        -0.75, 0.5,  0.0,  0.0, 0.0, 0.0,
        -1.0,  0.5,  0.0,  0.0, 0.0, 0.0,

        -0.5,  0.25, 0.0,  0.0, 0.0, 0.0,
        -0.25, 0.25, 0.0,  0.0, 0.0, 0.0,
        -0.25, 0.5,  0.0,  0.0, 0.0, 0.0,
        -0.5,  0.5,  0.0,  0.0, 0.0, 0.0,

         0.0,  0.25, 0.0,  0.0, 0.0, 0.0,
         0.25, 0.25, 0.0,  0.0, 0.0, 0.0,
         0.25, 0.5,  0.0,  0.0, 0.0, 0.0,
         0.0,  0.5,  0.0,  0.0, 0.0, 0.0,

         0.5,  0.25, 0.0,  0.0, 0.0, 0.0,
         0.75, 0.25, 0.0,  0.0, 0.0, 0.0,
         0.75, 0.5,  0.0,  0.0, 0.0, 0.0,
         0.5,  0.5,  0.0,  0.0, 0.0, 0.0,

    #   cuarta fila
        -0.75, 0.0,  0.0,  0.0, 0.0, 0.0,
        -0.5,  0.0,  0.0,  0.0, 0.0, 0.0,
        -0.5,  0.25, 0.0,  0.0, 0.0, 0.0,
        -0.75, 0.25, 0.0,  0.0, 0.0, 0.0,

        -0.25, 0.0,  0.0,  0.0, 0.0, 0.0,
        -0.0,  0.0,  0.0,  0.0, 0.0, 0.0,
        -0.0,  0.25, 0.0,  0.0, 0.0, 0.0,
        -0.25, 0.25, 0.0,  0.0, 0.0, 0.0,

         0.25, 0.0,  0.0,  0.0, 0.0, 0.0,
         0.5,  0.0,  0.0,  0.0, 0.0, 0.0,
         0.5,  0.25, 0.0,  0.0, 0.0, 0.0,
         0.25, 0.25, 0.0,  0.0, 0.0, 0.0,

         0.75, 0.0,  0.0,  0.0, 0.0, 0.0,
         1.0,  0.0,  0.0,  0.0, 0.0, 0.0,
         1.0,  0.25, 0.0,  0.0, 0.0, 0.0,
         0.75, 0.25, 0.0,  0.0, 0.0, 0.0,


    #   quinta fila
        -1.00, -0.25, 0.0,  0.0, 0.0, 0.0,
        -0.75, -0.25, 0.0,  0.0, 0.0, 0.0,
        -0.75,  0.0,  0.0,  0.0, 0.0, 0.0,
        -1.00,  0.0, 0.0,  0.0, 0.0, 0.0,

        -0.5,  -0.25, 0.0,  0.0, 0.0, 0.0,
        -0.25, -0.25, 0.0,  0.0, 0.0, 0.0,
        -0.25,  0.0,  0.0,  0.0, 0.0, 0.0,
        -0.5,   0.0,  0.0,  0.0, 0.0, 0.0,

         0.0,  -0.25, 0.0,  0.0, 0.0, 0.0,
         0.25, -0.25, 0.0,  0.0, 0.0, 0.0,
         0.25,  0.0,  0.0,  0.0, 0.0, 0.0,
         0.0,   0.0,  0.0,  0.0, 0.0, 0.0,

         0.5,  -0.25, 0.0,  0.0, 0.0, 0.0,
         0.75, -0.25, 0.0,  0.0, 0.0, 0.0,
         0.75,  0.0,  0.0,  0.0, 0.0, 0.0,
         0.5,   0.0,  0.0,  0.0, 0.0, 0.0,

    #   sexta fila
        -0.75, -0.5,  0.0,  0.0, 0.0, 0.0,
        -0.5,  -0.5,  0.0,  0.0, 0.0, 0.0,
        -0.5,  -0.25, 0.0,  0.0, 0.0, 0.0,
        -0.75, -0.25, 0.0,  0.0, 0.0, 0.0,

        -0.25, -0.5,  0.0,  0.0, 0.0, 0.0,
        -0.0,  -0.5,  0.0,  0.0, 0.0, 0.0,
        -0.0,  -0.25, 0.0,  0.0, 0.0, 0.0,
        -0.25, -0.25, 0.0,  0.0, 0.0, 0.0,

         0.25, -0.5,  0.0,  0.0, 0.0, 0.0,
         0.5,  -0.5,  0.0,  0.0, 0.0, 0.0,
         0.5,  -0.25, 0.0,  0.0, 0.0, 0.0,
         0.25, -0.25, 0.0,  0.0, 0.0, 0.0,

         0.75, -0.5,  0.0,  0.0, 0.0, 0.0,
         1.0,  -0.5,  0.0,  0.0, 0.0, 0.0,
         1.0,  -0.25, 0.0,  0.0, 0.0, 0.0,
         0.75, -0.25, 0.0,  0.0, 0.0, 0.0,

    #   septima fila
        -1.00, -0.75, 0.0,  0.0, 0.0, 0.0,
        -0.75, -0.75, 0.0,  0.0, 0.0, 0.0,
        -0.75, -0.5, 0.0,  0.0, 0.0, 0.0,
        -1.00, -0.5, 0.0,  0.0, 0.0, 0.0,

        -0.5,  -0.75, 0.0,  0.0, 0.0, 0.0,
        -0.25, -0.75, 0.0,  0.0, 0.0, 0.0,
        -0.25, -0.5, 0.0,  0.0, 0.0, 0.0,
        -0.5,  -0.5, 0.0,  0.0, 0.0, 0.0,

         0.0,  -0.75, 0.0,  0.0, 0.0, 0.0,
         0.25, -0.75, 0.0,  0.0, 0.0, 0.0,
         0.25,  -0.5,  0.0,  0.0, 0.0, 0.0,
         0.0,   -0.5,  0.0,  0.0, 0.0, 0.0,

         0.5,  -0.75, 0.0,  0.0, 0.0, 0.0,
         0.75, -0.75, 0.0,  0.0, 0.0, 0.0,
         0.75,  -0.5, 0.0,  0.0, 0.0, 0.0,
         0.5,   -0.5, 0.0,  0.0, 0.0, 0.0,

    #   octava fila
        -0.75, -1.0,  0.0,  0.0, 0.0, 0.0,
        -0.5,  -1.0,  0.0,  0.0, 0.0, 0.0,
        -0.5,  -0.75, 0.0,  0.0, 0.0, 0.0,
        -0.75, -0.75, 0.0,  0.0, 0.0, 0.0,

        -0.25, -1.0,  0.0,  0.0, 0.0, 0.0,
        -0.0,  -1.0,  0.0,  0.0, 0.0, 0.0,
        -0.0,  -0.75, 0.0,  0.0, 0.0, 0.0,
        -0.25, -0.75, 0.0,  0.0, 0.0, 0.0,

         0.25, -1.0,  0.0,  0.0, 0.0, 0.0,
         0.5,  -1.0,  0.0,  0.0, 0.0, 0.0,
         0.5,  -0.75, 0.0,  0.0, 0.0, 0.0,
         0.25, -0.75, 0.0,  0.0, 0.0, 0.0,

         0.75, -1.0,  0.0,  0.0, 0.0, 0.0,
         1.0,  -1.0,  0.0,  0.0, 0.0, 0.0,
         1.0,  -0.75, 0.0,  0.0, 0.0, 0.0,
         0.75, -0.75, 0.0,  0.0, 0.0, 0.0
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array(
        [
    #   primera fila
         0, 1, 2,
         2, 3, 0,

         4, 5, 6,
         6, 7, 4,

         8, 9, 10,
         10, 11, 8,
         
         12, 13, 14,
         14, 15, 12,

    #   segunda fila
         16, 17, 18,
         18, 19, 16,

         20, 21, 22,
         22, 23, 20,

         24, 25, 26,
         26, 27, 24,
         
         28, 29, 30,
         30, 31, 28,

    #   tercera fila
         32, 33, 34,
         34, 35, 32,

         36, 37, 38,
         38, 39, 36,

         40, 41, 42,
         42, 43, 40,
         
         44, 45, 46,
         46, 47, 44,

    #   cuarta fila
         48, 49, 50,
         50, 51, 48,

         52, 53, 54,
         54, 55, 52,

         56, 57, 58,
         58, 59, 56,
         
         60, 61, 62,
         62, 63, 60,

    #   quinta fila
         0, 1, 2,
         2, 3, 0,

         4, 5, 6,
         6, 7, 4,

         8, 9, 10,
         10, 11, 8,
         
         12, 13, 14,
         14, 15, 12,

    #   sexta fila
         0, 1, 2,
         2, 3, 0,

         4, 5, 6,
         6, 7, 4,

         8, 9, 10,
         10, 11, 8,
         
         12, 13, 14,
         14, 15, 12,

    #   séptima fila
         0, 1, 2,
         2, 3, 0,

         4, 5, 6,
         6, 7, 4,

         8, 9, 10,
         10, 11, 8,
         
         12, 13, 14,
         14, 15, 12,

    #   octava fila
         0, 1, 2,
         2, 3, 0,

         4, 5, 6,
         6, 7, 4,

         8, 9, 10,
         10, 11, 8,
         
         12, 13, 14,
         14, 15, 12,

         ], dtype= np.uint32)

    size = len(indices)
    return bs.Shape(vertexData, indices)
    



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Drawing a quad via a EBO and classes", None, None)

    if not window:
        glfw.terminate()
        glfw.set_window_should_close(window, True)

    glfw.make_context_current(window)

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, on_key)
    
    # Creating our shader program and telling OpenGL to use it
    pipeline = es.SimpleShaderProgram()

    # Creating shapes on GPU memory for createTablero
    Tshape = createFondo()
    gpuTshape = GPUShape().initBuffers()
    pipeline.setupVAO(gpuTshape)
    gpuTshape.fillBuffers(Tshape.vertices, Tshape.indices, GL_STATIC_DRAW)

    Qshape = createQuads()
    gpuQshape = GPUShape().initBuffers()
    pipeline.setupVAO(gpuQshape)
    gpuQshape.fillBuffers(Qshape.vertices, Qshape.indices, GL_STATIC_DRAW)


    
    # Setting up the clear screen color
    glClearColor(0.15, 0.15, 0.15, 1.0)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        # Invoking the draw call
        glUseProgram(pipeline.shaderProgram)
        pipeline.drawCall(gpuTshape)
        pipeline.drawCall(gpuQshape)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuTshape.clear()
    gpuQshape.clear()

    glfw.terminate()
