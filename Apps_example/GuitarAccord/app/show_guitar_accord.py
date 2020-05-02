#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Display guitar chords from listedesaccords database
"""
# import des blibliothèques python

import sys
import tkinter as tk
import tkinter.ttk as ttk

# import des paramètres géométriques
from .guitare_parameter import CORDES_ESPACEMENT, \
                              CORDES_OFFSET, \
                              FRETTES_NOMBRE, \
                              FRETTES_ESPACEMENT, \
                              GUITARE_LARGEUR, \
                              GUITARE_HAUTEUR, \
                              WOOD_BG
# import du dictionnaire d'accords
from .listedesaccords import CHORDS
# création d'un manche en bois si WOOD_BG = True
if WOOD_BG : from .woodenbackground import get_background # créé image de fond (optionel)

################# Interface Principale ##############################
class MainGui:
    """
    Créé un object de classe Guitare qui à l'interaction crée des listes déroulantes.
    L'object est placé selon la méthode 'pack()' de tkinter, suivant la position 'pos'
    Appelle la classe Guitare, un canvas contenant la grille, TextAccord, une boite
    de texte pour afficher le nom de l'accord selectionné, DropList, des listes pour
    selectionner l'accord à afficher.
    Usage : MainGui(fenetre, position = [x,y])
    """

    #: crée un grille interactive représentant une guitare
    def __init__(self, root, pos=[0,0]):

        mainframe = tk.Frame(root, relief="sunken", borderwidth=3)

        #: Création d'une grille représentant une guitare
        frame1=tk.Frame(mainframe)
        self.name = TextAccord(frame1) # pour affichage du nom de l'accord
        self.guitare = Guitare(frame1, callback=self.on_click) # grille
        frame1.pack(side=tk.BOTTOM)

        mainframe.grid(row=pos[0], column=pos[1])
        
        root.bind('<Escape>', lambda e: sys.exit())

    #: A l'interaction, Création de listes déroulantes pour selection de l'accord
    def on_click(self, event):

        self.popup_frame = tk.Toplevel() # popup window
        self.accordage = DropList(frame = self.popup_frame,
                                  text = "accordage",
                                  liste = list(CHORDS),
                                  callback = self.change_accords_liste)
        self.accord = DropList(frame = self.popup_frame,
                               text = "accord",
                               callback = self.change_variantes_liste)
        self.variante = DropList(frame = self.popup_frame,
                                 text = "variante",
                                 callback = self.dessine_tablature)

    #: Modification de la liste des accords (appellé par DropList)
    def change_accords_liste(self, event):

        accordage = self.accordage.box.get() # accordage selectionné
        accords = list( CHORDS[accordage] ) # liste des accords pour cet accordage

        self.accord.box['values'] = accords # on applique au widjet

    #: Modification de la liste des variantes de l'accord (appellé par DropList)
    def change_variantes_liste(self, event):

        accordage = self.accordage.box.get()
        accord = self.accord.box.get()
        variantes = list( CHORDS[accordage][accord] )

        self.variante.box['values'] = variantes

    #: Affichage de l'accord sur le manche et ferme la popup
    def dessine_tablature(self, event):

        accordage = self.accordage.box.get()
        accord = self.accord.box.get()
        variante = self.variante.box.current()
        accord_choisi = CHORDS[accordage][accord][variante]

        self.popup_frame.destroy() # detruit la popup
        self.name.display_name(accord) # affiche le nom de l'accord
        self.guitare.show_accord(accord_choisi)


################# Widgets & Canvas #####################################

class TextAccord:
    """
    Crée une boite pour l'affichage du nom de l'accord,
    appellé à la selection de la variante
    """

    def __init__(self, frame):
        self.name = tk.StringVar()
        self.box_name = tk.Message(frame,
                                   textvariable=self.name,
                                   font=("Comics", 12),
                                   width=80)
        self.box_name.pack(side=tk.TOP)

    #: Affiche le nom de l'accord
    def display_name(self, accord):
        self.name.set(str(accord))

class DropList:
    """
    Créé une liste déroulante afin de selectionner les accords à afficher
    affiche la liste "values" et excecute "callback" à la selection
    Usage : DropList(fenetre, nom_de_la_liste, callback, values)
    """

    def __init__(self, frame, text, callback, liste=None):

        subframe = tk.Frame(frame)
        self.value = tk.StringVar()
        self.box = ttk.Combobox(subframe,
                                textvariable=self.value,
                                width = 11)
        self.box.bind('<<ComboboxSelected>>', callback)
        self.box['values'] = liste
        self.box.pack(side=tk.RIGHT)

        self.name = tk.StringVar()
        self.name = tk.Message(subframe, text=text, font=("Comics", 12), width=100)
        self.name.pack(side=tk.RIGHT)

        subframe.pack(side=tk.TOP)


class Guitare:
    """
    Crée une grille représentant un manche de guitare et affiche l'accord
    selectionné.
    Au clique gauche, ouvre un popup permettant de choisir l'accord à afficher
    Usage : Guitare(fenetre, callback = on_click)
    """

    #: Création de l'espace de dessin
    def __init__(self, frame, callback):

        self.frame = frame
        # Espace de dessin
        self.canvas1 = tk.Canvas(self.frame,
                                 width = GUITARE_LARGEUR,
                                 height = GUITARE_HAUTEUR)
        self.canvas1.bind("<Button-1>", callback) # au clique gauche : callback

        # Listera les objets pour manipulation/suppression
        self.accord_precedent = [0]*6 # par défaut, on crée un manche avec 6 cordes
        self.numero_frette = [] # indice de la première frette affichée

        # Création du manche de guitare en fonction du nombre de cordes
        nb_cordes = len(list(CHORDS)[0])
        self.guitare = self.create_guitare(nb_cordes)

        self.canvas1.pack(side=tk.TOP)
    
    #: Création du manche (frettes + cordes + background)
    def create_guitare(self, cordes_nombre):

        # On supprime tout ce qu'on a pu dessiner précédemment
        self.canvas1.delete("all")

        # Obtention des dimensions du manche
        self.largeur = (cordes_nombre - 1) * CORDES_ESPACEMENT\
                        + 2 * CORDES_OFFSET
        self.longueur = FRETTES_NOMBRE * FRETTES_ESPACEMENT

        # Génération procédurale d'une image de manche en bois
        if WOOD_BG :
            self.canvas1.background = get_background((self.largeur*2, self.longueur*2))
            self.background = self.canvas1.create_image(0, 0, image=self.canvas1.background)

        # Création des frettes
        Frette(self.canvas1, 1, self.largeur, width=5) # 1ère plus large
        for n in range(FRETTES_NOMBRE) : # puis les autres
            Frette(self.canvas1, n, self.largeur)

        # Création des cordes
        self.cordes_list=[] # on enregistrera les objects corde
        for n in range(cordes_nombre):
            corde = Corde(self.canvas1, n)
            self.cordes_list.append(corde)

    #: Dessine l'accord sur le manche
    def show_accord(self, accord_choisi):

        # On efface l'accord précédent
        self.clear_accord()

        # on redessine le manche si le nombre de cordes à changé
        if len(accord_choisi) != len(self.accord_precedent) :
            self.create_guitare(len(accord_choisi))

        # On l'affiche à partir de la première frette utilisée
        accord_norm, position_frette = self.get_accord_norm(accord_choisi)

        # On dessine, une à une, les notes de l'accord
        self.accord_precedent = [] # remise à zero
        for n, note in enumerate(accord_norm) :
            self.accord_precedent.append(self.cordes_list[n].play(note))

        # On affiche le numero de frette
        self.print_frette_number(position_frette)

    #: Efface l'accord précédent
    def clear_accord(self):

        for n in range(len(self.accord_precedent)):
            self.canvas1.delete(self.accord_precedent[n])

    #: Correction de la valeur des notes pour afficher uniquement la zone du manche utilisée
    def get_accord_norm(self, accord_choisi):

        note_min = 50 # indice de la note la plus basse sur le manche (ni "0" ni "x")
        for i, note in enumerate (accord_choisi):
            if isinstance(note, int): # ni x
                if note >= 1 : # ni 0
                    if note < note_min :
                        note_min = note

        accord_norm = [0] * len(accord_choisi) # accord abaissé de note_min
        for i, note in enumerate (accord_choisi):
            if isinstance(note, str): # si étouffée ('x')
                accord_norm[i] = note
            elif note >= 1 : # si normale
                accord_norm[i] = note - note_min + 1
            else : # si jouée à vide (0)
                accord_norm[i] = note

        return accord_norm, note_min-1

    #: Affiche le numéro de frette
    def print_frette_number(self, number):

        self.canvas1.delete(self.numero_frette)
        self.numero_frette = self.canvas1.create_text(self.largeur+15,
                                                      CORDES_ESPACEMENT+20,
                                                      text=str(number),
                                                      font=("Comics", 16))

class Corde :
    """
    Crée une corde et affiche la note envoyée
    Usage : Corde(fenetre, numero_de_la_corde
    """

    def __init__(self, canvas, number):

        self.canvas1 = canvas
        self.num = number # numéro de la corde
        self.pos_x = self.num * CORDES_ESPACEMENT + CORDES_OFFSET
        self.taille = FRETTES_NOMBRE * FRETTES_ESPACEMENT

        self.draw()

    #: Dessine une corde
    def draw(self):

        x = self.pos_x
        y0 = 0
        y1 = self.taille
        width = (7-self.num)/3 # taille des cordes décroissante

        self.canvas1.create_line(x, y0, x, y1, width=width, fill="darkgray")

    #: Joue/affiche une note sur la corde
    def play(self, note):

        color = self.get_color_from_note(note)
        if note == 'x' : note = 0 # notes étouffées s'affichent en 0
        r = 7 # rayon de la note affichée
        x = self.pos_x
        y = (note + 1/2) * FRETTES_ESPACEMENT # 1/2 frette plus loin que la frette

        note_nouvelle = self.canvas1.create_oval(x-r, y-r, x+r, y+r,
                                                 fill = color,
                                                 width = 2)
        return note_nouvelle

    #: Change la couleur de la note suivant la manière de la jouer (ex : étouffée)
    def get_color_from_note(self, note) :

        if note == 0 : # à vide
            return  None
        elif note == 'x' : # étouffées
            return 'black'
        else : # normalement
            return 'snow'


class Frette:
    """  Affiche une frette, pas de méthode particulière"""
    def __init__(self, canvas, n, largeur, width=1.5):
        x0 = 0
        y = FRETTES_ESPACEMENT * n
        x1 = largeur
        canvas.create_line(x0, y, x1, y, fill = "black", width = width)



############### Boucle #################################
if __name__ == '__main__':
    root=tk.Tk()

    for i in range(3):
        for j in range (6):
            guitare  = MainGui(root, [i,j])
    root.mainloop()


