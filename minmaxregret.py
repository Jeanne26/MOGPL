from gurobipy import *
import numpy as np
from pb_sac_a_dos import solveExemple1, variableExemple1, solveGen, extractABC, modelGen
from utils_graphe import get_in,get_out, find_shortest_path


"""
Implémentation des fonctions pour résoudre des problèmes d'optimisation 
au sens du critère MinMaxRegret. Fonctions:
    - MinMaxRegretEx1 :  résolution de l'exemple 1 en utilisant le critère MinMaxRegret.
    - MinMaxRegret :  résolution généralisée de problèmes MinMax sur plusieurs modèles .
    - find_minmax_path : recherche d'un chemin robuste dans un graphe sous incertitude .
    - affichageMinMaxRegret : affichage des résultats pour le critère MinMAx
"""

def MinMaxRegretEx1():
    """Application du critère MinMax regret pour la resolution de l'exemple 1
    Returns:
    - x : solution optimal de l'exemple 1 au sens du minmax regret
    - t : solution dont l'evaluation dans le pire cas est la meilleure possible
    - z : vecteur image de x
    """
    #Recuperation des valeurs à l'optimum dans le scenario 1 et 2
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

def affichageMinMaxRegret(x_opt,z_opt,t_opt):
    """
    Affiche le resultat de la resolution du programme lineaire pour le critere minmax regret
    """

    print("-----------------------------------------")
    print("-----------------------------------------")
    print(f"Solution optimale x'* : {x_opt}")
    print(f"Vecteur image z(x'*) : {z_opt}")
    print(f"Valeur de la fonction objectif g(x'*) : {t_opt}")
    print("-----------------------------------------")
    print("-----------------------------------------")

def MinMaxRegret(models, vars):
    """Application du critère MinMax Regret pour la resolution d'un probleme generalise
    Args:
        models (list) : liste de modeles
        vars (list) : liste de variables associees au modeles
    Returns:
    - x : solution optimal du probleme generalise au sens du maxmin
    - t : solution dont l'evaluation dans le pire cas est la meilleure possible
    - z : vecteur image de x
    """
    #Recuperation des valeurs des variables a l'optimum
    _,objs = solveGen(models,vars)

    #Definition du problème de l'exemple 1
    A,B,C = extractABC(models,vars)

    #nombre de variable
    p = len(vars[0])
    n = len(C)

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
    m.update()
    #Definition des contraintes
    for i in range(n):
        m.addConstr(t>= objs[i]- quicksum(C[i][j]*x[j] for j in range(p)))
    m.addConstr(quicksum(A[i]*x[i] for i in range(p))<= B[0])
    m.update()
    #Resolution
    m.optimize()

    x_opt = [round(var.x) for var in x]
    z_opt = [int(sum(C[i][j] * x_opt[j] for j in range(p))) for i in range(n)]
    t_opt = t.x
    
    return x_opt,z_opt,t_opt

def find_minmax_path(G,d,a):
    """Application du critère minlax regret pour la recherche d'un chemin robuste

    Args:
        G (tuple): graphe
        d (char): sommet de depart
        a (char): sommet d'arrivee
    Returns:
        path: liste des aretes du plus court chemin trouve
        total_cost: cout total du plus court chemin        
    """
    V,A =G
    m= Model("minmax_path")
    m.setParam('OutputFlag',0)
    #recuperation du nombre de scenarios
    S= len(next(iter(A.values())))

    #ajout des variables pour les arcs
    x= {}
    for (i,j) in  A:
        x[(i,j)] = m.addVar(vtype=GRB.BINARY,lb=0, name=f"x_{i}_{j}")
    m.update()
    #variable pour le critère
    y = m.addVar(vtype=GRB.CONTINUOUS,lb= -GRB.INFINITY, name="y")
    m.update()
    #definition de l'objectif
    m.setObjective(y, GRB.MINIMIZE)
    m.update()

    #contraintes pour s'assurer que c'est un chemin realisable
    for v in V:
        in_v = get_in(G,v)
        out_v = get_out(G,v)

        if v == d:  # Sommet de depart
            m.addConstr(
                quicksum(x[arc] for arc in out_v) == 1
            )
        elif v == a:  # Sommet d'arrivee
            m.addConstr(
                quicksum(x[arc] for arc in in_v ) == 1
            )
        else: 
            m.addConstr(
                quicksum(x[arc] for arc in out_v) -
                quicksum(x[arc] for arc in in_v) == 0
            )
    m.update()  

    # contraintes pour s'assurer que c'est un maximum
    for s in range(S):
        #recuperation du cout du plus court chemin dans le scenario s
        _,cost_star = find_shortest_path(G,s,d,a)
        m.addConstr((y>= -(cost_star - quicksum(A[arc][s]*x[arc] for arc in A))))
    m.update()

    m.optimize()

    path= [arc for arc in A if x[arc].X>0.5]
    total_costs= [sum([A[arc][s] for arc in path]) for s in range(S)]
    obj = m.ObjVal

    return path, total_costs, obj
    
