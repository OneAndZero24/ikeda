import numpy as np
from PIL import Image
from progress.bar import Bar

# (parameter), point
def ikeda(u):
    def a(p):
        x, y = p
        t = 6.0/((x**2)+(y**2)+1)
        c = np.cos(t)
        s = np.sin(t)
        return (1+u*((x*c)-(y*s)), u*((x*s)+(y*c)))
    return a

# size, range, point
def toidx(size, R, p):
    x, y = p
    lx = R[0][1] - R[0][0]
    ly = R[1][1] - R[1][0]
    sx = lx/(size[0]-1)
    sy = ly/(size[1]-1)
    xr = int(np.round((x-R[0][0])/sx))
    yr = int(np.round((y-R[1][0])/sy))
    return (xr, yr)

# (factor), value
def invscale(f):
    def a(x):
        return 255-x*(255/f)
    return a

# size, range, N, point, function
def frame(size, R, N, p, func):
    T = np.zeros(size)

    for _ in range(N):
        new_p = func(p)
        p = new_p
        if(p[0] >= R[0][0] and p[0] <= R[0][1] and p[1] >= R[1][0] and p[1] <= R[1][1]):
            xi, yi = toidx(size, R, p)
            T[yi][xi] += 1

    f = np.max(T)
    for x, y in np.ndindex(T.shape):
        T[y][x] = invscale(f)(T[y][x])

    return Image.fromarray(T).convert('L').convert('P')  

# size, range, N, point, parameter range, func
def generate(size, R, N, p, U, func):
    imgs = []
    with Bar('Rendering', max=np.shape(U)[0]) as bar:
        for u in U:
            imgs.append(frame(size, R, N, p, func(u)))
            bar.next()
    imgs[0].save('ikeda.gif', save_all=True, append_images=imgs[1:], duration=30, loop=0)

if __name__ == "__main__":
    generate((1000, 1000), ((-1.5, 2.5),(-1.5, 3.5)), 1000000, (0, 0), np.linspace(0.6, 0.999, 100), ikeda)