from math import *
import numpy as np
import random
 
 
"""
Node
-----
 Cette classe représente un noeud individuel dans l'arbre génétique (ou autre structure), qui peut être un terminal ou une fonction. Chaque noeud peut avoir un ou plusieurs enfants, en fonction de la structure de l'arbre (fonction binaire, unaire, ou terminal).
"""
class Node():
    """
    Classe représentant un noeud dans un arbre génétique.
    Chaque noeud peut être un terminal (une valeur) ou une fonction (unaire ou binaire).
    Un arbre génétique est composé de plusieurs noeuds reliés entre eux par des branches.
    
    Attributs :
        gene (obj): Le gene du noeud, qui peut être une fonction ou un terminal.
        parent (Node): Le parent du noeud actuel (None si c'est la racine).
        left (Node): L'enfant gauche du noeud, utilisé dans le cas des fonctions binaires ou unaires.
        right (Node): L'enfant droit du noeud, utilisé dans le cas des fonctions binaires.
        id (int): Un identifiant unique pour chaque noeud.
        x (int): Coordonnée x pour l'affichage graphique du noeud.
        y (int): Coordonnée y pour l'affichage graphique du noeud.
    """
    def __init__(self,gene,parent,left,right,id,x,y):
        """
        Initialise un noeud avec les informations fournies.

        Args:
            gene (obj): Le gene du noeud, représentant soit une fonction (par exemple, '+', 'sin', etc.) soit un terminal (par exemple, 'x', '5').
            parent (Node): Le parent du noeud, ou None si c'est la racine.
            left (Node): L'enfant gauche du noeud, utilisé dans les fonctions binaires ou unaires.
            right (Node): L'enfant droit du noeud, utilisé dans les fonctions binaires.
            id (int): Un identifiant unique pour chaque noeud.
            x (int): Position x du noeud pour l'affichage graphique.
            y (int): Position y du noeud pour l'affichage graphique.
        """
        self.gene = gene     # Nom du noeud (fonction ou terminal).
        self.parent = parent # Parent du noeud (None si c'est la racine).
        self.left = left     # Enfant gauche du noeud (utilisé dans les fonctions binaires ou unaires).
        self.right = right   # Enfant droit du noeud (utilisé dans les fonctions binaires).
        self.id = id         # Identifiant unique du noeud.
        self.x = x           # Coordonnée x pour l'affichage graphique.
        self.y = y           # Coordonnée y pour l'affichage graphique.

#---------------------------------------------------------------------------------------

"""
TreeGP
-------
Cette classe représente un individu génétique sous forme d'arbre dans un algorithme de programmation génétique (GP). Elle contient des méthodes permettant de gérer la création de l'arbre.
Attributs
	root : Le noeud racine de l'arbre, point d'entrée de la structure génétique.
	x et y : Coordonnées utilisées pour le dessin graphique de l'arbre.
	nbNode : Nombre de noeuds dans l'arbre, utilisé pour le suivi et le contrôle de la taille de l'arbre.
 
"""

class TreeGP():
    """
    Classe représentant un individu génétique sous forme d'arbre dans un algorithme de programmation génétique.
 
    
    Attributs :
        root (Node) : Le noeud racine de l'arbre, représentant le point d'entrée de l'arbre génétique.
        x (int)     : Coordonnée x pour l'affichage graphique de l'arbre.
        y (int)     : Coordonnée y pour l'affichage graphique de l'arbre.
        nbNode (int): Nombre total de noeuds dans l'arbre.
    """
    
    def __init__(self,depth,x=0,y=0):
        """
        Initialise un arbre génétique avec une profondeur donnée et une méthode d'initialisation spécifiée.

        Args:
            depth (int): Profondeur maximale de l'arbre.
            method (str): Méthode d'initialisation de l'arbre ('full', 'grow', etc.).
            x (int, optional): Coordonnée x pour la position de l'arbre (par défaut 0).
            y (int, optional): Coordonnée y pour la position de l'arbre (par défaut 0).
        """
        self.root = None         # Le noeud racine de l'arbre.
        self.x = x               # Position en x de l'arbre.
        self.y = y               # Position en y de l'arbre.
        self.nbNode = 0          # Initialisation du nombre de noeuds à 0.
        self.depth=depth
 
#----------------
    def read(self,gen,depth):  
        """
        Lit une représentation génétique  et construit l'arbre.
        
        Args:
            gen (list): Génome représentant l'individu sous forme d'une liste d'éléments (nœuds).
            depth (int): Profondeur de l'arbre (utilisée dans la lecture des génomes).
        """
        self.depth=depth
        self.root = self.__read_aux(None,gen,0,False,self.depth)[1]
 
    def __read_aux(self,curent_node,gen,position,is_left,depth):
        """
        Fonction auxiliaire qui construit l'arbre à partir du génome donné en utilisant la position et la profondeur.
        
        Args:
            current_node (Node): Le noeud courant dans l'arbre.
            gen (list): Liste représentant le génome.
            position (int): Position actuelle dans le génome.
            is_left (bool): Indique si le noeud doit être placé à gauche ou à droite du noeud parent.
            depth (int): Profondeur restante pour la construction de l'arbre.

        Returns:
            tuple: (nouvelle position, noeud créé)
        """
        elem=gen[position] # Récupère l'élément du génome à la position actuelle

        if curent_node is not None:
            offsetX=2**depth # Calcul du décalage pour la position des sous-arbres
            # Ajuste la position en fonction de si le noeud est à gauche ou à droite
            if(is_left):
                pos_x=curent_node.x-(offsetX *20)
            else:
                pos_x=curent_node.x+(offsetX *20)
            pos_y=curent_node.y -10
        else:
            offsetX=0
            pos_x=self.x
            pos_y=self.y
        depth=depth-1
        if elem.is_terminal():
            return position,Node(elem,curent_node,None,None,position,pos_x,pos_y)
        elif elem.is_fonction_binaire():
            node=Node(elem,curent_node,None,None,position,pos_x,pos_y)
            position,node.left=self.__read_aux(node,gen,position + 1,True,depth)# Sous-arbre gauche
            position,node.right=self.__read_aux(node,gen,position + 1,False,depth)# Sous-arbre droit
            return position, node
        elif elem.is_fonction_unaire():
            node=Node(elem,curent_node,None,None,position,pos_x,pos_y)
            position,node.left=self.__read_aux(node,gen,position + 1,True,depth)# Sous-arbre
            return position,node
#----------------
    def draw(self,ax,select=None):
        """
        Dessine l'arbre génétique sur un graphique donné.

        Args:
            ax (matplotlib.axes.Axes): L'axe sur lequel l'arbre sera dessiné.
            select (optional): ID du noeud à sélectionner (met en surbrillance ce noeud).
        """
        if self.root  != None :
            self.__draw_aux(ax,self.root,select)
    def __draw_aux(self,ax,node,select):
        """
        Fonction auxiliaire pour dessiner récursivement l'arbre génétique.

        Args:
            ax (matplotlib.axes.Axes): L'axe sur lequel l'arbre sera dessiné.
            node (Node): Le noeud actuel de l'arbre à dessiner.
            select (optional): ID du noeud à sélectionner.
        """
        if node is None:
            return
        # Définition de la couleur et du style de chaque type de noeud
        if select is not None and node.id==select : # Surbrillance du noeud sélectionné
            bbox=dict(boxstyle='square',fc='red')
        elif node.gene.is_terminal():      # Noeud terminal
            bbox=dict(boxstyle='square',fc='green')
        elif node.gene.is_fonction_binaire():       # Noeud binaire
            bbox=dict(boxstyle='round,pad=0.3',fc='orange')
        else:
            bbox=dict(boxstyle='square',fc='yellow')# Noeud unaire

        # Affiche le nom du noeud avec le style de la boîte
        ax.text(node.x,node.y,str(node.gene.name_gen),bbox=bbox,fontsize=8,ha='center',va='center')  

        # Dessine les arêtes reliant les noeuds parents et enfants
        if node.parent is not None:
             ax.plot((node.parent.x, node.x), (node.parent.y, node.y),color='k') # Ligne entre parent et enfant
        if node.left is not None :
             self.__draw_aux(ax,node.left,select)  # Dessine le sous-arbre gauche
        if node.right is not None :
             self.__draw_aux(ax,node.right,select) # Dessine le sous-arbre droit


