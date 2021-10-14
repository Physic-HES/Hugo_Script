from vpython import *

# Giroscopo Pasco, o en su ausencia

# Usar laes ecuaciones de Lagrange
# Use los ángulos de Euler theta   (eje 3 con z) ,
#  asimutal  phi, y de spin psi (rotacion alrededor del eje 3).

scene.width = 800
scene.height = 600
scene.range = 1.2
scene.title = "Giróscopo: libre (balance gravitatorio) o con precesión y nutación por desbalance gravitatorio"

# Datos de la escena y del sistema fisico:

Leje = 2  # Longitud del Giroscopo
Reje = 0.01  # radio del eje del Giroscopo
M1 = 0.2  # masa del Disco 1 del Giroscopo (eje sin masa)
M2 = 1  # masa del Disco 2 del Giroscopo balanceado
m = 0.3  # masa extra para desbalance gravitatorio
d = Leje / 2  # m se pone a Leje/2 del centro, del lado en que está M1
r = d * m / (M1 + M2 + m)  # distancia del soporte al centro de masa,
Rdisco2 = 0.4  # radio del Disco 2 del Giroscopo
Ddisco2 = 0.05  # espesor del Disco 2 del Girosco
Rdisco1 = 0.2  # radio del Disco 1 del Giroscopo
Ddisco1 = 0.1  # espesor del Disco 1 del Girosco
I3 = M1 / 2 * Rdisco1 ** 2 + M2 / 2 * Rdisco2 ** 2  # Momento de inercia del Giroscopo con respecto al eje de simetria LLENAR con las vbariables apropiadas!!
I1 = M1 * (1 / 4 * Rdisco1 ** 2 + 1 / 12 * Ddisco1 ** 2 + (Leje / 2) ** 2) + M2 * (
            1 / 4 * Rdisco2 ** 2 + 1 / 12 * Ddisco2 ** 2 + (
                Leje / 4) ** 2) + m * d ** 2  # Momento de inercia del Giroscopo con respecto al eje perpendicular al de simetria  LLENAR con las variables apropiadas!!
hpedestal = Leje / 2  # altura del pedestal
wpedestal = 0.02  # ancho del pedestal
tbase = 0.05  # espesor del la  base
wbase = 30 * wpedestal  # ancho de la base
g = 9.8  # aceleracion de la gravedad
# Fgrav = vector(0,-M*g,0)

#  Se crean los elementos del sistema

top = vector(0, 0, 0)  # tope del pedestal
eje = cylinder(pos=vector(-Leje / 2, 0, 0), axis=vector(Leje, 0, 0), radius=Reje, color=color.orange)
disco1 = cylinder(pos=vector(Leje / 4, 0, 0), axis=vector(Ddisco1, 0, 0),  #
                  radius=Rdisco1, color=color.gray(0.9))
disco2 = cylinder(pos=vector(-Leje / 2, 0, 0), axis=vector(Ddisco2, 0, 0),  #
                  radius=Rdisco2, color=color.gray(0.9))
base = sphere(color=eje.color, radius=1.5 * Reje)
if m > 0:
    end = sphere(pos=vector(Leje / 2, 0, 0), color=disco1.color, radius=3 * Reje)
else:
    end = sphere(pos=vector(Leje / 2, 0, 0), color=eje.color, radius=Reje)

gyro = compound([eje, disco1, disco2, end])  # ensambla en un solo objeto llamado giroscopo

gyro_center = gyro.pos
gyro.texture = textures.metal  # textura del Giroscopo
tip = sphere(pos=0.5 * eje.axis, radius=eje.radius / 2, make_trail=True,
             retain=1500)  # genera la trayectoria de la punta del Giroscopo
tip.trail_color = color.green
tip.trail_radius = 0.15 * Reje

pedestal = box(pos=top - vector(0, hpedestal / 2 + eje.radius / 2, 0),
               height=hpedestal - eje.radius, length=wpedestal, width=wpedestal, texture=textures.wood)
pedestal_base = box(pos=top - vector(0, hpedestal + tbase / 2, 0),
                    height=tbase, length=wbase, width=wbase, texture=textures.wood)
# Graficos
gL3 = gcurve(color=color.green, label="Momento L3")
gE = gcurve(color=color.red, label="Energia")
gLz = gcurve(color=color.blue, label="Momento Lz")
gL2 = gcurve(color=color.orange, label="Momento L2")
gL1 = gcurve(color=color.yellow, label="Momento L1")

#  Algunas condiciones iniciales (se usan las definidas en la funcion reset()

theta = 0
theta_dot = 0
psi = 0
psi_dot = 0
phi = 0
phi_dot = 0
pureprecession = False


def reset():
    global theta, theta_dot, psi, psi_dot, phi, phi_dot
    theta = 0.4 * pi  # angulo polar inicial del eje con la vertical ( 0.3*pi )
    theta_dot = 0  # initial rate of change of polar angle
    psi = 0  # initial spin angle
    psi_dot = 25  # initial rate of change of spin angle (spin ang. velocity)
    phi = pi / 2  # initial azimuthal angle
    phi_dot = 1 / 2 / pi * sqrt(m * g * Leje / 2 / I3)  # initial rate of change of azimuthal angle
    if pureprecession:  # Set to True if you want pure precession, without nutation    # LEVANTAR COMENTARIOS Y LLENAR
        a = sin(theta) * cos(theta) * (I1 - I3)
        b = -2 * psi_dot * sin(theta) * I3
        c = m * g * d * sin(theta)
        phi_dot = (-b + sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    gyro.axis = gyro.length * vector(sin(theta) * sin(phi), cos(theta), sin(theta) * cos(phi))
    A = norm(gyro.axis)
    gyro.pos = 0 * Leje * A  # 0.5*
    tip.pos = 0.5 * Leje * A
    tip.clear_trail()


reset()
scene.waitfor('textures')

dt = 0.00001
t = 0
Nsteps = 20  # numero de pasos nates de actualizar el grafico

while True:
    rate(2000)
    for step in range(Nsteps):  # se usan calculos multiples para exactitud
        # Calcula las aceleraciones usando el Lagrangiano en funcion de los angulos de Euler
        theta_dotdot = sin(theta) * cos(theta) * phi_dot ** 2 * (I1 - I3) / I1 - I3 / I1 * psi_dot * phi_dot * sin(
            theta) + m * g * Leje / 2 / I1 * sin(theta)  # LLENAR!
        phi_dotdot = I3 / I1 * psi_dot * theta_dot / sin(theta) - (2 * I1 - I3) / I1 * theta_dot * phi_dot / tan(
            theta)  # LLENAR!
        psi_dotdot = theta_dot * phi_dot * sin(theta) - I3 / I1 * psi_dot * theta_dot / tan(theta) + (
                    2 * I1 - I3) / I1 * theta_dot * phi_dot / tan(theta) * cos(theta)  # LLENAR!
        # Actualiza las velocidades de los angulos de Euler:
        theta_dot += theta_dotdot * dt
        phi_dot += phi_dotdot * dt
        psi_dot += psi_dotdot * dt
        # Actualiza los angulos de Euler:
        theta += theta_dot * dt
        phi += phi_dot * dt
        psi += psi_dot * dt
        # Graficos:
        V = -d * m * g * cos(theta)
        T = I1 / 2 * (theta_dot ** 2 + sin(theta) ** 2 * phi_dot ** 2) + (
                    cos(theta) ** 2 * phi_dot ** 2 + psi_dot * phi_dot * 2 * cos(theta)) * I3 / 2
        L3 = (phi_dot * cos(theta) + psi_dot) * I3
        L2 = (sin(theta) * cos(psi) * phi_dot - theta_dot * sin(phi)) * I1
        L1 = (phi_dot * sin(theta) * sin(psi) + theta_dot * cos(psi)) * I1
        Lz = (I1 * phi_dot * sin(theta) ** 2 + cos(theta) * L3)
        gL3.plot(pos=(t, L3))
        gE.plot(pos=(t, T + V))
        gLz.plot(pos=(t, Lz))
        gL2.plot(pos=(t, L2))
        gL1.plot(pos=(t, L1))

    gyro.axis = gyro.length * vector(sin(theta) * sin(phi), cos(theta), sin(theta) * cos(phi))
    # Display approximate rotation of rotor and shaft:
    gyro.rotate(angle=psi_dot * dt * Nsteps)
    A = norm(gyro.axis)
    gyro.pos = 0 * Leje * A
    tip.pos = 0.5 * Leje * A
    t = t + dt * Nsteps

