import sys
import math
import time
import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QCoreApplication,    Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit,QLabel,QSlider,QListWidget,QCheckBox,QComboBox 
from tools.mathsToolsGP import MathsToolsGP
from tools.configToolsGP import ConfigToolsGP
from algo.chromosomeGP import ChromosomeGP
from dlg.treeGP import TreeGP
from algo.algoGP import AlgoGP
from algo.algoThreadGP import AlgoThreadGP
from dlg.dialogueUI import DialogWidget


"""
	Résumé
	La classe DialogueGP est l'interface graphique principale de l'application d'apprentissage par programmation génétique. Elle permet de configurer les paramètres, d'exécuter l'algorithme, et d'afficher les résultats sous forme graphique.

	Cette classe s'appuie sur PyQt5 pour gérer l'interface utilisateur et Matplotlib pour les visualisations graphiques.

	Attributs principaux
 		algo : Instance de l'algorithme génétique (AlgoGP ou AlgoGP_Thread).
		Widgets graphiques :
		graph, graph_resultats, graph_convergence : Graphiques pour afficher les formules, résultats et convergence.
		formule_edit, formule_resultat, formule_fitness : Entrées texte et affichage pour les formules et la fitness.
		jauge : Widget de jauge pour indiquer la progression. 

	Méthodes principales
	1. Initialisation
		Configure les widgets PyQt5 pour permettre :
		La saisie des paramètres utilisateur.
		L'affichage des résultats graphiques et des formules générées.
		Le contrôle de l'exécution de l'algorithme (boutons Démarrer, Stop, etc.).
	2.Widgets de progression : (set_jauge_value)
		Appelée pour indiquer la progression des calculs ou des itérations.
		Utilisée pour mettre à jour dynamiquement la jauge lors de l'exécution.
	3.Affichage des résultats : affiche_reultats
		Dessine les graphiques suivants :
			Prédictions comparées aux valeurs réelles.
			Courbe de convergence de la fitness.
		Met à jour les champs affichant la formule générée et sa fitness.
		Affiche l'arbre ou le graphe correspondant à la meilleure solution.
	4.Exécution de l'algorithme : run_it
		Vérifie si un algorithme est déjà en cours d'exécution.
		Récupère les paramètres définis dans les widgets (taille de population, profondeur, etc.).
		Prépare les données d'entrée et les sorties basées sur une formule donnée.
		Démarre l'algorithme dans un thread séparé via AlgoGP_Thread.
	5.Dessin d'une fonction utilisateur : draw_it
		Calcule les valeurs de la fonction définie par l'utilisateur (formule mathématique).
		Affiche la courbe dans un graphique intégré.
	6.Gestion des clics boutons: on_click
		Dessiner : Dessine la fonction spécifiée.
		run : Lance l'algorithme.
		stop : Arrête l'algorithme en cours.
		exit : Quitte l'application.
	7. Widgets utilitaires
		Création de widgets graphiques:create_button,create_jauge,create_graph,create_pixmap,create_edit
		Entrées utilisateur avec sliders:create_edit_slider
"""

class DialogueGP(DialogWidget):
    """
    Classe principale pour la gestion de l'interface graphique de l'application.
    Permet de configurer et d'exécuter l'algorithme génétique programmatique (GP)
    tout en affichant les résultats et la convergence.

    Hérite de QWidget pour l'intégration dans PyQt5.
    """
    def __init__(self,config):
        """
        Initialise l'interface graphique et configure tous les widgets nécessaires.
        """
        super().__init__()

        # Instance de configuration
        self.config = config


        self.algo = None  # Instance de l'algorithme GP.
        self.setWindowTitle('Apprentissage de fonction par Genetic Programming')
        grid = QGridLayout()

        # Création des widgets de l'interface.
        self.graph=self.create_hand_graph( grille=grid,callBack=None,row=0, column=0,rowspan=1,colspan=5)

        # Widgets pour les paramètres de formule et leurs affichages.
        self.formule_edit=self.create_edit( text="Formule", grille=grid,valeur=config.formule,readonly=False,row=1, column=0,rowspan=1,colspan=3)
        self.create_button( text="Dessiner", grille=grid,commande="Dessiner",row=1, column=3,rowspan=1,colspan=1)
        self.nbcoord_edit=self.create_edit(text="Nombre de variables",grille=grid,valeur=1,readonly=False,row=2, column=0,rowspan=1,colspan=2)
        self.formule_x1=self.create_edit( text="X min", grille=grid,valeur=config.xmin,readonly=False,row=3, column=0,rowspan=1,colspan=2)
        self.formule_x2=self.create_edit( text="X max", grille=grid,valeur=config.xmax,readonly=False,row=3, column=2,rowspan=1,colspan=2)
         
        # Widgets pour les paramètres de l'algorithme.
        self.max_size_population_edit=self.create_edit(  text="Nombre de populations", grille=grid,valeur=config.size_population,readonly=False,row=4, column=0,rowspan=1,colspan=2)
        self.max_iterations_edit=self.create_edit(  text="Nombre d'itérations", grille=grid,valeur=config.max_iterations,readonly=False,row=4,column=2,rowspan=1,colspan=2)


        self.dim_echantillon_edit=self.create_edit( text="Dimension de l'échantillon", grille=grid,valeur=config.size_echantillon,readonly=False,row=5,column=0,rowspan=1,colspan=2)
        self.max_depth_edit=self.create_edit( text="Profondeur d'arbre", grille=grid,valeur=config.max_depth,readonly=False,row=5,column=2,rowspan=1,colspan=2)

        self.max_N_valeur_edit=self.create_edit( text="Intervalle N d'entiers", grille=grid,valeur=config.max_N_valeur,readonly=False,row=6,column=0,rowspan=1,colspan=2)
        self.seed_edit=self.create_edit( text="Graine d'initialisation", grille=grid,valeur=config.seed,readonly=False,row=6,column=2,rowspan=1,colspan=2)

        self.tolerance_gene_length_edit=self.create_edit( text="Tolérance longueur gén", grille=grid,valeur=config.tolerance_gene_Length,readonly=False,row=7, column=0,rowspan=1,colspan=2)
        self.tolerance_gene_Mutate_edit=self.create_edit( text="Tolérance mutation gén", grille=grid,valeur=config.tolerance_gene_Mutate,readonly=False,row=7, column=2,rowspan=1,colspan=2)
        self.seuil_fitness_edit=self.create_edit( text="seuil d'arret fitness ", grille=grid,valeur=config.seuil_fitness,readonly=False,row=8, column=0,rowspan=1,colspan=2)
        self.duree_maximum_edit=self.create_edit( text="durée maximum (s)", grille=grid,valeur=config.duree_maximum,readonly=False,row=8, column=2,rowspan=1,colspan=2)
        #self.fichier_populate_edit=self.create_edit( text="Fichier de populations", grille=grid,valeur=config.fichier_populate,readonly=False,row=8, column=0,rowspan=1,colspan=4)

        self.max_funct_binaire=self.create_liste("Fonction binaire", grid,config.funct_binaire,9,0)
        self.max_funct_unaire=self.create_liste("Fonction unaire", grid,config.funct_unaire,9,2)

        self.mode_selection_combo=self.create_Combo("Opérateur de sélection", grid,config.modes_selection,config.mode_selection,row=10, column=0,rowspan=1,colspan=5)
        self.mode_mariage_combo=self.create_Combo("Opérateur de mariage", grid,config.modes_mariage,config.mode_mariage,row=11, column=0,rowspan=1,colspan=5)
        self.mode_croisement_combo=self.create_Combo("Opérateur de croisement", grid,config.modes_croisement,config.mode_croisement,row=12, column=0,rowspan=1,colspan=5)
        self.mode_mutation_combo=self.create_Combo("Opérateur de mutation", grid,config.modes_mutation,config.mode_mutation,row=13, column=0,rowspan=1,colspan=5)
        self.mode_remplacement_combo=self.create_Combo("Opérateur de remplacement", grid,config.modes_remplacement,config.mode_remplacement,row=14, column=0,rowspan=1,colspan=5)

        # Widgets pour afficher les résultats et la progression.
        self.graph_convergence=self.create_graph( grille=grid,callBack=self.callBackConvergence,row=0, column=5,rowspan=1,colspan=5)
        self.jauge = self.create_jauge(  grille=grid,row=1, column=5,rowspan=1,colspan=5)
        self.formule_iteration=self.create_edit( text="Itération", grille=grid,valeur="",readonly=False,row=2, column=5,rowspan=1,colspan=2)
        self.create_button( text="Afficher", grille=grid,commande="Afficher",row=2, column=7,rowspan=1,colspan=1)
        self.formule_resultat=self.create_edit( text="Résultat", grille=grid,valeur="",readonly=True,row=3, column=5,rowspan=1,colspan=5)
        self.formule_fitness=self.create_edit( text="Fitness", grille=grid,valeur="",readonly=True,row=4, column=5,rowspan=1,colspan=5)
        self.formule_generation=self.create_label( text="Génération", grille=grid,valeur="",row=5, column=5,rowspan=1,colspan=5)
        self.graph_resultats=self.create_graph( grille=grid,callBack=None,row=6, column=5,rowspan=9,colspan=5 )

        # Boutons pour contrôler l'exécution de l'algorithme.
        self.verbose_check=self.create_Check( text="Afficher les traces", grille=grid,state=config.verbose,readonly=False,row=15, column=0,rowspan=1,colspan=1)
        self.create_button( text="Démarrer", grille=grid,commande="run",row=15, column=1,rowspan=1,colspan=2)
        self.create_button( text="Stop", grille=grid,commande="stop",row=15, column=3,rowspan=1,colspan=2)

        self.pixmap=self.create_pixmap( pixFile='dlg/ENAC-Bleu.png', grille=grid,row=15, column=5,rowspan=1,colspan=1)
        self.create_button( text="Quitter", grille=grid,commande="exit",row=15, column=7,rowspan=1,colspan=3)

        # Configuration finale du layout.
        self.setLayout(grid)


    def set_jauge_value(self,str_message,pos_value,max_value):
        """
        Met à jour la jauge de progression avec un message et une nouvelle valeur.
        
        Args:
            str_message (str): Message affiché dans la jauge (par exemple, "Calcul en cours").
            pos_value (int): Valeur actuelle de progression.
            max_value (int): Valeur maximale de progression.
        """
        # Met à jour la jauge avec les valeurs fournies.
        self.jauge.set_jauge_value(str_message,pos_value,max_value)
        if(not self.config.bl_thread):
            self.jauge.update()
            self.jauge.repaint()
        QCoreApplication.processEvents() 

    def affiche_chromosome(self,iteration,chromosome):
        """
        Met à jour la convergence avec une nouvelle valeur.
        
        Args:
            str_message (str): Message affiché dans la jauge (par exemple, "Calcul en cours").
            iteration (int): Valeur actuelle de iteration.
            chromosome (obj): Valeur chromosome.
        """
        # Met à jour le graphe avec les valeurs fournies.
        self.graph_convergence.draw_convergente_item(self.config.max_iterations,iteration,chromosome.fitness)

        self.formule_iteration.setText(str(iteration))
        self.formule_resultat.setText(MathsToolsGP.simplifie_formule(chromosome.formule))
        self.formule_fitness.setText(str(chromosome.fitness))
        self.formule_generation.setText(str(chromosome.generation))
        QCoreApplication.processEvents() 

    def affiche_resultats(self):
        """
        Affiche les résultats de l'algorithme, y compris la formule générée,
        la fitness, la convergence et les prédictions graphiques.
        
        Args:
            y_pred (list): Liste des valeurs prédites par le meilleur individu.
            y_conv (list): Liste des valeurs de convergence de la fitness à chaque itération.
        """
        # Vérifie que l'algorithme est initialisé avant d'afficher les résultats.
        if(self.algo== None):
            return
        # Récupère le meilleur individu de la population.
        best= self.algo.get_best()
        
        # calcule les valeurs à afficher.
        y_pred = [best.evaluate(x) for x in self.algo.inputs]
        y_conv = [best.fitness for best in self.algo.best_results] 

        # Dessine le graphique des résultats (valeurs réelles vs prédites).
        self.graph.draw_resultat(self.algo.inputs,self.algo.outputs,y_pred)

        # Dessine le graphique de la convergence de la fitness.
        self.graph_convergence.draw_convergente(y_conv)

        # Affiche la formule générée par le meilleur individu.
        formule_pred=MathsToolsGP.simplifie_formule(best.formule) 
        self.formule_iteration.setText(str(len(self.algo.best_results)))
        self.formule_resultat.setText(formule_pred)

        # Affiche la fitness du meilleur individu.
        self.formule_fitness.setText(str(best.fitness))
        self.formule_generation.setText(str(best.generation))

        # Réinitialise la jauge.
        self.set_jauge_value("",1,100)

        # Dessine l'arbre ou le graphe correspondant au meilleur individu.
          
        depth=best.depth
        tree= TreeGP(depth,0.5,0.75)
        tree.read(best.gen,depth)
        self.graph_resultats.draw_graph(tree)
        
    def callBackConvergence(self,num_iteration):
        """
        Affiche les résultats de l'algorithme, pour une itération donnée compris la formule générée,
        """
        # Vérifie que l'algorithme est initialisé avant d'afficher les résultats.
        if(self.algo== None):
            return
        # Récupère le meilleur individu de la population.
        best=self.algo.get_best_iteration(num_iteration)
        if(best is not None):
            # Dessine l'arbre ou le graphe correspondant .

            tree= TreeGP(best.depth,0.5,0.75)
            tree.read(best.gen,best.depth)
            self.graph_resultats.draw_graph(tree)
            # Affiche la formule générée par le meilleur individu.
            formule_pred=MathsToolsGP.simplifie_formule(best.formule)
            self.formule_iteration.setText(str(num_iteration))
            self.formule_resultat.setText(formule_pred)
            self.formule_fitness.setText(str(best.fitness))
            self.formule_generation.setText(str(best.generation))
            # Dessine l'arbre ou le graphe correspondant .
            y_pred = [best.evaluate(x) for x in self.algo.inputs]
            self.graph.draw_resultat(self.algo.inputs,self.algo.outputs,y_pred)

    def show_it(self):
        num_iteration=self.formule_iteration.text()
        if(num_iteration!=""):
            self.callBackConvergence(int(num_iteration))
            
    def run_it(self):
        """
        Configure et lance l'exécution de l'algorithme génétique en fonction
        des paramètres définis par l'utilisateur.
        """
        # Vérifie si un algorithme est déjà en cours d'exécution.
        if(self.algo!= None):
            if(self.algo.isRunning):
                return
            else:
                self.stop_it()

        nbcoord                     = int(self.nbcoord_edit.text())
        # Récupère les paramètres définis par l'utilisateur via les widgets.
        self.config.formule         = self.formule_edit.text()
        self.config.size_population = int(self.max_size_population_edit.text()) 
        self.config.size_echantillon= int(self.dim_echantillon_edit.text())
        self.config.max_depth       = int(self.max_depth_edit.text())
        self.config.max_iterations  = int(self.max_iterations_edit.text())
        self.config.funct_binaire   = [item.text() for item in self.max_funct_binaire.selectedItems()]
        self.config.funct_unaire    = [item.text() for item in self.max_funct_unaire.selectedItems()]
        self.config.seed            = int(self.seed_edit.text())
        self.config.max_N_valeur    = int(self.max_N_valeur_edit.text())
        self.config.terminal_set    = ["x"+str(k) for k in range(nbcoord)] if nbcoord!=1 else ["x"]

        self.config.mode_selection      = self.config.modes_selection[self.mode_selection_combo.currentIndex()][1]
        self.config.mode_mariage          = self.config.modes_mariage[self.mode_mariage_combo.currentIndex()][1]
        self.config.mode_croisement       = self.config.modes_croisement[self.mode_croisement_combo.currentIndex()][1]
        self.config.mode_mutation         = self.config.modes_mutation[self.mode_mutation_combo.currentIndex()][1]
        self.config.mode_remplacement     = self.config.modes_remplacement[self.mode_remplacement_combo.currentIndex()][1]


        self.config.tolerance_gene_Length = float(self.tolerance_gene_length_edit.text())
        self.config.tolerance_gene_Mutate = float(self.tolerance_gene_Mutate_edit.text())
        self.config.seuil_fitness         = float(self.seuil_fitness_edit.text())
        self.config.duree_maximum         = int(self.duree_maximum_edit.text()) 
        self.config.verbose               = self.verbose_check.checkState()
        #self.config.fichier_populate      = self.fichier_populate_edit.text()

        # Nettoie les graphiques précédents et réinitialise les champs de texte.
        self.graph_resultats.clear()
        self.graph_convergence.clear()
        self.formule_iteration.setText("")
        self.formule_resultat.setText("")
        self.formule_fitness.setText("")
        self.formule_generation.setText("")
        if(self.config.formule!=""):
            try:
                x1 = float(self.formule_x1.text())
                x2 = float(self.formule_x2.text())
                self.graph.draw_formule(self.config.formule,x1,x2)
                # Génère les données d'entrée (X) et les sorties correspondantes (y).
                if nbcoord > 1:
                    mot = ""
                    for k in range(nbcoord):
                        exec("X%s = np.linspace(x1,x2,10)" % (str(k))) ##################### NDT : On peut changer le 10 mais ça rend le programme très lent
                        mot += "X0" if k==0 else ", X"+str(k)
                    exec("X = np.array(np.meshgrid(%s)).T.reshape(-1, nbcoord)" % (mot))
                    Y = [MathsToolsGP.evaluate_formule(self.config.formule,{"x"+str(k):x[k] for k in range(nbcoord)}) for x in X]
                else :
                    X = [x for x in np.arange(x1, x2, 0.1)]
                    Y = [MathsToolsGP.evaluate_formule(self.config.formule,x=x1) for x1 in X]
            except Exception as ex:
                # Si une erreur se produit (ex. domaine incorrect), affiche un message d'erreur.
                print(ex)
                formule = self.formule_edit.text()
                self.formule_edit.setText('Erreur ou domaine incorrect:'+formule)
                return
        else:
            X=self.graph.x
            Y=self.graph.y

        # Configure la jauge de progression.
        self.jauge.set_jauge_value("Départ",1,self.config.size_population)
 
        # Initialise et configure l'algorithme génétique.
        if(self.config.bl_thread):
            self.algo=AlgoThreadGP()
            self.algo.initialise(self.config,X,Y,self)
            self.algo.start()                           # Démarre l'exécution de l'algorithme .
        else:
            self.algo=AlgoGP()
            self.algo.initialise(self.config,X,Y,self)
            self.algo.execute()                          # Démarre l'exécution de l'algorithme dans un thread séparé.

 

    def stop_it(self):
        """
            Arrête l'exécution de l'algorithme génétique en cours, 
            si un algorithme est en cours d'exécution. 

            Cette méthode effectue les étapes suivantes :
            1. Vérifie si une instance d'algorithme est active (`self.algo`).
            2. Si active, elle appelle la méthode `stop` pour demander l'arrêt du thread.
            3. Attend que le thread se termine proprement avec `join`.
            4. Réinitialise la jauge de progression.
            5. Libère la référence à l'instance d'algorithme pour indiquer qu'il n'y a plus d'exécution en cours.
        """
        # Vérifie si un algorithme est actuellement actif
        if(self.algo is not None):
            if self.config.bl_thread :
                self.algo.setStop()
                # Demande à l'algorithme (thread) de s'arrêter
                self.algo.stop()
                # Attend la terminaison propre du thread
                self.algo.join()
            else:
                self.algo.setStop()
            # Réinitialise la jauge de progression à vide
            self.jauge.set_jauge_value("",1,100) 
            
            

    def draw_it(self):
        """
        Dessine le graphique de la fonction spécifiée par l'utilisateur 
        dans la plage définie par X1 et X2.
        """
        try:
            nbcoord=int(self.nbcoord_edit.text())
            if nbcoord>1:
                # Récupère les limites de l'intervalle d'entrée (X1 et X2).
                x1 = float(self.formule_x1.text())
                x2 = float(self.formule_x2.text())
                # Récupère la formule définie par l'utilisateur et dessine le graphique par rapport à la première coordonnée.
                mot=""
                for k in range(nbcoord):
                    mot += ".replace('x"+str(k)+"','0')" if k!=0 else ".replace('x"+str(k)+"','x')"
                exec("self.formule = self.formule_edit.text()%s" % (mot))
                self.graph.draw_formule(self.formule,x1,x2)
            else:
                # Récupère les limites de l'intervalle d'entrée (X1 et X2).
                x1 = float(self.formule_x1.text())
                x2 = float(self.formule_x2.text())
                # Récupère la formule définie par l'utilisateur et dessine le graphique.
                formule = self.formule_edit.text()
                self.graph.draw_formule(formule,x1,x2)
        except Exception as exp:
            # Si une erreur se produit (ex. domaine incorrect), affiche un message d'erreur.
            formule = self.formule_edit.text()
            self.formule_edit.setText('Erreur ou domaine incorrect:'+formule)
            print(exp)

    def on_click(self, key):
        """
        Gère les clics sur les boutons de l'interface.
        Args:
            key (str): Identifiant de la commande associée au bouton.
        """
        if key == 'Dessiner':
            self.draw_it()
        if key == 'Afficher':
            self.show_it()
        elif key == 'run':
            self.run_it()
        elif key == 'stop':
            self.stop_it()
        elif key == 'exit':
            self.stop_it()
            sys.exit(0)
        else:
            pass
