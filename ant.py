from vpython import *
import numpy

L = 30
u = 1
v = 5

scene = canvas(width=600, height=600, center=vec(-0.5*L,0,0), background=color.yellow, align = 'left')
rod = cylinder(pos=vector(0, 0, 0), axis=vector(-1 * L,0,0), radius=0.5)
wall = box(width=15, height=15, length=0.2, pos=vector(0,0,0), color=color.purple)
  
ant = sphere(radius = 0.3, color=color.black, pos = vec(L*-1, 0.7, 0))
ant.v = vec(u, 0, 0)

dt = 0.0001
t = 0
while (ant.pos.x < 0):
    rate(50000)
    ant.pos += ant.v*dt
    rod.axis -= vector(v, 0 ,0)*dt
    ant.pos -= vector(v, 0 ,0)*dt*(-1*ant.pos.x/(L+v*t))
    t += dt
    
# T = (L/v)*log(u/(u-v))
T2 = (L/v)*(exp(v/u)-1)
print(t, T2, (t-T2)/t*100)
msg = text(text = "error% = " + str((t-T2)/t*100), color=color.black, pos=vec(rod.axis.x*0.5,10,0), height=3)