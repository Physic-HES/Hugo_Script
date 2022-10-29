# -*- coding: utf-8 -*-
"""
Created on Tue Oct  4 09:04:24 2022

@author: Publico
"""

# -*- coding: utf-8 -*-
"""
LOCKIN Stanford Research SR830
Manual: http://www.thinksrs.com/downloads/PDFs/Manuals/SR830m.pdf
Manual: https://github.com/diegoshalom/labosdf/blob/master/manuales/SR830m.pdf
"""


import pyvisa as visa
import time

class SR830:
    '''Clase para el manejo amplificador Lockin SR830 usando PyVISA de interfaz'''

    scale_values = (2e-9, 5e-9, 10e-9, 20e-9, 50e-9, 100e-9, 200e-9, 500e-9, 1e-6,
                    2e-6, 5e-6, 10e-6, 20e-6, 50e-6, 100e-6, 200e-6, 500e-6, 1e-3,
                    2e-3, 5e-3, 10e-3, 20e-3, 50e-3, 100e-3, 200e-3, 500e-3, 1) # in V

    time_constant_values = (10e-6, 30e-6, 100e-6, 300e-6, 1e-3, 3e-3, 10e-3, 30e-3, 100e-3, 300e-3,
                    1e0, 3e0, 10e0, 30e0, 100e0, 300e0, 1e3, 3e3, 10e3, 30e3) # in s

    def __init__(self, resource):
        self._lockin = visa.ResourceManager().open_resource(resource)
        #print(self._lockin.query('*IDN?')) # habria que ver si es mejor no pedir IDN. Puede que trabe la comunicacion al ppio
        self._lockin.write("LOCL 2") #Bloquea el uso de teclas del Lockin
        time.sleep(1) # tal vez ayuda a evitar errores de comunicacion del pyvisa
        self.scale = self.get_scale()
        self.time_constant = self.get_time_constant()

    def __del__(self):
        self._lockin.write("LOCL 0") #Desbloquea el Lockin
        self._lockin.close()

    def set_modo(self, modo):
        '''Selecciona el modo de medición, A, A-B, I, I(10M)'''
        self._lockin.write("ISRC {0}".format(modo))

    def set_filtro(self, sen, tbase, slope):
        '''Setea el filtro de la instancia'''
        #Página 90 (5-4) del manual
        self._lockin.write("OFLS {0}".format(slope))
        self._lockin.write("OFLT {0}".format(tbase))
        self._lockin.write("SENS {0}".format(sen))
       
    def set_aux_out(self, auxOut = 1, auxV = 0):
        '''Setea la tensión de salida de al Aux Output indicado.
        Las tensiones posibles son entre -10.5 a 10.5'''
        self._lockin.write('AUXV {0}, {1}'.format(auxOut, auxV))
           
    def set_referencia(self,isIntern, freq, voltaje = 1):
        if isIntern:
            #Referencia interna
            #Configura la referencia si es así
            self._lockin.write("FMOD 1")
            self._lockin.write("SLVL {0:f}".format(voltaje))
            self._lockin.write("FREQ {0:f}".format(freq))
        else:
            #Referencia externa
            self._lockin.write("FMOD 0")
           
    def set_scale(self, scale_number):
        self.scale = min(scale_number,len(self.scale_values))
        self._lockin.write(f'SENS {self.scale}')
        return self.scale
   
    def get_scale(self):
        self.scale = int(self._lockin.query_ascii_values('SENS ?')[0])
        return self.scale

    def set_time_constant(self, time_constant_number):
        self._lockin.write(f'OFLT {time_constant_number}')
        self.time_constant = time_constant_number
        return self.time_constant
   
    def get_time_constant(self):
        return int(self._lockin.query_ascii_values('OFLT ?')[0])

    def set_display(self, isXY):
        if isXY:
            self._lockin.write("DDEF 1, 0") #Canal 1, x
            self._lockin.write('DDEF 2, 0') #Canal 2, y
        else:
            self._lockin.write("DDEF 1,1") #Canal 1, R
            self._lockin.write('DDEF 2,1') #Canal 2, T
   
    def get_display(self):
        '''Obtiene la medición que acusa el display.
        Es equivalente en resolución a la medición de los parámetros con SNAP?'''
        orden = "SNAP? 10, 11"
        return self._lockin.query_ascii_values(orden, separator=",")
       
    def get_medicion(self,isXY = True):
        '''Obtiene X,Y o R,Ang, dependiendo de isXY'''
        orden = "SNAP? "
        if isXY:
            self._lockin.write("DDEF 1,0") #Canal 1, XY
            orden += "1, 2" #SNAP? 1,2
        else:
            self._lockin.write("DDEF 1,1") #Canal 1, RTheta
            orden += "3, 4" #SNAP? 3, 4
        return self._lockin.query_ascii_values(orden, separator=",")

    def auto_scale(self):
        '''
            Utiliza medicion polar (r, angulo)          
            inf_threshold es el porcentaje minimo de la escala  para el cual el
            autoescalado empiza a efectuarse: intenta mantenerse sobre ese rango. valor float de 0 a 1
        '''
        debug = True
        sup_theshold = 1
        inf_threshold = 0.1        
        nespera = 5 # se recomienda esperar entre 3 y 5 veces el tiempo de medicion entre escalado y medicion        
        tespera = self.time_constant_values[self.time_constant] * nespera
        time.sleep(tespera)
        r,tita = self.get_medicion(isXY=False)

        while r < self.scale_values[self.scale] * inf_threshold and self.scale > 0:
            if debug:
                print('Valor por debajo de threshold, bajo escala (r=%g, oldscale=%g)'%(r,self.scale_values[self.scale]))
            self.scale -= 1
            self.set_scale(self.scale)
            time.sleep(tespera) # esperar N * el tiempo de integracion antes de medir
            r,tita = self.get_medicion(isXY=False)

        while r > self.scale_values[self.scale] * sup_theshold and self.scale < (len(self.scale_values)-1):
            if debug:
                print('Overloaded, subo escala (oldscale=%g)'%(self.scale_values[self.scale]))
            self.scale += 1
            self.set_scale(self.scale)
            time.sleep(tespera)
            r,tita = self.get_medicion(isXY=False)
       
        if debug:
            print('Listo (r=%g, scale=%g)'%(r, self.scale_values[self.scale]))

        return r, tita