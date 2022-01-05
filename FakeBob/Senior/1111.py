import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from scipy.stats import uniform
import seaborn
seaborn.set()

n = 1000000
r = 1.0
o_x, o_y = (0., 0.)


uniform_x = uniform(o_x-r,2*r).rvs(n)
uniform_y = uniform(o_y-r,2*r).rvs(n)

d_array = np.sqrt((uniform_x - o_x) ** 2 + (uniform_y - o_y) ** 2)
res = sum(np.where(d_array < r, 1, 0))
pi = (res / n) /(r**2) * (2*r)**2

fig, ax = plt.subplots(1, 1)
ax.plot(uniform_x, uniform_y, 'ro', markersize=0.3)
plt.axis('equal')
circle = Circle(xy=(o_x, o_y),radius=r, alpha=0.5)

ax.add_patch(circle)

print('pi={}'.format(pi))
plt.show()