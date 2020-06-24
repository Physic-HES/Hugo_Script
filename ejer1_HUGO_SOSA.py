## EJERCICIO 1
## HUGO SOSA
## LU 205/07.

# La ecuación de la recta es y=m*x+b
# m la obtenemos como la vaciacion en y sobre la variacion en x
# mientras que b se obtiene evaluando en el punto (x1,y1) y despejando b
y1 = 10
y2 = 100
x1 = 10
x2 = 25
m = (y2-y1)/(x2-x1)
b = y1-m*x1
print('')
print('Cuando la recta es y=m*x+b')
print('El valor de m es',m)
print('El valor de b es',b)
# La ecuación de la recta es y=b*e^(m*x)
# esa ecuacion es una recta si la coordenada Y esta medida en escala logaritmica
# es decir: log(y)=(log(b*e^(mx))=log(b)+log(e^(m*x))=m*x+log(b)
# por lo que evaluando para y1 e y2 podemos obtener m = log(y2/y1)/(x2-x1)
# y evaluando en el punto (x1,y1) obtenemos b = y1/(e^(m*x1))
import numpy as np
y1 = 10
y2 = 100
x1 = 10
x2 = 25
m = np.log(y2/y1)/(x2-x1)
b = y1/np.exp(m*x1)
print('')
print('Cuando la recta es y=b*e^(m*x)')
print('El valor de m es',m)
print('El valor de b es',b)