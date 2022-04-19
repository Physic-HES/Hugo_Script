import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

folder_selected='/home/hugo_sosa/Documents/CNEA/CEBP/EECE-032-2022/'
arch='EECE0322022_'
Caudal=['Q15_','Q20_','Q25_','Q30_','Q35_']
barrido=['01.txt','02.txt']
head=38

def ensayo(cau,barr,type):
      folder_selected = '/home/hugo_sosa/Documents/CNEA/CEBP/EECE-032-2022/txt/'
      arch = 'EECE0322022_'
      if type=='DP':
            col=[0,2,3,4,5,6,7,8,9]
            datframe = pd.read_csv(folder_selected + arch + r'Q%2.0f_' % cau + r'%02.0f.txt' % barr,
                                   delimiter='\t', usecols=col, index_col=False, header=34, nrows=65)
      elif type=='ABS':
            col=[1,10,11,12]
            datframe = pd.read_csv(folder_selected + arch + r'Q%2.0f_' % cau + r'%02.0f.txt' % barr,
                             delimiter='\t', usecols=col, index_col=False, header=34)
      return datframe

