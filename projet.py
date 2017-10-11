import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#Définition des constantes
G = 6.67408 * 10**(-11)
dt = 1
masse_terre = 5.9722*(10)**24
rayon_terre = 6378.137 *(10)**3



#Définition d'une classe planète
class Planet:

    #Définir les différents attributs
    def __init__(self,mass,rayon,x,y,vx,vy):
        self.mass = mass
        self.rayon = rayon
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy


    #Définir les différentes méthodes
    #Distance
    def distance(self, autre_planete):
        d = np.sqrt((autre_planete.x-self.x)**2 + (autre_planete.y-self.y)**2)
        return d

    #Acélération
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
            if planets is self:
                pass
            else:
                d = self.distance(planets)
                ax += (G * planets.mass)/(d**2) * (planets.x - self.x)/d
                ay += (G * planets.mass)/(d**2) * (planets.y - self.y)/d

        return ax, ay

    #Actualiser la vitesse
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


#Définition d'une fonction pour pour actualiser la position de plusieurs planètes à la fois
def actualiser_systeme(liste_planetes, dt=1):
    while True:
        ancienne_liste = []

        #Garder en mémoire les planètes initiales lors de l'actualisation
        ancienne_liste = [ i for i in liste_planetes ]

        #Actualise la vitesse et la position de toutes le planètes
        nouvelle_liste = []

        for planete in liste_planetes:
            ax, ay = planete.acceleration(ancienne_liste)
            planete.vx, planete.vy = planete.actualiser_vitesse(ax,ay,dt)
            planete.x, planete.y = planete.actualiser_position(dt)
            nouvelle_liste.append(planete)

        liste_planetes = nouvelle_liste
        yield liste_planetes


#Programme principal
def main():
    #Définition des constantes
    masse_terre = 5.9722*(10)**24
    rayon_terre = 6378.137 *(10)**3

    #Initialisation des planètes
    #Exemple 1: corps central et orbite
    #planete1 = Planet(100*masse_terre,rayon_terre,0,0,0,0)
    #planete2 = Planet(masse_terre,rayon_terre,5000*10**3,0,0,70000)
    #Liste de planètes
    #global liste_planetes
    #liste_planetes = [planete1, planete2]


    #Exemple 2: trois planètes
    planete1 = Planet(masse_terre,rayon_terre,1000*10**3,0,4000,4000)
    planete2 = Planet(masse_terre,rayon_terre,-5000*10**3,-5000*10**3,4000,-4000)
    planete3 = Planet(masse_terre,rayon_terre,-5000*10**3,5000*10**3,-4000,-4000)
    #Liste de planètes
    global liste_planetes
    liste_planetes = [planete1, planete2, planete3]


    #Initialisation de la figure
    fig, ax = plt.subplots()

    #Paramètres esthétiques
    ax.set_xlim([-10000000,10000000])
    ax.set_ylim([-10000000,10000000])

    #Initilisation de points pour chacune des planètes
    position_x = []
    position_y = []
    for planet,i in zip(liste_planetes,range(len(liste_planetes))):
        position_x.append([planet.x])
        position_y.append([planet.y])

    #Traçage des points initiaux
    points_espace = [plt.plot([], [], '-') for i in liste_planetes]

    #Définition de la fonction d'animation du système
    def run(data):
        nouvelle_liste_planete = data

        #Incrémentation de l'évolution des planètes
        for planet,i in zip(nouvelle_liste_planete,range(len(nouvelle_liste_planete))):
            position_x[i].append(planet.x)
            position_y[i].append(planet.y)

        #actualisation du graphique
        for planete,points,i in zip(nouvelle_liste_planete,points_espace,range(len(nouvelle_liste_planete))):
            points[0].set_data(position_x[i],position_y[i])

        #Impression de la position (débuggage)
        #for planet in nouvelle_liste_planete:
            #print(planet.x,planet.y)

        return points

    #Animation
    anim = animation.FuncAnimation(fig, run, actualiser_systeme(liste_planetes), interval=10, blit=False, repeat=True)

    #Traçage de l'animation
    plt.show()


if __name__ == "__main__":
    main()
