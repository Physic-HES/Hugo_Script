import datetime
import numpy as np
import pandas as pd

class horario:
    def __init__(self):
        self.acum=datetime.timedelta(days=0,hours=0,minutes=0)
        self.fichados=0
        self.resto=0
        self.hoy=datetime.datetime.now()
        self.tabla=pd.DataFrame({'Dia':[],'Entrada':[],'Salida':[],'Saldo':[],'Resto':[]})
        self.dias=[]

    def fichado(self,d,E,S):
        self.dias.append(d)
        Ent=datetime.datetime.replace(self.hoy,day=d,hour=E[0],minute=E[1])
        self.fichados += 1
        if len(S)>1:
            Sal=datetime.datetime.replace(self.hoy,day=d,hour=S[0],minute=S[1])
            self.acum+=Sal-Ent
            self.rest()
            if self.resto<0:
                row=pd.DataFrame({'Dia': [f'{d:02.0f}'],
                                   'Entrada': [f'{E[0]:02.0f}:{E[1]:02.0f}'],
                                   'Salida': [f'{S[0]:02.0f}:{S[1]:02.0f}'],
                                   'Saldo': ['-'],
                                   'Resto': [f'{np.abs(int(self.resto / 60 / 60)):02.0f}:{np.abs((self.resto / 60 / 60 - int(self.resto / 60 / 60)) * 60):02.0f}']})
                self.tabla=pd.concat([self.tabla,row], ignore_index=True)
            else:
                row=pd.DataFrame({'Dia': [f'{d:02.0f}'],
                                   'Entrada': [f'{E[0]:02.0f}:{E[1]:02.0f}'],
                                   'Salida': [f'{S[0]:02.0f}:{S[1]:02.0f}'],
                                   'Saldo': ['+'],
                                   'Resto': [f'{int(self.resto / 60 / 60):02.0f}:{(self.resto / 60 / 60 - int(self.resto / 60 / 60)) * 60:02.0f}']})
                self.tabla=pd.concat([self.tabla,row], ignore_index=True)
        else:
            self.acum += self.hoy - Ent
            self.rest()
            salida = self.hoy - datetime.timedelta(seconds=self.resto)
            if self.resto<0:
                print(f'----->  Deberías salir a las {salida.hour:02.0f}:{salida.minute:02.0f} hs')
                row=pd.DataFrame({'Dia': [f'{d:02.0f}'],
                                   'Entrada': [f'{E[0]:02.0f}:{E[1]:02.0f}'],
                                   'Salida': ['  :  '],
                                   'Saldo': ['-'],
                                   'Resto': [f'{np.abs(int(self.resto / 60 / 60)):02.0f}:{np.abs((self.resto / 60 / 60 - int(self.resto / 60 / 60)) * 60):02.0f}']})
                self.tabla=pd.concat([self.tabla,row], ignore_index=True)
            else:
                print(f'----->  Deberías haber salido a las {salida.hour:02.0f}:{salida.minute:02.0f} hs')
                row=pd.DataFrame({'Dia': [f'{d:02.0f}'],
                                   'Entrada': [f'{E[0]:02.0f}:{E[1]:02.0f}'],
                                   'Salida': ['  :  '],
                                   'Saldo': ['+'],
                                   'Resto': [f'{int(self.resto / 60 / 60):02.0f}:{(self.resto / 60 / 60 - int(self.resto / 60 / 60)) * 60:02.0f}']})
                self.tabla=pd.concat([self.tabla,row], ignore_index=True)

    def rest(self):
        self.acum += datetime.datetime.now() - self.hoy
        self.hoy = datetime.datetime.now()
        self.resto = self.acum.total_seconds() - datetime.timedelta(hours=self.fichados * 8 ).total_seconds()
        if self.resto<0:
            print(f'El día {self.dias[-1]:02.0f} te faltan {np.abs(int(self.resto/60/60)):02.0f} hs y '
                  f'{np.abs((self.resto/60/60-int(self.resto/60/60))*60):02.0f} min')
        else:
            print(f'El día {self.dias[-1]:02.0f} tenés a favor {int(self.resto/60/60):02.0f} hs y '
                  f'{(self.resto/60/60-int(self.resto/60/60))*60:02.0f} min')

    def faltan(self):
        self.acum += datetime.datetime.now()-self.hoy
        self.hoy=datetime.datetime.now()
        self.rest()

    def planilla(self):
        print('PLANILLA HORARIA - CAC ',self.hoy.strftime("%B %Y"))
        print(self.tabla)
        print(' ')


def balance():
    sem=horario()
    print(' ')
    print(':::::: BALANCE HORARIO DE LA SEMANA :::::::')
    sem.fichado(22,[8,0],[16,9])
    #sem.fichado(16,[10,47],[18,36])
    #sem.fichado(17,[7,1],[15,11])
    #sem.fichado(18,[8,7],[16,40])
    sem.fichado(23,[9,2],[0])
    print(' ')
    sem.planilla()
    sem.tabla.to_csv('Horas.txt', sep='\t', index=False)

balance()

horas=horario()