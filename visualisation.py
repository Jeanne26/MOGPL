import matplotlib.pyplot as plt
from pb_sac_a_dos import solveExemple1, variableExemple1,modelGen
from maxmin import solve_MaxMin, solve_MaxMinG
from minmaxregret import solve_MinMaxRegret, solve_MinMaxRegretG
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

def etude_evo_tps():
    """Étude de l'évolution du temps de résolution en fonction de n et p
    """
    n_values = [5, 10, 15]
    p_values = [10, 15, 20]

    # init list temps moyen
    avg_times_maxmin = []
    avg_times_minmax = []

    for i in n_values:
        for j in p_values:
            print("\n--------------")
            print(f"\nÉtude pour n = {i}, p = {j}")
            times_maxmin = []
            times_minmax = []

            for _ in range(10):
                # generation des modeles
                models, variables = modelGen(i, j)
                
                # critere MaxMin
                start_time = time.time()
                solve_MaxMinG(models, variables)
                chrono_maxmin = time.time() - start_time
                times_maxmin.append(chrono_maxmin)
                
                #critere MinMax Regret
                start_time = time.time()
                solve_MinMaxRegretG(models, variables)
                chrono_minmax = time.time() - start_time
                times_minmax.append(chrono_minmax)

            # Calcul temps moyen pour chaque critere
            avg_time_maxmin = np.mean(times_maxmin)
            avg_time_minmax = np.mean(times_minmax)
            
            #ajout du temps moyen au tableau de tous les temps moyen
            avg_times_maxmin.append(avg_time_maxmin)
            avg_times_minmax.append(avg_time_minmax)

            print(f"  Temps moyen MaxMin: {avg_time_maxmin:.4f} secondes")
            print(f"  Temps moyen MinMax Regret: {avg_time_minmax:.4f} secondes")
    
    # reshape des tableaux pour la visualisation
    avg_times_maxmin = np.array(avg_times_maxmin).reshape(len(n_values), len(p_values))
    avg_times_minmax = np.array(avg_times_minmax).reshape(len(n_values), len(p_values))

    # creation des figures
    fig, ax = plt.subplots(1, 2, figsize=(14, 6))

    # temps moyen maximin
    cax1 = ax[0].imshow(avg_times_maxmin, interpolation='nearest', cmap='viridis')
    ax[0].set_title("Temps moyen avec le critère MaxMin")
    ax[0].set_xticks(np.arange(len(p_values)))
    ax[0].set_yticks(np.arange(len(n_values)))
    ax[0].set_xticklabels(p_values)
    ax[0].set_yticklabels(n_values)
    ax[0].set_xlabel("p")
    ax[0].set_ylabel("n")
    fig.colorbar(cax1, ax=ax[0])

    # temps moyen minmax
    cax2 = ax[1].imshow(avg_times_minmax, interpolation='nearest', cmap='viridis')
    ax[1].set_title("Temps moyen avec le critère MinMax Regret")
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

