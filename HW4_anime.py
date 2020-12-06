import numpy as np
from vpython import *

A, N, omega = 0.10, 50, 2 * pi / 1.0
size, m, k, d = 0.06, 0.1, 10.0, 0.4
scene = canvas(title='Spring Wave', width=800, height=300, background=vec(1,1,1), center=vec((N - 1) * d / 2, 0, 0))
balls = [sphere(radius=size, color=color.red, pos=vector(i * d, 0, 0), v=vector(0, 0, 0)) for i in range(N)]  # 3
springs = [helix(radius=size / 2.0, thickness=d / 15.0, pos=vector(i * d, 0, 0), axis=vector(d, 0, 0)) for i in
           range(N - 1)]  # 3
c = curve([vector(i * d, 1.0, 0) for i in range(N)], color=color.black)
ball_pos, ball_orig, ball_v, spring_len = np.arange(N) * d, np.arange(N) * d, np.zeros(N), np.ones(N) * d  # 5
t, dt = 0, 0.01
while True:
    rate(100)
    t += dt
    ball_pos[0] = A * sin(omega * t)  # 4
    spring_len[:-1] = ball_pos[1:] - ball_pos[:-1]
    ball_v[1:] += (spring_len[1:] - spring_len[:-1]) * k / m * dt
    spring_len[N - 1] = ball_pos[0] - ball_pos[N - 1] + N * d
    ball_v[0] += (spring_len[0] - spring_len[N - 1]) * k / m * dt
    ball_pos += ball_v * dt

    for i in range(N): balls[i].pos.x = ball_pos[i]  # 3
    for i in range(N - 1):  # 3
        springs[i].pos = balls[i].pos  # 3
        springs[i].axis = balls[i + 1].pos - balls[i].pos  # 3
    ball_disp = ball_pos - ball_orig
    for i in range(N):
        c.modify(i, y=ball_disp[i] * 4 + 1)
