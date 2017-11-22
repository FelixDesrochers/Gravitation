import numpy as np


#Définition des constantes
G = 6.67408 * 10**(-11)
dt = 1
masse_terre = 5.9722*(10)**24
rayon_terre = 6378.137 *(10)**3
t = 0



###############################################
#      Définition d'une classe planète        #
###############################################
class Planet:

    #Définir les différents attributs
    def __init__(self,mass,rayon,x,y,vx,vy,nom,x0=0,y0=0,init=False):
        self.mass = mass
        self.rayon = rayon
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.nom = nom
        self.x0 = x0
        self.y0 = y0
        self.init = init


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
    def actualiser_sys(self,ax,ay,dt):
        if not self.init:
            self.init = True
            #Change the speed with the acceleration using Euler method
            self.vx = self.vx + ax * dt
            self.vy = self.vy + ay * dt

            #Compute the position using the spedd and Euler's method
            x = self.x + self.vx * dt + (1/2) * ax * dt**2
            y = self.y + self.vy * dt + (1/2) * ay * dt**2

            #Update the values of the position (x,y) and old position (x0,y0)
            # 1) Old position
            self.x0 = self.x
            self.y0 = self.y

            # 2) New position
            self.x = x
            self.y = y

            #Else, use verlet integration method to actualize position and speed
        else:
            #Defining the new position
            x_t2 = 2 * self.x - self.x0 + ax * dt**2
            y_t2 = 2 * self.y - self.y0 + ay * dt**2

            #Defining the new speed with the new position
            self.vx = ((x_t2 - self.x0) / (2*dt))
            self.vy = ((y_t2 - self.y0) / (2*dt))

            #Updating the position
            # 1) Old positions
            self.x0 = self.x
            self.y0 = self.y

            # 2) New positions
            self.x = x_t2
            self.y = y_t2

    #Énergie cinétique
    def ECin(self):
        T = 0.5 * self.mass * (self.vx**2 + self.vy**2)
        return T

    #Énergie potentielle gravitationnelle entre deux planètes
    def EGrav(self, autre_planete):
        U = - (G * self.mass * autre_planete.mass) / self.distance(autre_planete)
        return U
