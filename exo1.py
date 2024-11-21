from gurobipy import *


def createExemple1():

    #Matrice des contraintes
    A=[60,10,15,20,25,20,5,15,20,60]

    #Second membre
    B= 100

    #fonction objectif scenario 1
    C1 = [70,18,16,14,12,10,8,6,4,2]
    #fonction objectif scenario 2
    C2 = [2,4,6,8,10,12,14,16,18,70]
    
    #nombre de scénario
    n= 2
    #nombre de variables du problème d'origine
    p=10
    #nombre de contraintes du problème d'origine
    q=1
    return A,B,C1,C2, n, p,q

A,B,C1,C2,n,p,q = createExemple1()


m1 = Model("scenario 1")
m2 = Model("scenario 2")

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

#Resolution
m1.optimize()
m2.optimize()
print("")
print("Solution optimale dans le scenario 1:")
for j in range(p):
    print('x%d'%(j+1), '=', x1[j].x)
print("")
print('Valeur de la fonction objectif dans le scenario 2:', m1.objVal)

   
print("")
print("Solution optimale dans le scenario 2:")
for j in range(p):
    print('x%d'%(j+1), '=', x2[j].x)
print("")
print('Valeur de la fonction objectif :', m2.objVal)

