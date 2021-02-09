import numpy as np

if __name__ == '__main__':
    arr2d = np.random.rand(2000, 2440)

    arr2d[0, 0] = 1
    arr2d[1000, 1000] = 1

    max = np.max(arr2d)
    pos = np.where(arr2d == max)
    coords = zip(pos[0], pos[1])
    for coord in coords:
        print(coord)