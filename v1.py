# -*- coding: utf-8 -*-
"""
Created on Mon May 21 14:46:09 2018

@author: Usuario
modulo fuzzy1
"""

import numpy as np
import openpyxl as opyx

"""===========================================================================
   Clase 1: Construccion de conjunto de terminos
   ========================================================================"""
   
class Armador:

    def __init__(self,D,dx,alpha,NE):
        self.D = float(D)
        self.dx = float(dx)
        self.alpha = float(alpha)
        self.NE = int(NE)               #NE: Número de cruces de etiqueta
      
#=============================================================================
# Metodo 1. Calculo de coeficientes a y b (y = ax + b) Matriz con Netiq-1 cols 
#=============================================================================
        
    def calcularCoef(self):
         
        coeficiente = np.empty((4,self.NE)) 
        
        for j in range(self.NE):
            coeficiente[0][j] = (self.D*(1+j)-self.dx+self.alpha)/(self.D-self.dx)
            coeficiente[1][j] = -1/(self.D-self.dx)
            coeficiente[2][j] = -(self.dx+self.D*j+self.alpha)/(self.D-self.dx)
            coeficiente[3][j] = 1/(self.D-self.dx)
            
        return coeficiente
    
#=============================================================================
# Metodo 2. Calculo de coeficientes a y b (y = ax + b) Matriz con Netiq cols 
#=============================================================================  
        
    def calcularCoef2(self,coeficiente):
        
        matrizColZero = np.zeros((2,1))
        filasSuperior = np.hstack((matrizColZero,coeficiente[2:4][:]))
        filasInferior = np.hstack((coeficiente[0:2][:],matrizColZero))
        coeficiente2 = np.vstack((filasSuperior,filasInferior))
      
        return coeficiente2
    
#=============================================================================
# Metodo 3. Calculo de dominios de rectas y (Matriz con Netiq cols)
#============================================================================= 
        
    def calcularDom(self):
        
        dominio = np.empty((4,self.NE))
        
        for j in range(self.NE):
            dominio[0][j] = self.D*j + self.alpha
            dominio[1][j] = self.D*(1+j) + self.alpha - self.dx
            dominio[2][j] = self.D*j + self.dx + self.alpha
            dominio[3][j] = self.D*(1+j) + self.alpha
            
        return dominio   

"""===========================================================================
   Clase 2: Calculador de grados de pertenencia
   ========================================================================"""

class GradoPertenencia:

    def __init__(self,numeroCruces,dato):
        self.numeroCruces = numeroCruces
        self.dato = dato
    
#=============================================================================
# Metodo 1. Calculo de grados de pertenencia 
#=============================================================================     
    
    def calcularGP(self,A,B):
        
        G = np.zeros((4,self.numeroCruces))        
        gp_0 = np.zeros((2,1))
        
        for j in range(self.numeroCruces):
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
        ET = np.zeros(self.numeroCruces+1)
                                 
        for i in range(2):
            for j in range(self.numeroCruces):
                if G[i][j] == 1:
                    ET[i+j] = gp_0[i]
                    
        return G, ET, gp_0

"""===========================================================================
   Clase 3: Calculador de puntos de cruce entre etiquetas
   ========================================================================"""

class CruceEtiqueta:
    
    def __init__(self,numeroCruces):
        self.numeroCruces = numeroCruces
    
#=============================================================================
# Metodo 1. Calculo de puntos de coordenadas de los puntos de cruce entre 
#           etiquetas
#=============================================================================
        
    def calcularCoordCruces(self,A):
        
        coord_x = np.zeros(self.numeroCruces)
        coord_y = np.zeros(self.numeroCruces)
        coord_xy = np.zeros((2,self.numeroCruces))
        
        for i in range(self.numeroCruces):
            coord_x[i] = (A[0][i]-A[2][i])/(A[3][i]-A[1][i])
            coord_y[i] = (A[0][i]+A[1][i]*coord_x[i])
            
        coord_xy = np.vstack((coord_x,coord_y))
        
        return coord_xy

"""===========================================================================
   Clase 4: Calculador de puntos de cruce entre etiquetas
   ========================================================================"""

class CargadorReglas:
    def __init__(self,n,A,string):
        self.n = n
        self.A = A

#=============================================================================
# Metodo 1. Construccion 
#=============================================================================  
    
    def obtenerReglas(self):
        string = self.string
        MRD = opyx.load_workbook("C:/Users/Usuario/FAAM-Terreno/Scld/2016-TEC-005-FUZZY-01.xlsx")
        hReglas = MRD.get_sheet_by_name("REGLAS")
        hEtiquetas = MRD.get_sheet_by_name("ETIQUETAS")
        
        nReglas = 0
        for i in hReglas:
            nReglas = nReglas + 1
            if hReglas['A'+str(nReglas)].value==None:
                break

        diccET={}
        
        for i in range(self.n):
            if hEtiquetas["A"+str(i+1)].value == string:
                diccET[hEtiquetas["A"+str(i+1)].value+hEtiquetas["B"+str(i+1)].value] = self.A[i]   
        
        MRD.save("C:/Users/Usuario/FAAM-Terreno/Scld/2016-TEC-005-FUZZY-01.xlsx")        
#        print(diccET)

"""===========================================================================
   Clase 5: Defuzzificador
   ========================================================================"""
class Defuzzificador:
    def __init__(self,numeroCruces):
        self.numeroCruces = numeroCruces
    
#=============================================================================
# Metodo 1. Calcular salida difusa 
#============================================================================= 
        
    def calcularSalida(self,GP,M,PC):
        pc = PC[1][0]        
        sumaProd = np.zeros(self.numeroCruces+1)
        sumaArea = np.zeros(self.numeroCruces+1)
        ajusteActuador = 0
        for i in range(self.numeroCruces+1):
            
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
                                                 
            elif i == self.numeroCruces:

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

        salidaDifusa = sum(sumaProd)/sum(sumaArea)-ajusteActuador
        print(salidaDifusa)
        
        return salidaDifusa