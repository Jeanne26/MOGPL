from pb_sac_a_dos import affichageExempl1, variableGen, modelGen, solveGen, afficheGen
from maxmin import affichageMaxMin, solve_MaxMin, solve_MaxMinG
from minmaxregret import affichageMaxMin as affichageMinMaxRegret
from visualisation import visualisation_Ex1


def main():
    
    print("1. Résolution de l'exemple 1 (scénarios 1 et 2)")
    print("2. Résolution avec le critère MaxMin de l'exemple 1")
    print("3. Résolution avec le critère MinMax Regret de l'exemple 1")
    print("4. Visualisation des solutions de l'exemple 1")
    print("5. Résolution d'un problème généralisé")
    
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
        affichageMinMaxRegret()
    elif choix == "4":
        print("\nVisualisation des solutions de l'exemple 1")
        visualisation_Ex1()
    elif choix == "5":
        print("\nRésolution d'un problème généralisé :")
        pb_generalise()

    else:
        print("\nChoix invalide. Veuillez entrer un numéro entre 1 et 5.")

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
        # print("3. Résolution avec le critère MinMax Regret ")
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
            x,z,t = solve_MaxMinG(models, variables)
            affichageMaxMin(x,z,t)

        elif choix =="0":
            break

    
    # affichage
    afficheGen(var_opt, objs)


if __name__ == "__main__":
    main()
