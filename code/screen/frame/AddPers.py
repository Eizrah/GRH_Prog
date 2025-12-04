import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import tkinter as tk


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

        # Appel de la méthode qui construit la vue (anciennement la fonction)
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
        
        if selected_type == "Fonctionnaire":
            # --- Champs Spécifiques Fonctionnaire ---
            
            # Diplôme
            self.entry_diplome = ctk.CTkEntry(self.dynamic_frame, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
            self.create_form_row(self.dynamic_frame, "Diplôme :", self.entry_diplome, row, 0)

            # Cadre (champ d'entrée libre)
            self.entry_cadre = ctk.CTkEntry(self.dynamic_frame, corner_radius=8, placeholder_text="Entrez le cadre", font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
            self.create_form_row(self.dynamic_frame, "Corps / Cadre :", self.entry_cadre, row, 2)
            row += 1
            
            # Grade (Colonne 1)
            grades = ["A1", "A2", "A3", "B1", "B2", "C1", "C2", "D1", "D2", "D3"]
            self.var_grade = ctk.StringVar(value=grades[0])
            self.combo_grade = ctk.CTkComboBox(self.dynamic_frame, values=grades, variable=self.var_grade, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
            self.create_form_row(self.dynamic_frame, "Échelle / Grade :", self.combo_grade, row, 0)
            
            # Classe (Colonne 2)
            classes = ["A", "B", "C", "D"]
            self.var_classe = ctk.StringVar(value=classes[0])
            self.combo_classe = ctk.CTkComboBox(self.dynamic_frame, values=classes, variable=self.var_classe, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
            self.create_form_row(self.dynamic_frame, "Classe :", self.combo_classe, row, 2)
            row += 1

        elif selected_type == "Agent Contractuel":
            # --- Champs Spécifiques Agent Contractuel ---

            # Cadre (champ d'entrée libre)
            self.entry_cadre = ctk.CTkEntry(self.dynamic_frame, corner_radius=8, placeholder_text="Entrez le cadre", font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
            self.create_form_row(self.dynamic_frame, "Corps / Cadre :", self.entry_cadre, row, 0)

            # Statut (Combobox)
            statuts = [
                "Agents appelés à occuper des emplois normalement dévolus à des fonctionnaires (EFA)",
                "Agents appelés à occuper des emplois de longue durée (ELD)",
                "Agents appelés à occuper des emplois de courte durée (ECD)",
                "Agents constituant la main d'œuvre (EMO)",
                "Agents appelés à occuper des emplois spéciaux (ES)"
            ]
            self.var_statut = ctk.StringVar(value=statuts[0])
            self.combo_statut = ctk.CTkComboBox(self.dynamic_frame, values=statuts, variable=self.var_statut, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
            self.create_form_row(self.dynamic_frame, "Statut :", self.combo_statut, row, 2)
            row += 1
            
            # Grade (Colonne 1)
            grades = ["A1", "A2", "A3", "B1", "B2", "C1", "C2", "D1", "D2", "D3"]
            self.var_grade = ctk.StringVar(value=grades[0])
            self.combo_grade = ctk.CTkComboBox(self.dynamic_frame, values=grades, variable=self.var_grade, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
            self.create_form_row(self.dynamic_frame, "Échelle / Grade :", self.combo_grade, row, 0)
            
            # Classe (Colonne 2)
            classes = ["A", "B", "C", "D"]
            self.var_classe = ctk.StringVar(value=classes[0])
            self.combo_classe = ctk.CTkComboBox(self.dynamic_frame, values=classes, variable=self.var_classe, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
            self.create_form_row(self.dynamic_frame, "Classe :", self.combo_classe, row, 2)
            row += 1

            # Date de Fin de Contrat
            date_fin_contrat_frame, self.entry_date_fin_contrat = self.create_date_input_group(self.dynamic_frame, "AAAA-MM-JJ")
            self.create_form_row(self.dynamic_frame, "Date de Fin de Contrat :", date_fin_contrat_frame, row, 0)
            row += 1

        # Mettre à jour la disposition pour refléter les nouveaux widgets
        self.dynamic_frame.update()
        
    def submit_personnel_mock(self):
        """ Simule l'envoi des données (logique de soumission). """
        messagebox.showwarning("Test","Vos données ont été bien soumis")

        
    def create_ajout_personnel_view(self, parent):
        """ Contient la structure de votre formulaire, maintenant appelée depuis __init__. """
        card_frame, form_frame = self.create_card_frame(parent, "🧑‍💼 Ajouter un Nouveau Personnel (Fonctionnaire ou Contractuel)")
        card_frame.pack(fill="x", padx=5, pady=10)
        
        # Configuration des colonnes pour un formulaire en deux colonnes
        form_frame.grid_columnconfigure((0, 2), weight=0) # Labels: taille fixe
        form_frame.grid_columnconfigure((1, 3), weight=1) # Widgets: taille étirable

        
        # --- SECTION 1: Champs de Personnel (Base) ---
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
        
        # Date d'Entrée
        date_entree_frame, self.entry_date_entree = self.create_date_input_group(form_frame, "AAAA-MM-JJ")
        self.create_form_row(form_frame, "Date d'Entrée :", date_entree_frame, row, 2)
        row += 1

        # Position (Combobox)
        positions = ["en activite", "en detachement", "hors cadre", "sous le drapeau", "en disponibilite", "en congé"]
        self.var_position = ctk.StringVar(value=positions[0])
        self.combo_position = ctk.CTkComboBox(form_frame, values=positions, variable=self.var_position, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.create_form_row(form_frame, "Position :", self.combo_position, row, 0)
        
        # Type de Personnel (Combobox) - Déclencheur du contenu dynamique
        types = ["Fonctionnaire", "Agent Contractuel"]
        self.var_type_personnel = ctk.StringVar(value=types[0])
        self.combo_type_personnel = ctk.CTkComboBox(form_frame, values=types, variable=self.var_type_personnel, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14),
                                                     command=self.update_personnel_type_fields)
        self.create_form_row(form_frame, "Type de Personnel :", self.combo_type_personnel, row, 2)
        row += 1
        
        # --- SECTION 2: Champs optionnels de Personnel (Sortie) ---
        
        # Date de Sortie (Optionnel)
        date_sortie_frame, self.entry_date_sortie = self.create_date_input_group(form_frame, "AAAA-MM-JJ (Optionnel)")
        self.create_form_row(form_frame, "Date de Sortie :", date_sortie_frame, row, 0)
        
        # Objet de Départ (Optionnel)
        self.entry_objet_depart = ctk.CTkEntry(form_frame, placeholder_text="(Optionnel)", corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.create_form_row(form_frame, "Objet de Départ :", self.entry_objet_depart, row, 2)
        row += 1
        
        # --- SECTION 3: Cadre Dynamique pour les Champs Spécifiques ---
        # Ce cadre sera mis à jour par la méthode 'update_personnel_type_fields'
        self.dynamic_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        self.dynamic_frame.grid(row=row, column=0, columnspan=4, sticky="ew", pady=(20, 0))
        # Initial call to set up the default fields (Fonctionnaire)
        self.update_personnel_type_fields(self.var_type_personnel.get())
        row += 1

        # --- SECTION 4: Bouton de Soumission ---
        self.ValiderBtn = ctk.CTkButton(form_frame, text="Créer le Personnel",
                      command=self.submit_personnel_mock,
                      font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=16, weight="bold"),
                      fg_color=COLORS['PRIMARY_BLUE'], hover_color="#3670B3", corner_radius=8)
        self.ValiderBtn.grid(row=row, column=0, columnspan=4, pady=(30, 10), sticky="e")
