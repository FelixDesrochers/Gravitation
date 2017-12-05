from code_efficace import *
from init_parametres2 import *
import numpy as np
import sys

##########################################
#     Définition des valeurs désirées    #
##########################################
dist_max = 10**7 #rayon du cercle dans lequel toutes les planètes sont situées
nbr_planetes = 200
masse_moyenne =  3*masse_terre
vitesse_moyenne = 25000
moment_ang_moyen = 2e+33

#Définition de la liste de planètes
liste_planetes = initialize_list(dist_max, nbr_planetes, masse_moyenne, vitesse_moyenne, moment_ang_moyen)

#Exécution du programme
main(liste_planetes)
