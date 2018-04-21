# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 17:40:09 2017

@author: Usuario
"""

import numpy as np
import openpyxl as opyx

class regDif():
    def __init__(self,n,A,string):
        self.n = n
        self.A = A
    
    def diccRegDif(self):
        n = self.n
        A = self.A
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
        
        for i in range(n):
            if hEtiquetas["A"+str(i+1)].value == string:
                diccET[hEtiquetas["A"+str(i+1)].value+hEtiquetas["B"+str(i+1)].value] = A[i]   
                
        print(diccET)
    
    
