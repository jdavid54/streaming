#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 13:09:15 2019

@author: jeandavid
"""
#La frequence est proportionnelle a l'inverse de la longueur
#On a : 1/L = F
#donc si l=L/2 -> 1/l= 2F
#pour trouver les frettes, on rajoute une longueur dl_n a l : l+dl_n
#la frequence est diviser par le ratio a chaque dl_n

# on a alors : 1/(l+dl_n) = F/ratio^n

#------------------------------------------   L frequence fondamentale F
#---------------------|--------------------   l=L/2 milieu octave de F = 2F
#-----------------|------------------------   l+dl
#-----------------|===|--------------------   dl

import numpy as np
import matplotlib.pyplot as plt

ratio=2**(1/12)
print(ratio)
l=0.5
frettes=[]
frequences=[]
for n in range(12,-1,-1):
    dl=(ratio**n-1)/2    #longueur ajoutee au milieu pour diviviser la frequence par ratio
    frettes.append(l-dl)  #mesure depuis la tete de guitare
    frequences.append(1/(l+dl))
print(frettes)

x=np.zeros(13)

plt.plot(frettes,x,'ro')
plt.show()


print(frequences)

chechF=list(ratio**t for t in range(13))
print('Verification :',chechF)