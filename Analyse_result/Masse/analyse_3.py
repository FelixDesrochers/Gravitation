import numpy as np
import matplotlib.pyplot as plt

nbr_planetes = []
masse_moyenne = []

with open('analyse_masse2.txt', encoding='UTF-8') as fichier:

    init = False
    deux = False

    #Parcour de toutes les ligens du fichier
    for ligne in fichier:

        #Séparation de la ligne en ces composantes
        l = ligne.split()

        #S'il s'agit de la première ligne d'un bloc ou si le bloc a déjà été passé, continuer
        if l and (l[-1] == 'Terre' or init):

            #S'il s'agit de la première ligne
            if l[-1] == 'Terre':
                masse = l[0]
                init = True
                deux = True

            #Vérifier si la ligne après fonctionne et si oui continuer
            elif deux:
                if l[2] == 'planètes':
                    masse_moyenne.append(float(masse))
                    nbr_planetes.append(float(l[-1]))
                    deux = False
                    init = False

                else:
                    init = False
                    deux = False



#Transformer en array numpy
nbr_planetes = np.array(nbr_planetes)

#À partir de tous les essais qui contienennt la même masse moyenne, faire la moyenne
masse_moyenne_2 = []
nbr_planetes2 = []

for mult in np.arange(0.3, 8.05, 0.05):
    mult = round(mult,2)

    #trouver les index à merge
    liste_index = []
    liste_index = [ j for i,j in zip(masse_moyenne,range(len(masse_moyenne)))  if i == mult]

    #faire de nouvelles listes moyennes
    masse_moyenne_2.append(mult)

    nbr_planetes2.append(nbr_planetes[liste_index[0] : liste_index[-1]+1].mean())

# 1) Stabilité moyenne VS masse moyenne
f, ax = plt.subplots(1)
plt.scatter(masse_moyenne_2, nbr_planetes2, color='red')

#Mettre des grilles
ax.minorticks_on()
ax.grid(b=True, which='major' , linestyle='dotted')

#Mettre les titres des axes
ax.set_xlabel(r'Masse moyenne (Masse terrestre)',fontsize=16,fontweight='bold')
ax.set_ylabel(r'Nombre de planètes restantes',fontsize=16,fontweight='bold')

plt.show()
