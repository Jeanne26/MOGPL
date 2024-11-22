import matplotlib.pyplot as plt
from exo1 import solveExemple1, variableExemple1
from maxmin import solve_MaxMin
from minmaxregret import solve_MinMaxRegret

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
plt.title('Représentation des solutions dans le plan $(z_1, z_2)$')
plt.legend()

plt.grid(True)
plt.show()