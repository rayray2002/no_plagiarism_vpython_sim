from vpython import *

fd = 120  # 120Hz
# (Your Parameters here)
T = 1 / fd
i = 0
v = 0
E = 0

C = 20E-6
L = 0.2
R = 30
Q = 0
i_old = i
E0 = 0

stage = 0

t = 0
dt = 1.0 / (fd * 5000)  # 5000 simulation points per cycle

scene1 = graph(align='left', xtitle='t', ytitle='i (A) blue, i_theory (A) cyan, v (100V) red,',
               background=vector(0.2, 0.6, 0.2))
scene2 = graph(align='left', xtitle='t', ytitle='Energy (J)', background=vector(0.2, 0.6, 0.2))

i_the_t = gcurve(color=color.cyan, graph=scene1)
i_t = gcurve(color=color.blue, graph=scene1)
v_t = gcurve(color=color.red, graph=scene1)
E_t = gcurve(color=color.red, graph=scene2)

# (Your program here)
while t <= 20 * T:
    if t < 12 * T:
        v = 36 * sin(2 * pi * fd * t)
        i_the = 0.40156 * sin(2 * pi * fd * t - 70 / 180 * pi)
        if stage == 0:
            if t >= 9 * T:
                print("t=9T compare i to theory:")
                print("i=", i, "A, i_theory:", i_the, 'A')
                print("error:", (i - i_the) / i_the * 100, '%')
                stage = 1
    else:
        if stage == 1:
            E0 = E
            stage = 2
        elif stage == 2:
            if E <= E0 / 10:
                print("decay time:", t - 12 * T, 's')
                stage = 3
        v = 0
        i_the = 0

    i = (v + L * i_old / dt - Q / C) / (R + dt / C + L / dt)

    Q += i * dt
    i_old = i
    t += dt
    E = i * i * R + Q * Q / C / 2 + L * i * i / 2

    i_t.plot(pos=(t, i))
    i_the_t.plot(pos=(t, i_the))
    v_t.plot(pos=(t, v / 100))
    E_t.plot(pos=(t, E))
