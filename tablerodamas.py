# Coding=utf-8
"""Dibujo de tablero de damas con sus piezas en posición inicial"""

# Import de todo lo que se utilizará
import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import numpy
import grafica.easy_shaders as es
import grafica.basic_shapes as bs
from grafica.gpu_shape import GPUShape, SIZE_IN_BYTES

# We will use 32 bits data, so floats and integers have 4 bytes
# 1 byte = 8 bits
SIZE_IN_BYTES = 4

# A class to store the application control
class Controller:
    fillPolygon = True

# We will use the global controller as communication with the callback function
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



# Función que genera un fondo cuadrado de color blanco
def createFondo():
    
    vertexData = np.array([
    #   positions   colors
        -1, -1, 0,  1.0, 1.0, 1.0,
         1, -1, 0,  1.0, 1.0, 1.0,
         1,  1, 0,  1.0, 1.0, 1.0,
        -1,  1, 0,  1.0, 1.0, 1.0
    # It is important to use 32 bits data
        ], dtype = np.float32)

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = np.array([
         0, 1, 2,
         2, 3, 0
         ], dtype= np.uint32)

    size = len(indices)
    # Ocupamos clase Shape del archivo basic_shapes.py
    return bs.Shape(vertexData, indices)


# Función que genera todos los cuadrados negros del tablero, usando cada una de sus posiciones
def createQuads():

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
    indices = np.array([ 
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
         64, 65, 66,
         66, 67, 64,

         68, 69, 70,
         70, 71, 68,

         72, 73, 74,
         74, 75, 72,
         
         76, 77, 78,
         78, 79, 76,

    #   sexta fila
         80, 81, 82,
         82, 83, 80,

         84, 85, 86,
         86, 87, 84,

         88, 89, 90,
         90, 91, 88,
         
         92, 93, 94,
         94, 95, 92,

    #   séptima fila
         96, 97, 98,
         98, 99, 96,

         100, 101, 102,
         102, 103, 100,

         104, 105, 106,
         106, 107, 104,
         
         108, 109, 110,
         110, 111, 108,

    #   octava fila
         112, 113, 114,
         114, 115, 112,

         116, 117, 118,
         118, 119, 116,

         120, 121, 122,
         122, 123, 120,
         
         124, 125, 126,
         126, 127, 124

         ], dtype= np.uint32)

    size = len(indices)
    # Ocupamos clase Shape del archivo basic_shapes.py
    return bs.Shape(vertexData, indices)
    

# Función que crea un arreglo con los vértices de un circulo
def crear_dama(x,y,r,g,b,radius):
    
    circle = []
    for angle in range(0,360,10):
        circle.extend([x, y, 0.0, r, g, b])
        circle.extend([x+numpy.cos(numpy.radians(angle))*radius, 
                       y+numpy.sin(numpy.radians(angle))*radius, 
                       0.0, r, g, b])
        circle.extend([x+numpy.cos(numpy.radians(angle+10))*radius, 
                       y+numpy.sin(numpy.radians(angle+10))*radius, 
                       0.0, r, g, b])
    return circle

# Función que genera todas las damas en base a función "crear_dama"
def createDamas():
    A1 = [-0.875, -0.375, 0.125, 0.625]
    A2 = [0.875, 0.375]
    A3 = [-0.625, -0.125, 0.375, 0.875]
    A4 = [-0.375, -0.875]
    F = []

    #para fila 1 y 3
    for i in A1:
        for j in A2:
            F.extend(crear_dama(i, j, 1, 0, 0, 0.1))

    #para fila 2
    for i in A3:
        F.extend(crear_dama(i, 0.625, 1, 0, 0, 0.1))
    A4 = [-0.375, -0.875]

    #para fila 6 y 8
    for i in A3:
        for j in A4:
            F.extend(crear_dama(i, j, 0, 0, 1, 0.1))

    #para fila 7
    for i in A1:
        F.extend(crear_dama(i, -0.625, 0, 0, 1, 0.1))

    # Ocupamos clase Shape del archivo basic_shapes.py
    return bs.Shape(F, range(len(F)))



if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        glfw.set_window_should_close(True)

    width = 600
    height = 600

    window = glfw.create_window(width, height, "Dibujando un tablero de damas", None, None)

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

    # Creating shapes on GPU memory for createQuads
    Qshape = createQuads()
    gpuQshape = GPUShape().initBuffers()
    pipeline.setupVAO(gpuQshape)
    gpuQshape.fillBuffers(Qshape.vertices, Qshape.indices, GL_STATIC_DRAW)

    # Creating shapes on GPU memory for createDamas
    Dshape = createDamas()
    gpuDshape = GPUShape().initBuffers()
    pipeline.setupVAO(gpuDshape)
    gpuDshape.fillBuffers(Dshape.vertices, Dshape.indices, GL_STATIC_DRAW)

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
        # Dibujar fondo blanco del tablero
        pipeline.drawCall(gpuTshape)
        # Dibujar cuadrados negros del tablero
        pipeline.drawCall(gpuQshape)
        # Dibujar todas las damas en su posición incial
        pipeline.drawCall(gpuDshape)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuTshape.clear()
    gpuQshape.clear()
    gpuDshape.clear()

    # Finalizar glfw
    glfw.terminate()
