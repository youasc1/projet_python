

from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import numpy as np

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

fenetre = Tk()
fenetre.geometry("500x500")
fenetre.title("mini-projet")
fenetre['bg']=("gray")


def importe():
    global donnees
    donnees = filedialog.askopenfilename()
    if donnees:
        try:
            donnees = pd.read_csv(donnees)
        except:
            try:
                donnees = pd.read_table(donnees,sep=" \t",header=0)
            except:
                return None
    tree["columns"] = donnees.columns.tolist()
    tree["show"] = "headings"

    # Ajouter les colonnes au Treeview
    for col in donnees.columns.tolist():
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

        # Ajouter les données au Treeview
        for index, row in donnees.iterrows():
            tree.insert("", "end", values=row.tolist())
    combobox_x["values"] = tree["columns"]
    combobox_y["values"] = tree["columns"]
    combobox_np["values"] = tree["columns"]


def calculer(event=None):
    element_selete=combobox_np.get()
    tableau_np=np.array(donnees[element_selete])
    fonction_np=combobox_op.get()
    if fonction_np:
        fonction = getattr(np, fonction_np)
        resultat = fonction(tableau_np)
    text_area.insert(END,str(resultat) +"\n")



def tracer(event=None):
    element_select=combobox_plt.get()
    if element_select=="histogram":
         colonne_selectionnee = combobox_x.get()
         # Créer le diagramme
         plt.figure(figsize=(6, 4))
         plt.hist(donnees[colonne_selectionnee], bins=10, color='skyblue', edgecolor='black')
         plt.xlabel(colonne_selectionnee)
         plt.ylabel('Fréquence')
         plt.title('Histogramme de ' + colonne_selectionnee)
         # Afficher le diagramme dans une fenêtre Tkinter
         canvas = FigureCanvasTkAgg(plt.gcf(), master=onglet2)
         canvas.draw()
         canvas.get_tk_widget().pack()
    elif element_select=="scatter":
        colonne_x = combobox_x.get()
        colonne_y = combobox_y.get()
        # Créer le nuage de points
        plt.figure(figsize=(6, 4))
        plt.scatter(donnees[colonne_x], donnees[colonne_y], color='blue', alpha=0.5)
        plt.xlabel(colonne_x)
        plt.ylabel(colonne_y)
        plt.title('Nuage de points entre ' + colonne_x + ' et ' + colonne_y)
        # Afficher le nuage de points dans une fenêtre Tkinter

        canvas = FigureCanvasTkAgg(plt.gcf(), master=onglet2)
        canvas.draw()
        canvas.get_tk_widget().pack()
    else:
        plt.clf()
        colonne_x = combobox_x.get()
        colonne_y = combobox_y.get()
        # Créer le graphique
        plt.figure(figsize=(6, 4))
        plt.plot(donnees[colonne_x], donnees[colonne_y], marker='o', linestyle='-', color='blue')
        plt.xlabel(colonne_x)
        plt.ylabel(colonne_y)
        plt.title('Graphique entre ' + colonne_x + ' et ' + colonne_y)
        # Afficher le graphique dans une fenêtre Tkinter
        canvas = FigureCanvasTkAgg(plt.gcf(), master=onglet2)
        canvas.draw()
        canvas.get_tk_widget().pack()

onglets = ttk.Notebook(fenetre)
onglet1 = ttk.Frame(onglets)
onglet2 = ttk.Frame(onglets)
onglet3 = ttk.Frame(onglets)
liste_valeurs_x=[]
liste_valeurs_y=[]
liste_valeurs_np=[]
# Ajouter les cadres aux onglets avec des étiquettes
onglets.add(onglet1, text='importation')
onglets.add(onglet2, text='visualisation')
onglets.add(onglet3, text='manipulation')
option =["scatter","histogram","boxplot"]
combobox_x = ttk.Combobox(onglet2)
combobox_y = ttk.Combobox(onglet2)
combobox_np=ttk.Combobox(onglet3)
fonctions_numpy = [fonction for fonction in dir(np) if callable(getattr(np, fonction))]
combobox_op = ttk.Combobox(onglet3 ,values=fonctions_numpy)
combobox_op.pack(padx=10,pady=10)
combobox_np.pack(padx=10,pady=10)
combobox_x.pack(padx=10,pady=10)
combobox_y.pack(padx=10,pady=10)
combobox_plt = ttk.Combobox(onglet2,values=option)
combobox_plt.current(0)
button_trace =Button(onglet2, text="tracer",width=10)
button_trace.bind("<Button-1>",tracer)
button_trace.pack()
combobox_plt.pack(padx=10, pady=10)
button_ajouter =Button(onglet3, text="calculer")
button_ajouter.bind("<Button-1>",calculer)
button_ajouter.pack()
text_area = Text(onglet3, height=20, width=40)
text_area.pack()

button_import = Button(onglet1, text="importer",font=("Arial",12,"bold"),command=importe)
button_import.pack()


tree = ttk.Treeview(onglet1)
# Afficher le Treeview dans un cadre avec barres de défilement
scroll_y = ttk.Scrollbar(onglet1, orient="vertical", command=tree.yview)
scroll_y.pack(side="right", fill="y")
scroll_x = ttk.Scrollbar(onglet1, orient="horizontal", command=tree.xview)
scroll_x.pack(side="bottom",fill="x")
tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
tree.pack(expand=True, fill="both")
onglets.pack(expand=True, fill='both', padx=10, pady=10)
#######################################

fenetre.mainloop()