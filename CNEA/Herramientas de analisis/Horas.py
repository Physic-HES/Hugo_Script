import datetime
import numpy as np

class horario:
    def __init__(self):
        self.acum=datetime.timedelta(days=0,hours=0,minutes=0)
        self.fichados=0
        self.resto=0
        self.hoy=datetime.datetime.now()
        self.tabla=[]

    def fichado(self,d,E,S):
        Ent=datetime.datetime.replace(self.hoy,day=d,hour=E[0],minute=E[1])
        self.fichados += 1
        if len(S)>1:
            Sal=datetime.datetime.replace(self.hoy,day=d,hour=S[0],minute=S[1])
            self.acum+=Sal-Ent
            self.rest()
            self.tabla.append([Ent,Sal])
        else:
            self.acum += self.hoy - Ent
            self.rest()
            self.tabla.append([Ent, self.hoy])
            salida = self.hoy - datetime.timedelta(seconds=self.resto)
            if self.resto<0:
                print(f'Deberias salir a las {salida.hour}:{salida.minute} hs')
            else:
                print(f'Deberias haber salido a las {salida.hour}:{salida.minute} hs')

    def rest(self):
        self.resto = self.acum.seconds - datetime.timedelta(hours=self.fichados * 8).seconds
        if self.resto>0:
            print(f'Tenes a favor {int(self.resto/60/60):02.0f} hs y '
                  f'{(self.resto/60/60-int(self.resto/60/60))*60:02.0f} min')
        if self.resto<0:
            print(f'Te faltan {np.abs(int(self.resto/60/60)):02.0f} hs y '
                  f'{np.abs((self.resto/60/60-int(self.resto/60/60))*60):02.0f} min')

    def faltan(self):
        self.acum += datetime.datetime.now()-self.hoy
        self.hoy=datetime.datetime.now()
        self.rest()