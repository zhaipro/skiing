from math import degrees

from scipy.spatial.transform import Rotation as R
from OpenGL.GL import *


def lxRotate(roll, pitch, yaw):
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html
    r = R.from_euler('zxy', [roll, pitch, yaw])
    x, y, z = r.as_rotvec()
    angle = degrees(r.magnitude())
    return glRotate(angle, x, y, z)


def lxVertex3f(x, y, z):
    return glVertex3f(-x, z, -y)


def lxDrawPhone():
    glBegin(GL_POLYGON)
    glColor4f(131 / 255, 175 / 255, 155 / 255, 1.0)
    glVertex3f(-0.0380, 0.005, -0.0675)
    glVertex3f(-0.0380, 0.005, 0.0675)
    glVertex3f(0.0380, 0.005, 0.0675)
    glVertex3f(0.0380, 0.005, -0.0675)
    glEnd()

    glBegin(GL_POLYGON)
    glColor4f(1.0, 1.0, 1.0, 1.0)
    glVertex3f(-0.0380, 0, -0.0675)
    glVertex3f(-0.0380, 0, 0.0675)
    glVertex3f(0.0380, 0, 0.0675)
    glVertex3f(0.0380, 0, -0.0675)
    glEnd()


def lxArrows():
    # 绘制指向右侧的箭头
    glBegin(GL_LINES)
    glVertex3f(-1.0, 0.0, 0.0)      # 设置x轴顶点（x轴负方向）
    glVertex3f(1.0, 0.0, 0.0)       # 设置x轴顶点（x轴正方向）
    glVertex3f(0.9, 0.1, 0)         # 箭头
    glVertex3f(1.0, 0.0, 0.0)
    glVertex3f(0.9, -0.1, 0.0)
    glVertex3f(1.0, 0.0, 0.0)
    glEnd()


def lxCoordinateSystem():
    glPushMatrix()
    # 以红色绘制x轴
    glColor4f(1.0, 0.0, 0.0, 1.0)        # 设置当前颜色为红色不透明
    lxArrows()
    # 以绿色绘制y轴
    glColor4f(0.0, 1.0, 0.0, 1.0)        # 设置当前颜色为绿色不透明
    glRotatef(90, 0.0, 0.0, 1.0)
    lxArrows()
    # 以蓝色绘制z轴
    glColor4f(0.0, 0.0, 1.0, 1.0)        # 设置当前颜色为蓝色不透明
    glRotate(-90, 0.0, 1.0, 0.0)
    lxArrows()
    glPopMatrix()


def lxLookAt(r, phi, theta):
    glTranslate(0, 0, -r)
    r = R.from_euler('XYZ', [-phi, -theta, 0], degrees=True)
    x, y, z = r.as_rotvec()
    angle = degrees(r.magnitude())
    return glRotate(angle, x, y, z)


def lxDrawTriangles():
    glBegin(GL_TRIANGLES)               # 开始绘制三角形（z轴负半区）

    glColor4f(1.0, 0.0, 0.0, 1.0)       # 设置当前颜色为红色不透明
    glVertex3f(-0.5, -0.366, 0)         # 设置三角形顶点
    glColor4f(0.0, 1.0, 0.0, 1.0)       # 设置当前颜色为绿色不透明
    glVertex3f(0.5, -0.366, 0)          # 设置三角形顶点
    glColor4f(0.0, 0.0, 1.0, 1.0)       # 设置当前颜色为蓝色不透明
    glVertex3f(0.0, 0.5, 0)             # 设置三角形顶点

    glEnd()                              # 结束绘制三角形
