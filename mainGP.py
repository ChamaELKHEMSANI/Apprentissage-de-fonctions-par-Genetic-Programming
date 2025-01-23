import sys
import random
import os.path
import numpy as np
from PyQt5.QtWidgets import QApplication # Module PyQt5 pour gérer les applications GUI.


from dlg.dialogueGP import DialogueGP  
from algo.algoGP import AlgoGP
from algo.algoThreadGP import AlgoThreadGP
from algo.chromosomeGP import ChromosomeGP
from tools.mathsToolsGP import MathsToolsGP
from tools.argParseToolsGP import ArgParseToolsGP
from tools.configToolsGP import ConfigToolsGP
from tools.drawToolsGP import DrawToolsGP

"""
La classe MainGP est un point d'entrée pour exécuter un algorithme génétique dans divers modes (par exemple, dialogue, exécution avec ou sans affichage, génération de population, etc.). 

Elle contient des méthodes pour :
	Initialiser et configurer l'algorithme en fonction des paramètres donnés.
	Lancer l'algorithme en fonction du mode (par exemple, en mode dialogue ou en mode ligne de commande).
	Afficher les résultats obtenus pendant l'exécution, soit sous forme de texte, soit sous forme graphique.
	Gérer la population (générer, écrire dans un fichier).
	Afficher une interface graphique pour interagir avec l'utilisateur.
	Elle permet ainsi une flexibilité dans l'exécution d'un algorithme génétique, que ce soit en mode batch ou interactif.
"""

class MainGP():
    # Définition des modes d'exécution possibles pour l'algorithme
    MODE_DEFAULT         = "run"
    MODE_DEUX_DIMENSION  = "2d"
    MODE_MULTI_DIMENSION = "multi"
    MODE_DIALOGUE        = "dialogue"
    MODE_POPULATE        = "populate"
    MODE_ITERATION       = "iterate"
    MODE_DRAW            = "draw"
    MODE_TEST            = "test"

    def __init__(self,params):
        """
        Initialise la classe MainGP avec les paramètres donnés.

        Args:
            params (dict): Dictionnaire des paramètres de l'algorithme (souvent récupéré d'un fichier de configuration).
        """
        self.params=params.deepcopy()
        self.config=ConfigToolsGP(self.params)

        # Si le mode est 'dialogue', affiche l'interface graphique
        if self.params.mode==self.MODE_DIALOGUE :
            self.affiche_dialogue()
        else:
            self.initialise()

    def run(self):
        """
        Lance l'algorithme en fonction du mode spécifié dans les paramètres.
        """
        # Si le mode est 'dialogue', on ne fait rien ici (l'interface graphique est déjà lancée).
        if self.params.mode==self.MODE_DIALOGUE :
            return
        if  self.algo == None :
            return
        # En fonction du mode, on effectue différentes actions :
        if self.params.mode==self.MODE_DRAW :
            self.draw_resultats() # Affiche les résultats graphiques
        elif self.params.mode==self.MODE_TEST :
            self.test( )  
        elif self.params.mode==self.MODE_POPULATE :
            self.genere_population(self.params.population_file) # Génère et écrit une population
        else:
            # Si le mode est différent, on démarre ou exécute l'algorithme
            if  self.params.bl_thread :
                self.algo.start() # Lance l'algorithme dans un thread séparé
            else:
                self.algo.execute()  # Exécute l'algorithme normalement

    def initialise(self):
        """
        Initialise les différents composants nécessaires à l'exécution de l'algorithme.
        """
        # Définit l'ensemble des terminaux en fonction du mode (2D ou non)
        if self.params.mode==self.MODE_DEUX_DIMENSION :
            self.config.terminal_set = ['x','y']
        elif self.params.mode == self.MODE_MULTI_DIMENSION:
            #################################################################################################################################
            self.config.terminal_set = ["x"+str(k) for k in range(self.params.nombre_coordonees)]
        else:
            self.config.terminal_set = ['x']

        self.init_input_output() # Initialise les entrées et sorties pour l'algorithme
        
        # Initialise l'algorithme avec ou sans thread
        if  self.params.bl_thread :
            self.algo = AlgoThreadGP() # Algorithme en mode thread
        else:
            self.algo = AlgoGP() # Algorithme sans thread

        # Initialise l'algorithme avec la configuration, les entrées et les sorties
        self.algo.initialise(self.config, self.inputs,self.outputs, self)



    def init_input_output(self):
        """
        Initialise les entrées et les sorties en fonction du mode de l'algorithme (2D ou non).
        """
        # Si le mode est 2D, on génère une grille de points (x, y) pour les entrées et calcule les sorties correspondantes        
        if self.params.mode==self.MODE_DEUX_DIMENSION:
            self.inputs = [[x,y] for x in np.arange(self.params.xmin, self.params.xmax, 0.1) for y in np.arange(self.params.ymin, self.params.ymax, 0.1)]
            self.outputs = [MathsToolsGP.evaluate_formule(self.config.formule,x=x1,y=y1) for [x1,y1] in self.inputs]
        elif self.params.mode == self.MODE_MULTI_DIMENSION:###############################################################################################################################################################
            mot=""
            for k in range(self.params.nombre_coordonees):
                exec("X%s = np.linspace(0,10,10)" % (str(k))) ################################################ 10
                mot += "X0" if k==0 else ", X"+str(k)
            exec("self.inputs = np.array(np.meshgrid(%s)).T.reshape(-1, self.params.nombre_coordonees)" % (mot))
            self.outputs = [MathsToolsGP.evaluate_formule(self.config.formule,{"x"+str(k):x[k] for k in range(self.params.nombre_coordonees)}) for x in self.inputs]
            #######################################################AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        else:
            # Si un fichier d'entrée est spécifié, on le lit pour initialiser les entrées et sorties
            if self.params.inputfile!="" :
                with open(self.params.inputfile, 'r') as file:
                    line_list = file.readlines()
                self.inputs=[]
                self.outputs=[]
                for line in line_list:
                    vals = line.strip().split(';')
                    self.inputs.append(float(vals[0]))
                    self.outputs.append(float(vals[1]))
            else:
                # Sinon, on génère des points d'entrée entre xmin et xmax et on évalue la formule pour obtenir les sorties
                self.inputs = [x for x in np.arange(self.config.xmin, self.config.xmax, 0.1)]
                self.outputs = [MathsToolsGP.evaluate_formule(self.config.formule, x=xval) for xval in self.inputs]



    def affiche_resultats(self):
        """
        Affiche les résultats de l'algorithme : la meilleure formule, la fitness, le nombre de générations, etc.
        """
        if  self.algo == None :
            return

        # Récupère le meilleur individu trouvé par l'algorithme
        best = self.algo.get_best()
        elapsed_time=self.algo.elapsed_time

        # Affiche les résultats dans la console
        print(best.fitness,best.generation, best.formule,elapsed_time)

        # Si un fichier de sortie est spécifié, écrit les résultats dans ce fichier
        if  self.params.outputfile != "" :
            self.params.args['generation']=best.generation
            self.params.args['time_exec']=elapsed_time
            self.params.args['fitness']=best.fitness
            self.params.args['newformule']=best.formule

            str_ligne=""
            if not os.path.isfile(self.params.outputfile):
                arr_list=self.params.args.keys()
                str_ligne = ";".join(arr_list)+"\n"

            with open(self.params.outputfile, 'a') as file:
                arr_list=self.params.args.values()
                str_ligne += ";".join(str(item) for item in arr_list)
                file.write(str_ligne+"\n")

        # Si le mode est 2D, affiche la surface 2D des résultats
        if self.params.mode==self.MODE_DEUX_DIMENSION :
            X = [x for x in np.arange(self.params.xmin, self.params.xmax, 0.1)]
            Y = [y for y in np.arange(self.params.ymin, self.params.ymax, 0.1)]
            DrawToolsGP.draw_surface_2(X,Y,self.params.formule,best.formule)

    def draw_resultats(self):
        """
        Dessine les résultats d'un fichier d'entrée contenant des données à afficher graphiquement.
        """
        valeurs=[]
        with open(self.params.draw_file, 'r') as file:
            head_list = file.readline().split(";");
            pos_field_x=head_list.index(self.params.draw_field_x)
            pos_field_y=head_list.index(self.params.draw_field_y)
            line =file.readline()
            while line !="":
                item = line.split(";")
                valeurs.append([float(item[pos_field_x]),float(item[pos_field_y])])
                line =file.readline()

        # Trie les valeurs par la première colonne
        valeurs.sort(reverse=False,key=lambda x:x[0])
        X = [row[0] for row in valeurs]
        Y = [row[1] for row in valeurs]

        # Affiche les résultats dans un graphique
        titre="Affichage de '"+self.params.draw_field_y+"' en fonction de '"+self.params.draw_field_x+"'"
        DrawToolsGP.draw_resultats(X,Y,self.params.draw_field_x,self.params.draw_field_y,titre)

    def genere_population(self,fichier_population):
        """
        Génère une population et l'écrit dans un fichier.
        
        Args:
            fichier_population (str): Chemin vers le fichier pour écrire la population.
        """
        self.algo.isRunning=True
        self.algo.populate_generate() # Génère la population
        self.algo.populate_write(fichier_population) # Écrit la population dans un fichier
        #self.algo.populate_read(fichier_population)
        #self.algo.populate_write(fichier_population+'.2.txt') # Écrit la population dans un fichier
        self.algo.isRunning=False

    def affiche_dialogue(self):
        """
        Affiche l'interface graphique pour le mode 'dialogue'.
        """
        app = QApplication(sys.argv)
        dlg_App = DialogueGP(self.config) # Crée l'interface de dialogue
        dlg_App.show()
        dlg_App.resize(600, 650)
        sys.exit(app.exec_()) # Lance l'interface graphique

    def set_jauge_value(self, str_message, pos_value, max_value):
        """
        Affiche la progression d'un processus sous forme de message dans la console.
        
        Args:
            str_message (str): Message à afficher.
            pos_value (int): Valeur actuelle.
            max_value (int): Valeur maximale.
        """
        if self.params.verbose :
            print(str_message,":",pos_value,"/",max_value)  

    def affiche_chromosome(self,iteration,chromosome):
        """
        Affiche la progression d'un processus sous forme de message dans la console.
        
        Args:
            str_message (str): Message à afficher.
            iteration (int): Valeur iteration.
            chromosome (obj): Valeur chromosome.
        """
        if self.params.verbose :
            print("* ",iteration,":",chromosome.fitness)  

    def test(self):
        self.algo.populate_read("data/populate_2000.txt")
 

 
