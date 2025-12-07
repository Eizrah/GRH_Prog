import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import tkinter as tk
import sqlite3
import uuid
#--------
#connexion à la bd db.sqlite3
conn = sqlite3.connect('database/db.sqlite3')
cursor = conn.cursor()



#--------
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir)
sys.path.append(project_root)

# Main imports
# from logic.BoiteDialogue import pannel_erreur 
from logic.modele.Cadre import Cadre
from logic.modele.Grade import Grade
from logic.modele.Fonctionnaire import Fonctionnaire
from logic.modele.AgentContractuel import AgentContractuel
from logic.modele.Emplois import Emplois
from logic.modele.Change_grade import ChangeGrade
from logic.modele.Affectation import Affectation
#--------
DEFAULT_FONT_FAMILY = "Arial"

COLORS = {
    "PRIMARY_BLUE": "#4A90E2",
    "ACCENT_GREEN": "#10B981",
    "ACCENT_RED": "#EF4444",
    "BG_LIGHT_GREY": "#F0F2F5",
    "CARD_WHITE": "#FFFFFF",
    "TEXT_DARK": "#374151",
    "TEXT_GREY": "#9CA3AF",
    "TEXT_BLACK": "#374151", # Alias pour TEXT_DARK
    "HEADER_BG": "#E5F0FF",
}

# Mapping pour la sélection dynamique des grades (pour la section Cadre/Classe/Grade)
GRADE_MAPPING = {
    "A": ["A1", "A2", "A3"],
    "B": ["B1", "B2"],
    "C": ["C1", "C2"],
    "D": ["D1", "D2", "D3"],
}

# Options pour la Classes de Grade
CLASSE_GRADE_OPTIONS = [
    "Classe Exceptionnelle", 
    "Classe Principale", 
    "Première Classe", 
    "Deuxième Classe"
]

# -------------------------------------------------------------------------
# --- CLASSES DE WIDGETS A RÉUTILISER (pour le Card Frame et le Date Picker) ---
# -------------------------------------------------------------------------

class DateSelector(ctk.CTkToplevel):
    """ Fenêtre Toplevel pour sélectionner une date via tkcalendar (si installé). """
    def __init__(self, master, entry_widget):
        super().__init__(master)
        self.title("Sélectionner la Date")
        self.entry_widget = entry_widget
        self.grab_set()  # Bloque l'interaction avec la fenêtre principale

        try:
            # Importation locale pour ne pas bloquer l'initialisation si tkcalendar manque
            from tkcalendar import Calendar 
            
            self.cal = Calendar(self, selectmode='day',
                                 date_pattern='yyyy-mm-dd',
                                 font=DEFAULT_FONT_FAMILY,
                                 background=COLORS['BG_LIGHT_GREY'],
                                 foreground=COLORS['TEXT_BLACK'])
            self.cal.pack(padx=10, pady=10)

            ctk.CTkButton(self, text="OK", command=self.set_date_and_destroy, 
                          fg_color=COLORS['ACCENT_GREEN'], hover_color="#059669").pack(pady=(0, 10))

        except ImportError:
            ctk.CTkLabel(self, text="Erreur: Le module tkcalendar n'est pas installé. Installation requise.").pack(padx=20, pady=20)
            ctk.CTkButton(self, text="Fermer", command=self.destroy).pack(pady=10)


    def set_date_and_destroy(self):
        """ Récupère la date sélectionnée et met à jour l'entrée. """
        try:
            selected_date = self.cal.get_date()
            self.entry_widget.delete(0, 'end')
            self.entry_widget.insert(0, selected_date)
            self.destroy()
        except AttributeError:
             # tkcalendar n'était pas disponible
            self.destroy()

class AjoutPersonnelView(ctk.CTkFrame):
    def __init__(self, master, controller=None, **kwargs):
        super().__init__(master, fg_color=COLORS['BG_LIGHT_GREY'], **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.controller = controller # Le contrôleur sera utilisé pour la soumission réelle
        
        # Le cadre scrollable permet d'assurer que le formulaire entier est visible
        self.scrollable_content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.scrollable_content.grid_columnconfigure(0, weight=1)

        # Appel de la méthode qui construit la vue
        self.create_ajout_personnel_view(self.scrollable_content)

    def create_card_frame(self, master, title):
        """ Crée le cadre blanc principal (la 'carte') pour le formulaire. """
        card_frame = ctk.CTkFrame(master, fg_color=COLORS['CARD_WHITE'], corner_radius=15)
        card_frame.grid_columnconfigure(0, weight=1)
        
        # Titre de la carte
        ctk.CTkLabel(card_frame, text=title, anchor="w",
                      font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=18, weight="bold"),
                      text_color=COLORS['TEXT_DARK']).pack(fill="x", padx=20, pady=(20, 10))

        # Cadre interne pour les champs de formulaire
        form_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        return card_frame, form_frame

    def open_date_selector(self, entry_widget):
        """ Ouvre la fenêtre de sélection de date. """
        DateSelector(self.master, entry_widget)
        
    def create_form_row(self, parent_frame, text, widget, row, col, columnspan=1):
        """ Helper pour créer une ligne de formulaire (Label et Widget). """
        ctk.CTkLabel(parent_frame, text=text, anchor="w",
                      font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                      text_color=COLORS['TEXT_BLACK']).grid(row=row, column=col, padx=10, pady=(15, 5), sticky="w")
        widget.grid(row=row, column=col + 1, padx=10, pady=(15, 5), sticky="ew", columnspan=columnspan)
        
    def create_date_input_group(self, parent_frame, placeholder):
        """ Helper pour les champs de date avec bouton calendrier. """
        frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        entry.pack(side="left", fill="x", expand=True)
        
        # Ajout d'une petite icône calendrier
        ctk.CTkButton(frame, text="📅", width=40, fg_color=COLORS['ACCENT_GREEN'],
                      hover_color="#059669",
                      command=lambda e=entry: self.open_date_selector(e)).pack(side="right", padx=(5,0))
        return frame, entry

    
    # ***************************************************************
    # *** LOGIQUE POUR LE LIEN CLASSE -> GRADE ***
    # ***************************************************************

    def update_grade_options(self, selected_classe):
        """ 
        Met à jour les options du ComboBox du grade en fonction de la classe sélectionnée.
        Est appelée lors de la sélection d'une nouvelle classe.
        """
        # Récupère les grades correspondants à la classe, ou une liste vide si la classe n'est pas trouvée
        grades = GRADE_MAPPING.get(selected_classe, [])
        
        # S'assure que le widget existe avant d'essayer de le configurer
        if hasattr(self, 'combo_grade'):
            self.combo_grade.configure(values=grades)
            
            # Réinitialise la valeur du grade à la première option (ou vide)
        else:
                self.var_grade.set("")

    def update_grade_echelon_options(self, selected_classe):
        """
        Met à jour la liste des échelons disponibles en fonction de la classe de grade choisie.
        Règle : Classe Exceptionnelle -> 1 à 2. Autres -> 1 à 3.
        """
        if selected_classe == "Classe Exceptionnelle":
            echelons = ["1", "2"]
        else:
            echelons = ["1", "2", "3"]
            
        if hasattr(self, 'combo_grade_echelon'):
            self.combo_grade_echelon.configure(values=echelons)
            self.var_grade_echelon.set(echelons[0])

    
    # ***************************************************************
    # *** LOGIQUE DE GESTION DES CHAMPS DYNAMIQUES ***
    # ***************************************************************

    def update_personnel_type_fields(self, selected_type):
        """ 
        Met à jour le contenu du cadre dynamique (self.dynamic_frame) 
        en fonction du type de personnel sélectionné. 
        """
        # Nettoyer les widgets précédents
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
        
        # Configuration des colonnes
        self.dynamic_frame.grid_columnconfigure((0, 2), weight=0)
        self.dynamic_frame.grid_columnconfigure((1, 3), weight=1)

        row = 0
        
        # Variables et widgets communs à Fonctionnaire et Contractuel
        
        # Cadre
        self.entry_cadre = ctk.CTkEntry(self.dynamic_frame, corner_radius=8, placeholder_text="Entrez le corps/cadre", font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.create_form_row(self.dynamic_frame, "Corps / Cadre :", self.entry_cadre, row, 0)
        
        # Classe (A, B, C, D)
        classes = list(GRADE_MAPPING.keys()) # Utilise les clés du mapping
        self.var_classe = ctk.StringVar(value=classes[0])
        combo_classe_widget = ctk.CTkComboBox(
            self.dynamic_frame, 
            values=classes, 
            variable=self.var_classe, 
            corner_radius=8, 
            font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14),
            command=self.update_grade_options, 
            state="readonly" # Rendu non éditable
        )
        self.create_form_row(self.dynamic_frame, "Cadre :", combo_classe_widget, row, 2)
        row += 1
        
        # Grade (sera mis à jour dynamiquement)
        self.var_grade = ctk.StringVar(value="") 
        self.combo_grade = ctk.CTkComboBox( 
            self.dynamic_frame, 
            values=[], 
            variable=self.var_grade, 
            corner_radius=8, 
            font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14),
            state="readonly" # Rendu non éditable
        )
        self.create_form_row(self.dynamic_frame, "Échelle :", self.combo_grade, row, 0)
        row += 1
        
        # Appel initial pour peupler le ComboBox du Grade en fonction de la Classe par défaut ("A")
        self.update_grade_options(self.var_classe.get())
        
        
        if selected_type == "Fonctionnaire":
            # --- Champs Spécifiques Fonctionnaire ---
            
            # Diplôme
            self.entry_diplome = ctk.CTkEntry(self.dynamic_frame, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
            self.create_form_row(self.dynamic_frame, "Diplôme :", self.entry_diplome, row, 0)
            
            # Duree (Indéterminée)
            self.entry_duree = ctk.CTkEntry(self.dynamic_frame, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
            self.entry_duree.insert(0, "Indéterminée")
            self.entry_duree.configure(state="disabled")
            self.create_form_row(self.dynamic_frame, "Durée Emploi :", self.entry_duree, row, 2)
            row += 1
            
            # Initialisation des variables Contractuel à None pour Ajout_personnel
            self.var_statut = None
            self.entry_date_fin_contrat = None
            
            
        elif selected_type == "Agent Contractuel":
            # --- Champs Spécifiques Agent Contractuel ---

            # Statut (Combobox)
            statuts = [
                "Agents appelés à occuper des emplois normalement dévolus à des fonctionnaires (EFA)",
                "Agents appelés à occuper des emplois de longue durée (ELD)",
                "Agents appelés à occuper des emplois de courte durée (ECD)",
                "Agents constituant la main d'œuvre (EMO)",
                "Agents appelés à occuper des emplois spéciaux (ES)"
            ]
            self.var_statut = ctk.StringVar(value=statuts[0])
            self.combo_statut = ctk.CTkComboBox(
                self.dynamic_frame, 
                values=statuts, 
                variable=self.var_statut, 
                corner_radius=8, 
                font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14),
                state="readonly" # Rendu non éditable
            )
            self.create_form_row(self.dynamic_frame, "Statut :", self.combo_statut, row, 0)

            # Date de Fin de Contrat (Pour la récupération dans Ajout_personnel)
            date_fin_contrat_frame, self.entry_date_fin_contrat = self.create_date_input_group(self.dynamic_frame, "AAAA-MM-JJ")
            self.create_form_row(self.dynamic_frame, "Date Fin Contrat :", date_fin_contrat_frame, row, 2)
            row += 1

            # Duree
            self.entry_duree = ctk.CTkEntry(self.dynamic_frame, corner_radius=8, placeholder_text="En mois", font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
            self.create_form_row(self.dynamic_frame, "Durée Emploi :", self.entry_duree, row, 0)
            row += 1
            
            # Initialisation de la variable Fonctionnaire à None pour Ajout_personnel
            self.entry_diplome = None

        # Mettre à jour la disposition pour refléter les nouveaux widgets
        self.dynamic_frame.update()

    

    
    
    # ***************************************************************
    # *** LOGIQUE DE SOUMISSION (CRÉATION DES CLASSES) ***
    # ***************************************************************
    
    def Ajout_personnel(self):
        """ 
        Récupère toutes les valeurs du formulaire et crée les instances 
        des classes Cadre, Grade, Emplois, et Personnel (Fonctionnaire/Contractuel).
        """
        
        personnel_data = {}
        
        # --- 1. Récupération des champs de base (Communs à tous) ---
        try:
            personnel_data = {
                "matricule": self.entry_matricule.get(),
                "nom": self.entry_nom.get(),
                "prenom": self.entry_prenom.get(),
                "lieu_naissance": self.entry_lieu_naissance.get(),
                "date_naissance": self.entry_date_naissance.get(), # format AAAA-MM-JJ
                "etat_civil": self.var_situation.get(),
                "date_entree": self.entry_date_entree.get(),     # format AAAA-MM-JJ
                "position": self.var_position.get(),
                
                # CHAMPS SUPPLÉMENTAIRES
                "classe_grade_nom": self.var_grade_classe.get(),
                "echelon_grade_num": self.var_grade_echelon.get(),
                "nom_poste": self.entry_job_title.get(),
                "lieu_travail": self.entry_workplace.get(),
                
                "type_personnel": self.var_type_personnel.get(),
                "date_sortie": self.entry_date_sortie.get() or None,      # Optionnel
                "objet_depart": self.entry_objet_depart.get() or None,    # Optionnel
                
                # CHAMPS DYNAMIQUES
                "cadre_corps": self.entry_cadre.get() if hasattr(self, 'entry_cadre') and self.entry_cadre is not None else None,
                "classe_corps": self.var_classe.get() if hasattr(self, 'var_classe') and self.var_classe is not None else None,
                "echelle_grade": self.var_grade.get() if hasattr(self, 'var_grade') and self.var_grade is not None else None,
                "duree_emploi": self.entry_duree.get() if hasattr(self, 'entry_duree') else "Indéterminée",

            }

        except Exception as e:
            # Gère les erreurs de récupération sur les champs principaux
            print(f"Erreur lors de la récupération des champs de base : {e}")
            messagebox.showerror("Erreur de Saisie", "Veuillez vérifier que tous les champs obligatoires sont remplis.")
            return

        # --- 2. Récupération des champs spécifiques (dynamiques) ---
        personnel_type = personnel_data["type_personnel"] 
        
        if personnel_type == "Fonctionnaire":
            try:
                personnel_data["diplome"] = self.entry_diplome.get()
                personnel_data["statut"] = None
                personnel_data["date_fin_contrat"] = None 
            except AttributeError:
                messagebox.showerror("Erreur", "Le champ 'Diplôme' du Fonctionnaire est manquant.")
                return
                
        elif personnel_type == "Agent Contractuel":
            try:
                personnel_data["statut"] = self.var_statut.get()
                personnel_data["date_fin_contrat"] = self.entry_date_fin_contrat.get()
                personnel_data["diplome"] = None
            except AttributeError:
                messagebox.showerror("Erreur", "Les champs spécifiques de l'Agent Contractuel sont manquants.")
                return

        cursor.execute('SELECT id_cadre from Cadre where echelle = ? and classe_corp = ? ', (personnel_data["echelle_grade"], personnel_data["classe_corps"]))
        result = cursor.fetchone()
        res = result[0]
        if result:
            id_cadre = result[0]
            print(f"ID Cadre trouvé: {id_cadre}")
        else:
            id_cadre = None
            print("Aucun cadre trouvé pour ces critères.")
            messagebox.showerror("Erreur", "Aucun cadre correspondant trouvé dans la base de données.")
            return
        # --- 3. Création des Objets de Modèle ---
        
        # a. Création de l'objet Cadre
        # chef_grade sera l'echelle spécifique (ex: A1, B2)
        # classe_corps sera le corps/cadre entré (texte)
        # echelle sera la classe (ex: A, B, C, D)
        #NOTE plus utile juste maka le valeur selectionner , mano recherche anat base aveo
        # try:
        #     cadre_obj = Cadre(
        #         classe_corps=personnel_data["cadre_corps"], 
        #         chef_grade=personnel_data["echelle_grade"], 
        #         echelle=personnel_data["classe_corps"] 
        #     )
        #     id_cadre = cadre_obj.id_cadre
        # except Exception as e:
        #     messagebox.showerror("Erreur Création Cadre", f"Impossible de créer l'objet Cadre: {e}")
        #     return
            
        # b. Création de l'objet Grade (Avec les nouvelles valeurs séparées)
        classe_grade = personnel_data["classe_grade_nom"]
        try:
            echelon_num = int(personnel_data["echelon_grade_num"])
        except ValueError:
             echelon_num = 1
             
        # Construction du titre complet pour l'affichage ou stockage
        # Construction du titre complet pour l'affichage ou stockage
        # suffix = "er" if echelon_num == 1 else "ème"
        # titre_complete = f"{classe_grade} {echelon_num}{suffix} échelon"
        titre = self.entry_titre_grade.get()
        
        try:
            grade_obj = Grade(
                titre=titre,          # Titre complet reconstruit
                classe=classe_grade,           # Classe (ex: Classe Exceptionnelle)
                echelon=echelon_num,           # Numero d'échelon
                id_cadre=id_cadre              # Clé étrangère / id_cadre à recuperer de la table Cadre
            )
            cursor.execute('INSERT INTO Grade (id_grade, titre, classe, echelon, id_cadre) VALUES (?, ?, ?, ?, ?)', 
                           (str(grade_obj.id_grade), grade_obj.titre, grade_obj.classe, grade_obj.echelon, str(grade_obj.id_cadre)))
        except Exception as e:
            messagebox.showerror("Erreur Création Grade", f"Impossible de créer l'objet Grade: {e}")
            return
        
        # c. Création de l'objet Emplois
        try:
            # NOTE: Duree (en années/mois ?) est définie à 0 par défaut car non présente dans le formulaire
            emplois_obj = Emplois(
                nom_poste=personnel_data["nom_poste"],
                duree=personnel_data["duree_emploi"],
                lieu=personnel_data["lieu_travail"]
            )
            #Enregistrement dans la base de donéé
            cursor.execute('INSERT INTO Emplois (nom_poste, dure, lieu) VALUES (?, ?, ?)', (emplois_obj.nom_poste, emplois_obj.duree, emplois_obj.lieu))
            conn.commit()
        except Exception as e:
            messagebox.showerror("Erreur Création Emploi", f"Impossible de créer l'objet Emplois: {e}")
            return
        #d. (DÉPLACÉ/IGNORÉ) Création de l'objet Affectation se fera après création du Personnel pour avoir l'ID
            
        # e. Création de l'objet Fonctionnaire ou AgentContractuel
        try:
            if personnel_type == "Fonctionnaire":
                personnel_obj = Fonctionnaire(
                    num_matricule=personnel_data["matricule"],
                    nom=personnel_data["nom"],
                    prenom=personnel_data["prenom"],
                    date_naissance=personnel_data["date_naissance"],
                    lieu_naissance=personnel_data["lieu_naissance"],
                    date_entree=personnel_data["date_entree"],
                    date_sortie=personnel_data["date_sortie"],
                    objet_depart=personnel_data["objet_depart"],
                    position=personnel_data["position"],
                    diplome=personnel_data["diplome"],
                    id_cadre=res
                )
                
                # Creation Affectation (Après Fonctionnaire pour avoir id_fonc)
                affectation_obj = Affectation(
                    date_debut=personnel_obj.date_entree,
                    date_fin=personnel_obj.date_sortie,
                    id_emploi=emplois_obj.id_emploi,
                    id_fonc=personnel_obj.id_fonc,
                    id_ag=None
                )
                
                # Creation ChangeGrade
                change_grade_obj = ChangeGrade(
                    date_av=personnel_obj.date_entree,
                    nouveau_grade=grade_obj.titre,
                    ancien_grade=None,
                    id_grade=grade_obj.id_grade,
                    id_fonc=personnel_obj.id_fonc,
                    id_ag=uuid.uuid4()
                )
                
                #insertion d'un Fonctionnaire dans la bd
                cursor.execute('INSERT INTO Fonctionnaire (num_matricule, nom, prenom, date_naissance, lieu_naissance, date_entre, date_sorti, objet_depart, position, diplome, id_cadre, id_fonc) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                               (personnel_obj.num_matricule, personnel_obj.nom, personnel_obj.prenom, personnel_obj.date_naissance, personnel_obj.lieu_naissance, personnel_obj.date_entree, personnel_obj.date_sortie, personnel_obj.objet_depart, personnel_obj.position, personnel_obj.diplome, res, str(personnel_obj.id_fonc)))
                
                # Insertion ChangeGrade
                cursor.execute('INSERT INTO Change_grade (id_changement, date_av, nouveau_grade, ancien_grade, id_grade, id_fonc, id_ag) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                               (str(change_grade_obj.id_changement), change_grade_obj.date_av, change_grade_obj.nouveau_grade, change_grade_obj.ancien_grade, str(change_grade_obj.id_grade), str(change_grade_obj.id_fonc), str(change_grade_obj.id_ag)))
                
                # Insertion Affectation Correcte (Extraction des IDs depuis les objets)
                # id_emploi vient de affectation_obj.id_emploi
                # id_fonc vient de affectation_obj.id_fonc
                # id_ag est None pour fonctionnaire
                cursor.execute('INSERT INTO Affectation (id_affectation, date_debut, date_fin, id_emploi, id_fonc, id_ag) VALUES (?, ?, ?, ?, ?, ?)', 
                               (str(affectation_obj.id_affectation), affectation_obj.date_debut, affectation_obj.date_fin, str(affectation_obj.id_emploi), str(affectation_obj.id_fonc), None))
                
                conn.commit()
                
            elif personnel_type == "Agent Contractuel":
                personnel_obj = AgentContractuel(
                    num_matricule=personnel_data["matricule"],
                    nom=personnel_data["nom"],
                    prenom=personnel_data["prenom"], 
                    date_naissance=personnel_data["date_naissance"],
                    lieu_naissance=personnel_data["lieu_naissance"],
                    date_entree=personnel_data["date_entree"],
                    date_sortie=personnel_data["date_sortie"],
                    objet_depart=personnel_data["objet_depart"],
                    position=personnel_data["position"],
                    statut=personnel_data["statut"],
                    id_cadre=res
                )
                
                # Creation Affectation (Avec IDs)
                # Date debut = date_entree, date_fin = date_sortie (pour Agent)
                affectation_obj = Affectation(
                    date_debut=personnel_obj.date_entree,
                    date_fin=personnel_obj.date_sortie,
                    id_emploi=emplois_obj.id_emploi,
                    id_fonc=None,
                    id_ag=personnel_obj.id_ag
                )
                
                cursor.execute('INSERT INTO AgentContractuel (num_matricule, nom, prenom, date_naissance, lieu_naissance, date_entre, date_sorti, objet_depart, position, satut, id_cadre, id_ag) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
                               (personnel_obj.num_matricule, personnel_obj.nom, personnel_obj.prenom, personnel_obj.date_naissance, personnel_obj.lieu_naissance, personnel_obj.date_entree, personnel_obj.date_sortie, personnel_obj.objet_depart, personnel_obj.position, personnel_obj.statut, res, str(personnel_obj.id_ag)))
                
                # Creation et Insertion ChangeGrade
                change_grade_obj = ChangeGrade(
                    date_av=personnel_obj.date_entree,
                    nouveau_grade=grade_obj.titre,
                    ancien_grade=None,
                    id_grade=grade_obj.id_grade,
                    id_fonc=uuid.uuid4(),
                    id_ag=personnel_obj.id_ag
                )
                cursor.execute('INSERT INTO Change_grade (id_changement, date_av, nouveau_grade, ancien_grade, id_grade, id_fonc, id_ag) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                               (str(change_grade_obj.id_changement), change_grade_obj.date_av, change_grade_obj.nouveau_grade, change_grade_obj.ancien_grade, str(change_grade_obj.id_grade), str(change_grade_obj.id_fonc), str(change_grade_obj.id_ag)))
                
                # Insertion Affectation Correcte
                # id_ag vient de affectation_obj.id_ag
                # id_fonc est None
                cursor.execute('INSERT INTO Affectation (id_affectation, date_debut, date_fin, id_emploi, id_fonc, id_ag) VALUES (?, ?, ?, ?, ?, ?)', 
                               (str(affectation_obj.id_affectation), affectation_obj.date_debut, affectation_obj.date_fin, str(affectation_obj.id_emploi), None, str(affectation_obj.id_ag)))
                
                conn.commit()
            
        except Exception as e:
            messagebox.showerror("Erreur Création Personnel", f"Impossible de créer l'objet Personnel ({personnel_type}): {e}")
            return
            

        # --- 4. Affichage du succès (Débogage) ---
        # print("--- Objets de Modèle Créés avec Succès ---")
        # print(f"Cadre ID: {cadre_obj.id_cadre} | Corps: {cadre_obj.classe_corps} | Échelle: {cadre_obj.echelle}")
        # print(f"Grade ID: {grade_obj.id_grade} | Titre: {grade_obj.titre} | Classe: {grade_obj.classe} | Échelon: {grade_obj.echelon}")
        # print(f"Emploi ID: {emplois_obj.id_emploi} | Poste: {emplois_obj.nom_poste} | Lieu: {emplois_obj._lieu} | Durée (Défaut): {emplois_obj.duree}")
        # print(f"Personnel ID: {personnel_obj.num_matricule} | Type: {personnel_type} | Nom: {personnel_obj.nom}")
        # print("---------------------------------------")
        messagebox.showinfo("Soumission Réussie", f"Personnel de type '{personnel_type}' créé avec succès. Détails en console.")
        

    # ***************************************************************
    # *** CONSTRUCTION DE LA VUE ***
    # ***************************************************************
    
    def create_ajout_personnel_view(self, parent):
        """ Contient la structure de votre formulaire, maintenant appelée depuis __init__. """
        card_frame, form_frame = self.create_card_frame(parent, "🧑‍💼 Ajouter un Nouveau Personnel (Fonctionnaire ou Contractuel)")
        card_frame.pack(fill="x", padx=5, pady=10)
        
        # Configuration des colonnes pour un formulaire en deux colonnes
        form_frame.grid_columnconfigure((0, 2), weight=0) # Labels: taille fixe
        form_frame.grid_columnconfigure((1, 3), weight=1) # Widgets: taille étirable

        
        # SECTION 1: Champs de Personnel (Statiques)
        row = 0
        
        self.entry_matricule = ctk.CTkEntry(form_frame, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.create_form_row(form_frame, "Numéro Matricule :", self.entry_matricule, row, 0)
        
        self.entry_nom = ctk.CTkEntry(form_frame, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.create_form_row(form_frame, "Nom :", self.entry_nom, row, 2)
        row += 1

        self.entry_prenom = ctk.CTkEntry(form_frame, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.create_form_row(form_frame, "Prénom :", self.entry_prenom, row, 0)
        
        self.entry_lieu_naissance = ctk.CTkEntry(form_frame, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.create_form_row(form_frame, "Lieu de Naissance :", self.entry_lieu_naissance, row, 2)
        row += 1

        # Date de Naissance
        date_naissance_frame, self.entry_date_naissance = self.create_date_input_group(form_frame, "AAAA-MM-JJ")
        self.create_form_row(form_frame, "Date de Naissance :", date_naissance_frame, row, 0)
        
        # État civil 
        situation = ["celibataire", "marié(e) sans enfant", "marié(e) avec enfant"]
        self.var_situation = ctk.StringVar(value=situation[0])
        self.combo_situation = ctk.CTkComboBox(
            form_frame, 
            values=situation, 
            variable=self.var_situation, 
            corner_radius=8, 
            font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14),
            state="readonly" # Rendu non éditable
        )
        self.create_form_row(form_frame, "État civil :", self.combo_situation, row, 2)
        row += 1
        
        # Date d'Entrée
        date_entree_frame, self.entry_date_entree = self.create_date_input_group(form_frame, "AAAA-MM-JJ")
        self.create_form_row(form_frame, "Date d'Entrée :", date_entree_frame, row, 0)
        
        # Position 
        positions = ["en activite", "en detachement", "hors cadre", "sous le drapeau", "en disponibilite", "en congé"]
        self.var_position = ctk.StringVar(value=positions[0])
        self.combo_position = ctk.CTkComboBox(
            form_frame, 
            values=positions, 
            variable=self.var_position, 
            corner_radius=8, 
            font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14),
            state="readonly" # Rendu non éditable
        )
        self.create_form_row(form_frame, "Position :", self.combo_position, row, 2)
        row += 1

        # --- NOUVEAUX CHAMPS REFACTORÉS : Classe et Échelon de Grade ---

        # 0. Titre du Grade (Nouveau champ demandé)
        self.entry_titre_grade = ctk.CTkEntry(form_frame, corner_radius=8,  placeholder_text="Ex: Administrateur", font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.create_form_row(form_frame, "Titre du Grade :", self.entry_titre_grade, row, 0)
        row += 1
        
        # 1. Classe de Grade
        self.var_grade_classe = ctk.StringVar(value=CLASSE_GRADE_OPTIONS[0])
        self.combo_grade_classe = ctk.CTkComboBox(
            form_frame, 
            values=CLASSE_GRADE_OPTIONS, 
            variable=self.var_grade_classe, 
            corner_radius=8, 
            font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14),
            command=self.update_grade_echelon_options,
            state="readonly" 
        )
        self.create_form_row(form_frame, "Classe du Grade :", self.combo_grade_classe, row, 0)

        # 2. Échelon (Dynamique)
        self.var_grade_echelon = ctk.StringVar(value="1")
        self.combo_grade_echelon = ctk.CTkComboBox(
            form_frame, 
            values=["1", "2", "3"], 
            variable=self.var_grade_echelon, 
            corner_radius=8, 
            font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14),
            state="readonly"
        )
        self.create_form_row(form_frame, "Échelon :", self.combo_grade_echelon, row, 2)
        
        # Init options based on default
        self.update_grade_echelon_options(self.var_grade_classe.get()) 
        row += 1

        # --- NOUVEAU CHAMP 2: Nom du Poste ---
        self.entry_job_title = ctk.CTkEntry(form_frame, corner_radius=8, placeholder_text="Ex: Chef de Service", font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.create_form_row(form_frame, "Nom du Poste :", self.entry_job_title, row, 0)
        
        # --- NOUVEAU CHAMP 3: Lieu de Travail ---
        self.entry_workplace = ctk.CTkEntry(form_frame, corner_radius=8, placeholder_text="Ex: Direction Générale", font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.create_form_row(form_frame, "Lieu de Travail :", self.entry_workplace, row, 2)
        row += 1
        
        # Type de Personnel (Combobox) - Déclencheur du contenu dynamique (LIGNE DÉCALÉE)
        types = ["Fonctionnaire", "Agent Contractuel"]
        self.var_type_personnel = ctk.StringVar(value=types[0])
        self.combo_type_personnel = ctk.CTkComboBox(
            form_frame, 
            values=types, 
            variable=self.var_type_personnel, 
            corner_radius=8, 
            font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14),
            command=self.update_personnel_type_fields,
            state="readonly" # Rendu non éditable
        )
        self.create_form_row(form_frame, "Type de Personnel :", self.combo_type_personnel, row, 0)
        row += 1
        
        # --- Cadre Dynamique ---
        self.dynamic_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        self.dynamic_frame.grid(row=row, column=0, columnspan=4, sticky="ew", pady=(20, 0))
        row += 1
        
        # Initial call to set up the default fields (Fonctionnaire) and the dynamic Grade options
        self.update_personnel_type_fields(self.var_type_personnel.get())
        
        # --- SECTION 2: Champs optionnels de Personnel (Sortie) (LIGNE DÉCALÉE) ---
        
        # Date de Sortie (Optionnel)
        date_sortie_frame, self.entry_date_sortie = self.create_date_input_group(form_frame, "AAAA-MM-JJ (Optionnel)")
        self.create_form_row(form_frame, "Date de Sortie :", date_sortie_frame, row, 0)
        
        # Objet de Départ (Optionnel)
        self.entry_objet_depart = ctk.CTkEntry(
            form_frame, 
            placeholder_text="(Optionnel)", 
            corner_radius=8, 
            font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14)
        )
        self.create_form_row(form_frame, "Objet de Départ :", self.entry_objet_depart, row, 2)
        row += 1

        # --- SECTION 4: Bouton de Soumission (LIGNE DÉCALÉE) ---
        self.ValiderBtn = ctk.CTkButton(
            form_frame, 
            text="Créer le Personnel",
            command=self.Ajout_personnel,
            font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=16, weight="bold"),
            fg_color=COLORS['PRIMARY_BLUE'], 
            hover_color="#3670B3", 
            corner_radius=8
        )
        self.ValiderBtn.grid(row=row, column=0, columnspan=4, pady=(30, 10), sticky="e")