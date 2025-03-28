from gurobipy import *
import numpy as np


"""
Contient plusieurs fonctions et modèles Gurobi associés à la résolution de problèmes de sac à dos robustes.Fonctions:
    - variableExemple1 : génére les variables de l'exemple 1
    - modelExempl1 : creer les deux modèles de l'exemple 1
    - solveExemple1 : résout l'exemple 1 dans les deux scénarios
    - variableGen : génére des variables aléatoirement pour un problème de sac à dos 
    - modelGen : génére des modèles de sac à dos robuste
    - extractABC : extrait les variables d'un modèles
    - solveGen : résout les programmes linéaires d'un problème de sac à dos 

"""

def variableExemple1():
    """Definie les variables de l'exemple 1

    Returns:
       - A : matrice des contraintes
       - B : second membre
       - C1 : coefficient fonction objectif dans le scenario 1
       - C2 : coefficient fonction objectif dans le scenario 2
    """
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
    """ Creer et retourne les deux modèles qui correspondent au scenario 1 et 2 
    de l'exemple 1
    Returns:
     - m1 : modèle du scenario 1 de l'exemple 1
     - m2 : modèle du scenario 1 de l'exemple 2
     - x1 : variable du modèles m1
     - x2 : variable du modèles m2 
    """
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

    #definition des contraintes
    m1.addConstr(quicksum(A[i]*x1[i] for i in range(p)) <= B)
    m2.addConstr(quicksum(A[i]*x2[i] for i in range(p)) <= B)

    return m1, m2, x1 , x2

def solveExemple1():
    """Resout les deux programmes lineaires de l'Exemple 1 celui du scenario 1
    et du scenario deux et renvoie les valeurs à l'objectif ainsi que le vecteur de 
    consequence
    Returns:
    - x1_opt : solution optimale dans le scenario 1 de l'exemple 1
    - x2_opt : solution optimale dans le scenario 2 de l'exemple 1
    - obj1 : valeur de l'objectif à l'optimum dans le scenario 1
    - obj2 : valeur de l'objectif à l'optimum dans le scenario 2
    """
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
    """
    Affiche les resultats de la resolution des programmes lineaires de l'exercice 1
    respectivement associe au scenario 1 et 2.
    """
    x1_opt, x2_opt, obj1, obj2 = solveExemple1()
    
    print("-----------------------------------------")
    print("-----------------------------------------")
    print("")
    print("Solution optimale dans le scénario 1:")
    print("x1* :",x1_opt)
    print("")
    print('Valeur de la fonction objectif dans le scenario 1:', obj1 )

    
    print("")
    print("Solution optimale dans le scénario 2:")
    print("x2* :", x2_opt)
    print("")
    print('Valeur de la fonction objectif dans le scenario 2:', obj2)
    print("-----------------------------------------")
    print("-----------------------------------------")

def variableGen(n,p):
    """Renvoie  les variables d'un problème de sac à dos robuste en présence
    de n scénarios et p variables

    Args:
        n (int): nombre de scénarios du problème
        p (int): nombre de variable du problème
    Returns:
        A (Array): vecteur des contraintes
        B (int): second membre
        C (Array): matrice des fonctions objectifs
    """
    #matrice des contraintes du problème
    A = np.random.randint(1,101, p)
    B = np.sum(A)//2
    C= np.array([np.random.randint(1,101, p) for i in range(n)])
    return A, B, C

def modelGen(n,p):
    """ Creer et retourne n modeles correspondant au n scenarios du probleme
    Args:
        n (int) : nombre de scenarios
        p (int) : nombre de variables/projets
    Returns:
     - models (list) : liste des modeles
     - variables (list): list des variables
    """
    A,B,C = variableGen(n,p)
    #nombre de scenarios
    n= C.shape[0]
    #nombre de variables
    p = len(A)

    models= []
    variables = []
    for i in range(n):
        model = Model()
        #ajout des variables au modele
        var = [model.addVar(vtype=GRB.BINARY, name=f"x{j+1}_s{i+1}") for j in range(p)]
        model.update()
        #definition de l'objectif
        obj = LinExpr();
        obj = 0

        for j in range(p):
            obj += C[i,j]*var[j]
        model.setObjective(obj, GRB.MAXIMIZE)
        model.update()

        #ajout de la contrainte
        model.addConstr(quicksum(A[j]*var[j] for j in range(p)) <= B)
        model.update()
        models.append(model)
        variables.append(var)

    return models, variables

def extractABC(models,variables):
    """Extrait la matrice des contraintes et le second membre des problemes ainsi que la matrice
    des listes des coefficient de la fonction objectif des problemes

    Args:
        models (list): liste de modele partageant la meme matrice de contraintes
        variables (list): liste des variables associées au probleme
    Returns:
        A (list) : matrice des contraintes
        B (int) : liste qui contient l'unique variable du second membre des modeles
        C (list) : liste des listes des coefficient de la fonction objectif des problemes
    """
    #nombre de scenarios
    n = len(models)
    #nombre de variables
    p = len(variables[0])
    A = None
    B = None
    C = []

    for i, model in enumerate(models):
        # recuperation des coefficients des fonctions objectif pour le scénario i
        C.append(model.getAttr("Obj", variables[i]))

        # Si premier modele on recupere A et B, uniquement dans ce cas car A et B sont communes
        #a tous les scenarios
        if i == 0:
            #on une contrainte donc on recupere la premiere contrainte de la liste des contraintes
            constr = model.getConstrs()[0]  
            A = [model.getCoeff(constr, var) for var in variables[i]]
            #recupere le Right Hand Side de la contrainte
            B = model.RHS

    return A, B, C

def solveGen(models, variables):
    """Resout les programmes lineaires contenu dans models

    Args:
        models (list): liste de modele
        variables (list): liste des variables associees au models contenu dans models

    Returns:
        var_opt (list) : liste contenant les variables optimales des modeles
        objs (list) : liste contenant les valeurs à l'optimum de chaque modele
    """
    var_opt = []
    objs = []
    for i in range(len(models)):
        m= models[i]
        x= variables[i]

        m.setParam('OutputFlag', 0)

        m.optimize()

        x_opt =[round(var.x) for var in x]

        obj = m.ObjVal

        var_opt.append(x_opt)
        objs.append(obj)
    
    return var_opt, objs

def afficheGen(var_opt, objs):
    """_summary_

    Args:
        var_opt (list) : liste contenant les variables optimales des modeles
        objs (list) : liste contenant les valeurs à l'optimum de chaque modele
    """
    for i in range(len(var_opt)):
        print("")
        print(f"Solution optimale dans le scénario {i+1}:")
        print(f"x{i+1}* :", var_opt[i])
        print("")
        print(f'Valeur de la fonction objectif dans le scénario {i+1}:', objs[i])
        print("-----------------------------------------")
        print("-----------------------------------------")
