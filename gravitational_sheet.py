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
from config import *
import pygame
import time

pygame.init()

A = L * W # m^2
sigma = M / A # kg / m^2
ax = -L / 2 # m
bx = L / 2 # m
ay = -W / 2 # m
by = W / 2 # m

surface = pygame.display.set_mode((width, height))

def f(x, y, z):
    return 1/(x**2 + y**2 + z**2) ** 1.5

#define some functions

def simpsons(f, a, b, N=10):
    h = (b - a) / N
    return 1/3 * h * (f(a) + f(b) + 4 * sum([f(a + (2*k - 1) * h) for k in range(1, int(N/2) + 1)]) + 2 * sum([f(a + 2 * k * h) for k in range(1, int(N/2))]))

def double_simpsons(f, a, b, c, d, N = 10):
    def F(y):
        return simpsons(lambda x: f(x, y), a, b, N)
    return simpsons(F, c, d, N)

def force(z):
    return G * m * sigma * z * double_simpsons(lambda x, y: f(x, y, z), ax, bx, ay, by, N=100)

def transform(z, w):
    return (width / 2 - w / 2, -z/15 * height + 2 * height / 3)

def detransform(x, y):
    return (15/height * (height/3 - y), width - 2 * x)

# print(force(z))

# xs = np.linspace(0.1, 10, 100)
# ys = [force(x_s) for x_s in xs]
# pylab.plot(xs, ys)
# pylab.show()

class Sheet:

    def __init__(self, z):
        self.w = 400
        self.z = z
        self.v = 0
        self.m = M
        self.h = 25

    def update(self, F, total_dt):
        n = 10
        for _ in range(n):
            dt = total_dt / n
            self.v += F / self.m * dt
            self.z += self.v * dt
        
    def draw(self):
        x, y = transform(self.z, self.w)
        pygame.draw.rect(surface, (0, 0, 255), [int(x), int(y), int(self.w), int(self.h)])

class Ball:

    def __init__(self, z):
        self.w = 50
        self.z = z
        self.v = -5
        self.m = m
        self.h = 50

    def update(self, F, total_dt, sheet):
        n = 10
        for _ in range(n):
            dt = total_dt / 10
            x, y = transform(self.z, self.w)
            sheet_x, sheet_y = transform(sheet.z, sheet.w)
            self.v += F / self.m * dt
            if y + self.h > sheet_y:
                self.z = sheet.z + detransform(0, self.h)[0]
                self.v = abs(self.v)
            self.z += self.v * dt
        
        self.v = self.v * min(abs(self.v), 3) / abs(self.v)

    def draw(self):
        x, y = transform(self.z, self.w)
        pygame.draw.circle(surface, (255, 0, 0), [int(x + self.w/2), int(y + self.h/2)], int(self.w/2))

sheet = Sheet(0)
ball = Ball(z)

current_time = time.time()

while True:
    for event in pygame.event.get():   
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()  

    surface.fill((255, 255, 255))

    next_time = time.time()

    dt = next_time - current_time
    F = force(ball.z - sheet.z)

    # F = F / abs(F)

    print(-F, ball.v, ball.z)

    sheet.update(F, dt)
    ball.update(-F, dt, sheet)
    sheet.draw()
    ball.draw()

    current_time = next_time

    pygame.display.update()