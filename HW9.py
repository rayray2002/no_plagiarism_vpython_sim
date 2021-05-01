from vpython import *
import numpy as np

R = 0.12
r = 0.06
h = 0.1

m = 1000
dx = r / m
n = 1000

flux = 0
for i in range(m):
    x = dx * i
    pos_p = vec(x, 0, h)
    B = vec(0, 0, 0)

    for j in range(n):
        theta = 2 * pi / n * j
        ds = 2 * pi * R / n * vec(cos(pi / 2 + theta), sin(pi / 2 + theta), 0)
        pos_s = R * vec(cos(theta), sin(theta), 0)

        dB = 1E-7 * cross(ds, norm(pos_p - pos_s)) / mag2(pos_p - pos_s)
        # print(theta*180/pi, norm(pos_p - pos_s), dB)
        B += dB

    flux += 2 * pi * x * dx * dot(B, vec(0, 0, 1))
    # print(x, B)
print(flux)

dx = R / m
flux = 0
for i in range(m):
    x = dx * i
    pos_p = vec(x, 0, 0)
    B = vec(0, 0, 0)

    for j in range(n):
        theta = 2 * pi / n * j
        ds = 2 * pi * r / n * vec(cos(pi / 2 + theta), sin(pi / 2 + theta), 0)
        pos_s = vec(r * cos(theta), r * sin(theta), h)

        dB = 1E-7 * cross(ds, norm(pos_p - pos_s)) / mag2(pos_p - pos_s)
        # print(x, theta*180/pi, (pos_p - pos_s), dB)
        B += dB

    flux += 2 * pi * x * dx * dot(B, vec(0, 0, 1))
    # print(x, B)
print(flux)
