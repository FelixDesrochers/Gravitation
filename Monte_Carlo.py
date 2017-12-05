from code_efficace import *
from init_parametres2 import *
import numpy as np
import sys
sys.stdout = open("vitesse.txt", "a")

#Prendre les paramètres d'entrées
i = float(sys.argv[1])
j = int(sys.argv[2])

i = 5
j = 1
#Impression d'un message permettant d'afficher l'essai en question
print('\n# Essai {0} - {1}'.format(i,j))

##########################################
#     Définition des valeurs désirées    #
##########################################
dist_max = 10**7 #rayon du cercle dans lequel toutes les planètes sont situées
nbr_planetes = 150
masse_moyenne =  3*masse_terre
vitesse_moyenne = 0.1+5000*i
moment_ang_moyen = 2e+33

#Définition de la liste de planètes
liste_planetes = initialize_list(dist_max, nbr_planetes, masse_moyenne, vitesse_moyenne, moment_ang_moyen)

#Exécution du programme
main(liste_planetes)
