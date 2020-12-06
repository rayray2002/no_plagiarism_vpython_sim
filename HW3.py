from vpython import *
import math

G = 6.673E-11
mass = {'earth': 5.97E24, 'moon': 7.36E22, 'sun': 1.99E30}
radius = {'earth': 6.371E6 * 10, 'moon': 1.317E6 * 10, 'sun': 6.95E8 * 10}  # 10 times larger for better view
earth_orbit = {'r': 1.495E11, 'v': 2.9783E4}
moon_orbit = {'r': 3.84E8, 'v': 1.022E3}
theta = 5.145 * pi / 180.0


def G_force(m1, m2, pos_vec):
    return -G * m1 * m2 / mag2(pos_vec) * norm(pos_vec)


scene = canvas(width=800, height=800, align='left', background=color.black)
scene.lights = []
# scene.forward = vector(0, -1, 0)

# plot = graph(width = 600, height = 380, align = 'right', title = "theta", xtitle = "t(s)", ytitle = "theta")
# theta_g = gcurve(graph = plot, color = color.blue, width = 2)

sun = sphere(pos=vec(0, 0, 0), radius=radius['sun'], m=mass['sun'], color=color.yellow)
local_light(pos=vector(0, 0, 0))

earth_ri = -moon_orbit['r'] * mass['moon'] / (mass['earth'] + mass['moon'])
earth = sphere(pos=vec(earth_ri * cos(theta) + earth_orbit['r'], earth_ri * sin(theta), 0), radius=radius['earth'],
               m=mass['earth'], texture={'file': textures.earth})
earth.v = vec(0, 0, moon_orbit['v'] * mass['moon'] / (mass['earth'] + mass['moon']) - earth_orbit['v'])

moon_ri = moon_orbit['r'] * mass['earth'] / (mass['earth'] + mass['moon'])
moon = sphere(pos=vec(moon_ri * cos(theta) + earth_orbit['r'], moon_ri * sin(theta), 0), radius=radius['moon'],
              m=mass['moon'])
moon.v = vec(0, 0, -moon_orbit['v'] * mass['earth'] / (mass['earth'] + mass['moon']) - earth_orbit['v'])

stars = [earth, moon]
dt = 60 * 60 * 6
t = 0
T = 0
speed = 1  # year/s

while True:
    rate(4*365)
    scene.center = earth.pos

    moon.a = (G_force(moon.m, earth.m, moon.pos - earth.pos) + G_force(moon.m, sun.m, moon.pos - sun.pos)) / moon.m
    earth.a = (G_force(moon.m, earth.m, earth.pos - moon.pos) + G_force(earth.m, sun.m, earth.pos - sun.pos)) / earth.m
    norm_x = norm(cross(cross(norm(moon.v - earth.v), norm(moon.pos - earth.pos)), vec(0, 1, 0))).z

    if math.isclose(1, norm_x) and T == 0 and t > 86400:
        T = t / (86400 * 365)
        print('period of the precession = ' + str(T) + ' years')

    for star in stars:
        star.v += star.a * dt
        star.pos += star.v * dt
    # theta_g.plot(pos=(t,norm_x))
    t += dt
