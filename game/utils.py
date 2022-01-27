import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation


class Skiter:

    def __init__(self, m, a):
        self._m = m                 # 身体质量
        self._g = 9.8               # 重力加速度m/s^2
        self._a = np.radians(a)     # 坡度
        # 重力
        self.W = np.array([0, 0, -self._m * self._g])
        # 雪坡的单位法线
        self.n = np.array([0, -np.sin(self._a), np.cos(self._a)])

    def func(self, b):
        # 雪板的朝向
        b = np.radians(b)
        self.f = np.array([np.cos(b), -np.cos(self._a) * np.sin(b), -np.sin(self._a) * np.sin(b)])
        # 垂直于雪坡的分力
        self.F_n = np.dot(self.n, self.W) * self.n
        # 在雪坡上的分力
        self.F_s = self.W - self.F_n
        # 与雪板平行的分力
        self.F_p = np.dot(self.f, self.W) * self.f
        # 与雪板垂直的分力
        self.F_lat = self.F_s - self.F_p


def gen_func(m, a, r, v):
    g = 9.8
    a = np.radians(a)
    W = np.array([0, 0, -m * g])
    n = np.array([0, -np.sin(a), np.cos(a)])
    def func(b):
        b = np.radians(b)
        i = np.array([np.cos(b), -np.sin(b), 0])
        F_n = np.dot(n, W) * n
        F_s = W - F_n
        R = Rotation.from_euler('x', a)
        f = R.apply(i)
        F_p = np.dot(f, F_s) * f
        F_lat = F_s - F_p
        F_load = F_n + F_lat
        F_C = m * v ** 2 / r * F_lat / np.linalg.norm(F_lat)
        F_LAT = F_lat + F_C
        F_LOAD = F_n + F_LAT
        return F_LOAD, f
    return func


if __name__ == '__main__':
    func = gen_func(65, 15, 10, 40 * 1000 / 60 / 60)
    r = func(90)
    print(-r)
    print(np.linalg.norm(r), 65 * 9.8)
