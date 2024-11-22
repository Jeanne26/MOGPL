from gurobipy import *
from utils import variableExemple1

def variableExemple1():
    """ Retourne la matrice de contraintes de contrainte, de second membre et les 
    matrice des fonctions objectifs du scénario 1 et 2 de l'exemple 1, ainsi que le
    nombre de scénarios, variables et contraintes du problème"""
    #Matrice des contraintes
    A=[60,10,15,20,25,20,5,15,20,60]

    #Second membre
    B= 100

    #fonction objectif scenario 1
    C1 = [70,18,16,14,12,10,8,6,4,2]
    #fonction objectif scenario 2
    C2 = [2,4,6,8,10,12,14,16,18,70]
    
    return A,B,C1,C2


def modelExemple1():
    """Créer et retourne les deux modèles qui correspondent au scénario 1 et 2 
    de l'exemple 1"""
    A,B,C1,C2 = variableExemple1()

    m1 = Model("scenario 1")
    m2 = Model("scenario 2")
    p= len(C1)
    #declaration variables de decision
    x1 = []
    for i in range(p):
        x1.append(m1.addVar(vtype=GRB.BINARY, name="x%d" % (i+1)))
    x2 = []
    for i in range(p):
        x2.append(m2.addVar(vtype=GRB.BINARY, name="x%d" % (i+1)))
    m1.update()
    m2.update()

    #definition de l'objectif en fonction du scenario choisis
    obj1 = LinExpr();
    obj2 = LinExpr();

    obj1 = 0
    obj2 = 0

    for j in range(p):
        obj1 += C1[j]*x1[j]
        obj2 += C2[j]*x2[j]

    m1.setObjective(obj1, GRB.MAXIMIZE)
    m2.setObjective(obj2, GRB.MAXIMIZE)

    #definition des contrainte
    m1.addConstr(quicksum(A[i]*x1[i] for i in range(p)) <= B)
    m2.addConstr(quicksum(A[i]*x2[i] for i in range(p)) <= B)

    return m1, m2, x1 , x2



def solveExemple1():
    """Résout les deux programmes linéaires de l'Exemple 1 celui du scénario 1
    et du scénario deux et renvoie les valeurs à l'objectif ainsi que le vecteur de 
    conséquence"""
    m1,m2,x1,x2= modelExemple1()

    #evite l'affichage des logs
    m1.setParam('OutputFlag', 0)
    m2.setParam('OutputFlag', 0)
    #Resolution
    m1.optimize()
    m2.optimize()
    
    #recuperation solution optimal
    x1_opt = [round(var.x) for var in x1]
    x2_opt = [round(var.x) for var in x2]


    #recuperation du vecteur de consequence optimal
    obj1 = m1.ObjVal
    obj2 = m2.ObjVal

    return x1_opt, x2_opt, obj1, obj2


def affichageExempl1():
    x1_opt, x2_opt, obj1, obj2 = solveExemple1()
    
    print("-----------------------------------------")
    print("-----------------------------------------")
    print("")
    print("Solution optimale dans le scenario 1:")
    print(x1_opt)
    print("")
    print('Valeur de la fonction objectif dans le scenario 1:', obj1 )

    
    print("")
    print("Solution optimale dans le scenario 2:")
    print(x2_opt)
    print("")
    print('Valeur de la fonction objectif :', obj2)
    print("-----------------------------------------")
    print("-----------------------------------------")

