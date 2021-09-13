# Coding=utf-8
"""Dibujo de tablero de damas con sus piezas en posición inicial"""

# Import de todo lo que se utilizará
import glfw
from OpenGL.GL import *
import numpy as np
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



# Función que genera un fondo cuadrado de color café claro
def createFondo():
    vertexData = np.array([
    #   positions   colors
        -1, -1, 0,  0.823, 0.694, 0.498,
         1, -1, 0,  0.823, 0.694, 0.498,
         1,  1, 0,  0.823, 0.694, 0.498,
        -1,  1, 0,  0.823, 0.694, 0.498
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


# Función para crear marco café claro
def createFrame():
    vertexData = np.array([
    #   positions        colors
        -1, -1, 0,       0.823, 0.694, 0.498,
         1, -1, 0,       0.823, 0.694, 0.498,
         1, -0.98, 0,    0.823, 0.694, 0.498,
        -1, -0.98, 0,    0.823, 0.694, 0.498,
 
         0.98, -1, 0,    0.823, 0.694, 0.498,
         1, -1, 0,       0.823, 0.694, 0.498,
         1, 1, 0,        0.823, 0.694, 0.498,
         0.98, 1, 0,     0.823, 0.694, 0.498,

        -1, 0.98, 0,     0.823, 0.694, 0.498,
         1, 0.98, 0,     0.823, 0.694, 0.498,
         1, 1, 0,        0.823, 0.694, 0.498,
        -1, 1, 0,        0.823, 0.694, 0.498,

        -1, -1, 0,       0.823, 0.694, 0.498,
        -0.98, -1, 0,    0.823, 0.694, 0.498,
        -0.98, 1, 0,     0.823, 0.694, 0.498,
        -1, 1, 0,        0.823, 0.694, 0.498
        ], dtype = np.float32)
    indices = np.array([
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
    # Ocupamos clase Shape del archivo basic_shapes.py
    return bs.Shape(vertexData, indices)


# Función para crear borde café oscuro de marco
def createSFrame():
    vertexData = np.array([
    #   positions              colors
        -0.984, -0.984, 0,     0.5, 0.25, 0.0,
         0.984, -0.984, 0,     0.5, 0.25, 0.0,
         0.984, -0.98, 0,      0.5, 0.25, 0.0,
        -0.984, -0.98, 0,      0.5, 0.25, 0.0,

         0.98, -0.984, 0,      0.5, 0.25, 0.0,
         0.984, -0.984, 0,     0.5, 0.25, 0.0,
         0.984, 0.984, 0,      0.5, 0.25, 0.0,
         0.98, 0.984, 0,       0.5, 0.25, 0.0,

        -0.984, 0.98, 0,       0.5, 0.25, 0.0,
         0.984, 0.98, 0,       0.5, 0.25, 0.0,
         0.984, 0.984, 0,      0.5, 0.25, 0.0,
        -0.984, 0.984, 0,      0.5, 0.25, 0.0,

        -0.984, -0.984, 0,     0.5, 0.25, 0.0,
        -0.98, -0.984, 0,      0.5, 0.25, 0.0,
        -0.98, 0.984, 0,       0.5, 0.25, 0.0,
        -0.984, 0.984, 0,      0.5, 0.25, 0.0
        ], dtype = np.float32)
    indices = np.array([
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
    # Ocupamos clase Shape del archivo basic_shapes.py
    return bs.Shape(vertexData, indices)


# Función que crea un arreglo con las coordenadas de un cuadrado en la posición (x,y,0) de color (r,g,b) y de lado a.
# (Posición dada por el vértice 1, es decir, el de abajo a la izquierda)
def crear_cuadrado(x,y,r,g,b,a):
    quad = []
    quad.extend([x, y, 0.0, r, g, b])
    quad.extend([x+a, y, 0.0, r, g, b])
    quad.extend([x+a, y+a, 0.0, r, g, b])
    quad.extend([x, y+a, 0.0, r, g, b])
    return quad


# Función que genera los 32 cuadrados del tablero en base a función "crear_cuadrado"
# Crea arreglo con los vértices e índices de los cuadrados
# Color elegido: café oscuro 
def createQuads():
    X = [-1, -0.5, 0.0, 0.5]
    Y = [0.75, 0.25, -0.25, -0.75]
    vertexData = []
    for i in X:
        for j in Y:
            vertexData.extend(crear_cuadrado(i, j, 0.5, 0.25, 0.0, 0.25))
    for i in X:
        for j in Y:
            vertexData.extend(crear_cuadrado(j, i, 0.5, 0.25, 0.0, 0.25))
    # Crear arreglo con indices
    indices = []
    a=0
    b=1
    c=2
    d=3
    while len(indices) <= len(vertexData):
        indices.append(a)
        indices.append(b)
        indices.append(c)
        indices.append(c)
        indices.append(d)
        indices.append(a)
        a=a+4
        b=b+4
        c=c+4
        d=d+4
    # Ocupamos clase Shape del archivo basic_shapes.py
    return bs.Shape(vertexData, indices)


# Función que crea un arreglo con los vértices de un circulo
def crear_dama(x,y,r,g,b,radius):
    circle = []
    for angle in range(0,360,10):
        circle.extend([x, y, 0.0, r, g, b])
        circle.extend([x+np.cos(np.radians(angle))*radius, 
                       y+np.sin(np.radians(angle))*radius, 
                       0.0, r, g, b])
        circle.extend([x+np.cos(np.radians(angle+10))*radius, 
                       y+np.sin(np.radians(angle+10))*radius, 
                       0.0, r, g, b])
    return circle


# Función que genera todas las damas en base a función "crear_dama"
# Color elegido para las damas de arriba: gris muy oscuro
# Color elegido para las damas de abajo: gris muy claro
def createDamas():
    A1 = [-0.875, -0.375, 0.125, 0.625]
    A2 = [0.875, 0.375]
    A3 = [-0.625, -0.125, 0.375, 0.875]
    A4 = [-0.375, -0.875]
    F = []
    #para fila 1 y 3
    for i in A1:
        for j in A2:
            F.extend(crear_dama(i, j, 0.3, 0.3, 0.3, 0.095))
    #para fila 2
    for i in A3:
        F.extend(crear_dama(i, 0.625, 0.3, 0.3, 0.3, 0.095))
    A4 = [-0.375, -0.875]
    #para fila 6 y 8
    for i in A3:
        for j in A4:
            F.extend(crear_dama(i, j, 0.9, 0.9, 0.9, 0.095))
    #para fila 7
    for i in A1:
        F.extend(crear_dama(i, -0.625, 0.9, 0.9, 0.9, 0.095))
    # Ocupamos clase Shape del archivo basic_shapes.py
    return bs.Shape(F, range(len(F)))


# Función que crea sombras tipo borde a las damas
def createSDamas():
    A1 = [-0.875, -0.375, 0.125, 0.625]
    A2 = [0.875, 0.375]
    A3 = [-0.625, -0.125, 0.375, 0.875]
    A4 = [-0.375, -0.875]
    F = []
    #para fila 1 y 3
    for i in A1:
        for j in A2:
            F.extend(crear_dama(i, j, 0.15, 0.15, 0.15, 0.1))
    #para fila 2
    for i in A3:
        F.extend(crear_dama(i, 0.625, 0.15, 0.15, 0.15, 0.1))
    A4 = [-0.375, -0.875]
    #para fila 6 y 8
    for i in A3:
        for j in A4:
            F.extend(crear_dama(i, j, 0.7, 0.7, 0.7, 0.1))
    #para fila 7
    for i in A1:
        F.extend(crear_dama(i, -0.625, 0.7, 0.7, 0.7, 0.1))
    # Ocupamos clase Shape del archivo basic_shapes.py
    return bs.Shape(F, range(len(F)))


# Función que crea sombras tipo cuerpo a las damas
def createS2Damas():
    A1 = [-0.875, -0.375, 0.125, 0.625]
    A2 = [0.875, 0.375]
    A3 = [-0.625, -0.125, 0.375, 0.875]
    A4 = [-0.375, -0.875]
    F = []
    #para fila 1 y 3
    for i in A1:
        for j in A2:
            F.extend(crear_dama(i, j, 0.15, 0.15, 0.15, 0.08))
    #para fila 2
    for i in A3:
        F.extend(crear_dama(i, 0.625, 0.15, 0.15, 0.15, 0.08))
    A4 = [-0.375, -0.875]
    #para fila 6 y 8
    for i in A3:
        for j in A4:
            F.extend(crear_dama(i, j, 0.7, 0.7, 0.7, 0.08))
    #para fila 7
    for i in A1:
        F.extend(crear_dama(i, -0.625, 0.7, 0.7, 0.7, 0.08))
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

    # Creating shapes on GPU memory for createFrame
    Fshape = createFrame()
    gpuFshape = GPUShape().initBuffers()
    pipeline.setupVAO(gpuFshape)
    gpuFshape.fillBuffers(Fshape.vertices, Fshape.indices, GL_STATIC_DRAW)

    # Creating shapes on GPU memory for createSFrame
    SFshape = createSFrame()
    gpuSFshape = GPUShape().initBuffers()
    pipeline.setupVAO(gpuSFshape)
    gpuSFshape.fillBuffers(SFshape.vertices, SFshape.indices, GL_STATIC_DRAW)

    #Creating shapes on GPU memory for createSDamas
    SDshape = createSDamas()
    gpuSDshape = GPUShape().initBuffers()
    pipeline.setupVAO(gpuSDshape)
    gpuSDshape.fillBuffers(SDshape.vertices, SDshape.indices, GL_STATIC_DRAW)

    #Creating shapes on GPU memory for createS2Damas
    S2Dshape = createS2Damas()
    gpuS2Dshape = GPUShape().initBuffers()
    pipeline.setupVAO(gpuS2Dshape)
    gpuS2Dshape.fillBuffers(S2Dshape.vertices, S2Dshape.indices, GL_STATIC_DRAW)

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
        # Dibujar fondo café claro del tablero
        pipeline.drawCall(gpuTshape)
        # Dibujar cuadrados cafe oscuro del tablero
        pipeline.drawCall(gpuQshape)
        # Dibujar sombras de damas
        pipeline.drawCall(gpuSDshape)
        # Dibujar todas las damas en su posición incial
        pipeline.drawCall(gpuDshape)
        # Dibujar marco/frame del tablero
        pipeline.drawCall(gpuFshape)
        # Dibujar borde marco/frame del tablero
        pipeline.drawCall(gpuSFshape)
        # Dibujar sombras 2 de damas
        pipeline.drawCall(gpuS2Dshape)

        # Once the render is done, buffers are swapped, showing only the complete scene.
        glfw.swap_buffers(window)

    # freeing GPU memory
    gpuTshape.clear()
    gpuQshape.clear()
    gpuDshape.clear()
    gpuFshape.clear()
    gpuSFshape.clear()
    gpuSDshape.clear()
    gpuS2Dshape.clear()


    # Finalizar glfw
    glfw.terminate()
