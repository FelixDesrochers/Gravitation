import numpy as np
from code_efficace import Planet

#Définition des constantes
masse_terre = 5.9722*(10)**24
rayon_terre = 6378.137 *(10)**3
densitee_terre = (masse_terre)/((4*np.pi*rayon_terre**3)/3)

#Définition d'une fonction pour évaluer la valeur absolue d'une liste
abs_liste = np.vectorize(abs)

#Définition des constantes pour la position des planètes
Rayon = 10**7

#Définition des valeurs désirées
nbr_planetes = 200
masse_moyenne = 4 * masse_terre
vitesse_moyenne = 22000
moment_ang_moyen = 1e+35

#Définition de la liste de planètes
# 1) Masse:
masse = np.array(abs_liste(np.random.normal(masse_moyenne, masse_moyenne/3, nbr_planetes)))
masse = masse * (masse_moyenne/masse.mean())

# 2) Rayon:
rayon = [(((3*m)/(densitee_terre * 4 * np.pi))**(1/3))/150 for m in masse]

# 3) Position
dist = np.random.rand(nbr_planetes) * Rayon
angle = np.random.rand(nbr_planetes) * 2 * np.pi

x = [ d * np.cos(theta) for d,theta in zip(dist,angle) ]
y = [ d * np.sin(theta) for d,theta in zip(dist,angle) ]

# 4) Vitesse
vitesse = np.random.normal(vitesse_moyenne, vitesse_moyenne/3, nbr_planetes)
vitesse = vitesse * (vitesse_moyenne/vitesse.mean())
angle2 = np.random.rand(nbr_planetes) * 2 * np.pi

vx = [ v * np.cos(theta) for v,theta in zip(vitesse,angle2) ]
vy = [ v * np.sin(theta) for v,theta in zip(vitesse,angle2) ]

# 5) Moment angulaire selon z
moment_ang = np.random.normal(moment_ang_moyen,abs(moment_ang_moyen/3),nbr_planetes)
angle3 = np.random.rand(nbr_planetes)* 2 *np.pi
V = [lz/(m*d*np.sin(theta)) for lz,m,d,theta in zip(moment_ang,masse,dist,angle3)]

vx = [v*np.cos(theta1+theta2) for v,theta1,theta2 in zip(V,angle,angle3)]
vy = [v*np.sin(theta1+theta2) for v,theta1,theta2 in zip(V,angle,angle3)]


# 6) Création des planètes
liste_planetes = [Planet(masse, rayon, x, y, vx, vy, '{}'.format(i)) for masse,rayon,x,y,vx,vy,i in zip(masse,rayon,x,y,vx,vy,range(1,len(masse)+1))]

