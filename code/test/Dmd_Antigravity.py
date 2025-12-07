import customtkinter as ctk
from tkinter import messagebox
import sqlite3
import os
import sys
from datetime import datetime, date
from tkcalendar import Calendar

# Ajouter le répertoire parent au path pour importer les modules logic
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir)
sys.path.append(project_root)

# Import de la fonction de calcul de congé cumulé
# Import de la fonction de calcul de congé cumulé
from logic.conge_cumule import calculer_conge_cumule
from logic.GestionAbsences import GestionAbsences

# --- COULEURS ET POLICES ---
COLORS = {
    "PRIMARY_BLUE": "#4A90E2",
    "ACCENT_GREEN": "#10B981",
    "ACCENT_RED": "#EF4444",
    "BG_LIGHT_GREY": "#F0F2F5",
    "CARD_WHITE": "#FFFFFF",
    "TEXT_DARK": "#374151",
    "TEXT_GREY": "#9CA3AF",
    "HEADER_BG": "#E5F0FF",
}

DEFAULT_FONT_FAMILY = "Arial"

class Dmd(ctk.CTkFrame):
    """Classe pour le formulaire de demande de congé"""
    
    def __init__(self, master=None, controller=None, **kwargs):
        super().__init__(master, fg_color=COLORS['BG_LIGHT_GREY'], **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Cadre scrollable pour tout le formulaire
        self.scrollable_content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.scrollable_content.grid_columnconfigure(0, weight=1)
        
        # Init gestionnaire absences
        self.gestionnaire = GestionAbsences()
        self.request_valid = False 
        self.current_personnel_data = None # Données du personnel actuellement affiché

        # Création de la vue
        self.create_demande_view(self.scrollable_content)
    
    def create_card_frame(self, master, title):
        """Crée un cadre blanc (carte) pour une section du formulaire"""
        card_frame = ctk.CTkFrame(master, fg_color=COLORS['CARD_WHITE'], corner_radius=15)
        card_frame.grid_columnconfigure(0, weight=1)
        
        # Titre de la carte
        ctk.CTkLabel(card_frame, text=title, anchor="w",
                     font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=18, weight="bold"),
                     text_color=COLORS['TEXT_DARK']).pack(fill="x", padx=20, pady=(20, 10))
        
        # Cadre interne pour le contenu
        content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        return card_frame, content_frame
    
    def create_form_row(self, parent_frame, text, widget, row, col=0, columnspan=1):
        """Helper pour créer une ligne de formulaire"""
        ctk.CTkLabel(parent_frame, text=text, anchor="w",
                      font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                      text_color=COLORS['TEXT_DARK']).grid(row=row, column=col, padx=10, pady=(15, 5), sticky="w")
        widget.grid(row=row, column=col+1, padx=10, pady=(15, 5), sticky="ew", columnspan=columnspan)
    
    def create_date_input_group(self, parent_frame, placeholder):
        """Helper pour créer un champ de date avec bouton calendrier"""
        frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        frame.grid_columnconfigure(0, weight=1)
        
        entry = ctk.CTkEntry(frame, placeholder_text=placeholder, corner_radius=8, 
                             font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        entry.pack(side="left", fill="x", expand=True)
        
        # Bouton calendrier (qui ouvre le popup)
        ctk.CTkButton(frame, text="📅", width=40, fg_color=COLORS['ACCENT_GREEN'],
                      hover_color="#059669",
                      command=lambda: self.open_calendar(entry)).pack(side="right", padx=(5,0))
        return frame, entry
    
    def open_calendar(self, entry_widget):
        """Ouvre une fenêtre popup avec un calendrier pour sélectionner une date"""
        top = ctk.CTkToplevel(self)
        top.title("Sélectionner une date")
        top.geometry("300x300")
        top.grab_set()  # Rend la fenêtre modale
        
        cal = Calendar(top, selectmode='day', date_pattern='dd/mm/yyyy')
        cal.pack(pady=20, expand=True)
        
        def set_date():
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, cal.get_date())
            top.destroy()
            self.update_validation() # Forcer la validation après sélection
            
        ctk.CTkButton(top, text="Valider", command=set_date, 
                      fg_color=COLORS['ACCENT_GREEN']).pack(pady=10)
    
    def calculer_solde_conge(self, date_entree_str):
        """
        Calcule le solde de congé cumulé basé sur la date d'entrée
        
        Args:
            date_entree_str (str): Date d'entrée au format string (peut être YYYY-MM-DD ou autre)
        
        Returns:
            int: Solde de congé en jours
        """
        try:
            # Date de demande = date actuelle
            # Date de demande = date du champ "Date de début" ou aujourd'hui par défaut
            date_demande = date.today()
            if hasattr(self, 'entry_date_debut'):
                val_date_debut = self.entry_date_debut.get()
                if val_date_debut.strip():
                     for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d']:
                        try:
                            date_demande = datetime.strptime(val_date_debut, fmt).date()
                            break
                        except ValueError:
                            continue
            
            # Parser la date d'entrée (peut être au format YYYY-MM-DD ou autre)
            if date_entree_str and date_entree_str != "-":
                # Essayer différents formats de date
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d']:
                    try:
                        date_entree = datetime.strptime(date_entree_str, fmt).date()
                        # Calculer le congé cumulé en utilisant la fonction importée
                        # Utiliser silent=True pour éviter les messages de débogage
                        solde = calculer_conge_cumule(date_entree, date_demande, jours_par_an=15, silent=True)
                        return solde
                    except ValueError:
                        continue
            
            # Si la date n'est pas valide, retourner 0
            return 0
            
        except Exception as e:
            print(f"Erreur lors du calcul du solde de congé: {e}")
            return 0


    
    def update_validation(self, event=None):
        """Valide la demande en temps réel et met à jour l'interface"""
        # 1. Récupérer les données
        type_conge = self.combo_type_conge.get()
        date_debut_str = self.entry_date_debut.get() if hasattr(self, 'entry_date_debut') else ""
        date_fin_str = self.entry_date_fin.get() if hasattr(self, 'entry_date_fin') else ""
        
        # Reset UI si incomplet
        if not date_debut_str or not date_fin_str:
            self.lbl_val_status.configure(text="⏳ En attente des dates...", text_color=COLORS['TEXT_GREY'])
            self.lbl_val_details.configure(text="")
            self.request_valid = False
            return

        # Récupérer solde (0 par défaut si pas de personnel sélectionné)
        solde = 0
        if self.current_personnel_data:
            solde = self.current_personnel_data.get('solde_conge', 0)
        
        # Appel du gestionnaire
        valide, message, infos = self.gestionnaire.valider_demande(
            type_conge, solde, date_debut_str, date_fin_str
        )
        
        self.request_valid = valide
        
        # Mise à jour UI
        if valide:
            self.lbl_val_status.configure(text="✅ DEMANDE VALIDE", text_color=COLORS['ACCENT_GREEN'])
            duree = infos.get('duree', '?')
            # Formatter le message pour être propre
            details = f"Durée calculée : {duree} jours\nNote : {message}"
            self.lbl_val_details.configure(text=details, text_color=COLORS['TEXT_DARK'])
        else:
            self.lbl_val_status.configure(text="❌ DEMANDE INVALIDE", text_color=COLORS['ACCENT_RED'])
            self.lbl_val_details.configure(text=message, text_color=COLORS['ACCENT_RED'])

    def rechercher_personnel(self):
        """Méthode pour rechercher et afficher les informations du personnel"""
        matricule = self.entry_matricule.get()
        
        if not matricule:
            messagebox.showwarning("Attention", "Veuillez entrer un numéro de matricule")
            return
        
        try:
            # Construire le chemin vers la base de données
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            project_root = os.path.dirname(parent_dir)
            db_path = os.path.join(project_root, 'database', 'db.sqlite3')
            
            # Connexion à la base de données
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Chercher d'abord dans la table Fonctionnaire
            cursor.execute('''
                SELECT f.num_matricule, f.nom, f.prenom, f.position, f.diplome,
                       g.classe, c.echelle, c.classe_corp, f.date_entre
                FROM Fonctionnaire f
                LEFT JOIN Change_grade cg ON f.id_fonc = cg.id_fonc
                LEFT JOIN Grade g ON cg.id_grade = g.id_grade
                LEFT JOIN Cadre c ON f.id_cadre = c.id_cadre
                WHERE f.num_matricule = ?
            ''', (matricule,))
            
            result_fonc = cursor.fetchone()
            
            if result_fonc:
                # Personnel trouvé dans la table Fonctionnaire
                data = {
                    "matricule": result_fonc[0] if result_fonc[0] else "-",
                    "nom": result_fonc[1] if result_fonc[1] else "-",
                    "prenom": result_fonc[2] if result_fonc[2] else "-",
                    "type": "Fonctionnaire",
                    "position": result_fonc[3] if result_fonc[3] else "-",
                    "diplome": result_fonc[4] if result_fonc[4] else "-",
                    "classe": result_fonc[5] if result_fonc[5] else "-",
                    "echelle": result_fonc[6] if result_fonc[6] else "-",
                    "corps": result_fonc[7] if result_fonc[7] else "-",
                    "date_embauche": result_fonc[8] if result_fonc[8] else "-",
                    "solde_conge": self.calculer_solde_conge(result_fonc[8] if result_fonc[8] else "-")
                }
                self.current_personnel_data = data
                conn.close()
                self.afficher_resume_personnel(data)
                return
            
            # Chercher dans la table AgentContractuel si non trouvé dans Fonctionnaire
            cursor.execute('''
                SELECT a.num_matricule, a.nom, a.prenom, a.position, a.satut,
                       g.classe, c.echelle, c.classe_corp, a.date_entre
                FROM AgentContractuel a
                LEFT JOIN Change_grade cg ON a.id_ag = cg.id_ag
                LEFT JOIN Grade g ON cg.id_grade = g.id_grade
                LEFT JOIN Cadre c ON a.id_cadre = c.id_cadre
                WHERE a.num_matricule = ?
            ''', (matricule,))
            
            result_agent = cursor.fetchone()
            
            if result_agent:
                # Personnel trouvé dans la table AgentContractuel
                data = {
                    "matricule": result_agent[0] if result_agent[0] else "-",
                    "nom": result_agent[1] if result_agent[1] else "-",
                    "prenom": result_agent[2] if result_agent[2] else "-",
                    "type": "Agent Contractuel",
                    "position": result_agent[3] if result_agent[3] else "-",
                    "statut": result_agent[4] if result_agent[4] else "-",
                    "classe": result_agent[5] if result_agent[5] else "-",
                    "echelle": result_agent[6] if result_agent[6] else "-",
                    "corps": result_agent[7] if result_agent[7] else "-",
                    "date_embauche": result_agent[8] if result_agent[8] else "-",
                    "solde_conge": self.calculer_solde_conge(result_agent[8] if result_agent[8] else "-")
                }
                self.current_personnel_data = data
                conn.close()
                self.afficher_resume_personnel(data)
                return
            
            # Si non trouvé dans les deux tables
            conn.close()
            messagebox.showerror("Erreur", 
                               f"Personnel avec le matricule '{matricule}' introuvable.\n\n"
                               f"Veuillez vérifier le numéro de matricule et réessayer.")
            
        except sqlite3.Error as e:
            messagebox.showerror("Erreur de base de données", 
                               f"Une erreur s'est produite lors de la recherche:\n{str(e)}")
            print(f"Erreur SQLite: {e}")
        except Exception as e:
            messagebox.showerror("Erreur", 
                               f"Une erreur inattendue s'est produite:\n{str(e)}")
            print(f"Erreur: {e}")
    
    def afficher_resume_personnel(self, data):
        """Affiche le résumé des informations du personnel"""
        # Vider le cadre de résumé
        for widget in self.resume_frame.winfo_children():
            widget.destroy()
        
        # Titre du résumé
        ctk.CTkLabel(self.resume_frame, text="📋 Résumé du Personnel", 
                     font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=16, weight="bold"),
                     text_color=COLORS['PRIMARY_BLUE']).pack(anchor="w", pady=(0, 15))
        
        # Cadre pour les informations
        info_frame = ctk.CTkFrame(self.resume_frame, fg_color=COLORS['BG_LIGHT_GREY'], corner_radius=10)
        info_frame.pack(fill="x", pady=5)
        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=2)
        
        row = 0
        
        # Matricule
        self.create_info_row(info_frame, "Matricule:", data.get('matricule', '-'), row)
        row += 1
        
        # Nom complet
        self.create_info_row(info_frame, "Nom complet:", f"{data.get('nom', '-')} {data.get('prenom', '-')}", row)
        row += 1
        
        # Type de personnel
        type_color = COLORS['PRIMARY_BLUE'] if data['type'] == "Fonctionnaire" else COLORS['ACCENT_GREEN']
        self.create_info_row(info_frame, "Type:", data['type'], row, type_color)
        row += 1
        
        # Position
        self.create_info_row(info_frame, "Position:", data.get('position', '-'), row)
        row += 1
        
        # Informations spécifiques selon le type
        if data['type'] == "Fonctionnaire":
            # Diplôme
            self.create_info_row(info_frame, "Diplôme:", data.get('diplome', '-'), row)
            row += 1
            
            # Classe
            self.create_info_row(info_frame, "Classe:", data.get('classe', '-'), row)
            row += 1
            
            # Échelle
            self.create_info_row(info_frame, "Échelle:", data.get('echelle', '-'), row)
            row += 1
            
            # Corps
            self.create_info_row(info_frame, "Corps:", data.get('corps', '-'), row)
            row += 1
        else:
            # Agent Contractuel
            # Statut
            self.create_info_row(info_frame, "Statut:", data.get('statut', '-'), row)
            row += 1
            
            # Classe
            self.create_info_row(info_frame, "Classe:", data.get('classe', '-'), row)
            row += 1
            
            # Échelle
            self.create_info_row(info_frame, "Échelle:", data.get('echelle', '-'), row)
            row += 1
            
            # Corps
            self.create_info_row(info_frame, "Corps:", data.get('corps', '-'), row)
            row += 1
        
        # Date d'embauche
        self.create_info_row(info_frame, "Date d'embauche:", data.get('date_embauche', '-'), row)
        row += 1
        
        # Solde de congé
        solde_conge = data.get('solde_conge', 0)
        solde_color = COLORS['ACCENT_GREEN'] if solde_conge > 10 else COLORS['ACCENT_RED']
        self.create_info_row(info_frame, "Solde de congé:", f"{solde_conge} jours", row, solde_color)

    
    def create_info_row(self, parent, label, value, row, value_color=None):
        """Crée une ligne d'information dans le résumé"""
        if value_color is None:
            value_color = COLORS['TEXT_DARK']
        
        ctk.CTkLabel(parent, text=label, anchor="w",
                     font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                     text_color=COLORS['TEXT_GREY']).grid(row=row, column=0, padx=15, pady=8, sticky="w")
        
        ctk.CTkLabel(parent, text=value, anchor="w",
                     font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14),
                     text_color=value_color).grid(row=row, column=1, padx=15, pady=8, sticky="w")
    
    def soumettre_demande(self):
        """Méthode pour soumettre la demande de congé"""
        matricule = self.entry_matricule.get()
        type_conge = self.combo_type_conge.get()
        motif = self.entry_motif.get("1.0", "end-1c")
        date_debut = self.entry_date_debut.get() if hasattr(self, 'entry_date_debut') else ""
        date_fin = self.entry_date_fin.get() if hasattr(self, 'entry_date_fin') else ""
        
        if not all([matricule, type_conge, motif]):
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs obligatoires")
            return
            
        # Vérification de la validation technique
        if not self.request_valid:
            messagebox.showerror("Erreur", "La demande est invalide (voir section validation).\nVeuillez corriger les dates ou le type de congé.")
            return
        
        # Préparer les données
        data = {
            "matricule": matricule,
            "type_conge": type_conge,
            "motif": motif,
            "date_debut": date_debut,
            "date_fin": date_fin
        }
        
        # Afficher un message de confirmation
        messagebox.showinfo("Demande soumise", 
                          f"Demande de congé soumise avec succès!\n\n"
                          f"Matricule: {matricule}\n"
                          f"Type: {type_conge}\n"
                          f"Motif: {motif}")
        
        # Si un contrôleur est défini, lui passer les données
        if self.controller and hasattr(self.controller, 'ajouter_demande'):
            self.controller.ajouter_demande(data)
    
    def create_demande_view(self, parent):
        """Crée l'interface de demande de congé"""
        
        # --- PREMIER BLOC: Informations de la demande ---
        card1, form1 = self.create_card_frame(parent, "📝 Demande de Congé/Absence")
        card1.pack(fill="x", padx=5, pady=(0, 20))
        
        # Configuration des colonnes
        form1.grid_columnconfigure(0, weight=0)  # Labels
        form1.grid_columnconfigure(1, weight=1)  # Widgets
        
        row = 0
        
        # Champ Matricule avec bouton recherche
        matricule_frame = ctk.CTkFrame(form1, fg_color="transparent")
        matricule_frame.grid_columnconfigure(0, weight=1)
        
        self.entry_matricule = ctk.CTkEntry(matricule_frame, placeholder_text="Ex: 001", 
                                           corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.entry_matricule.pack(side="left", fill="x", expand=True)
        
        ctk.CTkButton(matricule_frame, text="🔍 Rechercher", width=120, 
                      fg_color=COLORS['PRIMARY_BLUE'], hover_color="#3670B3",
                      command=self.rechercher_personnel).pack(side="right", padx=(10, 0))
        
        self.create_form_row(form1, "Numéro Matricule :", matricule_frame, row)
        row += 1
        
        # Type de congé/absence
        types_conge = [
            "Congé annuel",
            "Congé maladie", 
            "Congé maternité",
            "Congé paternité",
            "Congé sans solde",
            "Congé formation",
            "Absence exceptionnelle",
            "Congé pour événements familiaux"
        ]
        self.combo_type_conge = ctk.CTkComboBox(form1, values=types_conge, corner_radius=8,
                                               font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.combo_type_conge.set("Congé annuel")
        self.create_form_row(form1, "Type de congé/absence :", self.combo_type_conge, row)
        row += 1
        
        # Dates (optionnelles)
        date_debut_frame, self.entry_date_debut = self.create_date_input_group(form1, "Date de début (Optionnel)")
        self.create_form_row(form1, "Date de début :", date_debut_frame, row)
        row += 1
        
        date_fin_frame, self.entry_date_fin = self.create_date_input_group(form1, "Date de fin (Optionnel)")
        self.create_form_row(form1, "Date de fin :", date_fin_frame, row)
        row += 1
        
        # Motif (champ texte multiligne)
        self.entry_motif = ctk.CTkTextbox(form1, height=100, corner_radius=8,
                                         font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.entry_motif.bind("<KeyRelease>", self.update_validation)
        self.create_form_row(form1, "Motif :", self.entry_motif, row)
        row += 1

        # --- SECTION VALIDATION (Nouveau) ---
        validation_frame = ctk.CTkFrame(form1, fg_color=COLORS['BG_LIGHT_GREY'], corner_radius=8)
        validation_frame.grid(row=row, column=0, columnspan=2, padx=10, pady=20, sticky="ew")
        validation_frame.grid_columnconfigure(1, weight=1)
        
        # Statut (Icone + Texte)
        self.lbl_val_status = ctk.CTkLabel(validation_frame, text="En attente de saisie...", 
                                         font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                                         text_color=COLORS['TEXT_GREY'])
        self.lbl_val_status.pack(anchor="w", padx=15, pady=(10, 5))
        
        # Détails (Durée, etc.)
        self.lbl_val_details = ctk.CTkLabel(validation_frame, text="", 
                                          font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=13),
                                          justify="left", text_color=COLORS['TEXT_DARK'])
        self.lbl_val_details.pack(anchor="w", padx=15, pady=(0, 10))

        # Bindings pour validation en temps réel
        self.combo_type_conge.configure(command=self.update_validation)
        self.entry_matricule.bind("<FocusOut>", self.update_validation) # Pour vérifier solde si dispo
        if hasattr(self, 'entry_date_debut'):
            self.entry_date_debut.bind("<KeyRelease>", self.update_validation)
            self.entry_date_debut.bind("<FocusOut>", self.update_validation)
        if hasattr(self, 'entry_date_fin'):
            self.entry_date_fin.bind("<KeyRelease>", self.update_validation)
            self.entry_date_fin.bind("<FocusOut>", self.update_validation)
        
        # --- DEUXIÈME BLOC: Résumé du personnel ---
        card2, form2 = self.create_card_frame(parent, "👤 Résumé du Demandeur")
        card2.pack(fill="x", padx=5, pady=(0, 20))
        
        # Cadre pour le résumé (sera rempli dynamiquement)
        self.resume_frame = ctk.CTkFrame(form2, fg_color="transparent")
        self.resume_frame.pack(fill="x", pady=10)
        
        # Message initial
        ctk.CTkLabel(self.resume_frame, 
                     text="Veuillez rechercher un personnel pour afficher ses informations",
                     text_color=COLORS['TEXT_GREY'],
                     font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, slant="italic")
                     ).pack(pady=20)
        
        # --- TROISIÈME BLOC: Bouton de soumission ---
        card3, form3 = self.create_card_frame(parent, "✅ Soumission")
        card3.pack(fill="x", padx=5, pady=(0, 20))
        
        # Bouton de soumission
        ctk.CTkButton(form3, text="📤 Soumettre la demande", 
                      font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=16, weight="bold"),
                      fg_color=COLORS['ACCENT_GREEN'], hover_color="#059669", 
                      corner_radius=8, height=50,
                      command=self.soumettre_demande).pack(pady=20)


# --- Pour tester la vue seule ---
