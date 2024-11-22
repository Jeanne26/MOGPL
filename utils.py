
def variableExemple1():

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