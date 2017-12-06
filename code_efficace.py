import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
#from init_parametres import *
from Planet import Planet


#Définition des constantes
G = 6.67408 * 10**(-11)
dt = 1
masse_terre = 5.9722*(10)**24
rayon_terre = 6378.137 *(10)**3
t = 0


####################################
#          Collision              #
###################################
def collision(liste_planetes):

    #Initialisation des paramètres
    index_fusion = []
    index_a_supprimer = []
    liste_collision = []

    #Construction d'une liste comprenant toutes les planètes en collision
    for planete,i in zip(liste_planetes,range(len(liste_planetes))):
        for Planete,j in zip(liste_planetes,range(len(liste_planetes))):
            #Si index 1 plus petit que 2 passe (pour prendre chaque interaction une seule fois en compte)
            if i >= j:
                pass

            #Si collision ajouter à la liste
            elif planete.distance(Planete) <= (Planete.rayon + planete.rayon) :
                if i in index_a_supprimer:
                    #Mettre comme premier indice l'indice de la première planète en collision seulement si le nouveau couple n,est pas déjà dans la liste
                    k = index_fusion[index_a_supprimer.index(i)][0]
                    if (k,j) in index_fusion:
                        pass
                    else:
                        index_fusion.append((k,j))
                        index_a_supprimer.append(j)
                        liste_collision.append((liste_planetes[k],Planete))
                else:
                    #Ajouter à la liste
                    liste_collision.append((planete,Planete))
                    #Garder en mémoire les index
                    index_fusion.append((i,j))
                    index_a_supprimer.append(j)


    #Changement des planètes dans la liste selon les collisions
    if liste_collision:
        for Planetes,i in zip(liste_collision,range(len(liste_collision))):
            Planete = Planetes[0]
            planete = Planetes[1]

            #Calcul de la vitesse de la nouvelle planète résultante
            vx = (planete.mass*planete.vx + Planete.mass * Planete.vx)/(Planete.mass+planete.mass)
            vy = (planete.mass * planete.vy + Planete.mass * Planete.vy) / (Planete.mass + planete.mass)

            #Changement des planètes dans la liste
            # i) Création d'une nouvelle planète
            new_rayon = (planete.rayon**3 + Planete.rayon**3)**(1/3)
            new_planete = Planet(planete.mass+Planete.mass, new_rayon, (planete.mass*planete.x+Planete.mass*Planete.x)/(planete.mass+Planete.mass), (planete.mass*planete.y+Planete.mass*Planete.y)/(planete.mass+Planete.mass), vx, vy, '{0} - {1}'.format(planete.nom,Planete.nom))

            # ii) Ajout de la nouvelle planète au premier indice
            liste_planetes[index_fusion[i][0]] = new_planete

            #Message indiquant une collision
            #print('Collission!!!')

        index_a_supprimer.sort()
        # iii) Effacer les planètes ayant fusionner de la liste (celle du 2e indice)
        for index in index_a_supprimer[::-1]:
            del liste_planetes[index]

    return liste_planetes,index_fusion,index_a_supprimer

#################################################
#    Calcul des énergies totales du système     #
#################################################
def Energie(liste_planetes):
    Ttot = 0
    Utot = 0

    for planete in liste_planetes:
        Ttot += planete.ECin()

        for Planete in liste_planetes:
            if planete is Planete:
                continue
            else:
                Utot += planete.EGrav(Planete)

    Utot = Utot/2
    Etot = Utot + Ttot

    return Etot, Ttot, Utot

#####################################################################################################
#    Définition d'une fonction pour pour actualiser la position de plusieurs planètes à la fois     #
#####################################################################################################
def actualiser_systeme(liste_planetes, dt=1):
    while True:
        # Création d'une liste des accélérations des planètes
        acceleration = []

        #Calcul de l'accélération de chaque planète
        for planete in liste_planetes:
            acceleration.append(planete.acceleration(liste_planetes))

        #Actualisation de la position et de la vitesse de chaque planète
        for planete,a,i in zip(liste_planetes,acceleration,range(len(liste_planetes))):
            planete.actualiser_sys(a[0],a[1],dt)

        liste_planetes,index_fusion,index_a_supprimer = collision(liste_planetes)

        Etot, Ttot, Utot = Energie(liste_planetes)
        #print('Etot = ', Etot)
        #print('Ttot = ', Ttot)
        #print('Utot = ', Utot)

        yield liste_planetes,index_fusion,index_a_supprimer,Etot


####################################################################################
#        Définition de fonctions pouvant déteminer les conditions initiales        #
####################################################################################

#Fonction pour calculer la masse moyenne
def masse_moyen(liste_planete):
    masse = 0
    for planete in liste_planete:
        masse += planete.mass

    masse = masse/len(liste_planete)
    return masse


#Fonction pour calculer le rayon moyen
def rayon_moyen(liste_planete):
    rayon = 0
    for planete in liste_planete:
        rayon += planete.rayon

    rayon = rayon/len(liste_planete)
    return rayon


#Fonction pour calculer la vitesse moyenne
def vitesse_moyen(liste_planete):
    vitesse = 0
    for planete in liste_planete:
        vitesse += np.sqrt( planete.vx**2 + planete.vy**2 )

    vitesse = vitesse/len(liste_planete)
    return vitesse

#Fonction pour calculer la quantité de mouvement moyenne
def quantite_mouvement_moyen(liste_planete):
    qte_mvt = 0
    for planete in liste_planete:
        qte_mvt += planete.mass * np.sqrt( planete.vx**2 + planete.vy**2 )

    qte_mvt = qte_mvt/len(liste_planete)
    return qte_mvt



#Fonction pour calculer le moment cinétique en z
def moment_angulaire_moyen(liste_planete):
    lz = 0
    for planete in liste_planete:
        vitesse = [planete.vx,planete.vy,0]
        position = [planete.x,planete.y,0]

        #Calul du moment angulaire par rapport à l'origine
        lz += planete.mass*np.cross(position,vitesse)[2]

    lz = lz/len(liste_planete)
    return lz


#####################################################################################
#       Définition d'une fonction pour déterminer la stabilité d'un système         #
#####################################################################################

# Fonction pour trouver la planète la plus massive
def trouver_massive(liste_planete, init):
    masse_max = 0
    planete_max = []

    if not init:
        for planete in liste_planete:
            if planete.mass > masse_max and planete.x>-3*20000000 and planete.x<3*20000000 and planete.y>-3*20000000 and planete.y<3*20000000:
                planete_max = planete
                masse_max = planete.mass
    else:
        for planete in liste_planete :
            if planete.mass > masse_max and planete.x>-5*20000000 and planete.x<5*20000000 and planete.y>-5*20000000 and planete.y<5*20000000:
                planete_max = planete
                masse_max = planete.mass

    return planete_max


#Fonction pour trouver toutes les planètes à l'intérieur d'un certain rayon autour de la planète
def get_other_planets(liste_planete, planete_mere):
    nbr_stable=0
    if planete_mere.mass < 18*masse_terre:
        pass
    else:
        for planete in liste_planete:
            if planete is not planete_mere and (planete_mere.distance(planete) < (2*10**7)) and (np.sqrt(planete.vx**2 + planete.vy**2) < np.sqrt(2*G*planete_mere.mass/planete_mere.distance(planete))):
                nbr_stable += 1

    return nbr_stable

#Fonction afin de déterminer si le système est vraiment stable
def define_stabilite(planete_mere, nbr_stable):
    if planete_mere == [] or nbr_stable == 0:
        stable = False
    else:
        stable = True

    return stable


######################################
#        Programme principal         #
######################################
def main(liste_planetes):

    #Importation d'une configuration initiale particulière
    # global liste_planetes
    #liste_planetes = initialize_list(dist_max, nbr_planetes, masse_moyenne, vitesse_moyenne, moment_ang_moyen)

    #Identification des différents paramètres initiaux
    MasseMoyenne = masse_moyen(liste_planetes)
    RayonMoyen = rayon_moyen(liste_planetes)
    VitesseMoyenne = vitesse_moyen(liste_planetes)
    qte_mvt_moyenne = quantite_mouvement_moyen(liste_planetes)
    lz = moment_angulaire_moyen(liste_planetes)

    print("nombre de planètes : {}".format(len(liste_planetes)))
    print("masse moyenne : {}".format(MasseMoyenne))
    print("rayon moyen : {}".format(RayonMoyen))
    print("vitesse moyenne : {}".format(VitesseMoyenne))
    print("quantité de mouvement moyenne : {}".format(qte_mvt_moyenne))
    print("lz : {}".format(lz))

    #Initialisation de la figure
    fig, ax = plt.subplots()

    #Initialisation d'un fond étoilé pour la figure
    ax.set_facecolor('black')
    ax.set_aspect(1)

    #Paramètres esthétiques
    limite_fig = 20000000
    ax.set_xlim([-limite_fig,limite_fig])
    ax.set_ylim([-limite_fig,limite_fig])

    #Écriture de l'énergie
    E_texte = ax.text(0.02, 0.95, '', color='w', transform=ax.transAxes)
    T_texte = ax.text(0.02, 0.90, '', color='w', transform=ax.transAxes)

    #Initilisation de points pour chacune des planètes
    position_x = []
    position_y = []
    for planet,i in zip(liste_planetes,range(len(liste_planetes))):
        position_x.append(planet.x)
        position_y.append(planet.y)

    #Traçage des planètes initiales
    planetes_espace = [plt.plot(planetes.x,planetes.y, 'o', color='r', markersize=(planetes.rayon*270)/limite_fig) for planetes,i in zip(liste_planetes,range(len(liste_planetes))) ]

    #Ajout d'une légende
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*1.1, box.height*1.1])

    #Définition de la fonction d'animation du système
    def run(data):
        nouvelle_liste_planete,index_fusion,index_a_supprimer,Etot = data

        #Retirer planetes collisionner de liste
        if index_fusion:
            for index in index_a_supprimer[::-1]:
                planetes_espace[index][0].set_markersize(0)
                del planetes_espace[index]

        #Incrémentation de l'évolution des planètes
        for planet,i in zip(nouvelle_liste_planete, range(len(nouvelle_liste_planete))):
            position_x[i] = planet.x
            position_y[i] = planet.y

        #Actualisation du graphique
        for planete,planetes in zip(nouvelle_liste_planete, planetes_espace):
            planetes[0].set_data(planete.x, planete.y)
            planetes[0].set_markersize((planete.rayon*270)/limite_fig)

        #Écriture de l'énergie
        E_texte.set_text('E = {:.2E} J'.format(Etot))

        #Écriture du temps
        global t
        t += dt
        T_texte.set_text('t = {}'.format(t))


        #Détermine si le système est stable
        # À la première itération
        if t == 500:
            init = False
            planete_mere = trouver_massive(nouvelle_liste_planete, init)
            nbr_stable = 0
            if planete_mere:
                nbr_stable = get_other_planets(nouvelle_liste_planete, planete_mere)
            else:
                stable = define_stabilite(planete_mere, nbr_stable)
                print('Nbr orbites : {}'.format(nbr_stable))
                print('stabilité : {}'.format(stable))
                raise SystemExit

        #Ensuite, s'il y a une planète mère
        if t > 500:
            init = True
            planete_mere = trouver_massive(nouvelle_liste_planete, init)
            nbr_stable = 0
            if planete_mere:
                nbr_stable = get_other_planets(nouvelle_liste_planete, planete_mere)

            if t > 650 or planete_mere == []:
                stable = define_stabilite(planete_mere, nbr_stable)
                print('Nombre de planètes : {}'.format(len(nouvelle_liste_planete)))
                print('Masse planète mère : {}'.format(planete_mere.mass))
                print('Nbr orbites : {}'.format(nbr_stable))
                print('stabilité : {}'.format(stable))
                #anim.event_source.quit()
                raise SystemExit
                #quit()

        return planetes

    #Animation
    #anim = animation.FuncAnimation(fig, run, actualiser_systeme(liste_planetes), frames=650, blit=False, repeat=False)
    anim = animation.FuncAnimation(fig, run, actualiser_systeme(liste_planetes), interval=5, blit=False, repeat=False, save_count=300,)

    #Traçage de l'animation
    plt.show()

    anim.save('planet.gif', writer='imagemagick', dpi=120, fps=27)

