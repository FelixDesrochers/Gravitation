import numpy as np
import matplotlib.pyplot as plt



Nbr_planetes = []
Nbr_restant = []
Masse_mere = []
nbr_orbites = []
stabilite = []

with open('vitesse2.txt', encoding='UTF-8') as fichier:

    init = False
    deux = False
    trois = False
    quatre = False
    cinq = False

    #Parcour de toutes les ligens du fichier
    for ligne in fichier:

        #Séparation de la ligne en ces composantes
        l = ligne.split()

        #S'il s'agit de la première ligne d'un bloc ou si le bloc a déjà été passé, continuer
        if l and (l[-1] == 'planetes' or init):

            #S'il s'agit de la première ligne
            if l[-1] == 'planetes':
                nbr = l[0]
                init = True
                deux = True

            #Vérifier si la ligne après fonctionne et si oui continuer
            elif deux:
                if l[0] == 'Nombre':
                    Nbr_planetes.append(float(nbr))
                    Nbr_restant.append(float(l[-1]))
                    deux = False
                    trois = True

                else:
                    init = False
                    deux = False

            elif trois:
                Masse_mere.append(float(l[-1]))
                trois = False
                quatre = True

            elif quatre:
                nbr_orbites.append(float(l[-1]))
                quatre = False
                cinq = True

            elif cinq:
                if l[-1] == 'False':
                    stabilite.append(0)
                else:
                    stabilite.append(1)
                cinq = False
                init = False


#Transformer en array numpy
Nbr_restant = np.array(Nbr_restant)
Masse_mere = np.array(Masse_mere)
nbr_orbites = np.array(nbr_orbites)
stabilite = np.array(stabilite)


#À partir de tous les essais qui contienennt la même masse moyenne, faire la moyenne
Masse_mere_2=[]
Nbr_planete_2=[]
Nbr_restant_2=[]
nbr_orbites_2=[]
stabilite_2=[]

for mult in np.arange(0.5, 60.5, 0.5):
    mult = round(mult,2)

    #trouver les index à merge
    liste_index = []
    liste_index = [ j for i,j in zip(Nbr_planetes,range(len(Nbr_planetes)))  if i == mult]


    #faire de nouvelles listes moyennes
    Nbr_planete_2.append(mult)


    Nbr_restant_2.append(Nbr_restant[liste_index[0] : liste_index[-1]+1].mean())
    Masse_mere_2.append(Masse_mere[liste_index[0] : liste_index[-1]+1].mean())
    nbr_orbites_2.append(nbr_orbites[liste_index[0] : liste_index[-1]+1].mean())
    stabilite_2.append(stabilite[liste_index[0] : liste_index[-1]+1].mean())


Nbr_planete_2=np.array(Nbr_planete_2) * 5000


# 1) Stabilité moyenne VS masse moyenne
f, ax = plt.subplots(1)
plt.scatter(Nbr_planete_2, stabilite_2, color='red')

#Mettre des grilles
ax.minorticks_on()
ax.grid(b=True, which='major' , linestyle='dotted')

#Mettre les titres des axes
ax.set_xlabel(r'Vitesse moyenne (m/s)',fontsize=16,fontweight='bold')
ax.set_ylabel(r'Stabilité moyenne ',fontsize=16,fontweight='bold')


plt.draw()

# 2) Masse moyenne planete Mere VS masse moyenne
f, ax = plt.subplots(1)
plt.scatter(Nbr_planete_2, Masse_mere_2, color='green')

#Mettre des grilles
ax.minorticks_on()
ax.grid(b=True, which='major' , linestyle='dotted')
#ax.set_xlim([0,8.1])

#Mettre les titres des axes
ax.set_xlabel(r'Vitesse moyenne (m/s)',fontsize=16,fontweight='bold')
ax.set_ylabel(r'Masse moyenne de la planète centrale (kg)',fontsize=16,fontweight='bold')
plt.show()



# 3) Nombre de planètes en orbite VS masse moyenne
f, ax = plt.subplots(1)
plt.scatter(Nbr_planete_2, nbr_orbites_2)

#Mettre des grilles
ax.minorticks_on()
ax.grid(b=True, which='major' , linestyle='dotted')
#ax.set_xlim([0,8.1])

#Mettre les titres des axes
ax.set_xlabel(r'Vitesse moyenne (m/s)', fontsize=16, fontweight='bold')
ax.set_ylabel(r'Nombre moyen de planètes en orbite', fontsize=16, fontweight='bold')


plt.show()


f, ax = plt.subplots(1)
plt.scatter(Nbr_planete_2, Nbr_restant_2, color='red')

#Mettre des grilles
ax.minorticks_on()
ax.grid(b=True, which='major' , linestyle='dotted')

#Mettre les titres des axes
ax.set_xlabel(r'Vitesse moyenne (m/s)', fontsize=16, fontweight='bold')
ax.set_ylabel(r'Nombre de planètes restantes', fontsize=16, fontweight='bold')

plt.show()
