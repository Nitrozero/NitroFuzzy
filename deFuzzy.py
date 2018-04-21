# -*- coding: utf-8 -*-


import numpy as np

class defuzificador():
    def __init__(self,N):
        self.N = N
    
    def salidaFuzzy(self,GP,M,PC):
        pc = PC[1][0]        
        sumaProd = np.zeros(self.N+1)
        sumaArea = np.zeros(self.N+1)
        ajusteActuador = 0
        for i in range(self.N+1):
            
            
            if i == 0:

                if GP[i]>pc:

                    dx1 = PC[0][i]
                    A1 = dx1*pc
                    dx2 = (GP[i]-M[2][i])/M[3][i]
                    A2 = dx2*(GP[i]-pc)
                    dx3 = PC[0][i]-(GP[i]-M[2][i])/M[3][i]
                    A3 = dx3*(GP[i]-pc)/2
                    A = A1 + A2 + A3
                    xg1 = 0.5*dx1
                    xA1 = xg1*A1
                    xg2 = 0.5*dx2
                    xA2 = xg2*A2
                    xg3 = 1/3*dx3
                    xA3 = xg3*A3
                    xA = xA1 + xA2 + xA3
                    
                    sumaProd[i] = sumaProd[i] + xA
                    sumaArea[i] = sumaArea[i] + A


                else:
                    dx = PC[0][i]
                    Ab = dx*GP[i]
                    xg = 0.5*PC[0][i]
                    xAb = xg*Ab
                    sumaProd[i] = sumaProd[i] + xAb
                    sumaArea[i] = sumaArea[i] + Ab
                    
                    if GP[i]>GP[i+1]:
                        pass
                    else:
                        if GP[i+1]>pc:
                            dx1 = PC[0][i]-(GP[i]-M[0][i+1])/M[1][i+1]
                            A1 = dx1*(pc-GP[i])/2
                            xg1 = (GP[i]-M[0][i+1])/M[1][i+1]+2/3*dx1
                            xA1 = xg1*A1
                            sumaProd[i] = sumaProd[i] + xA1
                            sumaArea[i] = sumaArea[i] + A1
                            
                        else:
                            dx1 = (GP[i+1]-M[0][i+1])/M[1][i+1]-(GP[i]-M[0][i+1])/M[1][i+1]
                            dx2 = PC[0][i]-(GP[i+1]-M[0][i+1])/M[1][i+1]
                            A1 = dx1*(GP[i+1]-GP[i])/2
                            A2 = dx2*(GP[i+1]-GP[i])
                            A = A1 + A2
                            xg1 = (GP[i]-M[0][i+1])/M[1][i+1] + 2/3*dx1
                            xg2 = 0.5*(PC[0][i]+(GP[i+1]-M[0][i+1])/M[1][i+1])
                            xA1 = xg1*A1
                            xA2 = xg2*A2
                            xA = xA1 + xA2
                            sumaProd[i] = sumaProd[i] + xA
                            sumaArea[i] = sumaArea[i] + A
                                                 
            elif i == self.N:

                if GP[i]>pc:
                    dx1 = (PC[0][i-1]+PC[0][0])-PC[0][i-1] #Espacio simetrico
                    A1 = dx1*pc    
                    dx2 = (PC[0][i-1]+PC[0][0])-(GP[i]-M[0][i])/M[1][i]
                    A2 = dx2*(GP[i]-pc)
                    dx3 = (GP[i]-M[0][i])/M[1][i]-PC[0][i-1]
                    A3 = dx3*(GP[i]-pc)/2
                    A = A1 + A2 + A3
                    xg1 = PC[0][i-1]+0.5*PC[0][0]
                    xA1 = xg1*A1
                    xg2 = 0.5*(PC[0][i-1]+PC[0][0]+(GP[i]-M[0][i])/M[1][i])
                    xA2 = xg2*A2
                    xg3 = PC[0][i-1]+2/3*dx3
                    xA3 = xg3*A3
                    xA = xA1 + xA2 + xA3
                    sumaProd[i] = sumaProd[i] + xA
                    sumaArea[i] = sumaArea[i] + A

                else:
                    dx = PC[0][i-1]+PC[0][0]-PC[0][i-1]
                    Ab = dx*GP[i]
                    xg = PC[0][i-1]+0.5*PC[0][0]
                    xAb = xg*Ab
                    sumaProd[i] = sumaProd[i] + xAb
                    sumaArea[i] = sumaArea[i] + Ab
                    
                    if GP[i]>GP[i-1]:
                        pass
                    else:
                        if GP[i-1]>pc:
                            dx1 = (GP[i]-M[2][i-1])/M[3][i-1]-PC[0][i-1]
                            A1 = dx1*(pc-GP[i])/2
                            xg1 = PC[0][i-1]+1/3*dx1
                            xA1 = xg1*A1
                            sumaProd[i] = sumaProd[i] + xA1
                            sumaArea[i] = sumaArea[i] + A1

                        else:
                            dx1 = (GP[i]-M[2][i-1])/M[3][i-1]-(GP[i-1]-M[2][i-1])/M[3][i-1]
                            dx2 = (GP[i-1]-M[2][i-1])/M[3][i-1]-PC[0][i-1]
                            A1 = dx1*(GP[i-1]-GP[i])/2
                            A2 = dx2*(GP[i-1]-GP[i])
                            A = A1 + A2
                            xg1 = (GP[i-1]-M[2][i-1])/M[3][i-1] + 1/3*dx1
                            xg2 = 0.5*((GP[i-1]-M[2][i-1])/M[3][i-1]+PC[0][i-1])
                            xA1 = xg1*A1
                            xA2 = xg2*A2
                            xA = xA1 + xA2
                            sumaProd[i] = sumaProd[i] + xA
                            sumaArea[i] = sumaArea[i] + A
                                      
            else:                                     
                if GP[i]>pc:
                    dx1 = PC[0][i]-PC[0][i-1]
                    A1 = pc*dx1
                    x1 = (GP[i]-M[0][i])/M[1][i]
                    x2 = (GP[i]-M[2][i])/M[3][i]
                    dx2 = x2-x1
                    A2 = dx2*(GP[i]-pc)
                    dx3 = x1-PC[0][i-1]
                    A3 = dx3*(GP[i]-pc)
                    
                    A = A1 + A2 + A3
                    xg = 0.5*(PC[0][i]+PC[0][i-1])
                    xA = xg*A
                    sumaProd[i] = sumaProd[i] + xA
                    sumaArea[i] = sumaArea[i] + A

                else:
                    dx = PC[0][i]-PC[0][i-1]
                    Ab = dx*GP[i]
                    xg = 0.5*(PC[0][i-1]+PC[0][i])
                    xAb = xg*Ab 
                    sumaProd[i] = sumaProd[i] + xAb
                    sumaArea[i] = sumaArea[i] + Ab
                                        
                    if GP[i]>GP[i+1]:
                        pass
                    else:
                        if GP[i+1]>pc:
                            dx1 = PC[0][i]-(GP[i]-M[0][i+1])/M[1][i+1]
                            A1 = (pc-GP[i])*dx1/2
                            xg1 = (GP[i]-M[0][i+1])/M[1][i+1]+2/3*dx1
                            xA1 = xg1*A1
                            sumaProd[i] = sumaProd[i] + xA1
                            sumaArea[i] = sumaArea[i] + A1
                            
                        else:
                            dx1 = (GP[i+1]-M[0][i+1])/M[1][i+1]-(GP[i]-M[0][i+1])/M[1][i+1]
                            dx2 = PC[0][i]-(GP[i+1]-M[0][i+1])/M[1][i+1]
                            A1 = dx1*(GP[i+1]-GP[i])/2
                            A2 = dx2*(GP[i+1]-GP[i])
                            A = A1 + A2
                            xg1 = (GP[i]-M[0][i+1])/M[1][i+1]+2/3*dx1
                            xg2 = 0.5*(PC[0][i]+(GP[i+1]-M[0][i+1])/M[1][i+1])
                            xA1 = xg1*A1
                            xA2 = xg2*A2
                            xA = xA1 + xA2
                            sumaProd[i] = sumaProd[i] + xA
                            sumaArea[i] = sumaArea[i] + A
                                
                    if GP[i]>GP[i-1]:
                        pass
                    else:
                        if GP[i-1]>pc:
                            dx1 = (GP[i]-M[2][i-1])/M[3][i-1]-PC[0][i-1]
                            A1 = dx1*(pc-GP[i])/2
                            xg1 = PC[0][i-1] + 1/3*dx1
                            xA1 = xg1*A1
                            sumaProd[i] = sumaProd[i] + xA1
                            sumaArea[i] = sumaArea[i] + A1

                        else:
                            dx1 = (GP[i]-M[2][i-1])/M[3][i-1]-(GP[i-1]-M[2][i-1])/M[3][i-1]
                            dx2 = (GP[i-1]-M[2][i-1])/M[3][i-1]-PC[0][i-1]
                            A1 = dx1*(GP[i-1]-GP[i])/2
                            A2 = dx2*(GP[i-1]-GP[i])
                            A = A1 + A2
                            xg1 = (GP[i-1]-M[2][i-1])/M[3][i-1]+1/3*dx1
                            xg2 = 0.5*((GP[i-1]-M[2][i-1])/M[3][i-1]+PC[0][i-1])
                            xA1 = xg1*A1
                            xA2 = xg2*A2
                            xA = xA1 + xA2
                            sumaProd[i] = sumaProd[i] + xA
                            sumaArea[i] = sumaArea[i] + A

        print(sum(sumaProd)/sum(sumaArea)-ajusteActuador) 