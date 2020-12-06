from vpython import *

control = 1  # customize trigger

N = 2  # N value

size = 0.2
m = 1
L = 2
h = 0.05
speed = 0.5

Ks, Us = 0, 0
t = 0
dt, k, g = 0.0001, 150000, vector(0, -9.8, 0)
reset = 0

scene = canvas(width=800, height=800, align='left', center=vec(0, -L / 2, 0),
               background=vec(112 / 255, 153 / 255, 173 / 255))  # open window

plot1 = graph(width=600, height=380, align='right', title="Instant Energy", xtitle="t(s)", ytitle="E(J)")
kinetic_i = gcurve(graph=plot1, color=color.blue, width=2)
potential_i = gcurve(graph=plot1, color=color.red, width=2)

plot2 = graph(width=600, height=380, align='right', title="Average Energy", xtitle="t(s)", ytitle="E(J)")
kinetic_a = gcurve(graph=plot2, color=color.blue, width=2)
potential_a = gcurve(graph=plot2, color=color.red, width=2)


def af_col_v(m1, m2, v1, v2, x1, x2):  # function after collision velocity
    v1_prime = v1 + 2 * (m2 / (m1 + m2)) * (x1 - x2) * dot(v2 - v1, x1 - x2) / dot(x1 - x2, x1 - x2)
    v2_prime = v2 + 2 * (m1 / (m1 + m2)) * (x2 - x1) * dot(v1 - v2, x2 - x1) / dot(x2 - x1, x2 - x1)
    return v1_prime, v2_prime


balls = []
pivots = []
ropes = []
for i in range(5):
    pivots.append(sphere(pos=vec(-4 * size + 2 * size * i, 0, 0), radius=0.07))
    ropes.append(cylinder(pos=vec(-4 * size + 2 * size * i, 0, 0), radius=0.05))

    if i < N:
        balls.append(
            sphere(pos=vec(-4 * size + 2 * size * i, -L, 0) + vec(-sqrt(L * L - (L - h) * (L - h)), h, 0), radius=size))
    else:
        balls.append(sphere(pos=vec(-4 * size + 2 * size * i, -L, 0), radius=size))
    balls[i].v = vec(0, 0, 0)

    ropes[i].axis = balls[i].pos - ropes[i].pos


def n_refresh(n):
    global N, reset
    N = n.value
    reset = 1


def l_refresh(n):
    global L, reset
    L = n.number
    reset = 1


def h_refresh(n):
    global h, reset
    h = n.number
    reset = 1


def k_refresh(n):
    global k, reset
    k = n.number
    reset = 1


def m_refresh(n):
    global m, reset
    m = n.number
    reset = 1


def speed_refresh(n):
    global speed
    speed = n.value


if control:
    scene.append_to_caption('N:')
    N_control = slider(min=1, max=4, step=1, value=N, bind=n_refresh)

    scene.append_to_caption('\nLength: ')
    L_control = winput(text=L, bind=l_refresh)

    scene.append_to_caption('\nLift Height: ')
    h_control = winput(text=h, bind=h_refresh)

    scene.append_to_caption('\nMass: ')
    m_control = winput(text=m, bind=m_refresh)

    scene.append_to_caption('\nk: ')
    k_control = winput(text=k, bind=k_refresh)

    scene.append_to_caption('\nSim Speed:')
    speed_control = slider(min=0, max=1, step=0.1, value=speed, bind=speed_refresh)

while True:
    rate(1 / dt * speed)
    t += dt

    Ki, Ui = 0, 0

    for i in range(5):
        ropes[i].axis = balls[i].pos - ropes[i].pos
        tension = -k * (mag(ropes[i].axis) - L) * ropes[i].axis.norm()
        balls[i].a = g + tension / m

        if (i < 4 and mag(balls[i].pos - balls[i + 1].pos) <= 2 * size and dot(balls[i].pos - balls[i + 1].pos,
                                                                               balls[i].v - balls[i + 1].v) <= 0):
            (balls[i].v, balls[i + 1].v) = af_col_v(m, m, balls[i].v, balls[i + 1].v, balls[i].pos, balls[i + 1].pos)

        balls[i].v += balls[i].a * dt
        balls[i].pos += balls[i].v * dt

        Ki += 0.5 * m * mag(balls[i].v) * mag(balls[i].v)
        Ui += m * mag(g) * (balls[i].pos.y - min(balls[0].pos.y, balls[1].pos.y, balls[2].pos.y, balls[3].pos.y,
                                                 balls[4].pos.y))

    Ks += Ki * dt
    Us += Ui * dt

    if not reset:
        kinetic_i.plot(pos=(t, Ki))
        potential_i.plot(pos=(t, Ui))

        kinetic_a.plot(pos=(t, Ks / t))
        potential_a.plot(pos=(t, Us / t))
    else:
        for i in range(5):
            if i < N:
                balls[i].pos = vec(-4 * size + 2 * size * i, -L, 0) + vec(-sqrt(L * L - (L - h) * (L - h)), h, 0)
            else:
                balls[i].pos = vec(-4 * size + 2 * size * i, -L, 0)
            balls[i].v = vec(0, 0, 0)
        t, Ks, Us = 0, 0, 0
        kinetic_i.delete()
        kinetic_a.delete()
        potential_a.delete()
        potential_i.delete()
        reset = 0
