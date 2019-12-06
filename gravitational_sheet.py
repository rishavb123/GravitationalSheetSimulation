# -*- coding: utf-8 -*-
"""Gravitational Sheet.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Q0fvJ2AWxfRszkvOnvfw08g9vcDyAVcF

## Gravitional Pull of a Uniform Sheet
A uniform rectangular sheet of length $L$ and width $W$ is floating motionless in space.
![](sheet.png)
The sheet has negligible thickness and has a mass $M$. Consider a point mass a distance $z$ from the center of the sheet with mass $m$.

The gravitional force on the mass in the $x$ and $y$ directions will cancel out since there is the same amount of mass on both sides. The only component that matters is the one along the $z$-axis. So,
$$F_z = \int dF_z = Gm\int \frac{dM}{r^2}\cos\theta$$
$$= Gm\int\frac{\sigma dA}{r^2}\frac{z}{r} = Gm\sigma z\int_{-W/2}^{W/2}\int_{-L/2}^{L/2} \frac{1}{(x^2 + y^2 + z^2)^{3/2}} dx\;dy$$
and $\vec{F} = F_z \hat{k}$ since there is only a $z$ component. So,
$$\vec{F} = \big(Gm\sigma z\int_{-W/2}^{W/2}\int_{-L/2}^{L/2} \frac{1}{(x^2 + y^2 + z^2)^{3/2}} dx\;dy\big)\hat{k}$$

Now, to calculate this.
"""

# imports
import numpy as np
import pylab

# define constants

G = 6.674e-11 # m^3kg^-1s^-2

def f(x, y, z):
    return 1/(x**2 + y**2 + z**2) ** 1.5

# define parameters

L = 10 # m
W = 10 # m
z = 10 # m
M = 10000 # kg
A = L * W # m^2
sigma = M / A # kg / m^2
ax = -L / 2 # m
bx = L / 2 # m
ay = -W / 2 # m
by = W / 2 # m

#define some functions

def simpsons(f, a, b, N=10):
    h = (b - a) / N
    return 1/3 * h * (f(a) + f(b) + 4 * sum([f(a + (2*k - 1) * h) for k in range(1, int(N/2) + 1)]) + 2 * sum([f(a + 2 * k * h) for k in range(1, int(N/2))]))

def double_simpsons(f, a, b, c, d, N = 10):
    def F(y):
        return simpsons(lambda x: f(x, y), a, b, N)
    return simpsons(F, c, d, N)

def force(z):
    return double_simpsons(lambda x, y: f(x, y, z), ax, bx, ay, by, N=100)

print(force(z))

xs = np.linspace(0.1, 10, 100)
ys = [force(x_s) for x_s in xs]
pylab.plot(xs, ys)
pylab.show()