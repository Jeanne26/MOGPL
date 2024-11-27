from gurobipy import *


def dual(z,k):
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
    m.write(f"model{k}.lp")
    
    m.optimize()
    v_opt = [var.x for var in v]
    z_opt = k*v_opt[0] - sum(v_opt[1:])

    return v_opt,z_opt


def find_composantes(z):
    c = []
    for k in range(1,len(z)+1):
        _,z_opt = dual(z,k)
        c.append(z_opt)
    return c