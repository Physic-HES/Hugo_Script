## EJERCICIO 4
## HUGO SOSA
## LU 205/07.

import numpy as np
import matplotlib.pyplot as plt


def V_prima(coefs, V):
    S_prima = -coefs[0] / coefs[2] * V[0] * V[1]
    I_prima = coefs[0] / coefs[2] * V[0] * V[1] - coefs[1] * V[1]
    R_prima = coefs[1] * V[1]
    return np.array([S_prima, I_prima, R_prima])


def paso_runge_kutta(coefs, V, dt, t):
    k1 = V_prima(coefs, V)
    k2 = V_prima(coefs, V+dt/2*k1)
    k3 = V_prima(coefs, V+dt/2*k2)
    k4 = V_prima(coefs, V+dt*k3)
    V = V + dt/6 * (k1 + 2 * k2 + 2 * k3 + k4)
    t = t + dt
    return [t, V]


def integra_runge_kutta(coefs, V0, t0, T, dt):
    t = [t0]
    V = [V0]
    while t[-1] < T:
        t_, V_ = paso_runge_kutta(coefs, V[-1], dt, t[-1])
        t.append(t_)
        V.append(V_)
    return [t, V]


def despliega_integracion(integracion):
    t = integracion[0]
    V = integracion[1]
    S = []
    I = []
    R = []
    for i in range(len(V)):
        S.append(V[i][0])
        I.append(V[i][1])
        R.append(V[i][2])
    return [np.array(t), np.array(S), np.array(I), np.array(R)]


graf = 1
betas = [1.3, 1.1, 0.9, 0.5]

# Aca baje un orden el numero inicial de infectados,
# y acorte tambien en un orden el tiempo final de la simulacion,
# simplemente para que se puedan ver los cambios
# cuando beta/gamma pasa de meyor a menor que 1

for j in np.arange(0, len(betas), 1):
    beta = betas[j]
    gamma = 1
    N = 10**4
    S0 = N*0.99
    I0 = N*0.001
    R0 = 0
    V0 = [S0, I0, R0]
    coefs = [beta, gamma, N]
    t0 = 0
    T = 100
    dt = 0.15
    Result_SIR = integra_runge_kutta(coefs, V0, t0, T, dt)
    [t, S, I, R] = despliega_integracion(Result_SIR)
    plt.figure(graf, figsize=(10, 5))
    plt.subplot(121)
    plt.plot(t, S, label='S - Suceptibles')
    plt.plot(t, I, label='I - Infectados')
    plt.plot(t, R, label='R - Recuperados')
    plt.plot(t, S+I+R, label='S+I+R - Poblacion')
    plt.grid()
    plt.legend()
    plt.xlabel('Dias')
    plt.ylabel('Cantidad de Personas')
    plt.subplot(222)
    plt.plot(t, I+R, label=r'Casos confirmados: $I+R$')
    plt.grid()
    plt.legend()
    plt.ylabel('Cantidad de personas')
    plt.subplot(224)
    plt.plot(t[1:], np.diff(I+R), label=r'Casos/dia: $-\frac{dS}{dt}$')
    plt.grid()
    plt.legend()
    plt.xlabel('Dias')
    plt.ylabel('Cantidad de personas')
    plt.suptitle(r'Simulacion SIR con $\beta=%g$, $\gamma=%g$ y $\frac{\beta}{\gamma}=%g$' % (beta, gamma, beta / gamma))
    plt.savefig(r'graf%g_Ej4.png' % graf)
    graf = graf + 1


# Si beta/gamma es menor a 1 no se produce el pico de de contagio,
# es decir la tasa de infectados disminuye continuamente
# En cambio, si beta/gamma es mayor que uno, no solo se produce el pico de infectados,
# si no que este se da en un tiempo mas corto a medida que crezca beta/gamma


def V_prima2(coefs, V):
    S_prima = -coefs[0] / coefs[2] * V[0] * V[1] + coefs[3] * V[2]
    I_prima = coefs[0] / coefs[2] * V[0] * V[1] - coefs[1] * V[1]
    R_prima = coefs[1] * V[1] - coefs[3] * V[2]
    return np.array([S_prima, I_prima, R_prima])


def paso_runge_kutta2(coefs, V, dt, t):
    k1 = V_prima2(coefs, V)
    k2 = V_prima2(coefs, V+dt/2*k1)
    k3 = V_prima2(coefs, V+dt/2*k2)
    k4 = V_prima2(coefs, V+dt*k3)
    V = V + dt/6 * (k1 + 2 * k2 + 2 * k3 + k4)
    t = t + dt
    return [t, V]


def integra_runge_kutta2(coefs, V0, t0, T, dt):
    t = [t0]
    V = [V0]
    while t[-1] < T:
        t_, V_ = paso_runge_kutta2(coefs, V[-1], dt, t[-1])
        t.append(t_)
        V.append(V_)
    return [t, V]


beta = 1.3
gamma = 1
alpha = 1.2
N = 10**4
S0 = N*0.99
I0 = N*0.001
R0 = 0
V0 = [S0, I0, R0]
coefs = [beta, gamma, N, alpha]
t0 = 0
T = 100
dt = 0.15
Result_SIR = integra_runge_kutta2(coefs, V0, t0, T, dt)
[t, S, I, R] = despliega_integracion(Result_SIR)
plt.figure(5, figsize=(10, 5))
plt.subplot(121)
plt.plot(t, S, label='S - Suceptibles')
plt.plot(t, I, label='I - Infectados')
plt.plot(t, R, label='R - Recuperados')
plt.plot(t, S+I+R, label='S+I+R - Poblacion')
plt.grid()
plt.legend()
plt.xlabel('Dias')
plt.ylabel('Cantidad de Personas')
plt.subplot(222)
plt.plot(t, I+R, label=r'Casos confirmados: $I+R$')
plt.grid()
plt.legend()
plt.ylabel('Cantidad de Personas')
plt.subplot(224)
plt.plot(t[1:], np.diff(I+R), label=r'Casos/dia: $-\frac{dS}{dt}$')
plt.grid()
plt.legend()
plt.xlabel('Dias')
plt.ylabel('Cantidad de Personas')
plt.suptitle(r'Simulacion sin inmunizacion SIR-R con $\beta=%g$, $\gamma=%g$, $\alpha=%g$ y $\frac{\beta}{\gamma}=%g$' % (beta, gamma, alpha, beta / gamma))
plt.savefig('graf5_Ej4.png')
plt.show()

# Al agregar esta modificacion, lo que se pierde es la inmunidad que adquirian los recuperados,
# haciendo que los infectados nunca dejen de serlo
