from gurobipy import *
import numpy as np
from pylab import plot, show
from exo1 import solveExemple1, variableExemple1

def solve_MinMaxRegret():
    """Application du critère MinMax regret pour la résolution de l'exemple 1, retourne
    la solution x,t et z à l'optimum, """
    #Recuperation des valeurs à l'optimum dans le scénario 1 et 2
    _,_,z1_opt, z2_opt = solveExemple1()

    #Definition du problème de l'exemple 1
    A,B,C1,C2= variableExemple1()

    #nombre de variable
    p = len(C1)
    n = 2

    #Coefficient fonctions objectifs de l'exemple 1, utiliser en tant que matrice 
    #des contraintes avec le critere maxmin
    C= np.stack((C1,C2),axis= 1 )

    m=Model("MinMaxRegret")
    m.setParam('OutputFlag', 0)

    #Declaration des variables de decision
    x=[]
    for i in range(p):
        x.append(m.addVar(vtype=GRB.BINARY, lb=0,name="x%d" % (i+1)))
    t= m.addVar(vtype=GRB.CONTINUOUS, name="t")

    #Integration des nouvelles variables
    m.update()

    #Definition de l'objectif
    m.setObjective(t, GRB.MINIMIZE)

    #Definition des contraintes
    m.addConstr(t>= z1_opt - quicksum(C[j][0]*x[j] for j in range(p)))
    m.addConstr(t>= z2_opt - quicksum(C[j][1]*x[j] for j in range(p)))

    m.addConstr(quicksum(A[i]*x[i] for i in range(p))<= B)

    #Resolution
    m.optimize()

    x_opt = [round(var.x) for var in x]
    z_opt = [int(sum(C[j][i] * x_opt[j] for j in range(10))) for i in range(2)]
    t_opt = t.x
    
    return x_opt,z_opt,t_opt

def affichageMaxMin():
    x_opt,z_opt,t_opt = solve_MinMaxRegret()

    print("-----------------------------------------")
    print("-----------------------------------------")
    print(f"Solution optimale x* : {x_opt}")
    print(f"Vecteur de conséquence z(x*) : {z_opt}")
    print(f"Valeur de la fonction objectif g(x*) : {t_opt}")
    print("-----------------------------------------")
    print("-----------------------------------------")
    
affichageMaxMin()