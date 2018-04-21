# -*- coding: utf-8 -*-


import numpy as np

class pc():
    def __init__(self,N):
        self.N = N
    
    def xdom(self,A):
        
        x = np.zeros(self.N)
        y = np.zeros(self.N)
        xy = np.zeros((2,self.N))
        
        for i in range(self.N):
            x[i] = (A[0][i]-A[2][i])/(A[3][i]-A[1][i])
            y[i] = (A[0][i]+A[1][i]*x[i])
            
        xy = np.vstack((x,y))
        
        
        return xy
        