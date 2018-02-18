# Gravitation

Ce programme permet de simuler un problème à N corps en contrôlant les paramètres initiaux (masse moyenne, vitesse moyenne, moment angulaire, position, etc.). Nous avons conçu cette simulation dans le cadre d'un projet scolaire afin d'étudier les paramètres favorisant l'émergence de systèmes planétaires stables.


## Exécution

Pour exécuter ce programme, cloner simplement le programme et exécuter le script Run.py 

 
```
 git clone https://github.com/FelixDesrochers/Gravitation/
 cd Gravitation
 python Run.py
```

Le fichier Run.py peut être modifié afin de modifier les paramètres initiaux de la simulation.

## Exemples

Le programme produit ce genre de résultats (ici, nous avons 200 corps initialement):

<img src="/Examples/planet3.gif?raw=true" width="1200" height="600" />


## Résultats

L'objectif de ce projet était d'étudier l'influence de différents paramètres comme la vitesse moyenne, le nombre de planètes ou encore la masse moyenne sur la formation de systèmes stables. Ainsi, nous avons implémenter une méthode Monte Carlo afin d'évaluer le rôle de ces différents paramètres. La méthode utilisée de même que les différents résultats obtenus sont expliqués dans le document Projet.pdf. Nous présentons ici sommairement les différents résultats obtenus.


### Influence de la masse moyenne

Par exemple, pour un système dont le nombre de planètes initial, la vitesse moyenne et le moment angulaire totale était fixé, mais dont la masse moyenne était varier de façon systématique, nous avons obtenu les résultats suivants:

#### Nombre moyen de corps formant un système stable

<img src="/Analyse_result/Masse/Nbr_orbite.png" width="1200" height="600" />

#### Nombre de corps restant à la fin de la simulation

<img src="/Analyse_result/Masse/Nbr_restant_Masse.png" width="1200" height="600" />


### Influence du nombre initial de corps

#### Nombre moyen de corps formant un système stable


<img src="/Analyse_result/Nbr_planetes/Nbr_orbites.png" width="1200" height="600" />

#### Nombre de corps restant à la fin de la simulation

<img src="/Analyse_result/Nbr_planetes/Nbr_restant.png" width="1200" height="600" />

#### Masse moyenne du corps central 

<img src="/Analyse_result/Nbr_planetes/Masse_centre.png" width="1200" height="600" />


### Influence de la vitesse initiale moyenne

#### Nombre moyen de corps formant un système stable

<img src="/Analyse_result/vitesse/orbite_v.png" width="1200" height="600" />

#### Nombre de corps restant à la fin de la simulation

<img src="/Analyse_result/vitesse/restant_v.png" width="1200" height="600" />

#### Masse moyenne du corps central 

<img src="/Analyse_result/vitesse/Masse_mere_v.png" width="1200" height="600" />



## Contribution

Nous sommes ouverts à tout type de contribution pour ce projet. Pour se faire, simplement suivre les étapes suivantes:

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request


## License
MIT - [http://alco.mit-license.org](http://alco.mit-license.org)

(Voir LICENSE.md pour plus d'informations)
