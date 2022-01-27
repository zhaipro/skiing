# https://download.blender.org/release/Blender2.83/
import json

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import utils
from gllx import *

import matplotlib.cm
from math import *
from scipy.spatial.transform import Rotation as R


light = (1,2,3)
faces = [
    [(1,0,0), (0,1,0), (0,0,1)],
    [(1,0,0), (0,0,-1), (0,1,0)],
    [(1,0,0), (0,0,1), (0,-1,0)],
    [(1,0,0), (0,-1,0), (0,0,-1)],
    [(-1,0,0), (0,0,1), (0,1,0)],
    [(-1,0,0), (0,1,0), (0,0,-1)],
    [(-1,0,0), (0,-1,0), (0,0,1)],
    [(-1,0,0), (0,0,-1), (0,-1,0)],
]

_faces = [
    [(-0.8, 0.05, 0), (0.8, 0.05, 0), (-0.8, -0.05, 0)],
    [(-0.8, -0.05, 0), (0.8, 0.05, 0), (0.8, -0.05, 0)],
]



class Game:

    def __init__(self):
        self.states = {}
        self.win_w, self.win_h = 640, 480   # 保存窗口宽度和高度的变量
        self.camera_x, self.camera_y, self.camera_z = 0, 0, 0
        self.mouse_x, self.mouse_y = 0, 0
        self.phi, self.theta = 0, 0
        self.ophi, self.otheta = 0, 0
        self.focal_length = 50
        self.realtime = False
        self.light = (1, 2, 3)

    def mouse(self, button, state, x, y):
        if button == 3:
            glTranslate(0, 0, 0.01)
        elif button == 4:
            glTranslate(0, 0, -0.01)
        self.states[button] = state
        self.mouse_x, self.mouse_y = x, y
        glutPostRedisplay()

    def motion(self, x, y):
        if self.states.get(GLUT_RIGHT_BUTTON) == GLUT_DOWN:
            dx = self.mouse_x - x
            dy = self.mouse_y - y
            self.mouse_x, self.mouse_y = x, y

            self.phi += 360 * dy / self.win_h
            self.phi %= 360
            self.theta += 360 * dx / self.win_w
            self.theta %= 360
        elif self.states.get(GLUT_LEFT_BUTTON) == GLUT_DOWN:
            dx = self.mouse_x - x
            dy = self.mouse_y - y
            self.mouse_x, self.mouse_y = x, y

            self.ophi += 360 * dy / self.win_h
            self.ophi %= 360
            self.otheta += 360 * dx / self.win_w
            self.otheta %= 360

        glutPostRedisplay()

    def keyboard(self, key, x, y):
        glutPostRedisplay()
        if key == b' ':
            glutDestroyWindow(glutGetWindow())

    def display(self):
        # 清除屏幕及深度缓存
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # 设置视点
        glTranslate(self.camera_x, self.camera_y, self.camera_z)
        lxLookAt(8.0, self.phi, self.theta)

        glPushMatrix()

        light = R.from_euler('xyz', [0, self.otheta, self.ophi], degrees=True).apply(self.light)
        lxDrawFaces(faces, light=light)

        # lxTestCmap()

        glPopMatrix()
        glPopMatrix()

        # glFlush()
        glutSwapBuffers()                    # 切换缓冲区，以显示绘制内容

    def reshape(self, width, height):
        self.win_w, self.win_h = width, height
        glViewport(0, 0, self.win_w, self.win_h)
        lxFrustum(self.focal_length, self.win_w, self.win_h, 0.01, 50.0)

    def init(self):
        glutInit()
        glutInitWindowSize(self.win_w, self.win_h)
        glutInitWindowPosition(300, 200)
        glutCreateWindow('Quidam Of OpenGL')
        glutDisplayFunc(self.display)       # 注册绘制
        glutReshapeFunc(self.reshape)       # 注册响应窗口改变的函数
        glutMouseFunc(self.mouse)           # 注册响应鼠标点击的函数
        glutMotionFunc(self.motion)         # 注册响应鼠标拖拽的函数
        glutKeyboardFunc(self.keyboard)     # 注册键盘输入的函数
        # 初始化画布
        glClearColor(0.5, 0.5, 0.5, 1.0)    # 设置画布背景色
        glEnable(GL_DEPTH_TEST)             # 开启深度测试，实现遮挡关系

        # gluPerspective(45, 1, 0.1, 50.0)
        # glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

    def main(self):
        glutMainLoop()                      # 进入glut主循环


if __name__ == '__main__':
    game = Game()
    game.init()
    game.main()
