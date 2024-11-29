from gurobipy import *
from pb_sac_a_dos import variableExemple1
import numpy as np


def dual(z,k):
    """retourne le dual du programme lineaire de la question 2.2

    Args:
        z (list)
        k (int)

    Returns:
        tuple: qui contient v_opt correspondant au vecteur optimal du programme
                        et z_opt la valeur de la fonction objectif à l'optimum
    """
    n= len(z)
    m = Model(f"model{k}")
    m.setParam('OutputFlag',0)
    v=[]
    v.append(m.addVar(vtype=GRB.CONTINUOUS,name=f"r{k}"))
    for i in range(1,n+1):
        v.append(m.addVar(vtype=GRB.CONTINUOUS,lb=0,name=f"b{i}{k}"))
    m.update()
    obj= LinExpr();
    obj= k*v[0] - sum(v[1:])

    m.setObjective(obj,GRB.MAXIMIZE)

    m.update()

    for i in range(1,n+1):
        m.addConstr(v[0]- v[i]<= z[i-1])

    m.update()
    
    m.optimize()
    v_opt = [round(var.x) for var in v]
    z_opt = k*v_opt[0] - sum(v_opt[1:])

    return v_opt,z_opt


def find_composantes(z):
    c = []
    for k in range(1,len(z)+1):
        _,z_opt = dual(z,k)
        c.append(z_opt)
    return c


def maxOWAex1():
    A,B,C1,C2= variableExemple1()
    C= np.stack((C1,C2),axis= 0 ).reshape((2,10))
    n=len(C) #=2
    p=len(A) #=10
    #poids w' w1'= w1-w2=1 et w2'=w2
    w= [1,1]

    m= Model("MaxOWAEx1")
    m.setParam("OutputFlag",0)
    #declaration des variables de decision
    x= [m.addVar(vtype=GRB.BINARY, lb=0,name=f"x{i+1}") for i in range(p)]
    r= [m.addVar(vtype=GRB.CONTINUOUS,name=f"r{i+1}")for i in range(n)]
    b= [[m.addVar(vtype=GRB.CONTINUOUS,lb=0,name=f"b{i+1}{j+1}") for i in range(n)] for j in range(n)]
    m.update()

    #x doit etre realisable contrainte de budget
    m.addConstr(quicksum(A[j]*x[j] for j in range(p))<=B)
    #ajout des contraintes
    # for i in range(n):
    #     for k in range(n):
    #         z = quicksum(C[i][j]*x[j] for j in range(p))
    #         m.addConstr(r[k] -b[i][k] <= z)

    for k in range(n):
        for i in range(n):
            z_i= quicksum(C[i][j]*x[j] for j in range(p))
            m.addConstr(r[k] - b[i][k] <= z_i)
    m.update()
    #ajout de la fonction objective
    obj = LinExpr();
    obj = quicksum(w[k]*((k+1)*r[k] - quicksum(b[i][k] for i in range(n))) for k in range(n))
    
    m.setObjective(obj,GRB.MAXIMIZE)
    m.update()
    print("Fonction objectif :", m.getObjective())
    m.write("model.lp")
    m.optimize()

    x_opt= [round(var.x) for var in x]
    z_opt = [int(sum(C[i][j] * x_opt[j] for j in range(p))) for i in range(n)]
    t_opt = m.objval
    return x_opt, z_opt,t_opt

def affichageMawOwa(x_opt,z_opt,t_opt):
    """Affiche le resultat de la resolution du programme lineaire pour le 
    critère maxOWA

    Args:
        x_opt (list): solution optimale
        z_opt (list): vecteur image de x_opt
        t_opt (int) : valeur de g(x) à l'optimum
    """

    print("-----------------------------------------")
    print("-----------------------------------------")
    print(f"Solution optimale x* : {x_opt}")
    print(f"Vecteur de conséquence z(x*) : {z_opt}")
    print(f"Valeur de la fonction objectif g(x*) : {t_opt}")
    print("-----------------------------------------")
    print("-----------------------------------------")
