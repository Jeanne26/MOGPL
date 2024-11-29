from gurobipy import *
from pb_sac_a_dos import variableExemple1,solveExemple1
import numpy as np


def minOWAex1():
    A,B,C1,C2= variableExemple1()
    C= np.stack((C1,C2),axis= 0 ).reshape((2,10))
    n=len(C) #=2
    p=len(A) #=10
    #poids w' w1'= w1-w2=1 et w2'=w2
    w= [1,1]
    _,_,z1_star,z2_star= solveExemple1()
    z_star =[z1_star,z2_star]
    m= Model("MinOWAEx1")
    m.setParam("OutputFlag",0)
    #declaration des variables de decision
    x= [m.addVar(vtype=GRB.BINARY, lb=0,name=f"x{i+1}") for i in range(p)]
    r= [m.addVar(vtype=GRB.CONTINUOUS,name=f"r{i+1}")for i in range(n)]
    b= [[m.addVar(vtype=GRB.CONTINUOUS,lb=0,name=f"b{i+1}{j+1}") for i in range(n)] for j in range(n)]
    m.update()

    #x doit etre realisable contrainte de budget
    m.addConstr(quicksum(A[j]*x[j] for j in range(p))<=B)
    #ajout des contraintes
    for k in range(n):
        for i in range(n):
            z_i= quicksum(C[i][j]*x[j] for j in range(p))
            m.addConstr(r[k] - b[i][k] >= z_star[i] - z_i)
    m.update()
    #ajout de la fonction objective
    obj = LinExpr();
    obj = quicksum(w[k]*((k+1)*r[k] + quicksum(b[i][k] for i in range(n))) for k in range(n))
    
    m.setObjective(obj,GRB.MINIMIZE)
    m.update()
    print("Fonction objectif :", m.getObjective())
    m.write("model.lp")
    m.optimize()

    x_opt= [round(var.x) for var in x]
    z_opt = [int(sum(C[i][j] * x_opt[j] for j in range(p))) for i in range(n)]
    t_opt = m.objval
    return x_opt, z_opt,t_opt
