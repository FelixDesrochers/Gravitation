'''
Ce fichier sers à initialiser la position des planètes. On y crée des listes de configurations initiales afin de le utiliser dans le programme
principal projet.py
'''

from projet import Planet

#Définition des constantes
masse_terre = 5.9722*(10)**24
rayon_terre = 6378.137 *(10)**3


#Configuration 1: corps central et orbite stable
planete1 = Planet(100*masse_terre,rayon_terre,0,0,0,20000)
planete2 = Planet(masse_terre,rayon_terre,5000*10**3,0,-5000,0)
liste_1 = [planete1, planete2]


#Configuration 2: trois planètes
planete1 = Planet(masse_terre,rayon_terre,1000*10**3,0,4000,4000)
planete2 = Planet(masse_terre,rayon_terre,-5000*10**3,-5000*10**3,4000,-4000)
planete3 = Planet(masse_terre,rayon_terre,-5000*10**3,5000*10**3,-4000,-4000)
liste_2 = [planete1, planete2, planete3]


#Configuration 3: quatres planètes
planete1 = Planet(masse_terre,rayon_terre,3000*10**3,3000*10**3,-8000,0)
planete2 = Planet(masse_terre,rayon_terre,3000*10**3,-3000*10**3,0,8000)
planete3 = Planet(masse_terre,rayon_terre,-3000*10**3,3000*10**3,0,-8000)
planete4 = Planet(masse_terre,rayon_terre,-3000*10**3,-3000*10**3,8000,0)
liste_3 = [planete1, planete2, planete3, planete4]
