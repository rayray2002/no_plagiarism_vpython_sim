from numpy import *
from vpython import *

epsilon = 8.854E-12
N = 101
h = 1E-2 / (N - 1)
L, d = 4E-3, 1E-3
V0 = 200


def solve_laplacian(u, u_cond, h, Niter=5000):
    V = array(u)

    for i in range(Niter):
        V[u_cond] = u[u_cond]
        V[1:-1, 1:-1] = (V[:-2, 1:-1] + V[2:, 1:-1] + V[1:-1, :-2] + V[1:-1, 2:]) / 4

    return V


def get_field(V, h):
    Ex, Ey = gradient(V)
    Ex, Ey = -Ex / h, -Ey / h
    return Ex, Ey


u = zeros([N, N])
u[int(N / 2) - int(L / h / 2.0):int(N / 2) + int(L / h / 2.0), int(N / 2) - int(d / h / 2.0)] = -V0 / 2
u[int(N / 2) - int(L / h / 2.0):int(N / 2) + int(L / h / 2.0), int(N / 2) + int(d / h / 2.0)] = V0 / 2
u_cond = not_equal(u, 0)

V = solve_laplacian(u, u_cond, h)

scene = canvas(title='non-ideal capacitor', height=1000, width=1000, center=vec(N * h / 2, N * h / 2, 0))
scene.lights = []
scene.ambient = color.gray(0.99)
box(pos=vec(N * h / 2, N * h / 2 - d / 2 - h, 0), length=L, height=h / 5, width=h)
box(pos=vec(N * h / 2, N * h / 2 + d / 2 - h, 0), length=L, height=h / 5, width=h)

for i in range(N):
    for j in range(N):
        point = box(pos=vec(i * h, j * h, 0), length=h, height=h, width=h / 10,
                    color=vec((V[i, j] + 100) / 200, (100 - V[i, j]) / 200, 0.0))

Ex, Ey = get_field(V, h)

for i in range(0, N):
    for j in range(0, N):
        ar = arrow(pos=vec(i * h, j * h, h / 10), axis=vec(Ex[i, j] / 2E9, Ey[i, j] / 2E9, 0), shaftwidth=h / 6.0,
                   color=color.black)

# find Q, find C_nonideal = Q/(delta V)
Q = 0
delta = 5
min_x = int(N / 2) - int(L / h / 2.0) - delta
max_x = int(N / 2) + int(L / h / 2.0) + delta
min_y = int(N / 2) - int(d / h / 2.0) - delta
max_y = int(N / 2) - int(d / h / 2.0) + delta

for i in range(min_x, max_x):
    Q += (Ey[i, max_y] - Ey[i, min_y]) * h

for i in range(min_y, max_y):
    Q += (Ex[max_x, i] - Ex[min_x, i]) * h

Q = -Q * epsilon
C_nonideal = Q / V0

# Compare C_nonideal to C_ideal
C_ideal = epsilon * (L / d)
print("Ideal: %.3e" % C_ideal)
print("non-Ideal: %.3e" % C_nonideal)
print("error percentage: %.3f" % ((C_ideal - C_nonideal) / C_ideal * -100))
