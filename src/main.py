# -*- coding: utf-8 -*-

import json

from OpenGL.GL import *
from OpenGL.GLUT import *

from gllx import *


class Game:

    def __init__(self):
        self.states = {}
        self.win_w, self.win_h = 640, 480   # 保存窗口宽度和高度的变量
        self.x, self.y = 0, 0
        self.phi, self.theta = 0, 0
        self.i = 0

    def load_data(self):
        self.datasets = []
        with open('data.json') as fp:
            for line in fp:
                self.datasets.append(json.loads(line))


    def mouseclick(self, button, state, x, y):
        self.states[button] = state
        self.x, self.y = x, y

    def mousemotion(self, x, y):
        if self.states.get(GLUT_LEFT_BUTTON) != GLUT_DOWN:
            return
        dx = self.x - x
        dy = self.y - y
        self.x, self.y = x, y

        self.phi += 360 * dy / self.win_h
        self.phi %= 360
        self.theta += 360 * dx / self.win_w
        self.theta %= 360

        glutPostRedisplay()

    def keydown(self, key, x, y):
        glutPostRedisplay()
        if key == b'[':
            self.i = (self.i + len(self.datasets) - 1) % len(self.datasets)
        elif key == b']':
            self.i = (self.i + 1) % len(self.datasets)
        elif key == b'q':
            glutDestroyWindow(glutGetWindow())

    def draw(self):
        print('draw')
        # glutPostRedisplay()
        # 清除屏幕及深度缓存
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()

        # 设置视点
        lxLookAt(0.25, self.phi, self.theta)

        glPushMatrix()
        glScale(0.10, 0.10, 0.10)
        lxCoordinateSystem()
        glPopMatrix()
        glPushMatrix()

        roll, pitch, yaw = self.datasets[self.i]['attitude']
        lxRotate(roll, pitch, yaw)
        lxDrawPhone()

        x, y, z = self.datasets[self.i]['gravity']

        glBegin(GL_LINES)
        lxVertex3f(0.0, 0.0, 0.0)      # 设置x轴顶点（x轴负方向）
        lxVertex3f(x, y, z)
        glEnd()

        # x, y, z = datasets[self.i]['user_acceleration']
        # glBegin(GL_LINES)
        # lxVertex3f(0.0, 0.0, 0.0)      # 设置x轴顶点（x轴负方向）
        # lxVertex3f(x, y, z)
        # glEnd()

        glPopMatrix()
        glPopMatrix()

        # glFlush()
        glutSwapBuffers()                    # 切换缓冲区，以显示绘制内容

    def reshape(self, width, height):
        self.win_w, self.win_h = width, height
        glViewport(0, 0, self.win_w, self.win_h)
        glLoadIdentity()
        # 视景体的left/right/bottom/top/near/far六个面
        glFrustum(-0.08 * self.win_w / self.win_h, 0.08 * self.win_w / self.win_h, -0.08, 0.08, 0.1, 2.0)

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
