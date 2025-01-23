import numpy as np
import math
from PyQt5.QtCore import QCoreApplication,    Qt
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit,QLabel,QSlider,QListWidget,QCheckBox,QComboBox 
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from tools.mathsToolsGP import MathsToolsGP


class DialogWidget(QWidget):
    """
    Classe   pour la gestion de l'interface graphique de l'application.
    """

    def create_jauge(self,  grille,row, column,rowspan=1,colspan=1):
        """
        Crée un widget pour afficher une jauge de progression.
        Args:
            grille (QGridLayout): Grille de disposition.
            row (int): Ligne de la grille.
            column (int): Colonne de la grille.
            rowspan (int): Nombre de lignes occupées.
            colspan (int): Nombre de colonnes occupées.
        Returns:
            JaugeWidget: Widget de jauge créé.
        """
        jauge = JaugeWidget(100)
        grille.addWidget(jauge, row, column,rowspan,colspan)
        return jauge

    def create_graph(self,callBack,  grille,row, column,rowspan=1,colspan=1):
        """
        Crée un graphique intégré à l'interface pour l'affichage des résultats.
        Args:
            callBack (fonction): fonction à appeler lors du click sur le graphe.
            grille (QGridLayout): Grille de disposition.
            row (int): Ligne de la grille.
            column (int): Colonne de la grille.
            rowspan (int): Nombre de lignes occupées.
            colspan (int): Nombre de colonnes occupées.
        Returns:
            GrapheWidget: Graphique créé.
        """
        graph = GrapheWidget(self,callBack)
        grille.addWidget(graph, row, column,rowspan,colspan)
        return graph
 
    def create_hand_graph(self,callBack,  grille,row, column,rowspan=1,colspan=1):
        """
        Crée un graphique intégré à l'interface pour l'affichage des résultats.
        Args:
            callBack (fonction): fonction à appeler lors du click sur le graphe.
            grille (QGridLayout): Grille de disposition.
            row (int): Ligne de la grille.
            column (int): Colonne de la grille.
            rowspan (int): Nombre de lignes occupées.
            colspan (int): Nombre de colonnes occupées.
        Returns:
            GrapheWidget: Graphique créé.
        """
        graph = GrapheWidgetHand(self,callBack)
        grille.addWidget(graph, row, column,rowspan,colspan)
        return graph  

    def create_pixmap(self, pixFile, grille,row, column,rowspan=1,colspan=1):
        """
        Crée une image  .
        Args:
            pixFile (str): Nom du fichier image à afficher(logo).
            grille (QGridLayout): Grille de disposition.
            row (int): Ligne de la grille.
            column (int): Colonne de la grille.
            rowspan (int): Nombre de lignes occupées.
            colspan (int): Nombre de colonnes occupées.
        Returns:
            QLabel: Widget pour afficher l'image.
        """
        label = QLabel(self)
        pixmap = QtGui.QPixmap(pixFile)
        pixmap=pixmap.scaled(70,50)
        label.setPixmap(pixmap)
        grille.addWidget(label, row, column,rowspan,colspan)
        return label

    def create_edit(self, text, grille,valeur,readonly, row, column, rowspan=1, colspan=1):
        """
        Crée une entrée texte avec une étiquette.
        Args:
            text (str): Texte de l'étiquette.
            grille (QGridLayout): Grille de disposition.
            valeur (str): Valeur initiale de l'entrée.
            readonly (bool): Si True, l'entrée est en lecture seule.
            row (int): Ligne de la grille.
            column (int): Colonne de la grille.
            rowspan (int): Nombre de lignes occupées.
            colspan (int): Nombre de colonnes occupées.
        Returns:
            QLineEdit: Widget d'entrée créé.
        """
        lbl_formule=QLabel(text)
        lbl_formule.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        grille.addWidget(lbl_formule, row, column)
        edit = QLineEdit()
        edit.setText(str(valeur))
        grille.addWidget(edit, row, column+1, rowspan, colspan-1)
        if(readonly):edit.setReadOnly(True)
        return edit

    def create_label(self, text, grille,valeur, row, column, rowspan=1, colspan=1):
        """
        Crée une entrée label avec une étiquette.
        Args:
            text (str): Texte de l'étiquette.
            grille (QGridLayout): Grille de disposition.
            valeur (str): Valeur initiale de l'entrée.
            row (int): Ligne de la grille.
            column (int): Colonne de la grille.
            rowspan (int): Nombre de lignes occupées.
            colspan (int): Nombre de colonnes occupées.
        Returns:
            QLineEdit: Widget d'entrée créé.
        """
        lbl_formule=QLabel(text)
        lbl_formule.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        grille.addWidget(lbl_formule, row, column)
        lbl = QLabel()
        lbl.setText(str(valeur))
        grille.addWidget(lbl, row, column+1, rowspan, colspan-1)
        return lbl

    def create_Check(self, text, grille,state,readonly, row, column, rowspan=1, colspan=1):
        """
        Crée une entrée texte avec une étiquette.
        Args:
            text (str): Texte de l'étiquette.
            grille (QGridLayout): Grille de disposition.
            state (bool): Valeur initiale de l'entrée.
            readonly (bool): Si True, l'entrée est en lecture seule.
            row (int): Ligne de la grille.
            column (int): Colonne de la grille.
            rowspan (int): Nombre de lignes occupées.
            colspan (int): Nombre de colonnes occupées.
        Returns:
            QCheckBox: Widget d'entrée créé.
        """
        checkBox = QCheckBox(text)
        checkBox.setChecked(state)
        checkBox.setLayoutDirection(Qt.RightToLeft) 
        grille.addWidget(checkBox, row, column, rowspan, colspan)
        if(readonly):checkBox.setReadOnly(True)
        return checkBox


    def create_button(self, text, grille,commande, row, column, rowspan=1, colspan=1):
        """
        Crée un bouton dans l'interface graphique.
        Args:
            text (str): Texte affiché sur le bouton.
            grille (QGridLayout): Grille de disposition.
            commande (str): Commande associée à l'événement du clic.
            row (int): Ligne de la grille.
            column (int): Colonne de la grille.
            rowspan (int): Nombre de lignes occupées.
            colspan (int): Nombre de colonnes occupées.
        """
        button = QPushButton(text)
        button.clicked.connect(lambda: self.on_click(commande))
        grille.addWidget(button, row, column, rowspan, colspan)

    def create_edit_slider(self, text, grille,valeur,val_min,val_max, row):
        """
        Crée un slider accompagné d'une entrée texte.
        Args:
            text (str): Texte de l'étiquette.
            grille (QGridLayout): Grille de disposition.
            valeur (int): Valeur initiale du slider.
            val_min (int): Valeur minimale du slider.
            val_max (int): Valeur maximale du slider.
            row (int): Ligne de la grille.
        Returns:
            QLineEdit: Widget d'entrée texte lié au slider.
        """
        lbl_size=QLabel(text)
        lbl_size.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        grille.addWidget(lbl_size, row, 0)
        edit = QLineEdit()
        edit.setText(str(valeur))
        grille.addWidget(edit, row, 1, 1, 1)
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(val_min)
        slider.setMaximum(val_max)
        slider.setValue(valeur)
        slider.valueChanged.connect(lambda value:edit.setText(str(value)))
        grille.addWidget(slider, row, 2, 1, 2)
        return edit

    def create_liste(self, text, grille,valeur,row,col):
        """
        Crée une listbox avec des valeurs pré-sélectionnées.
        Args:
            text (str): Texte de l'étiquette.
            grille (QGridLayout): Grille de disposition.
            valeur (list): liste à afficher.
            row (int): Ligne de la grille.
            col (int): Colonne de la grille.
        Returns:
            QListWidget: Widget de la listbox.
        """
        lbl_size=QLabel(text)
        lbl_size.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        grille.addWidget(lbl_size, row, col)
        listWidget = QListWidget()
        listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection )
        listWidget.setGeometry(QtCore.QRect(10, 10, 211, 291))
        listWidget.setStyleSheet('QListWidget::item:selected{background: rgb(128,128,255);}');
        for val in valeur:
            item = QtWidgets.QListWidgetItem( val)
            listWidget.addItem(item)
            item.setSelected(True)
        grille.addWidget(listWidget, row, col+1, 1, 1)
        return listWidget

    def create_Combo(self, text, grille,valeurs,val_sel,row, column, rowspan=1, colspan=1):
        """
        Crée une listbox avec des valeurs pré-sélectionnées.
        Args:
            text (str): Texte de l'étiquette.
            grille (QGridLayout): Grille de disposition.
            valeur (list): liste à afficher.
            row (int): Ligne de la grille.
            column (int): Colonne de la grille.
            rowspan (int): Nombre de lignes occupées.
            colspan (int): Nombre de colonnes occupées.
        Returns:
            QListWidget: Widget de la listbox.
        """
        lbl_size=QLabel(text)
        lbl_size.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
        grille.addWidget(lbl_size, row, column)
        comboWidget = QComboBox()
        for strItem,strCmd in valeurs:
            comboWidget.addItem(strItem,strCmd)
        comboWidget.setCurrentIndex(comboWidget.findData(val_sel))
        grille.addWidget(comboWidget, row,  column+1, rowspan, colspan-1)
        return comboWidget


#----------------------------------------------------------------------------------------------
"""
GrapheWidget:
-------------
Structure et fonctionnalités principales
	La classe GrapheWidget encapsule une figure Matplotlib pour l'intégrer dans une application PyQt5.
	Elle fournit des méthodes pour dessiner différents types de graphiques (formules mathématiques, résultats, convergence, graphes génétiques).
	Une barre d'outils Matplotlib est incluse pour permettre une interaction directe avec le graphique (zoom, déplacement).
Méthodes importantes
	clear : Réinitialise la figure en effaçant tout contenu précédent.
	draw_formule : Permet de tracer une fonction mathématique spécifiée dans un intervalle donné.
	draw_resultat : Affiche les résultats réels comparés aux prédictions.
	draw_convergente : Trace une courbe de convergence pour montrer l'évolution de la fitness.
	draw_graph : Affiche une structure d'arbre génétique en tant que graphe.
	Gestion des événements
	onpick : Permet de détecter un clic sur un élément du graphique et d'interagir avec ses données (par exemple, récupérer les coordonnées d'un point cliqué).
"""
 

class GrapheWidget(FigureCanvas):
    """
    Classe personnalisée pour afficher des graphiques Matplotlib dans une application PyQt5.
    Hérite de `FigureCanvas` et encapsule la gestion des graphiques.

    Fonctionnalités principales :
    - Supporte plusieurs types de graphiques (formules, résultats, convergence, graphes).
    - Permet de dessiner, mettre à jour, et interagir avec les graphiques.
    - Intègre un outil de navigation (zoom, déplacement) pour les graphiques.

    Attributes:
        fig (Figure): Instance de figure Matplotlib utilisée pour dessiner les graphiques.
        axes (Axes): Axes principaux de la figure pour le tracé des données.
        toolbar (NavigationToolbar): Barre d'outils Matplotlib pour manipuler le graphique.
    """
  
    def __init__(self,parent=None,callBack=None, width=5, height=4, dpi=100): #callBack : appelé pour regarder la valeur de la fitness à la ieme itération
        """
        Initialise une instance de graphique Matplotlib intégrée à l'interface PyQt5.

        Args:
            parent (QWidget, optional): Widget parent dans lequel le graphique sera intégré.
            width (int, optional): Largeur de la figure en pouces. Par défaut 5.
            height (int, optional): Hauteur de la figure en pouces. Par défaut 4.
            dpi (int, optional): Résolution de la figure en points par pouce. Par défaut 100.
        """
        # Crée une figure Matplotlib avec les dimensions et la résolution spécifiées.
        matplotlib.rcParams.update({'font.size': 6})
        # Crée un ensemble d'axes par défaut et active la grille.
        self.fig = Figure(figsize=(width, height), dpi=dpi,)
        self.axes = self.fig.gca()
        self.axes.grid()
        # Initialise la classe parente FigureCanvas.
        FigureCanvas.__init__(self, self.fig)
        # Définit le parent pour l'intégration dans PyQt.
        self.setParent(parent)
        # Ajoute une barre d'outils pour manipuler le graphique (zoom, déplacement, etc.).
        self.toolbar = NavigationToolbar(self, self)
        self.toolbar.setFixedHeight( 20)
        # Définit la taille minimale du widget pour éviter des dimensions trop petites.
        self.setMinimumSize(300, 150)
        self.callBackFonct=callBack
        self.x_conv=[]
        self.y_conv=[]
        if(self.callBackFonct is not None):
            self.fig.canvas.mpl_connect('pick_event', self.onpick)


    def clear(self):
        """
        Efface le contenu du graphique actuel, réinitialise les axes et redessine.
        """
        self.x_conv=[]
        self.y_conv=[]
        self.axes.clear()
        self.axes.grid()  # Réactive la grille après nettoyage.
        self.draw()  # Redessine le graphique avec un contenu vide.

    def draw_formule(self, formule, x1, x2):
        """
        Dessine le graphique correspondant à une formule mathématique donnée.

        Args:
            formule (str): Formule mathématique à tracer .
            x1 (float): Limite inférieure de l'intervalle des x.
            x2 (float): Limite supérieure de l'intervalle des x.
        """
        self.clear()  # Efface le graphique précédent.

        # Définir un titre avec la formule.
        self.axes.set_title(formule)
        self.axes.clear()
        if(formule!=""):
            # Génère les points à tracer.
            X = [x for x in np.arange(x1, x2, 0.01)]  # Intervalle de x avec pas de 0.01.
            y = [MathsToolsGP.evaluate_formule(formule,x=x1) for x1 in X]  # Évaluation de la formule pour chaque x.

            # Trace la courbe.
            self.axes.plot(X, y, color='b', dashes=[6, 2])
            self.draw()  # Redessine le graphique.


    def draw_resultat(self, X, y, y_pred):
        """
        Dessine le graphique des résultats réels (y) comparés aux prédictions (y_pred).

        Args:
            X (list): Liste des valeurs d'entrée.
            y (list): Liste des valeurs réelles (sorties).
            y_pred (list): Liste des valeurs prédites.
        """
        self.clear()  # Efface le graphique précédent.
        self.axes.clear()

        # Trace les résultats réels en bleu.
        self.axes.plot(X, y, color='b', dashes=[6, 2])

        # Trace les prédictions en rouge.
        self.axes.plot(X, y_pred, color='r', dashes=[6, 3])
        self.draw()  # Redessine le graphique.

    def draw_convergente(self, y_conv):
        """
        Trace la courbe de convergence de la fitness au cours des itérations.

        Args:
            y_conv (list): Liste des valeurs de fitness à chaque itération.
        """
        self.clear()  # Efface le graphique précédent.

        # Génère l'axe x (les indices des itérations).
        Z = [x for x in range(len(y_conv))]

        # Trace la courbe de convergence en rouge.
        self.axes.plot(Z, y_conv, color='r',  picker=True, pickradius=3)
        self.draw()  # Redessine le graphique.

    def draw_convergente_item(self,max_iterations,iteration,fitness):
        """
        Trace la courbe de convergence de la fitness au cours des itérations.

        Args:
            y_conv (list): Liste des valeurs de fitness à chaque itération.
        """
        # Génère l'axe x (les indices des itérations).
        self.x_conv.append(iteration)  
        self.y_conv.append(fitness)  
        # Trace la courbe de convergence en rouge.
        self.axes.set_xlim([0, max_iterations+1])        # Fixe les limites de l'axe x
        self.axes.set_autoscalex_on(False)             # Désactive l'auto-échelle sur l'axe x
        self.axes.plot(self.x_conv, self.y_conv, color='r')
        self.draw()  # Redessine le graphique.

    def draw_graph(self, tree):
        """
        Dessine un graphe représentant une structure d'arbre génétique.

        Args:
            tree (Tree): Instance d'arbre à dessiner.
        """
        self.clear()  # Efface le graphique précédent.

        # Demande à l'arbre de dessiner ses noeuds et connexions sur les axes.
        tree.draw(self.axes)

        # Désactive les axes pour un affichage plus propre.
        self.axes.set_axis_off()
        self.draw()  # Redessine le graphique. 

    def onpick(self,event):
        """
        Gère l'événement de sélection d'un élément graphique (par exemple, un point ou une courbe).

        Args:
            event (PickEvent): Événement déclenché lors d'un clic sur un élément.
        """
        # si il n'y a pas de fonction callback: ne rien faire
        if self.callBackFonct is  None :
            return
        # Récupère les données de l'élément cliqué.
        thisline = event.artist
        ind = event.ind
        pos=ind[0]
        #appeler la fonction callback
        self.callBackFonct(pos)

#------------------------------------------------------------------------------------------
"""
Classe GrapheWidgetHand : Cette classe hérite de GrapheWidget et ajoute des fonctionnalités interactives pour dessiner à main levée sur un graphique, tout en conservant la possibilité d'afficher des formules mathématiques.

Méthodes press, move, release : Ces méthodes gèrent les événements de la souris pour permettre à l'utilisateur de dessiner en cliquant et en déplaçant la souris sur le graphique.

press : Lorsqu'un bouton de la souris est pressé, il initialise le dessin.
move : Lorsque la souris est déplacée, elle dessine une ligne entre les points précédents et le point actuel.
release : Lorsque le bouton de la souris est relâché, le dessin s'arrête.
Méthode draw_formule : Cette méthode permet de dessiner une formule mathématique sur le graphique. Si aucune formule n'est fournie, elle trace une ligne rouge par défaut, sinon elle appelle la méthode de la classe parente pour dessiner la formule.

Objectif :
    Cette classe permet d'ajouter une fonctionnalité d'interaction avec l'utilisateur pour dessiner des courbes sur un graphique, tout en intégrant la possibilité de superposer une formule mathématique. Elle est idéale pour des applications nécessitant une visualisation interactive et l'affichage de formules.

"""
class GrapheWidgetHand(GrapheWidget):
    """
    Cette classe hérite de GrapheWidget et permet d'ajouter des fonctionnalités interactives de dessin à main levée.
    Elle permet de dessiner des lignes sur un graphique en traçant les mouvements de la souris, tout en maintenant 
    les fonctionnalités de la classe parent pour afficher des formules mathématiques.
    """
    def __init__(self,parent=None,callBack=None, width=5, height=4, dpi=100):
        """
        Initialisation de la classe GrapheWidgetHand.
        
        Args:
            parent (object, optional): Le parent du widget (par défaut None).
            callBack (function, optional): Fonction de rappel (par défaut None).
            width (int, optional): Largeur de la figure (par défaut 5).
            height (int, optional): Hauteur de la figure (par défaut 4).
            dpi (int, optional): Résolution de la figure (par défaut 100).
        """
        # Initialisation de la classe parente (GrapheWidget) avec les paramètres par défaut
        GrapheWidget.__init__(self,parent=None,callBack=None, width=5, height=4, dpi=100)

        # Initialisation des attributs pour gérer l'interaction avec la souris
        self.onpress=False # Indique si le bouton de la souris est enfoncé
        self.formule=""    # Formule mathématique à afficher (initialement vide)
        self.x=[]          # Liste des coordonnées x pour dessiner
        self.y=[]          # Liste des coordonnées y pour dessiner
        self.x1=0
        self.x2=10
        # Connexion des événements de la souris à des méthodes
        self.fig.canvas.mpl_connect('button_press_event', self.press)     # Lors d'un clic de souris
        self.fig.canvas.mpl_connect('button_release_event', self.release) # Lors d'un relâchement de la souris
        self.fig.canvas.mpl_connect('motion_notify_event', self.move)     # Lors d'un mouvement de la souris

        # Efface l'écran au démarrage
        self.clear()

    def clear(self):
            super().clear()
            if len(self.formule)==0 :
                self.axes.set_xlim([self.x1, self.x2])        # Fixe les limites de l'axe x
                self.axes.set_ylim([-100, 100])       # Fixe les limites de l'axe y
                self.axes.set_autoscalex_on(False)  # Désactive l'auto-échelle sur l'axe x
                self.axes.set_autoscaley_on(False)  # Désactive l'auto-échelle sur l'axe y
                # Trace une ligne rouge par défaut entre les deux points
                self.axes.plot([self.x1,-10], [self.x2,10], color='r',scalex=False, scaley=False,  dashes=[6, 2])
                self.draw() 
    def move(self, event):
        """
        Gère le mouvement de la souris, permettant de dessiner des lignes à main levée.
        
        Args:
            event (matplotlib.backend_bases.MouseEvent): L'événement de mouvement de la souris.
        """
        # Si une formule est déjà dessinée, on ne permet pas d'interaction
        if len(self.formule)!=0 :
            return
        
        # Si le bouton de la souris est enfoncé, on dessine une ligne
        if(self.onpress==True):
            # Vérification de la validité des coordonnées
            if event.xdata is None or event.xdata is None  :return
            
            # Ajoute les nouvelles coordonnées à la liste
            self.x.append(event.xdata)
            self.y.append(event.ydata)

            # Trace une ligne entre les deux derniers points
            X=[self.old_x,event.xdata]
            Y=[self.old_y,event.ydata]
            self.old_x=event.xdata     # Mise à jour des anciennes coordonnées
            self.old_y=event.ydata     # Mise à jour des anciennes coordonnées
            self.axes.plot(X, Y, color='b',scalex=False, scaley=False,  dashes=[6, 2])
            self.draw()  # Redessine le graphique.

    def press(self, event):
        """
        Gère l'événement de pression du bouton de la souris, initialisant le dessin.
        
        Args:
            event (matplotlib.backend_bases.MouseEvent): L'événement de pression du bouton.
        """
        # Si une formule est déjà affichée, on ne permet pas d'interaction
        if len(self.formule)!=0 :
            return
        # Efface le graphique précédent et initialise les nouvelles coordonnées
        self.clear()
        self.old_x=event.xdata
        self.old_y=event.ydata
        self.x=[]            # Vide les listes de coordonnées
        self.y=[]            # Vide les listes de coordonnées
        self.onpress=True    # Le bouton de la souris est enfoncé, on commence à dessiner

    def release(self, event):
        """
        Gère l'événement de relâchement du bouton de la souris, arrêtant le dessin.
        
        Args:
            event (matplotlib.backend_bases.MouseEvent): L'événement de relâchement du bouton.
        """
        # Si une formule est déjà affichée, on ne permet pas d'interaction
        if len(self.formule)!=0 :
            return
        # Arrête l'interaction avec la souris
        self.onpress=False
        
        # Mise à jour des coordonnées si elles sont valides
        if event.xdata is None or event.xdata is None :return
        self.old_x=event.xdata
        self.old_y=event.ydata
        


    def draw_formule(self,formule,x1,x2):
        """
        Dessine une formule mathématique sur le graphique.
        
        Args:
            formule (str): La formule à afficher.
            x1 (float): Limite gauche de l'axe x.
            x2 (float): Limite droite de l'axe x.
        """
        # Si une formule est spécifiée, elle est utilisée pour le dessin
        self.formule=formule
        if(len(self.formule)==0):
            self.x1=x1
            self.x2=x2
            self.clear()
        else:
            # Si une formule est fournie, on appelle la méthode parent pour l'afficher
            super().draw_formule(self.formule,x1,x2)
#--------------------------------------------------------------------------------
"""
JaugeWidget:
------------
Structure et fonctionnalités principales
	La classe JaugeWidget permet d'afficher une jauge de progression sous forme de barre, en mettant à jour la barre au fur et à mesure que le processus progresse.
	Elle offre une personnalisation complète du texte et de l'apparence de la jauge, y compris les couleurs, les graduations et le message d'accompagnement.

Méthodes importantes
	__init__ :
		Initialise les attributs essentiels de la jauge (valeur, message, graduations, etc.).
		Définit la taille minimale du widget et la police pour afficher le texte.
	set_jauge_value :
		Permet de mettre à jour la valeur actuelle de la jauge, le message à afficher et la valeur maximale.
		Met à jour également les graduations (valeurs divisées en pourcentages ou étapes) et redessine la jauge.
	paintEvent :
		Gère l'événement de peinture. C'est ici que le widget est redessiné à chaque fois que la valeur ou les attributs sont mis à jour.
	drawWidget :
		Dessine la jauge et ses différentes parties (partie remplie, partie vide, graduations et texte) en utilisant QPainter.
		Affiche également les graduations et le texte de message si nécessaire.

Gestion des graduations et du message :
	La jauge est divisée en étapes égales, et les valeurs sont dessinées pour représenter la progression.
	Le message est centré sur la jauge si une valeur est définie.

Aspect visuel et design
	Couleur : La jauge est colorée en bleu pour la progression et en jaune clair pour la partie remplie. La partie vide est colorée en gris.
	Bordure et graduation : La bordure est noire et chaque graduation est espacée régulièrement. Les valeurs de progression sont affichées en bas de la jauge.
"""

class JaugeWidget(QtWidgets.QWidget):
    """
    Classe représentant un widget personnalisé de jauge de progression.
    Ce widget est utilisé pour afficher visuellement l'avancement d'un processus
    (par exemple, une opération de calcul) en mettant à jour la valeur de la jauge.
    
    Attributs :
        value (int): La valeur actuelle de la jauge.
        max_value (int): La valeur maximale de la jauge.
        str_message (str): Le message à afficher sur la jauge.
        font (QFont): Police de caractère utilisée pour afficher le texte.
    """
    def __init__(self, max_value):
        """
        Initialise le widget de jauge de progression.

        Args:
            max_value (int): La valeur maximale de la jauge (par exemple, 100% ou 1000).
        """
        super().__init__()
        
        # Initialisation de la taille minimale du widget.
        self.setMinimumSize(1, 30)

        # Valeur actuelle de la jauge (initialement à 1).
        self.value = 1

        # Message affiché sur la jauge.
        self.str_message = ""

        # Valeur maximale de la jauge.
        self.max_value = max_value


        # Police de caractère pour le texte.
        self.font = QtGui.QFont('Serif', 7, QtGui.QFont.Light)

    def set_jauge_value(self, str_message, pos_value, max_value):
        """
        Met à jour les informations et la valeur de la jauge.

        Args:
            str_message (str): Le message à afficher sur la jauge (par exemple, "En cours").
            pos_value (int): La valeur actuelle de la jauge (par exemple, l'étape actuelle).
            max_value (int): La valeur maximale de la jauge.
        """
        # Met à jour la valeur et le message de la jauge.
        self.value = pos_value
        self.max_value = max_value
        self.str_message = str_message
        
        
        # Redessine le widget avec les nouvelles valeurs.
        self.update()

    def paintEvent(self, e):
        """
        Redessine le widget chaque fois qu'il est mis à jour (lors d'un changement de valeur).

        Args:
            e (QPaintEvent): L'événement de peinture (n'est pas utilisé ici, mais nécessaire).
        """
        # Crée un objet QPainter pour dessiner sur le widget.
        qp = QtGui.QPainter()
        
        # Commence le dessin.
        qp.begin(self)
        
        # Dessine la jauge (barre de progression).
        self.drawWidget(qp) 
         
        # Termine le dessin.
        qp.end()

    def drawWidget(self, qp):
        """
        Dessine la jauge de progression sur le widget en utilisant QPainter.
        
        Args:
            qp (QPainter): L'objet QPainter utilisé pour dessiner la jauge.
        """
        # Définit la police pour le texte.
        qp.setFont(self.font)
        
        # Récupère la taille actuelle du widget.
        size = self.size()
        w = size.width()
        h = size.height()

        # Calcule les étapes pour la jauge en fonction de la taille du widget.
        step = int(round(w / 10.0))
        
        # Calcule la position du remplissage de la jauge.
        till = int(((w / self.max_value) * self.value))
        full = int(((w / self.max_value) * self.max_value))

        # Si la jauge est pleine, on dessine une partie colorée différente pour indiquer la progression.
        if self.value >= self.max_value:
            qp.setPen(QtGui.QColor(255, 255, 255))  # Couleur blanche pour la partie pleine.
            qp.setBrush(QtGui.QColor(255, 255, 184))  # Couleur jaune clair pour la partie remplie.
            qp.drawRect(0, 0, full, h)  # Dessine la partie pleine de la jauge.

            qp.setPen(QtGui.QColor(255, 175, 175))  # Couleur grise pour la partie restante.
            qp.setBrush(QtGui.QColor(255, 175, 175))  # Couleur grise.
            qp.drawRect(full, 0, till - full, h)  # Dessine la partie vide restante.
        else:
            # Si la jauge n'est pas encore pleine, on affiche la progression en bleu.
            qp.setPen(QtGui.QColor(255, 255, 255))
            qp.setBrush(QtGui.QColor(0, 128, 0))  # Couleur bleue pour la progression.
            qp.drawRect(0, 0, till, h)  # Dessine la barre de progression.

        # Définit les paramètres pour dessiner la bordure de la jauge.
        pen = QtGui.QPen(QtGui.QColor(20, 20, 20), 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawRect(0, 0, w - 1, h - 1)  # Dessine la bordure de la jauge.

        if self.str_message != "":
            # Si un message est défini, on l'affiche au centre de la jauge.
            texte = self.str_message + ' : ' + str(self.value) + ' / ' + str(self.max_value)
            metrics = qp.fontMetrics()
            fw = metrics.width(texte)
            qp.drawText(int((w - fw) / 2), int(3 * h / 4), texte)  # Dessine le texte au centre.

        # Dessine les graduations sur la jauge.
        j = 1  # Initialisation de l'index pour les graduations.
        for i in range(step, 10 * step, step):
            qp.drawLine(i, 0, i, 5)  # Trace les lignes de graduation.
            if self.str_message == "":
                # Affiche les valeurs des graduations sous forme de texte.
                metrics = qp.fontMetrics()
                fw = metrics.width(str(j))
                qp.drawText(int(i - fw / 2), int(h / 2), str(j))  # Affiche les numéros sur la jauge.
            j = j + 1 

 