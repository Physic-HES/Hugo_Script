import cv2
import numpy as np
import matplotlib.pyplot as plt

# Inicializar la captura de video desde la cámara
cap = cv2.VideoCapture(0)

# Leer el primer frame
ret, frame1 = cap.read()

# Función para calcular y dibujar flechas sobre los objetos en movimiento
def draw_arrows(frame, arrows):
    for arrow in arrows:
        cv2.arrowedLine(frame, arrow[0], arrow[1], (0, 255, 0), 2)

# Bucle principal
while True:
    # Leer el siguiente frame
    ret, frame2 = cap.read()

    # Convertir los frames a escala de grises
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Calcular la diferencia entre los dos frames
    diff = cv2.absdiff(gray1, gray2)

    # Aplicar un umbral para resaltar las áreas con cambios significativos
    _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)

    # Encontrar contornos de las áreas con cambios
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Inicializar lista para almacenar las flechas
    arrows = []

    # Iterar sobre los contornos y calcular la dirección del movimiento
    for contour in contours:
        if cv2.contourArea(contour) > 10:
            x, y, w, h = cv2.boundingRect(contour)
            center_x = x + w // 2
            center_y = y + h // 2

            # Dibujar un rectángulo alrededor del objeto en movimiento
            #cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Calcular la dirección del movimiento
            _,_,_,desp=cv2.minMaxLoc(cv2.matchTemplate(gray2,gray1[y:y+h,x:x+h],cv2.TM_CCOEFF_NORMED))
            # Calcular el vector de desplazamiento entre frames consecutivos
            displacement_vector = ( desp[0]-x, desp[1]-y)
            norm=np.linalg.norm(displacement_vector)
            print(displacement_vector)
            if norm<10:
                arrow_end = (center_x + 4*displacement_vector[0],
                             center_y + 4*displacement_vector[1])
                arrows.append(((center_x,center_y), arrow_end))

    # Dibujar las flechas sobre el frame
    draw_arrows(frame2, arrows)

    # Mostrar el frame resultante
    cv2.imshow('Motion Detection', frame2)

    # Actualizar el frame anterior
    frame1 = frame2

    # Salir del bucle al presionar la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos
cap.release()
cv2.destroyAllWindows()

