import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

T = [0, 1]
N = 10 ** 3
h = (T[1] - T[0]) / N
Y1 = [1]
t = np.arange(T[0], T[1] + h, h)
for j in np.arange(0, N):
    Y1.append(
        Y1[j] + h * (np.sin(Y1[j]) + t[j] ** 2 + h / 2 * (2 * t[j] + np.cos(Y1[j]) * (np.sin(Y1[j]) + t[j] ** 2))))

print([len(t), len(Y1)])
print(5 / 3 * h ** 2)
plt.plot(t, Y1)


def f(t1, y1):
    return np.sin(y1) + t1 ** 2


sol = solve_ivp(f, [0, 1], [1], t_eval=t)

print(sol.t)
print(sol.y[0])

print(np.array(sol.y[0])-np.array(Y1))

plt.plot(sol.t, sol.y[0])
plt.show()
