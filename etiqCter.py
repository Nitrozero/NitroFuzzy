# -*- coding: utf-8 -*-


import numpy as np

"1. Adquisicion de parametros de conjuntos de terminos"

class cjtm():
    def __init__(self,D,dx,alpha,NE):
        self.D = float(D)
        self.dx = float(dx)
        self.alpha = float(alpha)
        self.NE = int(NE)               #NE: Número de cruces de etiqueta
      
    "Matriz de coeficientes de rectas"
    
    def coef(self):
         
        A = np.empty((4,self.NE)) 
        
        for j in range(self.NE):
            A[0][j] = (self.D*(1+j)-self.dx+self.alpha)/(self.D-self.dx)
            A[1][j] = -1/(self.D-self.dx)
            A[2][j] = -(self.dx+self.D*j+self.alpha)/(self.D-self.dx)
            A[3][j] = 1/(self.D-self.dx)
            
        return A
    
    def coef2(self):
        
        B = np.empty((4,self.NE+1))
        
        for j in range(self.NE+1):
            if j == 0:
                B[0][j] = 0
                B[1][j] = 0
                B[2][j] = (self.D*(1+j)-self.dx+self.alpha)/(self.D-self.dx)
                B[3][j] = -1/(self.D-self.dx)
            elif j == self.NE:
                B[0][j] = -(self.dx+self.D*(j-1)+self.alpha)/(self.D-self.dx)
                B[1][j] = 1/(self.D-self.dx)
                B[2][j] = 0
                B[3][j] = 0
            else:
                B[0][j] = -(self.dx+self.D*(j-1)+self.alpha)/(self.D-self.dx)
                B[1][j] = 1/(self.D-self.dx)
                B[2][j] = (self.D*(j+1)-self.dx+self.alpha)/(self.D-self.dx)
                B[3][j] = -1/(self.D-self.dx)
        
        return B
    
    
    "Matriz de dominios"
    
    def dom(self):
        
        d = np.empty((4,self.NE))
        
        for j in range(self.NE):
            d[0][j] = self.D*j + self.alpha
            d[1][j] = self.D*(1+j) + self.alpha - self.dx
            d[2][j] = self.D*j + self.dx + self.alpha
            d[3][j] = self.D*(1+j) + self.alpha
            
    
        return d          