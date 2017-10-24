import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#Définition des constantes
G = 6.67408 * 10**(-11)
dt =1
masse_terre = 5.9722*(10)**24
rayon_terre = 6378.137 *(10)**3



###############################################
#      Définition d'une classe planète        #
###############################################
class Planet:

    #Définir les différents attributs
    def __init__(self,mass,rayon,x,y,vx,vy,nom):
        self.mass = mass
        self.rayon = rayon
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.nom = nom


    #Définir les différentes méthodes
    #Distance
    def distance(self, autre_planete):
        d = np.sqrt((autre_planete.x-self.x)**2 + (autre_planete.y-self.y)**2)
        return d

    #Calcul de l'accélération résultante
    def acceleration(self,liste_planetes,G=6.67408 * 10**(-11)):
        ax = 0
        ay = 0
        for planets in liste_planetes:
            if planets is self or self.x == planets.x:
                pass
            else:
                d = self.distance(planets)
                ax += (G * planets.mass)/(d**2) * (planets.x - self.x)/d
                ay += (G * planets.mass)/(d**2) * (planets.y - self.y)/d

        return ax, ay

    #Actualiser la vitesse de la planète
    def actualiser_vitesse(self,ax,ay,dt):

        vx = self.vx + ax*dt
        vy = self.vy + ay*dt
        return vx,vy

    #Actualiser la position de la planète
    def actualiser_position(self,dt):

        x = self.x + self.vx*dt
        y = self.y + self.vy*dt
        return x,y



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
            new_rayon = (planete.rayon**2 + Planete.rayon**2)**(1/2)
            new_planete = Planet(planete.mass+Planete.mass, new_rayon, (planete.mass*planete.x+Planete.mass*Planete.x)/(planete.mass+Planete.mass), (planete.mass*planete.y+Planete.mass*Planete.y)/(planete.mass+Planete.mass), vx, vy, '{0} - {1}'.format(planete.nom,Planete.nom))

            # ii) Ajout de la nouvelle planète au premier indice
            liste_planetes[index_fusion[i][0]] = new_planete

            #Message indiquant une collision
            print('Collission!!!')

        index_a_supprimer.sort()
        # iii) Effacer les planètes ayant fusionner de la liste (celle du 2e indice)
        for index in index_a_supprimer[::-1]:
            del liste_planetes[index]

    return liste_planetes,index_fusion,index_a_supprimer



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
            planete.vx, planete.vy = planete.actualiser_vitesse(a[0],a[1],dt)
            planete.x, planete.y = planete.actualiser_position(dt)

        liste_planetes,index_fusion,index_a_supprimer = collision(liste_planetes)

        yield liste_planetes,index_fusion,index_a_supprimer


######################################
#        Programme principal         #
######################################
def main():

    #Importation d'une configuration initiale particulière
    from initialisation import liste_4
    global liste_planetes
    liste_planetes = liste_4


    #Initialisation de la figure
    fig, ax = plt.subplots()

    #Initialisation d'un fond étoilé pour la figure
    ax.set_facecolor('black')
    ax.set_aspect(1)

    #Paramètres esthétiques
    limite_fig = 20000000
    ax.set_xlim([-limite_fig,limite_fig])
    ax.set_ylim([-limite_fig,limite_fig])

    #Initilisation de points pour chacune des planètes
    position_x = []
    position_y = []
    for planet,i in zip(liste_planetes,range(len(liste_planetes))):
        position_x.append(planet.x)
        position_y.append(planet.y)

    #Traçage des planètes initiales
    planetes_espace = [plt.plot(planetes.x,planetes.y, 'o', color='r', markersize=(planetes.rayon*375)/limite_fig) for planetes,i in zip(liste_planetes,range(len(liste_planetes))) ]

    #Ajout d'une légende
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*1.1, box.height*1.1])

    #Définition de la fonction d'animation du système
    def run(data):
        nouvelle_liste_planete,index_fusion,index_a_supprimer = data

        #Retirer planetes collisionner de liste
        if index_fusion:
            for index in index_a_supprimer[::-1]:
                planetes_espace[index][0].set_markersize(0)
                del planetes_espace[index]

        #Incrémentation de l'évolution des planètes
        for planet,i in zip(nouvelle_liste_planete, range(len(nouvelle_liste_planete))):
            position_x[i] = planet.x
            position_y[i] = planet.y

        #actualisation du graphique
        for planete,planetes,i in zip(nouvelle_liste_planete, planetes_espace, range(len(nouvelle_liste_planete))):
            planetes[0].set_data(planete.x, planete.y)
            planetes[0].set_markersize((planete.rayon*375)/limite_fig)

        return planetes

    #Animation
    anim = animation.FuncAnimation(fig, run, actualiser_systeme(liste_planetes), interval=5, blit=False, repeat=True)

    #Traçage de l'animation
    plt.show()


if __name__ == "__main__":
    main()
