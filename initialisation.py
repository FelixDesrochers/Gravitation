'''
Ce fichier sert à initialiser la position des planètes. On y crée des listes de configurations initiales afin de le utiliser dans le programme
principal projet.py
'''
import numpy as np
from projet import Planet

#Définition des constantes
masse_terre = 5.9722*(10)**24
rayon_terre = 6378.137 *(10)**3


#####################################################
#Configuration 1: corps central et orbite stable
planete1 = Planet(100*masse_terre,rayon_terre/3,0,0,0,0, 'Montréal')
planete2 = Planet(masse_terre,rayon_terre/10,5000*10**3,0,0,100000, 'Laval')
liste_11 = [planete1, planete2]

planete1 = Planet(masse_terre,rayon_terre/10,0,0,30000,20000, 'laval')
planete2 = Planet(masse_terre,rayon_terre/10,3000*10**3,0,-30000,20000, 'Montréal')
liste_12 = [planete1, planete2]


#####################################################
#Configuration 2: trois planètes
planete1 = Planet(10*masse_terre,rayon_terre/10,1000*10**3,0,10000,10000, 'terre')
planete2 = Planet(10*masse_terre,rayon_terre/10,-5000*10**3,-5000*10**3,10000,-10000, 'terre2')
planete3 = Planet(10*masse_terre,rayon_terre/10,-5000*10**3,5000*10**3,-10000,-10000, 'terre3')
liste_2 = [planete1, planete2, planete3]


#####################################################
#Configuration 3: quatres planètes

planete1 = Planet(masse_terre,rayon_terre/10,2000*10**3,2000*10**3,-8000,0, "zebulon")
planete2 = Planet(masse_terre,rayon_terre/10,2000*10**3,-2000*10**3,0,8000, "l'étoile de la mort")
planete3 = Planet(masse_terre,rayon_terre/10,-2000*10**3,2000*10**3,0,-8000, 'Gatineau-78')
planete4 = Planet(masse_terre,rayon_terre/10,-2000*10**3,-2000*10**3,8000,0, 'La Poune')

liste_3 = [planete1, planete2, planete3, planete4]


#####################################################
#Configuration 4: 50 planètes

abs_liste = np.vectorize(abs)

# 1) Masse:
masse = abs_liste(np.random.normal(5*masse_terre,2*masse_terre,50))

# 2) Rayon:
rayon = abs_liste(np.random.normal(rayon_terre/10,rayon_terre/30,50))

# 3) Position
x = np.random.rand(50)*2*10**7 - 10**7
y = np.random.rand(50)*2*10**7 - 10**7

# 4) Vitesse
vx = np.random.normal(0,15000,50)
vy = np.random.normal(0,15000,50)

# 5) Création des planètes
liste_4 = [Planet(masse, rayon, x, y, vx, vy, 'Planète {}'.format(i)) for masse,rayon,x,y,vx,vy,i in zip(masse,rayon,x,y,vx,vy,range(1,len(masse)+1))]
