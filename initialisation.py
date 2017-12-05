'''
Ce fichier sert à initialiser la position des planètes. On y crée des listes de configurations initiales afin de le utiliser dans le programme
principal projet.py
'''
import numpy as np
from projet import planet

#Définition des constantes
masse_terre = 5.9722*(10)**24
rayon_terre = 6378.137 *(10)**3
densitee_terre = (masse_terre)/((4*np.pi*rayon_terre**3)/3)


#####################################################
#Configuration 1: corps central et orbite stable
planete1 = planet(100*masse_terre,rayon_terre/3,0,0,0,0, 'Beach Club')
planete2 = planet(masse_terre,rayon_terre/10,5000*10**3,0,0,100000, 'Laval')
liste_11 = [planete1, planete2]

planete1 = planet(masse_terre,rayon_terre/10,0,0,30000,20000, 'laval')
planete2 = planet(masse_terre,rayon_terre/10,3000*10**3,0,-30000,20000, 'Montréal')
liste_12 = [planete1, planete2]


#####################################################
#Configuration 2: trois planètes
planete1 = planet(10*masse_terre,rayon_terre/10,1000*10**3,0,10000,10000, 'terre')
planete2 = planet(10*masse_terre,rayon_terre/10,-5000*10**3,-5000*10**3,10000,-10000, 'terre2')
planete3 = planet(10*masse_terre,rayon_terre/10,-5000*10**3,5000*10**3,-10000,-10000, 'terre3')
liste_2 = [planete1, planete2, planete3]


#####################################################
#Configuration 3: quatres planètes

planete1 = planet(masse_terre,rayon_terre/100,2000*10**3,2000*10**3,-8000,0, "zebulon")
planete2 = planet(masse_terre,rayon_terre/100,2000*10**3,-2000*10**3,0,8000, "l'étoile de la mort")
planete3 = planet(masse_terre,rayon_terre/100,-2000*10**3,2000*10**3,0,-8000, 'Gatineau-78')
planete4 = planet(masse_terre,rayon_terre/100,-2000*10**3,-2000*10**3,8000,0, 'La Poune')

liste_3 = [planete1, planete2, planete3, planete4]


#####################################################
#Configuration 4: 100 planètes

abs_liste = np.vectorize(abs)

# 1) Masse:
masse = abs_liste(np.random.normal(4200,1050,200))

# 2) Rayon:
rayon = [(((3*m)/(densitee_terre * 4 * np.pi))**(1/3))/150 for m in masse]

#rayon = abs_liste(np.random.normal(rayon_terre/100,rayon_terre/170,100))

# 3) Position
x = np.random.rand(200)*2*10**7 - (10**7)
y = np.random.rand(200)*2*10**7 - (10**7)

# 4) Vitesse
vx = np.random.normal(0,15000,200)
vy = np.random.normal(0,15000,200)

# 5) Création des planètes
liste_4 = [planet(masse, rayon, x, y, vx, vy, '{}'.format(i)) for masse,rayon,x,y,vx,vy,i in zip(masse,rayon,x,y,vx,vy,range(1,len(masse)+1))]



