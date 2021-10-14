from vpython import *

scene = canvas(pos=vector(0, 2, 0))  # crea otra escena
s = '''Arrastre el boton derecho para rotar la camara y ver 3D.
       Use la ruedita para acercar y alejar la imagen.
       En el celu(tablet) puede hacerlo con los dedos.'''
scene.caption = s

scene.append_to_caption('  ')

# Widgets
running = False  # variable running se asigna como falsa  (no ejecutara el lazo inicialmente)


def Play(
        b):  # define la funcion  Play ligada al boton play_button abajo, que modifica running (para o ejecuta alternadamente, poniendo el texto correspondiente)
    global running
    running = not running
    if running:
        b.text = "Pausar"
    else:
        b.text = "Iniciar"


play_button = button(bind=Play,
                     text='Iniciar')  # enlace al boton play_button la función Play  (muestra el boton y ejecuta Play cada vez que se lo apriete, con lo que running cambia
scene.append_to_caption('  ')  # deja linea en blanco

# Constantes fisicas del sistema:
m = 1  ##  no depende de este valor
g = 9.8  # aceleracion de la gravedad
tita = pi / 6

# Condiciones iniciales
r = 2
r_dot = 0.
phi = 0.
phi_dot = sqrt(5 * sqrt(3) * g / r)
Lz = m * r ** 2 * sin(tita) ** 2 * phi_dot

# lz=m1*rho0*v0

#  Creamos el sistema
cone(color=color.white, pos=vec(0, 0, 4), radius=4 * tan(tita), axis=vec(0, 0, -4),
     opacity=0.1)  ### cono, instancia de la clase cone
bola1 = sphere(color=color.red, pos=vector(r * sin(tita) * cos(phi), r * sin(tita) * sin(phi), r * cos(tita)),
               radius=0.2, make_trail=True)  ### masa m1, instancia de la clase sphere

#    Creamos las figuras
gT = gcurve(color=color.green,
            label="Cinética")  ## genera una obheto grafico  gcurve con ciertas propiedades de color y etiqueta  llamado gT
gV = gcurve(color=color.blue, label="Potencial")
gE = gcurve(color=color.red, label="Energia=T+V")
gLz = gcurve(color=color.yellow, label="Momento Angular Lz")
gr = gcurve(color=color.black, label="r")

#  Inicialización del bucle (lazo)
t = 0  ### Asigna a la variable t el valor 0.
dt = 0.001  ### Asigna a la variable dt el valor 0.01
while True:  # Lazo de iteración sin salida ( Mientras Verdadero haga:), notar los : y el indentado)
    rate(5000)  # Controla la taza de muestreo, normalmente hacer que dt*rate sea del orden de la unidad

    if running:
        r_dotdot = r * sin(tita) ** 2 * phi_dot ** 2 - g * cos(tita)
        r_dot += r_dotdot * dt
        r += r_dot * dt
        phi_dot = Lz / (m * r ** 2 * sin(tita) ** 2)
        phi += phi_dot * dt

        bola1.pos = vec(r * sin(tita) * cos(phi), r * sin(tita) * sin(phi),
                        r * cos(tita))  ## modifica la posicion de la bola 1

        # Calculo de magnitudes fisicas (verificar conservaciones)
        T = 1 / 2 * m * (r_dot ** 2 + (r * sin(tita) * phi_dot) ** 2)
        V = m * g * r * cos(tita)
        E = T + V
        Lz = m * r ** 2 * sin(tita) ** 2 * phi_dot

        #    Ploteamos puntos en las figuras
        gT.plot(pos=(t, T))
        gV.plot(pos=(t, V))
        gE.plot(pos=(t, E))
        gLz.plot(pos=(t, Lz))
        gr.plot(pos=(t, r))

        t += dt  ## asignacion del nuevo tiempo t=t+dt