import numpy as np
import matplotlib.pyplot as plt


def shearingFunc(x, y, h, v):
    return x + h * y, x * v + y


if __name__ == '__main__':
    x = np.arange(-10, 11, 1)
    y = np.arange(-10, 11, 1)

    x, y = np.meshgrid(x, y)
    hx, hy = shearingFunc(x, y, 1.25, 0)
    vx, vy = shearingFunc(x, y, 0, 1.25)

    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, s=2, c='#ff0000')
    plt.scatter(hx, hy, s=2, c='#000000')
    plt.scatter(vx, vy, s=2, c='#0000ff')
    plt.show()