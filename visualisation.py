import matplotlib.pyplot as plt
from pb_sac_a_dos import solveExemple1, variableExemple1,modelGen
from maxmin import solve_MaxMin,find_maxmin_path
from minmaxregret import solve_MinMaxRegret,find_minmax_path
from maxOWA import find_maxOWA_path
from minOWA import find_minOWA_path
from utils_graphe import genGraph, find_shortest_path
import numpy as np
import time


def visualisation_Ex1():
    """Representation dans le plan des differentes solutions de l'exemple 1
    """
    _,_,C1,C2= variableExemple1()

    #Recuperation des coordonnees des point
    x1_star, x2_star, z1_x1_star,z2_x2_star = solveExemple1()
    z2_x1_star = sum([x1_star[i]*C2[i] for i in range(len(x1_star)) ])
    z1_x2_star = sum([x2_star[i]*C1[i] for i in range(len(x2_star)) ])

    _,z_x_star,_ = solve_MaxMin()

    _,z_x_star_prime,_ = solve_MinMaxRegret()

    z1 = [z1_x1_star, z1_x2_star, z_x_star[0], z_x_star_prime[0]]
    z2 = [z2_x1_star, z2_x2_star, z_x_star[1], z_x_star_prime[1]]

    print(z1[0], z2[0])
    print(z1[1], z2[1])

    plt.scatter(z1[0], z2[0], color='red', label= r'$z(x_1^*)$ solution optimale dans le scénario 1')
    plt.scatter(z1[1], z2[1], color='blue', label= r'$z(x_2^*)$ solution optimale dans le scénario 2')
    plt.scatter(z1[2], z2[2], color='green', label= r'$z(x^*)$ critère maxmin')
    plt.scatter(z1[3], z2[3], color='orange', label= r"$z(x^*')$ critère minmax regret")
    plt.plot([z1[0], z1[1]], [z2[0], z2[1]], alpha = 0.3, color='purple', linestyle='--')


    plt.xlabel(r'$z_1(x)$')
    plt.ylabel(r'$z_2(x)$')
    # plt.title('Représentation des solutions dans le plan $(z_1, z_2)$')
    plt.legend()

    plt.grid(True)
    plt.show()

def etude_evo_tps(crit1, crit2):
    """Étude de l'évolution du temps de résolution en fonction de n et p 

    Args:
        crit1 (function) : premier critere pour la comparaison
        crit2 (function) : deuxieme critere pour la comparaison
    """
    n_values = [5, 10, 15]
    p_values = [10, 15, 20]

    # init list temps moyen
    avg_times1 = []
    avg_times2 = []

    for i in n_values:
        for j in p_values:
            print("\n--------------")
            print(f"\nÉtude pour n = {i}, p = {j}")
            times1 = []
            times2 = []

            for _ in range(10):
                # generation des modeles
                models, variables = modelGen(i, j)
                
                # premier critere
                start_time = time.time()
                crit1(models, variables)
                chrono1 = time.time() - start_time
                times1.append(chrono1)
                
                #second critere
                start_time = time.time()
                crit2(models, variables)
                chrono2 = time.time() - start_time
                times2.append(chrono2)

            # Calcul temps moyen pour chaque critere
            avg_time1 = np.mean(times1)
            avg_time2 = np.mean(times2)
            
            #ajout du temps moyen au tableau de tous les temps moyen
            avg_times1.append(avg_time1)
            avg_times2.append(avg_time2)

            print(f"  Temps moyen {crit1.__name__}: {avg_time1:.4f} secondes")
            print(f"  Temps moyen {crit2.__name__}: {avg_time2:.4f} secondes")
    
    # reshape des tableaux pour la visualisation
    avg_times1 = np.array(avg_times1).reshape(len(n_values), len(p_values))
    avg_times2 = np.array(avg_times2).reshape(len(n_values), len(p_values))

    # creation des figures
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))

    # temps moyen maximin
    cax1 = ax[0].imshow(avg_times1, interpolation='nearest', cmap='viridis')
    ax[0].set_title(f"Temps moyen avec le critère {crit1.__name__}")
    ax[0].set_xticks(np.arange(len(p_values)))
    ax[0].set_yticks(np.arange(len(n_values)))
    ax[0].set_xticklabels(p_values)
    ax[0].set_yticklabels(n_values)
    ax[0].set_xlabel("p")
    ax[0].set_ylabel("n")
    fig.colorbar(cax1, ax=ax[0])

    # temps moyen minmax
    cax2 = ax[1].imshow(avg_times2, interpolation='nearest', cmap='viridis')
    ax[1].set_title(f"Temps moyen avec le critère {crit2.__name__}")
    ax[1].set_xticks(np.arange(len(p_values)))
    ax[1].set_yticks(np.arange(len(n_values)))
    ax[1].set_xticklabels(p_values)
    ax[1].set_yticklabels(n_values)
    ax[1].set_xlabel("p")
    ax[1].set_ylabel("n")
    fig.colorbar(cax2, ax=ax[1])

    # affichage
    plt.show()
    return 



def etude_evo_tps_path():
    """Étude de l'évolution du temps de résolution du problème du plus court chemin pour les 4 critères étudiés
    en fonction du nombre de scénarios du nombre de noeuds des graphes
    """
    n_values = [2,5,10]
    p_values = [10, 15, 20]

    # init list temps moyen
    avg_times1 = []
    avg_times2 = []
    avg_times3 = []
    avg_times4 = []

    for i in n_values:
        for j in p_values:
            print("\n--------------")
            print(f"\nÉtude pour n = {i}, p = {j}")
            times1 = []
            times2 = []
            times3 = []
            times4 = []

            for _ in range(10):

                #le while permet de generer un nouveau graphe si il n'existe pas de chemin entre V[0] et V[-1]
                existe_chemin = False
                while not existe_chemin:
                    V, A = genGraph(i, j)
                    try:
                        # Vérifier l'existence d'un chemin entre V[0] et V[-1] pour le premier scénario (s=0)
                        _,_ = find_shortest_path((V, A), 0, V[0], V[-1])
                        existe_chemin = True
                    except Exception as e:
                        print(f"Aucun chemin trouvé ({e}). Génération d'un nouveau graphe...")

                # maxmin
                start_time = time.time()
                _,_,_= find_maxmin_path((V,A), V[0],V[-1])
                chrono1 = time.time() - start_time
                times1.append(chrono1)
                
                #minmax
                start_time = time.time()
                _,_,_= find_minmax_path((V,A), V[0],V[-1])
                chrono2 = time.time() - start_time
                times2.append(chrono2)

                w = [j-k for k in range(j)]
                #maxOWA
                start_time = time.time()
                _,_,_= find_maxOWA_path((V,A), V[0],V[-1],w)
                chrono3 = time.time() - start_time
                times3.append(chrono3)

                #minOWA
                start_time = time.time()
                _,_,_= find_minOWA_path((V,A), V[0],V[-1],w)
                chrono4 = time.time() - start_time
                times4.append(chrono4)


            # Calcul temps moyen pour chaque critere
            avg_time1 = np.mean(times1)
            avg_time2 = np.mean(times2)
            avg_time3 = np.mean(times3)
            avg_time4 = np.mean(times4)
            
            #ajout du temps moyen au tableau de tous les temps moyen
            avg_times1.append(avg_time1)
            avg_times2.append(avg_time2)
            avg_times3.append(avg_time3)
            avg_times4.append(avg_time4)

            print(f"  Temps moyen critère MinMax: {avg_time1:.4f} secondes")
            print(f"  Temps moyen MaxMin regret: {avg_time2:.4f} secondes")
            print(f"  Temps moyen MaxOWA: {avg_time3:.4f} secondes")
            print(f"  Temps moyen MinOWA : {avg_time4:.4f} secondes")
    
    # reshape des tableaux pour la visualisation
    avg_times1 = np.array(avg_times1).reshape(len(n_values), len(p_values))
    avg_times2 = np.array(avg_times2).reshape(len(n_values), len(p_values))
    avg_times3 = np.array(avg_times3).reshape(len(n_values), len(p_values))
    avg_times4 = np.array(avg_times3).reshape(len(n_values), len(p_values))

    # creation des figures
    fig, ax = plt.subplots(2, 2, figsize=(20, 12))

    # temps moyen maximin
    cax1 = ax[0,0].imshow(avg_times1, interpolation='nearest', cmap='viridis')
    ax[0,0].set_title(f"Temps moyen avec le critère MaxMin")
    ax[0,0].set_xticks(np.arange(len(p_values)))
    ax[0,0].set_yticks(np.arange(len(n_values)))
    ax[0,0].set_xticklabels(p_values)
    ax[0,0].set_yticklabels(n_values)
    ax[0,0].set_xlabel("p")
    ax[0,0].set_ylabel("n")
    fig.colorbar(cax1, ax=ax[0,0])

    # temps moyen minmax
    cax2 = ax[0,1].imshow(avg_times2, interpolation='nearest', cmap='viridis')
    ax[0,1].set_title(f"Temps moyen avec le critère MinMax")
    ax[0,1].set_xticks(np.arange(len(p_values)))
    ax[0,1].set_yticks(np.arange(len(n_values)))
    ax[0,1].set_xticklabels(p_values)
    ax[0,1].set_yticklabels(n_values)
    ax[0,1].set_xlabel("p")
    ax[0,1].set_ylabel("n")
    fig.colorbar(cax2, ax=ax[0,1])

    # temps moyen maxOWA
    cax3 = ax[1,0].imshow(avg_times3, interpolation='nearest', cmap='viridis')
    ax[1,0].set_title(f"Temps moyen avec le critère MaxOWA")
    ax[1,0].set_xticks(np.arange(len(p_values)))
    ax[1,0].set_yticks(np.arange(len(n_values)))
    ax[1,0].set_xticklabels(p_values)
    ax[1,0].set_yticklabels(n_values)
    ax[1,0].set_xlabel("p")
    ax[1,0].set_ylabel("n")
    fig.colorbar(cax3, ax=ax[1,0])

    # temps moyen minOWA
    cax4 = ax[1,1].imshow(avg_times4, interpolation='nearest', cmap='viridis')
    ax[1,1].set_title(f"Temps moyen avec le critère MinOWA")
    ax[1,1].set_xticks(np.arange(len(p_values)))
    ax[1,1].set_yticks(np.arange(len(n_values)))
    ax[1,1].set_xticklabels(p_values)
    ax[1,1].set_yticklabels(n_values)
    ax[1,1].set_xlabel("p")
    ax[1,1].set_ylabel("n")
    fig.colorbar(cax4, ax=ax[1,1])


    # affichage
    plt.show()
    return 

