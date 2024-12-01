from gurobipy import *
import random

def graphe_1():
    """Retourne le graphe de gauche de l'exemple 2

    Returns:
        tuple: G: V (list): ensemble des sommets du graphe
                  A (dict): ensemble des aretes du graphe
    """
    #liste des sommets
    V= ["a","b","c","d","e","f"]
    #dictionnaire des aretes
    A = dict()
    A[("a","b")]= [4,3]
    A[("a","c")]= [5,1]
    A[("b","c")]= [2,1]
    A[("b","e")]= [2,2]
    A[("b","f")]= [7,5]
    A[("b","d")]= [1,4]
    A[("c","e")]= [2,7]
    A[("c","d")]= [5,1]
    A[("d","f")]= [3,2]
    A[("e","f")]= [5,2]

    return (V, A)

def graphe_2():
    """Retourne le graphe de gauche de l'exemple 2

    Returns:
        tuple: G: V (list): ensemble des sommets du graphe
                  A (dict): ensemble des aretes du graphe
    """
    #liste des sommets
    V= ["a","b","c","d","e","f","g"]
    #dictionnaire des aretes
    A = dict()
    A[("a","b")]= [5, 3]
    A[("a","c")]= [10, 4]
    A[("a","d")]= [2, 6]
    A[("b","d")]= [1, 3]
    A[("b","c")]= [4, 2]
    A[("b","e")]= [4, 6]
    A[("c","e")]= [3, 1]
    A[("c","f")]= [1, 2]
    A[("d","c")]= [1, 4]
    A[("d","f")]= [3, 5]
    A[("e","g")]= [1, 1]
    A[("f","g")]= [1, 1]


    return (V, A)


def get_out(G,s):
    """retourne la liste de toutes les aretes sortantes de s

    Args:
        s (char): sommet
        G (dict) : graphe

    Returns:
        out (list) : liste de toutes les aretes sortantes de s
    """
    (V,A) = G
    out_s= []
    for (i,j) in A.keys():
        if i==s:
            out_s.append((i,j))

    return out_s



def get_in(G,s):
    """retourne la liste de toutes les aretes entrantes de s

    Args:
        s (char): sommet
        G (dict) : graphe

    Returns:
        out (list) : liste de toutes les aretes entrantes de s
    """
    (V,A) = G
    out_s= []
    for (i,j) in A.keys():
        if j==s:
            out_s.append((i,j))

    return out_s


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




def genGraph(n, p):
    """
    Genere un graphe aleatoire avec n scenario et p noeuds

    Args:
        n (int): Le nombre de scénarios.
        p (int): Le nombre de nœuds du graphe.
    
    Returns:
        tuple: Un tuple contenant :
            - V (list): Liste des nœuds du graphe.
            - A (dict): Dictionnaire des arcs et de leurs coûts pour chaque scénario.
    """
    V = [chr(i) for i in range(97, 97 + p)]  # 'a', 'b', ..., jusqu'à 'p'
    
    # Initialisation des arcs
    A = {}

    #choix du nombre d'arc dans le graphe
    nb_arcs = random.randint(int(0.3 * p * (p - 1)), int(0.5 * p * (p - 1))) 
    #creer la liste de tous les arcs possibles
    all_arcs = [(u, v) for u in V for v in V if u != v]
    #melange la liste
    random.shuffle(all_arcs)
    
    # choix de nb_arcs parmis tous les arcs possibles
    chosen_arcs = all_arcs[:nb_arcs]
    
    # Remplir le dictionnaire des arcs avec des coûts pour chaque scénario
    for (u, v) in chosen_arcs:
        A[(u, v)] = [random.randint(1, 100) for _ in range(n)]  # Tirer un coût pour chaque scénario

    return V, A



