# Heuristics-Chips-Circuits
De GitHub repository behorende tot deze opdracht kan gevonden worden via: https://github.com/mdhk/Heuristics-Chips-Circuits 

## Informatie

Deze files bevatten onze aanpak van de case 'Chips and Circuits', door Hasine, Marianne en Maurits.

De aanpak is zoveel mogelijk modulair gehouden, zodat bij verschillende methoden van dezelfde functies gebruik gemaakt kan worden.
Alle scripts zijn hoofdzakelijk geschreven in Python v2.7.x.

Benodigde externe libraries:
Om de 2D visualizatie te kunnen runnen is Pygame noodzakelijk.
Verder zijn voor analyse matplotlib en numpy gebruikt.

## Scripts en folders

###Folders

visualizations

    2D visualizatie van de grid.

data

    oorspronkelijke data: info over de grootte van de grids, posities van gates en de netlists.

###Scripts

#### Methoden

Gebruiksaanwijzing van de methoden:

Na het runnen van een van de methodes (bijv. >>> python run_Sort.py) wordt gevraagd om input: de juiste chip en netlist kunnen hier gekozen worden. 
Aan de hand van de in het script hard-gecodeerde variabelen zal het script wel/geen visualizatie tonen en een bepaald aantal iteraties runnen.

run_Sort.py

run_Cross.py

run_Disconnect.py

run_randomLayer.py

#### Modules

core.py

Core bevat functies die een Graph kunnen maken en aanpassen (bijvoorbeeld om connecties tussen vertices te creeeren of wegnemen). Ook bevinden zich hier functies om berekeningen uit te voeren, zoals het berekenen van de manhattan distance tussen een vertice-paar.

algorithms.py

Algorithms bevat manieren om het (kortste) pad te berekenen tussen twee vertices: Breadth First search en AStar, met bijbehorende heuristiek.
