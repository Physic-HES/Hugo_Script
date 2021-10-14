import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from tqdm import tqdm
import pandas as pd
from datetime import date

def resume():
    I = pd.read_csv('C:/Users/Yo/Documents/Hugo/Hugo_Script/CNEA/Herramientas de analisis/sant.txt', delimiter='\t')
    return I

def gasto(des,imp,c,f):
    g='%s\t%s\t%s\t%s\t%s\t%s'%(des,np.str(imp),np.str(c),np.str(f[0]),np.str(f[1]),np.str(f[2]))
    with open('C:/Users/Yo/Documents/Hugo/Hugo_Script/CNEA/Herramientas de analisis/sant.txt', 'a') as a_file:
        a_file.write("\n")
        a_file.write(g)
    return resume()


mes=[]
mes_2=[]
for j in range(1,np.max(np.array(M_[:,2]))):
    if np.int(M[-2])+j<12:
        mes_2.append([np.int(M[-1]), np.int(M[-2])+j, np.int(M[-3])])
    elif np.int(M[-2])+j>=12:
        mes_2.append([np.int(M[-1]), 1, np.int(M[-3])+1])
    mes.append(date(mes_2[-1][0],mes_2[-1][1],mes_2[-1][2]).strftime('%d-%m-%Y'))

def Gen_res(I):
    meses=[]
    for j in range(1,len(I)):

        if I.Cuotas[j]==0:
