#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 21:11:43 2017

@author: isaac
"""

def MarkovEquiv(A,B):
    immoralitiesA = getImmoralities(A)
    immoralitiesB = getImmoralities(B)
    if(len(immoralitiesA)!=len(immoralitiesB)):
        return False
    for imm in immoralitiesA:
        if not(imm in immoralitiesB):
            return False
    return True and equalSkeletons(A,B)

def matString2Int(ptr):
    mat = [(re.sub("[^0-9]",",",i)).split(",") for i in ptr]
    ptr.close()
    for i in mat:
        while("" in i):
            i.remove("")
    while([] in mat):
        mat.remove([])
    return [[int(j) for j in i] for i in mat]

def getImmoralities(A):
    immoralities = []
    order = len(A)
    for j in range(order):
        for i in range(order-1):
            for k in range(i+1,order):
                if(A[i][j]==1 and A[k][j]==1):
                    if not(A[i][k]==1 or A[k][i]==1):
                        imm = (i+1,k+1,j+1)
                        if not imm in immoralities:
                            immoralities.append(imm)
    print(immoralities)
    return immoralities
    
def equalSkeletons(A,B):
    if(len(A)!=len(B)):
        return False
    for i in range(len(A)):
        for j in range(len(A)):
            if(A[i][j]):
                A[j][i] = 1
            if(B[i][j]):
                B[j][i] = 1
    if(A==B):
        return True
        
import re
    
file_a = open("A.mat","r")
file_b = open("B.mat","r")

for i in range(5):
    file_a.readline()
    file_b.readline()

A = matString2Int(file_a)
B = matString2Int(file_b)

print(MarkovEquiv(A,B))