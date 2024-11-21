from gurobipy import *
from numpy import arange,array,ones,linalg,sum
from pylab import plot, show


#Matrice des contraintes
A=[60,10,15,20,25,20,5,15,20,60]
#Second membre
B= 100
#Coefficient des fonctions objectif des différents scénarios
C= [[70,2],
    [18,4],
    [16,6],
    [14,8],
    [12,10],
    [10,12],
    [8,14],
    [6,16],
    [4,18],
    [2,70]]

#nombre de scénario
n= 2
#nombre de variables du problème d'origine
p=10
#nombre de contraintes du problème d'origine
q=1
m= Model("MaxMin")

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

print("")
print("Solution optimale:")
for j in range(p):
    print("x%d"%(j+1), " = ", x[j].x )
print("")
print("Valeur de la fonction objectif:", m.ObjVal)