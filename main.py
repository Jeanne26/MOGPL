from pb_sac_a_dos import affichageExempl1, variableGen, modelGen, solveGen, afficheGen
from maxmin import affichageMaxMin, solve_MaxMin, MaxMin, find_maxmin_path
from minmaxregret import affichageMinMaxRegret, solve_MinMaxRegret, MinMaxRegret, find_minmax_path
from visualisation import visualisation_Ex1, etude_evo_tps
from maxOWA import find_composantes, maxOWAex1,affichageMawOwa,maxOWA, find_maxOWA_path
from minOWA import minOWAex1, minOWA
from chemin_robuste import find_shortest_path
from utils_graphe import graphe_1,graphe_2

def main():
    
    print("1. Résolution de l'exemple 1 (scénarios 1 et 2)")
    print("2. Résolution avec le critère MaxMin de l'exemple 1")
    print("3. Résolution avec le critère MinMax Regret de l'exemple 1")
    print("4. Visualisation des solutions de l'exemple 1")
    print("5. Résolution d'un problème généralisé")
    print("6. Etude de l'évolution du temps de résolution en fonction de n et p (q.1.4)\n pour les critères maxmin et minmax")
    print("7. Trouver les composantes du vecteur L(2, 9, 6, 8, 5, 4)")
    print("8. Résolution exemple 1 avec le critère maxOwa")
    print("9. Résolution exemple 1 avec le critère minOwa")
    print("10. Etude de l'évolution du temps de résolution en fonction de n et p (q.1.4)\n pour les critères maxOWA et minOWA")
    print("11. Détermination du plus court chemin des graphes de l'exemple 2")
    print("12. Plus courts chemins et critères")
    choix = input("Entrez le numéro de votre choix : ")
    
    if choix == "1":
        print("\nRésolution de l'exemple 1 :")
        affichageExempl1()
        
    elif choix == "2":
        print("\nRésolution avec le critère MaxMin :")
        x,z,t = solve_MaxMin()
        affichageMaxMin(x,z,t)
    elif choix == "3":
        print("\nRésolution avec le critère MinMax Regret :")
        x,z,t = solve_MinMaxRegret()
        affichageMinMaxRegret(x,z,t)
    elif choix == "4":
        print("\nVisualisation des solutions de l'exemple 1")
        visualisation_Ex1()
    elif choix == "5":
        print("\nRésolution d'un problème généralisé :")
        pb_generalise()
    
    elif choix == "6":
        print("\nEtude de l'évolution du temps de résolution en fonction de n et p (q.1.4)")
        etude_evo_tps(MaxMin,MinMaxRegret)

    elif choix == "7":
        print("\nComposantes du vecteur L(2, 9, 6, 8, 5, 4):")
        z = [2, 9, 6, 8, 5, 4]
        c = find_composantes(z)
        print(f"\nL({z}) = (", end="")
        for i in range(len(c) - 1):
            print(f"L_{i+1} = {c[i]}", end=", ")
        print(f"L_{len(c)} = {c[-1]})")
            
    elif choix == "8":
        print("\nRésolution de l'exemple 1 avec le critère maxOWA")
        x,z,t= maxOWAex1()
        affichageMawOwa(x,z,t)

    elif choix == "9":
        print("\nRésolution de l'exemple 1 avec le critère minOWA")
        x,z,t= minOWAex1()
        affichageMawOwa(x,z,t)

    elif choix == "10":
        print("\nEtude de l'évolution du temps de résolution en fonction de n et p (q.1.4)\n pour les critères maxOWA et minOWA")
        etude_evo_tps(maxOWA,minOWA)
    
    elif choix == "11":
        plus_court_chemin_exemple2()

    elif choix == "12":
        plus_court_chemin_criteres()
    else:
        print("\nChoix invalide. Veuillez entrer un numéro entre 1 et 11.")


def pb_generalise():
    """
    Scenario pour resoudre un probleme generalise où l'utilisateur entre les parametres desires
    """
    n = int(input("nombre de scénarios (n) : "))
    p = int(input("nombre de projets (p) : "))
    
    # creation des modeles
    models, variables = modelGen(n,p)
    
    while(True):
        print("\n########################################")
        print(f"1. Résolution des {n} problèmes")
        print("2. Résolution avec le critère MaxMin")
        print("3. Résolution avec le critère MinMax Regret ")
        print("0. Quitter")
        print("\n########################################")

        choix = input("Entrez le numéro de votre choix : ")

        if choix == "1":
            print(f"\nRésolution des {n} problèmes")
            # resolution des modeles
            var_opt, objs = solveGen(models, variables)
            # affichage
            afficheGen(var_opt, objs)        

        elif choix == "2":
            print("\nRésolution avec le critère MaxMin :")
            x,z,t = MaxMin(models, variables)
            affichageMaxMin(x,z,t)

        elif choix=="3":
            print("\nRésolution avec le critère MinMax Regret :")
            x,z,t = MinMaxRegret(models, variables)
            affichageMinMaxRegret(x,z,t)

        elif choix =="0":
            break


def plus_court_chemin_exemple2():
    """Scenario pour la determination du plus court chemin de l'exemple 2
    """
    print("\n########################################")

    g = int(input("Graphe (gauche: 1, droite: 2) : "))
    s = int(input("Scénario (s: {0,1}) : "))

    if g not in {1,2} or s not in {0,1}:
        print("Les valeurs renseignées sont incompatibles")
        return

    elif g==1:
        G = graphe_1()
        path, total_time = find_shortest_path(G, s, "a", "f")
        print("---------------------------------------------")
        print(f"Plus court chemin dans le graphe {g} pour le scénario {s}")
        print("Chemin optimal :", path)
        print("Temps total :", total_time)
        print("---------------------------------------------")

    else:
        G = graphe_2()
        path, total_time = find_shortest_path(G, s, "a", "g")
        print("---------------------------------------------")
        print(f"Plus court chemin dans le graphe {g} pour le scénario {s}")
        print("Chemin optimal :", path)
        print("Temps total :", total_time)
        print("---------------------------------------------")


def plus_court_chemin_criteres():
    c = int(input("Choix du critère : \n 1:maxmin 2:minmax 3:maxOWA 4:minOWA ->"))
    g = int(input("Graphe (gauche: 1, droite: 2) : "))
    
    if g not in {1,2} or c not in {1,2,3,4}:
        print("Les valeurs renseignées sont incompatibles")
        return

    if c==1:
        print("---------------------------------------------")
        print(f"Critère maxmin pour la recherche d'un chemin robuste dans le graphe {g}")
        if g==1:
            path, costs,obj = find_maxmin_path(graphe_1(),"a","f")
        else:
            path,costs,obj = find_maxmin_path(graphe_2(),"a","g")
        print("Chemin maxmin P:", path)
        print("t(P)(critère maxmin):", costs)
        print("Valeur de la fonction objectif:" ,obj)
        print("---------------------------------------------")
    if c==2:
        print("---------------------------------------------")
        print(f"Critère minmax regret pour la recherche d'un chemin robuste dans le graphe {g}")
        if g==1:
            path, costs,obj = find_minmax_path(graphe_1(),"a","f")
        else:
            path,costs,obj = find_minmax_path(graphe_2(),"a","g")
        print("Chemin minmax P:", path)
        print("t(P)(critère minmax):", costs)
        print("Valeur de la fonction objectif:" ,obj)
        print("---------------------------------------------")
    
    if c==3:
        print("---------------------------------------------")
        print(f"Critère maxOWA pour la recherche d'un chemin robuste dans le graphe {g}\n résultat avec différentes pondérations")
        
        for k in [1,2, 4, 8, 16]:
            if g==1:
                G= graphe_1()
                a="f"
            else:
                G= graphe_2()
                a="g"
            w = [k, 1]  # Poids décroissants pour les scénarios
            path, costs, obj = find_maxOWA_path(G, "a", a, w)
            print(f"\n--- Résultats pour k = {k} ---")
            print("Chemin maxOWA P:", path)
            print("t(P):", costs)
            print("Valeur de la fonction objectif:" ,obj)
            print("---------------------------------------------")
        

if __name__ == "__main__":
    main()


