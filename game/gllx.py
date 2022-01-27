from math import degrees

from scipy.spatial.transform import Rotation as R
from OpenGL.GL import *
import matplotlib.cm
# from vectors import *
import numpy as np
from math import *


def lxRotate(roll, pitch, yaw):
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html
    r = R.from_euler('zxy', [roll, pitch, yaw])
    x, y, z = r.as_rotvec()
    angle = degrees(r.magnitude())
    return glRotate(angle, x, y, z)


def lxFrustum(focal_length, width, height, near, far):
    q = 35.9 / focal_length
    p = min(1, 3 / 4 * width / height)
    right = q * near / 2 * p
    top = right * height / width
    # 视景体的left/right/bottom/top/near/far六个面
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-right, right, -top, top, near, far)
    glMatrixMode(GL_MODELVIEW)


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


def lxDrawRect(w, l):
    glBegin(GL_POLYGON)
    glVertex3f(-w / 2, -l / 2, 0)
    glVertex3f(-w / 2, l / 2, 0)
    glVertex3f(w / 2, l / 2, 0)
    glVertex3f(w / 2, -l / 2, 0)
    glEnd()


def lxDrawSnow(a):
    glPushMatrix()
    glRotate(a, 1, 0, 0)
    glTranslate(0, 0, -1.5)
    glColor4f(0.9, 0.9, 0.9, 1.0)
    lxDrawRect(10, 100)
    glPopMatrix()


def lxDrawSki(a, b):
    glPushMatrix()
    glRotate(a, 1, 0, 0)
    glRotate(b, 0, 0, -1)
    glColor4f(220 / 255, 20 / 255, 60 / 255, 1.0)
    lxDrawRect(1.60, 0.10)
    glPopMatrix()


# https://livebook.manning.com/book/math-for-programmers/a-loading-and-rendering-3d-models-with-opengl-and-pygame/v-8/32
def normal(face):
    face = np.array(face)
    return np.cross(face[1] - face[0], face[2] - face[0])

def unit(v):
    return v / np.linalg.norm(v)
  

def shade(face, cmap, light):
    return cmap(1 + np.dot(unit(normal(face)), unit(light)))


def lxDrawFaces(faces, cmap_name='Blues', light=(1, 2, 3)):
    # https://matplotlib.org/stable/api/cm_api.html#matplotlib.cm.get_cmap
    cmap = matplotlib.cm.get_cmap(cmap_name)
    # glTranslate(2.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    for face in faces:
        color = shade(face, cmap, light)
        for vertex in face:
            glColor4fv(color)
            glVertex3fv(vertex)
    glEnd()
    # glTranslate(-2.0, 0.0, 0.0)


def lxTestCmap():
    w = 5.0
    l = 0.6
    blues = matplotlib.cm.get_cmap('Blues')
    glBegin(GL_POLYGON)
    glColor4fv(blues(0))
    glVertex3f(-w / 2, -l / 2, 0)
    glVertex3f(-w / 2, l / 2, 0)
    glColor4fv(blues(1.0))
    glVertex3f(w / 2, l / 2, 0)
    glVertex3f(w / 2, -l / 2, 0)
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
