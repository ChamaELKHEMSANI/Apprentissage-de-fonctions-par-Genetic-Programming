import sys
import numpy as np
from mainGP import MainGP
from tools.argParseToolsGP import ArgParseToolsGP

# -------------------------
# python  main.py -mode "dialogue"  

# python  main.py -mode "populate"  

# python  main.py -mode "run" -f "x**2+x*sin(x)" -xmin 0 -xmax 10 -s 123 -v 1 -out "data\output.txt"

# python main.py -mode "iterate" -f "x**2+x*sin(x)" -xmin 0 -xmax 10 -s 123 -iter_field size_depth -iter_min 4 -iter_max 11  -iter_step 1 -out "data\output_profondeur_4_10.csv"    -v 

# python main.py -mode "2d" -f "sin(x)*x**2+cos(x)*y**2" -xmin 1 -xmax 2 -ymin 1 -ymax 2 -s 123 

# python main.py   -mode "draw" -draw_file "data\output_profondeur_4_10.csv" -draw_field_x "size_depth" -draw_field_y "fitness"

arguments = ArgParseToolsGP()                   
arguments.parse_arguments()                      #parcours de la ligne de commande
if arguments.verbose :
    print(str(arguments.args))

if arguments.mode==MainGP.MODE_ITERATION :
    tab_iteration   = [x for x in np.arange(arguments.iter_min, arguments.iter_max, arguments.iter_step)]
    for val in tab_iteration:
        print(arguments.iter_field,val)          #afficher le champ de l'itération et sa valeur
        arguments.args[arguments.iter_field]=val #affectation de la valeur
        item=MainGP(arguments)                   #création et initialisation de l'item
        item.run()                               #exécution 
else:
    main_app = MainGP(arguments)                 #création et initialisation de l'item
    main_app.run()                               #exécution 
