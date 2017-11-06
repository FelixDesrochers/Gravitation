import numpy as np
from code_efficace import Planet

#Définition des constantes
masse_terre = 5.9722*(10)**24
rayon_terre = 6378.137 *(10)**3
densitee_terre = (masse_terre)/((4*np.pi*rayon_terre**3)/3)

#Définition d'une fonction pour évaluer la valeur absolue d'une liste
abs_liste = np.vectorize(abs)


##########################################
#     Définition des valeurs désirées    #
##########################################
dist_max = 10**7 #rayon du cercle dans lequel toutes les planètes sont situées
nbr_planetes = 143
masse_moyenne = 4 * masse_terre
vitesse_moyenne = 22000
moment_ang_moyen = 2e+35


#########################################
#   Définition de la liste de planètes  #
#########################################
# 1) Masse:
masse = np.array(abs_liste(np.random.normal(masse_moyenne, masse_moyenne/3, nbr_planetes)))
masse = masse * (masse_moyenne/masse.mean())

# 2) Rayon:
rayon = [(((3*m)/(densitee_terre * 4 * np.pi))**(1/3))/150 for m in masse]

# 3) Position
dist = np.random.rand(nbr_planetes) * dist_max
angle = np.random.rand(nbr_planetes) * 2 * np.pi

x = [ d * np.cos(theta) for d,theta in zip(dist,angle) ]
y = [ d * np.sin(theta) for d,theta in zip(dist,angle) ]

# 4) Vitesse
vitesse = np.random.normal(vitesse_moyenne, vitesse_moyenne/3, nbr_planetes)
vitesse = vitesse * (vitesse_moyenne/vitesse.mean())


# 5) Moment angulaire selon z
#Selon le vecteur vitesse, définir le moment angulaire maximal et le moment angulaire maximal pour chaque planète
lz_max = 0
lz_max_liste = []
for v,m,x1,y1 in zip(vitesse,masse,x,y):
    lz_max += v * m * np.sqrt(x1**2+y1**2)
    lz_max_liste.append(v * m * np.sqrt(x1**2+y1**2))
lz_max = lz_max/nbr_planetes
lz_max_liste = np.array(lz_max_liste)
print('lz_max: {}'.format(lz_max))

#Si le moment angulaire demandé est suprérieur au moment angulaire maximal, avertir et définir de nouveau
if lz_max < moment_ang_moyen:
    print("Attention!!! Moment angulaire demandé supérieur au moment angulaire maximal")
    moment_ang_moyen = lz_max

#Définir le multiple moyen requis
multiple_moyen = moment_ang_moyen*nbr_planetes/lz_max_liste.sum() if moment_ang_moyen*nbr_planetes/lz_max_liste.sum() < 1 else 1

#Boucle sur tous les mutliples jusqu'à obtention d'une liste convenable
multiple2=[2]
index = 0
while not all(i<=1 and i>=-1 for i in multiple2):
    multiple2=[]

    #Définition d'une liste aléatoire de multiple moyen selon le multiple moyen
    multiple = np.random.normal(multiple_moyen, 2*(np.e**(-multiple_moyen+1)-1), nbr_planetes)

    #Définition d'une nouvelle liste de multiple de manière à ce qu'ils soient tous entre 0 et 1
    multiple2 = []
    for m in multiple:
        if m>1 or m<-1:
            multiple2.append(2*np.random.rand()-1)
        else:
            multiple2.append(m)
    multiple2 = np.array(multiple2)

    #Normalisation de la deuxième liste de multiple
    correction = moment_ang_moyen /(sum([l*m for l,m in zip(lz_max_liste,multiple2)]) / nbr_planetes)
    multiple2 = multiple2 * correction

    index += 1

#Définir les angles associé pour chaque multiple
angle2 = []
for m in multiple2:
    a = np.random.rand()
    if a >= 0.5:
        angle2.append(np.arcsin(m))
    else:
        angle2.append(np.pi-np.arcsin(m))

#Définir les vitesse associées
vx = [v*np.cos(theta1+theta2) for v,theta1,theta2 in zip(vitesse,angle,angle2)]
vy = [v*np.sin(theta1+theta2) for v,theta1,theta2 in zip(vitesse,angle,angle2)]


# 5) Moment angulaire selon z (2e façon)
moment_ang = np.random.normal(moment_ang_moyen,abs(moment_ang_moyen/3),nbr_planetes)
moment_ang = moment_ang * (moment_ang_moyen / moment_ang.mean())
angle3 = np.random.rand(nbr_planetes)* 2 *np.pi
V = [lz/(m*d*np.sin(theta)) for lz,m,d,theta in zip(moment_ang,masse,dist,angle3)]

#vx = [v*np.cos(theta1+theta2) for v,theta1,theta2 in zip(V,angle,angle3)]
#vy = [v*np.sin(theta1+theta2) for v,theta1,theta2 in zip(V,angle,angle3)]


# 6) Création des planètes
liste_planetes = [Planet(masse, rayon, x, y, vx, vy, '{}'.format(i)) for masse,rayon,x,y,vx,vy,i in zip(masse,rayon,x,y,vx,vy,range(1,len(masse)+1))]

