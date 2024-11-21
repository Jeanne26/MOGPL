from gurobipy import *
import numpy as np
from pylab import plot, show
from exo1 import createExemple1


#Definition du problème 1

A,B,C1,C2,n,p,q = createExemple1()

#Coefficient fonction objectif critère maxmin
C= np.stack((C1,C2),axis= 1 )

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


#affichage des resultat
x_opt = [round(x[j].x) for j in range(10)]
t_opt = t.x
z_opt = [int(sum(C[j][i] * x_opt[j] for j in range(10))) for i in range(2)]
print(f"Solution optimale x* : {x_opt}")
print(f"Valeur minimale (t*) : {t_opt}")
print(f"Valeur minimale (z*) : {z_opt}")

