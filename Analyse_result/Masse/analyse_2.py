import numpy as np
import matplotlib.pyplot as plt


masse_moyenne = []
Masse_mere = []
nbr_orbites = []
stabilite = []

with open('analyse_masse.txt', encoding='UTF-8') as fichier:

    init = False
    deux = False
    trois = False
    quatre = False

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
                if l[-3] == 'mère':
                    masse_moyenne.append(float(masse))
                    Masse_mere.append(float(l[-1]))
                    deux = False
                    trois = True

                else:
                    init = False
                    deux = False

            elif trois:
                nbr_orbites.append(float(l[-1]))
                trois = False
                quatre = True

            elif quatre:
                if l[-1] == 'False':
                    stabilite.append(0)
                else:
                    stabilite.append(1)
                quatre = False
                init = False



#Transformer en array numpy
Masse_mere = np.array(Masse_mere)
nbr_orbites = np.array(nbr_orbites)
stabilite = np.array(stabilite)


#À partir de tous les essais qui contienennt la même masse moyenne, faire la moyenne
Masse_mere_2=[]
masse_moyenne_2=[]
nbr_orbites_2=[]
stabilite_2=[]

for mult in np.arange(0.3, 8.05, 0.05):
    mult = round(mult,2)

    #trouver les index à merge
    liste_index = []
    liste_index = [ j for i,j in zip(masse_moyenne,range(len(masse_moyenne)))  if i == mult]

    #faire de nouvelles listes moyennes
    masse_moyenne_2.append(mult)

    Masse_mere_2.append(Masse_mere[liste_index[0] : liste_index[-1]+1].mean())
    nbr_orbites_2.append(nbr_orbites[liste_index[0] : liste_index[-1]+1].mean())
    stabilite_2.append(stabilite[liste_index[0] : liste_index[-1]+1].mean())

# 1) Stabilité moyenne VS masse moyenne
f, ax = plt.subplots(1)
plt.scatter(masse_moyenne_2, stabilite_2, color='red')

#Mettre des grilles
ax.minorticks_on()
ax.grid(b=True, which='major' , linestyle='dotted')

#Mettre les titres des axes
ax.set_xlabel(r'Masse moyenne (Masse terrestre)',fontsize=16,fontweight='bold')
ax.set_ylabel(r'Stabilité moyenne ',fontsize=16,fontweight='bold')
ax.set_xlim([0,8.1])

plt.show()

# 2) Masse moyenne planete Mere VS masse moyenne
f, ax = plt.subplots(1)
plt.scatter(masse_moyenne_2, Masse_mere_2, color='green')

#Mettre des grilles
ax.minorticks_on()
ax.grid(b=True, which='major' , linestyle='dotted')
ax.set_xlim([0,8.1])

#Mettre les titres des axes
ax.set_xlabel(r'Masse moyenne (Masse terrestre)',fontsize=16,fontweight='bold')
ax.set_ylabel(r'Masse moyenne de la planète centrale (kg)',fontsize=16,fontweight='bold')
plt.show()



# 3) Nombre de planètes en orbite VS masse moyenne
f, ax = plt.subplots(1)
plt.scatter(masse_moyenne_2, nbr_orbites_2)

#Mettre des grilles
ax.minorticks_on()
ax.grid(b=True, which='major' , linestyle='dotted')
ax.set_xlim([0,8.1])

#Mettre les titres des axes
ax.set_xlabel(r'Masse moyenne (Masse terrestre)', fontsize=16, fontweight='bold')
ax.set_ylabel(r'Nombre moyen de planètes en orbite', fontsize=16, fontweight='bold')


plt.show()




