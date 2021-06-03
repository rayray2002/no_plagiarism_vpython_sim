from vpython import *
from numpy import *

N = 100
R, lamda = 1.0, 500E-9
d = 100E-6
k = 2 * pi / lamda

dx, dy = d / N, d / N

scene1 = canvas(align='left', height=600, width=600, center=vector(N * dx / 2, N * dy / 2, 0))
scene2 = canvas(align='right', x=600, height=600, width=600, center=vector(N * dx / 2, N * dy / 2, 0))
scene1.lights, scene2.lights = [], []
scene1.ambient, scene2.ambient = color.gray(0.99), color.gray(0.99)

side = linspace(-0.01 * pi, 0.01 * pi, N)
x, y = meshgrid(side, side)

side_source = linspace(-d / 2, d / 2, N)
pos_x, pos_y = meshgrid(side_source, side_source)

mask = ((pos_x ** 2 + pos_y ** 2) <= ((d / 2) ** 2))

E_field = zeros((N, N))
for i in range(N):
    for j in range(N):
        E_field[i, j] = sum(cos(k * x[i, j] * pos_x + k * y[i, j] * pos_y) * dx * dy * mask)

Inte = abs(E_field) ** 2
maxI = amax(Inte)
for i in range(N):
    for j in range(N):
        box(canvas=scene1, pos=vector(i * dx, j * dy, 0), length=dx, height=dy, width=dx,
            color=vector(Inte[i, j] / maxI, Inte[i, j] / maxI, Inte[i, j] / maxI))

theta = 0
pre_pre = Inte[49, 49]
pre = Inte[49, 50]
for i in range(51, N):
    now = Inte[49, i]
    if (pre < pre_pre and pre < now):
        theta = -0.01 * pi + (i - 1) * (0.02 * pi) / N
        break
    pre = pre_pre
    pre = now

print("sim:", theta)
print("theory:", 1.22 * lamda / d)

Inte = abs(E_field)
maxI = amax(Inte)
for i in range(N):
    for j in range(N):
        box(canvas=scene2, pos=vector(i * dx, j * dy, 0), length=dx, height=dy, width=dx,
            color=vector(Inte[i, j] / maxI, Inte[i, j] / maxI, Inte[i, j] / maxI))
