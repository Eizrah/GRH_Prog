import sqlite3
import Cadre
from tkinter import ttk
import tkinter
import sys
import os

# Ajouter le chemin du projet pour les imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir)
sys.path.append(project_root)

# Import de l'utilitaire de base de données
from logic.db_utils import get_database_path

mainFenetre = tkinter.Tk()
mainFenetre.title("Ajout d'un personnel")
mainFenetre.geometry("800x600")

# Connexion à la base de données (compatible PyInstaller)
connexion = sqlite3.connect(get_database_path())
cursor = connexion.cursor()


def recDonne():
    
    classe = entryCB.get()
    echelle = labelEchelle.get()
   
    cadre  = Cadre.Cadre(classe,echelle)
    print(cadre.id_cadre)
    cursor.execute("INSERT INTO Cadre (id_cadre, classe_corp, echelle) VALUES (?, ?, ?)", (str(cadre.id_cadre), cadre.classe_corps, cadre.echelle))
    connexion.commit()
# Combobox pour la Classe (A, B, C, D)
labelClasse = tkinter.Label(mainFenetre, text="Classe :")
labelClasse.pack(pady=(10, 0))

entryCB = ttk.Combobox(mainFenetre, values=["A", "B", "C", "D"])
entryCB.pack(pady=5)

# Combobox pour l'Echelle (A1...D3)
labelEchelleTitle = tkinter.Label(mainFenetre, text="Echelle :")
labelEchelleTitle.pack(pady=(10, 0))

labelEchelle = ttk.Combobox(mainFenetre, values=["A1","A2","A3","B1","B2","C1","C2","D1","D2","D3"])
labelEchelle.pack(pady=5)

btnSub = ttk.Button(mainFenetre, text="Soumettre",command=recDonne)
btnSub.pack(pady=10)
# Start the main loop correctly at the end






mainFenetre.mainloop()