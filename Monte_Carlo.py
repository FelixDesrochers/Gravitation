from code_efficace import *
from init_parametres import *
import sys
sys.stdout = open("Resultats.txt", "a")


##########################################
#     Définition des valeurs désirées    #
##########################################
dist_max = 10**7 #rayon du cercle dans lequel toutes les planètes sont situées
nbr_planetes = 143
masse_moyenne = 4 * masse_terre
vitesse_moyenne = 25000
moment_ang_moyen = 2e+35

#Définition de la liste de planètes
liste_planetes = initialize_list(dist_max, nbr_planetes, masse_moyenne, vitesse_moyenne, moment_ang_moyen)

#Exécution du programme
print('\n# Essai')
main(liste_planetes)
