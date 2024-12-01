from gurobipy import *
from utils_graphe import get_in,get_out, graphe_2


def find_shortest_path(G, s,d,a):
    """"
    Retourne le chemin le plus rapide de d à a du graphe G dans le scenario s
    Args:
        G (tuple) : graphe
        s (int) : numero du scenario
        d (char) : sommet de depart 
        a (char) : sommet d'arrivee
    Returns:
        path: liste des aretes du plus court chemin trouve
        total_cost: cout total du plus court chemin
    """
    V,A=G
    path = []
    m= Model("short_path")
    m.setParam('OutputFlag', 0)

    #une variable par arc
    x={}
    for (i, j) in A:
        x[(i, j)] = m.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")
    m.update()

    #definition de l'objectif
    m.setObjective(
        quicksum(A[(i, j)][s] * x[(i, j)] for (i, j) in A),
        GRB.MINIMIZE
    )
    m.update()

    for i in range(len(V)):
        if V[i] == d or V[i]==a:
            continue
        entrant = []
        sortant=[]

    #contraintes de conservation du flot
    for s in V:
        in_s = get_in(G,s)
        out_s = get_out(G,s)

        if s == d:  # Sommet de depart
            m.addConstr(
                quicksum(x[arc] for arc in out_s) == 1)
        elif s == a:  # Sommet d'arrivee
            m.addConstr(
                quicksum(x[arc] for arc in in_s ) == 1
            )
        else: 
            m.addConstr(
                quicksum(x[arc] for arc in out_s) -
                quicksum(x[arc] for arc in in_s) == 0
            )
    m.update()

    m.optimize()


    path = [arc for arc in A if x[arc].x > 0]
    total_cost= m.ObjVal

    return path, total_cost


