from gurobipy import *
import numpy as np
from pb_sac_a_dos import variableExemple1

def solve_MaxMin():
    """Application du critère MaxMin pour la résolution de l'exemple 1
    Returns:
    - x : solution optimal de l'exemple 1 au sens du maxmin
    - t : solution dont l'evaluation dans le pire cas est la meilleure possible
    - z : vecteur image de x
    """
    #Definition du problème de l'exemple 1
    A,B,C1,C2= variableExemple1()
    #nombre de variable
    p = len(C1)
    n = 2
    #Coefficient fonctions objectifs de l'exemple 1, utiliser en tant que matrice 
    #des contraintes avec le critere maxmin
    C= np.stack((C1,C2),axis= 1 )

    m= Model("MaxMin")
    m.setParam('OutputFlag', 0)

    #Declaration des variables de decision
    x=[]
    for i in range(p):
        x.append(m.addVar(vtype=GRB.BINARY, lb=0,name="x%d" % (i+1)))
    t= m.addVar(vtype=GRB.CONTINUOUS, name="t")

    #Integration des nouvelles variables
    m.update()

    #Definition de l'objectif
    m.setObjective(t, GRB.MAXIMIZE)

    #Definition de contraintes
    for i in range(n):
        m.addConstr(t<= quicksum(C[j][i]*x[j] for j in range(p)))

    m.addConstr(quicksum(A[i]*x[i] for i in range(p))<= B)

    #Resolution
    m.optimize()

    x_opt = [round(var.x) for var in x]
    z_opt = [int(sum(C[j][i] * x_opt[j] for j in range(10))) for i in range(2)]
    t_opt = t.x
    
    return x_opt,z_opt,t_opt



def affichageMaxMin():
    """
    Affiche le resultat de la resolution du programme lineaire pour le critere minmax
    """
    x_opt,z_opt,t_opt = solve_MaxMin()

    print("-----------------------------------------")
    print("-----------------------------------------")
    print(f"Solution optimale x* : {x_opt}")
    print(f"Vecteur de conséquence z(x*) : {z_opt}")
    print(f"Valeur de la fonction objectif g(x*) : {t_opt}")
    print("-----------------------------------------")
    print("-----------------------------------------")
    