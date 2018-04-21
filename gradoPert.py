# -*- coding: utf-8 -*-

""" ..Grados de Pertenencia"""

import numpy as np

class gp_calc():
    def __init__(self,N,dato):
        self.N = N
        self.dato = dato
    
    def gp(self,A,B):
        
        G=np.zeros((4,self.N))        
        gp_0 = np.zeros((2,1))
        
        
        for j in range(self.N):
            for i in range(3):
                if (self.dato >= B[i][j] and self.dato < B[i+1][j]):
                    
                    
                    if (B[i+1][j] > B[i][j]):

                        G[i][j] = 1
                        G[i+1][j] = 1
                        
                        if i<2:
                            gp_0[0] = A[i][j] + A[i+1][j]*self.dato
                        elif i>=2:
                            gp_0[1] = A[i][j] + A[i+1][j]*self.dato
        
        
        G = np.vstack((G[0][:],G[2][:])) 
        ET = np.zeros(self.N+1)
                                 
        for i in range(2):
            for j in range(self.N):
                if G[i][j] == 1:
                    ET[i+j] = gp_0[i]
                    
                
        return G, ET, gp_0