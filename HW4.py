import numpy as np
from vpython import *

A, N = 0.10, 50
m, k, d = 0.1, 10.0, 0.4
dt, avg_count = 0.0003, 10

g = graph(title='Dispersion Relationship', width=1200, height=600, align='left', xtitle="n", ytitle="Angular Frequency")
p = gcurve(graph=g, color=color.blue, width=2)


class Obj:
    pass


balls = [Obj for i in range(N)]
springs = [Obj for i in range(N - 1)]

for n in arange(1.0, N // 2, 1.0):
    Unit_K = 2.0 * pi / (N * d)
    Wavevector = n * Unit_K
    phase = Wavevector * arange(N) * d
    ball_pos, ball_v, spring_len = np.arange(N) * d + A * np.sin(phase), np.zeros(N), np.ones(N) * d

    t, count = 0.0, 0
    while count < 2 * avg_count:
        t += dt

        spring_len[:-1] = ball_pos[1:] - ball_pos[:-1]
        ball_v[1:] += (spring_len[1:] - spring_len[:-1]) * k / m * dt
        spring_len[N - 1] = ball_pos[0] - ball_pos[N - 1] + N * d
        ball_v[0] += (spring_len[0] - spring_len[N - 1]) * k / m * dt
        if ball_pos[0] * (ball_pos[0] + ball_v[0] * dt) < 0 and t > 5 * dt:
            count += 1
        ball_pos += ball_v * dt

    T = t / avg_count
    print(n, 2.0 * pi / T)
    p.plot(n, 2.0 * pi / T)
