from vpython import *

g = 9.8  # g = 9.8 m/s^2
size = 0.25  # ball radius = 0.25 m
height = 15.0  # ball center initial height = 15 m
C_drag = 0.9
theta = pi / 4
count = 0

scene = canvas(width=600, height=600, center=vec(0, height / 2, 0), background=color.yellow, align='left')
floor = box(length=30, height=0.01, width=10, color=color.black)

ball = sphere(radius=size, color=color.red, make_trail=True)
ball.pos = vec(-15, size, 0)
ball.v = vec(20 * cos(theta), 20 * sin(theta), 0)  # ball initial velocity

v_arrow = arrow(color=color.green, shaftwidth=0.2)

plot = graph(width=600, align='left', title="v_t", xtitle="t(s)", ytitle="v(m/s)")
v_t = gcurve(graph=plot, color=color.blue, width=4)
# h = gcurve(graph = plot, color=color.red, width=4)

t = 0
distance = 0
max_h = 0

dt = 0.001  # time step
while count < 3:  # until the ball hit the ground
    rate(1000)  # run 1000 times per real second

    v_arrow.pos = ball.pos
    v_arrow.axis = ball.v * 0.5

    v_t.plot(pos=(t, ball.v.mag))
    # h.plot(pos = (t, ball.pos.y))

    ball.v += vec(0, -g, 0) * dt - C_drag * ball.v * dt
    ball.pos += ball.v * dt
    t += dt
    distance += (ball.v * dt).mag

    if ball.pos.y <= size and ball.v.y < 0:  # new: check if ball hits the ground
        ball.v.y = - ball.v.y  # if so, reverse y component of velocity
        count += 1

    if ball.pos.y > max_h:
        max_h = ball.pos.y

displacement_msg = text(text='Displacement = ' + str((ball.pos - vec(-15, size, 0)).mag), pos=vec(-10, 15, 0),
                        color=color.black)
total_distance_msg = text(text='Total Distance = ' + str(distance), pos=vec(-10, 13, 0), color=color.black)
largest_height_msg = text(text='The Largest Height = ' + str(max_h), pos=vec(-10, 11, 0), color=color.black)
