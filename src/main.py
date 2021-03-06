# -*- coding: utf-8 -*-

import json

import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *

from gllx import *


class Game:

    def __init__(self):
        self.states = {}
        self.win_w, self.win_h = 640, 480   # 保存窗口宽度和高度的变量
        self.camera_x, self.camera_y, self.camera_z = 0, 0, 0
        self.mouse_x, self.mouse_y = 0, 0
        self.phi, self.theta = 0, 0
        self.i = 0
        self.j = 0
        self.focal_length = 50
        self.realtime = False
        self.p = np.zeros(3)      # 位置
        self.v = np.zeros(3)      # 速度
        self.r = 100           # 阻力

    def load_data(self):
        self.datasets = []
        with open('data.json') as fp:
            for line in fp:
                self.datasets.append(json.loads(line))

    def mouseclick(self, button, state, x, y):
        if button == 3:
            glTranslate(0, 0, 0.01)
        elif button == 4:
            glTranslate(0, 0, -0.01)
        self.states[button] = state
        self.mouse_x, self.mouse_y = x, y
        glutPostRedisplay()

    def mousemotion(self, x, y):
        if self.states.get(GLUT_RIGHT_BUTTON) == GLUT_DOWN:
            dx = self.mouse_x - x
            dy = self.mouse_y - y
            self.mouse_x, self.mouse_y = x, y

            self.phi += 360 * dy / self.win_h
            self.phi %= 360
            self.theta += 360 * dx / self.win_w
            self.theta %= 360
        elif self.states.get(GLUT_LEFT_BUTTON) == GLUT_DOWN:
            dx = (self.mouse_x - x) / self.win_w
            dy = (self.mouse_y - y) / self.win_h
            self.mouse_x, self.mouse_y = x, y
            self.camera_x -= dx / 5
            self.camera_y += dy / 5

        glutPostRedisplay()

    def keydown(self, key, x, y):
        glutPostRedisplay()
        if key == b'[':
            self.i = (self.i + len(self.datasets) - 1) % len(self.datasets)
        elif key == b']':
            roll, pitch, yaw = self.datasets[self.i]['attitude']
            r = R.from_euler('zxy', [roll, pitch, yaw])
            x, y, z = self.datasets[self.i]['user_acceleration']
            a = np.array([-x, z, -y])
            a = r.inv().apply(a)
            t = 0.1
            self.v += a * t
            self.v *= max(0, 1 - self.r * np.linalg.norm(self.v) * t)
            self.p += self.v * t
            self.i = (self.i + 1) % len(self.datasets)
        elif key == b' ':
            glutDestroyWindow(glutGetWindow())
        elif key == b'w':
            glTranslate(0, 0, 0.01)
        elif key == b's':
            glTranslate(0, 0, -0.01)
        elif key == b'a':
            glTranslate(0.01, 0, 0)
        elif key == b'd':
            glTranslate(-0.01, 0, 0)
        elif key == b'q':
            glTranslate(0, 0.01, 0)
        elif key == b'e':
            glTranslate(0, -0.01, 0)
        elif key == b'r':
            self.focal_length += 1
            lxFrustum(self.focal_length, self.win_w, self.win_h, 0.1, 2.0)
        elif key == b'f':
            self.focal_length -= 1
            lxFrustum(self.focal_length, self.win_w, self.win_h, 0.1, 2.0)
        elif key == b'p':
            self.realtime = not self.realtime

    def draw(self):
        if self.realtime:
            glutPostRedisplay()
            self.j += 1
            if self.j == 100:
                self.j = 0
                self.i = (self.i + 1) % len(self.datasets)
        # 清除屏幕及深度缓存
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # 设置视点
        glTranslate(self.camera_x, self.camera_y, self.camera_z)
        lxLookAt(0.50, self.phi, self.theta)

        glPushMatrix()
        glScale(0.10, 0.10, 0.10)
        lxCoordinateSystem()
        glPopMatrix()
        glPushMatrix()

        glTranslate(*self.p)

        roll, pitch, yaw = self.datasets[self.i]['attitude']
        lxRotate(roll, pitch, yaw)
        lxDrawPhone()

        x, y, z = self.datasets[self.i]['gravity']

        glBegin(GL_LINES)
        lxVertex3f(0.0, 0.0, 0.0)      # 设置x轴顶点（x轴负方向）
        lxVertex3f(x, y, z)
        glEnd()

        x, y, z = self.datasets[self.i]['user_acceleration']
        glBegin(GL_LINES)
        lxVertex3f(0.0, 0.0, 0.0)      # 设置x轴顶点（x轴负方向）
        lxVertex3f(x, y, z)
        glEnd()

        '''
        x, y, z, _ = self.datasets[self.i]['magnetic_field']
        glBegin(GL_LINES)
        lxVertex3f(0.0, 0.0, 0.0)      # 设置x轴顶点（x轴负方向）
        glVertex3f(x, y, z)
        glEnd()
        '''

        glPopMatrix()
        glPopMatrix()

        # glFlush()
        glutSwapBuffers()                    # 切换缓冲区，以显示绘制内容

    def reshape(self, width, height):
        self.win_w, self.win_h = width, height
        glViewport(0, 0, self.win_w, self.win_h)
        lxFrustum(self.focal_length, self.win_w, self.win_h, 0.01, 2.0)

    def init(self):
        glutInit()
        glutInitWindowSize(self.win_w, self.win_h)
        glutInitWindowPosition(300, 200)
        glutCreateWindow('Quidam Of OpenGL')
        glutDisplayFunc(self.draw)          # 注册绘制
        glutReshapeFunc(self.reshape)       # 注册响应窗口改变的函数
        glutMouseFunc(self.mouseclick)      # 注册响应鼠标点击的函数
        glutMotionFunc(self.mousemotion)    # 注册响应鼠标拖拽的函数
        glutKeyboardFunc(self.keydown)      # 注册键盘输入的函数
        # 初始化画布
        glClearColor(0.5, 0.5, 0.5, 1.0)    # 设置画布背景色
        glEnable(GL_DEPTH_TEST)             # 开启深度测试，实现遮挡关系

    def main(self):
        glutMainLoop()                      # 进入glut主循环


if __name__ == '__main__':
    game = Game()
    game.init()
    game.load_data()
    game.main()
