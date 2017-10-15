import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.misc import imread

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
    index_1 = []
    index_2 = []
    for planete in liste_planetes:
        for Planete in liste_planetes:
            if planete == Planete:
                pass

            elif planete.distance(Planete) < 0.98*(Planete.rayon + planete.rayon) :

                #Calcul de la vitesse de la nouvelle planète résultante
                vx = (planete.mass*planete.vx + Planete.mass * Planete.vx)/(Planete.mass+planete.mass)
                vy = (planete.mass * planete.vy + Planete.mass * Planete.vy) / (Planete.mass + planete.mass)

                ######Changement des planètes dans la liste
                # 1) Création d'une nouvelle planète
                new_rayon = (planete.rayon**3 + Planete.rayon**3)**(1/3)
                new_planete =  Planet(planete.mass+Planete.mass, new_rayon, (planete.mass*planete.x+Planete.mass*Planete.x)/(planete.mass+Planete.mass), (planete.mass*planete.y+Planete.mass*Planete.y)/(planete.mass+Planete.mass), vx, vy, '{0} - {1}'.format(planete.nom,Planete.nom))

                # 2) Garder en mémoire les index
                index_1 = liste_planetes.index(planete)
                index_2 = liste_planetes.index(Planete)

                # 3) Ajout de la nouvelle planète
                liste_planetes[index_2] = new_planete

                # 4) Effacer les planètes dans la liste
                del liste_planetes[index_1]

                print('Collission!!!')
                return liste_planetes,index_1,index_2
    return liste_planetes,index_1,index_2



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

        liste_planetes,index_1,index_2 = collision(liste_planetes)

        yield liste_planetes,index_1,index_2


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
    img = imread("fond_etoiles.jpeg")
    ax.imshow(img,zorder=0,extent=[-10000000, 10000000, -10000000, 10000000])

    #Paramètres esthétiques
    limite_fig = 10000000
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
        nouvelle_liste_planete,index_1,index_2 = data

        #Retirer planetes collisionner de liste
        if not index_1==[]:
            planetes_espace[index_1][0].set_markersize(0)
            del planetes_espace[index_1]

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
    anim = animation.FuncAnimation(fig, run, actualiser_systeme(liste_planetes), interval=10, blit=False, repeat=True)

    #Traçage de l'animation
    plt.show()


if __name__ == "__main__":
    main()
