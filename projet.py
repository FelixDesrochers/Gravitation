import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
from scipy.misc import imread

#Définition des constantes
G = 6.67408 * 10**(-11)
dt =1
masse_terre = 5.9722*(10)**24
rayon_terre = 6378.137 *(10)**3



#Définition d'une classe planète
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
        '''Calcul de l'accélération pour une planètes selon toutes les autres planètes préssntes dans la simualtion

           Paramètres:
           -----------
           self (planet) : La planète dont l'on veut calculer l'accélération
           *arg (planet) : Toutes les autres planètes présentes dans la simulation

           Retourne:
           ---------
           ax (float) : l'accélération de la planète en x
           ay (float) : l'accélération de la plnète en y
        '''

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
        '''Actualise la vitesse de la planète à partir de l'accélération (utilisation de la méthode d'Euler)

           Paramètres:
           -----------
           self (planet) : La planète dont l'on veut actualiser la position
           ax (float) : l'accélération de la planète en x
           ay (float) : l'accélération de la plnète en y
           dt (float) : Intervalle infinitésimale de temps

           Returns:
           --------
           vx (float) : vitesse de la planète en x
           vy (float) : vitesse de la planète en y
        '''

        vx = self.vx + ax*dt
        vy = self.vy + ay*dt
        return vx,vy

    #Actualiser la position de la planète
    def actualiser_position(self,dt):
        '''Actualise la position de la planète à partir de la vitesse  (utilisation de la méthode d'Euler)

           Paramètres:
           -----------
           self (planet) : La planète dont l'on veut actualiser la position
           vx (float) : la vitesse de la planète en x
           vy (float) : la vitesse de la planète en y
           dt (float) : Intervalle infinitésimale de temps

           Returns:
           --------
           x (float) : position de la planète en x
           y (float) : position de la planète en y
        '''

        x = self.x + self.vx*dt
        y = self.y + self.vy*dt
        return x,y


###########################################################################
 # Première ébauche d'une collision (à prendre avec des petites pincettes)

def collision(liste_planetes):
    cpt1 = 0
    reponse = 0

    for planete in liste_planetes:
        cpt2 = 0

        for Planete in liste_planetes:
            if (Planete.x==planete.x) or cpt1 == cpt2:
                a=0


            ######Seuil de distance entre 2 planètes pour avoir une collision
            elif (np.sqrt((planete.x - Planete.x) ** 2 + (planete.y - Planete.y) ** 2) < 0.1*(Planete.rayon + planete.rayon)) and reponse == 0:

                reponse = 1

                if planete.vx >= 0 and planete.vy >= 0:
                    directionp = np.arctan(planete.vy / planete.vx)
                elif planete.vx < 0 and planete.vy >= 0:
                    directionp = 3.1416 + np.arctan(planete.vy / planete.vx)

                elif planete.vx >= 0 and planete.vy < 0:
                    directionp = np.arctan(planete.vy / planete.vx)

                elif planete.vx < 0 and planete.vy < 0:
                    directionp = -3.1416 + np.arctan(planete.vy / planete.vx)

                if Planete.vx >= 0 and Planete.vy >= 0:
                    directionP = np.arctan(Planete.vy / Planete.vx)
                elif Planete.vx < 0 and Planete.vy >= 0:
                    directionP = 3.1416 + np.arctan(Planete.vy / Planete.vx)

                elif Planete.vx >= 0 and Planete.vy < 0:
                    directionP = np.arctan(Planete.vy / Planete.vx)

                elif Planete.vx < 0 and Planete.vy < 0:
                    directionP = -3.1416 + np.arctan(Planete.vy / Planete.vx)

                Angle_impact = abs(np.arctan((planete.y - Planete.y) / (planete.y - Planete.x)))

                ########Analyse de toutes les collisions entre les deux masses possibles
                ########(Attention, les angles sont merdiques, et c'est clairement pas optimal, mais l'intention est là)
                if planete.x >= Planete.x and planete.y >= Planete.y:

                    angle = Angle_impact

                    V_planetein = np.sqrt(planete.vx ** 2 + planete.vy ** 2) * np.cos((directionp - angle))
                    V_Planetein = np.sqrt(Planete.vx ** 2 + Planete.vy ** 2) * np.cos((directionP - angle))

                    V_planeteit = np.sqrt(planete.vx ** 2 + planete.vy ** 2) * np.sin((directionp - angle))
                    V_Planeteit = np.sqrt(Planete.vx ** 2 + Planete.vy ** 2) * np.sin((directionP - angle))

                    Vitessen = (planete.mass * V_planetein + Planete.mass * V_Planetein) / (planete.mass + Planete.mass)
                    Vitesset = (planete.mass * V_planeteit + Planete.mass * V_Planeteit) / (planete.mass + Planete.mass)

                    angle2 = np.arctan(Vitessen / Vitesset)

                    vx = np.sqrt(Vitessen ** 2 + Vitesset ** 2) * np.cos(angle2 + angle - 3.1416 / 2)
                    vy = np.sqrt(Vitessen ** 2 + Vitesset ** 2) * np.sin(angle2 + angle + 3.1416 / 2)


                elif planete.x >= Planete.x and planete.y < Planete.y:

                    angle = Angle_impact

                    V_planetein = np.sqrt(planete.vx ** 2 + planete.vy ** 2) * np.cos(directionp + angle)
                    V_Planetein = np.sqrt(Planete.vx ** 2 + Planete.vy ** 2) * np.cos(-(directionP + angle))

                    V_planeteit = np.sqrt(planete.vx ** 2 + planete.vy ** 2) * np.sin(directionp + angle-3.1416/2)
                    V_Planeteit = np.sqrt(Planete.vx ** 2 + Planete.vy ** 2) * np.sin(-(directionP + angle)+3.1416/2)

                    Vitessen = (planete.mass * V_planetein + Planete.mass * V_Planetein) / (planete.mass + Planete.mass)
                    Vitesset = (planete.mass * V_planeteit + Planete.mass * V_Planeteit) / (planete.mass + Planete.mass)


                    angle2 = np.arctan(Vitesset / Vitessen)

                    vx = np.sqrt(Vitessen ** 2 + Vitesset ** 2) * np.cos(angle2)
                    vy = np.sqrt(Vitessen ** 2 + Vitesset ** 2) * np.sin(angle2-3.1416/2)

                elif planete.x < Planete.x and planete.y >= Planete.y:

                    angle = 3.1416 + Angle_impact
                    V_planetein = np.sqrt(planete.vx ** 2 + planete.vy ** 2) * np.cos(-(directionp - angle))
                    V_Planetein = np.sqrt(Planete.vx ** 2 + Planete.vy ** 2) * np.cos((directionP - angle))

                    V_planeteit = np.sqrt(planete.vx ** 2 + planete.vy ** 2) * np.sin(-(directionp - angle)+3.1416/2)
                    V_Planeteit = np.sqrt(Planete.vx ** 2 + Planete.vy ** 2) * np.sin((directionP - angle))

                    Vitessen = (planete.mass * V_planetein + Planete.mass * V_Planetein) / (planete.mass + Planete.mass)
                    Vitesset = (planete.mass * V_planeteit + Planete.mass * V_Planeteit) / (planete.mass + Planete.mass)

                    angle2 = np.arctan(Vitesset / Vitessen)
                    vx = np.sqrt(Vitessen ** 2 + Vitesset ** 2) * np.cos(angle2)
                    vy = np.sqrt(Vitessen ** 2 + Vitesset ** 2) * np.sin(angle2)

                elif planete.x < Planete.x and planete.y < Planete.y:

                    angle = -3.1416 + Angle_impact
                    V_planetein = np.sqrt(planete.vx ** 2 + planete.vy ** 2) * np.cos(-(directionp - angle))
                    V_Planetein = np.sqrt(Planete.vx ** 2 + Planete.vy ** 2) * np.cos((directionP - angle))

                    V_planeteit = np.sqrt(planete.vx ** 2 + planete.vy ** 2) * np.sin(-(directionp - angle)-3.1416/2)
                    V_Planeteit = np.sqrt(Planete.vx ** 2 + Planete.vy ** 2) * np.sin((directionP - angle)+3.1416/2)

                    Vitessen = (planete.mass * V_planetein + Planete.mass * V_Planetein) / (planete.mass + Planete.mass)
                    Vitesset = (planete.mass * V_planeteit + Planete.mass * V_Planeteit) / (planete.mass + Planete.mass)

                    angle2 = np.arctan(Vitesset / Vitessen)
                    vx = np.sqrt(Vitessen ** 2 + Vitesset ** 2) * np.cos(angle2)
                    vy = np.sqrt(Vitessen ** 2 + Vitesset ** 2) * np.sin(angle2)

                #planete1 = Planet(planete.mass + Planete.mass, planete.rayon,planete.x,planete.y,vx,vy)
                #planete2 = planete1

                ######Changement des planètes dans la liste
                liste_planetes[cpt1] = Planet(planete.mass , planete.rayon,planete.x,planete.y,vx,vy,'Montréal ou Laval')
                liste_planetes[cpt2] = Planet(Planete.mass,Planete.rayon,planete.x,planete.y,vx,vy,'Montréal ou Laval')

            cpt2 = cpt2+1
        cpt1 = cpt1 + 1

    #if reponse == 1:
        #liste_planetes = [planete1,planete2]

    return liste_planetes
##################################################################################

#Définition d'une fonction pour pour actualiser la position de plusieurs planètes à la fois
def actualiser_systeme(liste_planetes, dt=1):
    while True:

        # Création d'une liste des accélérations des planètes
        acceleration = []
        ancienne_liste = liste_planetes

        #Calcul de l'accélération de chaque planète
        for planete in liste_planetes:
            acceleration.append(planete.acceleration(liste_planetes))

        reponse = 0
        #Actualisation de la position et de la vitesse de chaque planète
        for planete,a in zip(liste_planetes,acceleration):

            planete.vx, planete.vy = planete.actualiser_vitesse(a[0],a[1],dt)
            planete.x, planete.y = planete.actualiser_position(dt)


        yield liste_planetes
        liste_planetes = collision(liste_planetes)





#Programme principal
def main():

    #Importation d'une configuration initiale particulière
    from initialisation import liste_2
    global liste_planetes
    liste_planetes = liste_2


    #Initialisation de la figure
    fig, ax = plt.subplots()

    #Initialisation d'un fond étoilé pour la figure
    img = imread("fond_etoiles.jpeg")
    ax.imshow(img,zorder=0,extent=[-10000000, 10000000, -10000000, 10000000])

    #Paramètres esthétiques
    limite_fig = 10000000
    ax.set_xlim([-limite_fig,limite_fig])
    ax.set_ylim([-limite_fig,limite_fig])

    #Initialisation de la couleur des graphiques
    colors = [cm.gist_ncar(1/i) for i in range(2,len(liste_planetes)+2) ]

    #Initilisation de points pour chacune des planètes
    position_x = []
    position_y = []
    for planet,i in zip(liste_planetes,range(len(liste_planetes))):
        position_x.append([planet.x])
        position_y.append([planet.y])

    #Traçage des orbites initiales
    lignes_espace = [plt.plot([], [], '-', color=colors[i], zorder=1, label=planetes.nom) for i,planetes in zip(range(len(liste_planetes)),liste_planetes) ]

    #Traçage des planètes initiales
    planetes_espace = [plt.plot(planetes.x,planetes.y, 'o', color=colors[i], markersize=(planetes.rayon*375)/limite_fig , zorder=2) for planetes,i in zip(liste_planetes,range(len(liste_planetes))) ]

    #Ajout d'une légende
    # Shrink current axis by 20%
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width*1.1, box.height*1.1])

    # Put a legend to the right of the current axis
    leg = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    leg.get_frame().set_alpha(1)

    #Définition de la fonction d'animation du système
    def run(data):
        nouvelle_liste_planete = data

        #Incrémentation de l'évolution des planètes
        for planet,i in zip(nouvelle_liste_planete, range(len(nouvelle_liste_planete))):
            position_x[i].append(planet.x)
            position_y[i].append(planet.y)
            if (len(position_x[0]) > 300) and (len(position_y[0]) > 300):
                for i in range(len(position_x)):
                    del position_x[i][0]
                    del position_y[i][0]

        #actualisation du graphique
        for planete,points,planetes,i in zip(nouvelle_liste_planete, lignes_espace, planetes_espace, range(len(nouvelle_liste_planete))):
            #i) Traçage des orbites
            points[0].set_data(position_x[i],position_y[i])
            planetes[0].set_data(position_x[i][-1],position_y[i][-1])

        #Impression de la position (débuggage)
        #for planet in nouvelle_liste_planete:
            #print(planet.x,planet.y)

        return points,planetes

    #Animation
    anim = animation.FuncAnimation(fig, run, actualiser_systeme(liste_planetes), interval=10, blit=False, repeat=True)

    #Traçage de l'animation
    plt.show()


if __name__ == "__main__":
    main()
