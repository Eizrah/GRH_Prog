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
from logic.conge_cumule import calculer_conge_cumule

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
            
        ctk.CTkButton(top, text="Valider", command=set_date, 
                      fg_color=COLORS['ACCENT_GREEN']).pack(pady=10)
                      
    def calculer_duree_conge(self, date_debut_str: str, date_fin_str: str) -> int:
        """
        Calcule la durée en jours (inclusive) entre la date de début et la date de fin.
        """
        if not date_debut_str or not date_fin_str:
            return 0
        
        d1, d2 = None, None
        
        # Essayer différents formats pour la date de début
        for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d']:
            try:
                d1 = datetime.strptime(date_debut_str, fmt).date()
                break
            except ValueError:
                pass
        
        # Essayer différents formats pour la date de fin
        for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%Y/%m/%d']:
            try:
                d2 = datetime.strptime(date_fin_str, fmt).date()
                break
            except ValueError:
                pass

        if d1 and d2 and d2 >= d1:
            # Durée inclusive (date_fin - date_debut + 1 jour)
            duration = (d2 - d1).days + 1
            return duration
        
        return 0
    
    def calculer_solde_conge(self, date_entree_str):
        """
        Calcule le solde de congé cumulé basé sur la date d'entrée
        """
        try:
            # Date de demande = Date de début du congé (si remplie) ou aujourd'hui par défaut
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
            
            # Parser la date d'entrée
            if date_entree_str and date_entree_str != "-":
                for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d']:
                    try:
                        date_entree = datetime.strptime(date_entree_str, fmt).date()
                        # Calculer le congé cumulé en utilisant la fonction importée
                        solde = calculer_conge_cumule(date_entree, date_demande, jours_par_an=15, silent=True)
                        return solde
                    except ValueError:
                        continue
            
            return 0
            
        except Exception as e:
            print(f"Erreur lors du calcul du solde de congé: {e}")
            return 0


    
    def rechercher_personnel(self):
        """Méthode pour rechercher et afficher les informations du personnel et de la demande"""
        matricule = self.entry_matricule.get()
        
        if not matricule:
            messagebox.showwarning("Attention", "Veuillez entrer un numéro de matricule")
            return
            
        # --- NOUVEAU: Récupérer les données de la demande ---
        type_conge = self.combo_type_conge.get()
        motif = self.entry_motif.get("1.0", "end-1c").strip()
        date_debut = self.entry_date_debut.get()
        date_fin = self.entry_date_fin.get()
        
        # Calculer la durée demandée
        duree_demandee = self.calculer_duree_conge(date_debut, date_fin)
        
        # Initialiser les données de la demande pour l'affichage
        demande_data = {
            "type_conge": type_conge,
            "motif": motif,
            "date_debut": date_debut,
            "date_fin": date_fin,
            "duree_demandee": duree_demandee
        }
        
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
                date_embauche = result_fonc[8] if result_fonc[8] else "-"
                solde_conge = self.calculer_solde_conge(date_embauche)
                
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
                    "date_embauche": date_embauche,
                    "solde_conge": solde_conge
                }
                conn.close()
                
                # --- NOUVEAU: Validation du solde ---
                if type_conge in ["Congé annuel", "Congé annuel cumulé"]:
                    if duree_demandee > solde_conge:
                        messagebox.showerror("Erreur de Solde Insuffisant", 
                                             f"La durée demandée ({duree_demandee} jours) pour le Congé annuel/cumulé "
                                             f"est supérieure au solde disponible ({solde_conge} jours).\n\n"
                                             f"Veuillez ajuster la durée ou choisir un autre type de congé.")
                
                self.afficher_resume_personnel(data, demande_data)
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
                date_embauche = result_agent[8] if result_agent[8] else "-"
                solde_conge = self.calculer_solde_conge(date_embauche)
                
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
                    "date_embauche": date_embauche,
                    "solde_conge": solde_conge
                }
                conn.close()
                
                # --- NOUVEAU: Validation du solde ---
                if type_conge in ["Congé annuel", "Congé annuel cumulé"]:
                    if duree_demandee > solde_conge:
                        messagebox.showerror("Erreur de Solde Insuffisant", 
                                             f"La durée demandée ({duree_demandee} jours) pour le Congé annuel/cumulé "
                                             f"est supérieure au solde disponible ({solde_conge} jours).\n\n"
                                             f"Veuillez ajuster la durée ou choisir un autre type de congé.")
                
                self.afficher_resume_personnel(data, demande_data)
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
    
    def afficher_resume_personnel(self, data, demande_data=None): # NOUVEAU: Ajout de demande_data
        """Affiche le résumé des informations du personnel et les détails de la demande"""
        # Vider le cadre de résumé
        for widget in self.resume_frame.winfo_children():
            widget.destroy()
        
        # --- SECTION 1: Résumé du Personnel ---
        ctk.CTkLabel(self.resume_frame, text="👤 Résumé du Demandeur", 
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
        
        # Informations spécifiques selon le type (Diplôme, Statut, etc.)
        if data['type'] == "Fonctionnaire":
            self.create_info_row(info_frame, "Diplôme:", data.get('diplome', '-'), row); row += 1
            self.create_info_row(info_frame, "Classe:", data.get('classe', '-'), row); row += 1
            self.create_info_row(info_frame, "Échelle:", data.get('echelle', '-'), row); row += 1
            self.create_info_row(info_frame, "Corps:", data.get('corps', '-'), row); row += 1
        else:
            self.create_info_row(info_frame, "Statut:", data.get('statut', '-'), row); row += 1
            self.create_info_row(info_frame, "Classe:", data.get('classe', '-'), row); row += 1
            self.create_info_row(info_frame, "Échelle:", data.get('echelle', '-'), row); row += 1
            self.create_info_row(info_frame, "Corps:", data.get('corps', '-'), row); row += 1
        
        # Date d'embauche
        self.create_info_row(info_frame, "Date d'embauche:", data.get('date_embauche', '-'), row)
        row += 1
        
        # Solde de congé
        solde_conge = data.get('solde_conge', 0)
        solde_color = COLORS['ACCENT_GREEN'] if solde_conge > 10 else COLORS['ACCENT_RED']
        self.create_info_row(info_frame, "Solde de congé:", f"{solde_conge} jours", row, solde_color)
        
        # --- SECTION 2: Détails de la Demande (NOUVEAU) ---
        if demande_data and demande_data['type_conge']:
            # Ligne de séparation visuelle
            ctk.CTkFrame(self.resume_frame, height=2, fg_color=COLORS['TEXT_GREY']).pack(fill="x", pady=15)

            ctk.CTkLabel(self.resume_frame, text="📄 Détails de la Demande", 
                         font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=16, weight="bold"),
                         text_color=COLORS['PRIMARY_BLUE']).pack(anchor="w", pady=(0, 15))
            
            demande_info_frame = ctk.CTkFrame(self.resume_frame, fg_color=COLORS['BG_LIGHT_GREY'], corner_radius=10)
            demande_info_frame.pack(fill="x", pady=5)
            demande_info_frame.grid_columnconfigure(0, weight=1)
            demande_info_frame.grid_columnconfigure(1, weight=2)
            
            r = 0
            
            # Type de congé/absence
            self.create_info_row(demande_info_frame, "Type de Demande:", demande_data['type_conge'], r)
            r += 1

            # Durée demandée
            duree = demande_data['duree_demandee']
            duree_color = COLORS['TEXT_DARK']
            
            # Mise en évidence si solde insuffisant pour le congé annuel
            if demande_data['type_conge'] in ["Congé annuel", "Congé annuel cumulé"] and duree > solde_conge:
                duree_color = COLORS['ACCENT_RED']
            
            self.create_info_row(demande_info_frame, "Durée demandée:", f"{duree} jours", r, duree_color)
            r += 1
            
            # Période
            if demande_data['date_debut'] and demande_data['date_fin']:
                self.create_info_row(demande_info_frame, "Période:", f"Du {demande_data['date_debut']} au {demande_data['date_fin']}", r)
                r += 1
            
            # Motif
            motif_display = demande_data['motif'] if len(demande_data['motif']) <= 50 else demande_data['motif'][:50] + "..."
            self.create_info_row(demande_info_frame, "Motif (Extrait):", motif_display or "-", r)
            r += 1
            
            # Rappel de la validation (pour information visuelle)
            if duree_color == COLORS['ACCENT_RED']:
                 ctk.CTkLabel(self.resume_frame, 
                              text=f"⚠️ La durée demandée est supérieure au solde de congé disponible.", 
                              text_color=COLORS['ACCENT_RED'],
                              font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold")
                              ).pack(fill="x", pady=10)

    
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
            
        # NOUVEAU: Validation avant soumission pour le congé annuel/cumulé
        duree_demandee = self.calculer_duree_conge(date_debut, date_fin)
        solde_conge = self.calculer_solde_conge(self.get_date_embauche_from_matricule(matricule)) # Nécessite une nouvelle fonction pour ne pas refaire la recherche DB complète

        if type_conge in ["Congé annuel", "Congé annuel cumulé"] and duree_demandee > solde_conge and solde_conge > 0:
             # Afficher l'erreur si la durée dépasse le solde
             messagebox.showerror("Erreur de Soumission", 
                                  f"IMPOSSIBLE de soumettre : La durée demandée ({duree_demandee} jours) "
                                  f"est supérieure au solde de congé disponible ({solde_conge} jours).")
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
                          f"Durée demandée: {duree_demandee} jours\n"
                          f"Motif: {motif[:50]}...")
        
        # Si un contrôleur est défini, lui passer les données
        if self.controller and hasattr(self.controller, 'ajouter_demande'):
            self.controller.ajouter_demande(data)
            
    # Fonction utilitaire pour récupérer la date d'embauche sans refaire toute la recherche
    def get_date_embauche_from_matricule(self, matricule):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            project_root = os.path.dirname(parent_dir)
            db_path = os.path.join(project_root, 'database', 'db.sqlite3')
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT date_entre FROM Fonctionnaire WHERE num_matricule = ?', (matricule,))
            result = cursor.fetchone()
            if result:
                conn.close()
                return result[0]
                
            cursor.execute('SELECT date_entre FROM AgentContractuel WHERE num_matricule = ?', (matricule,))
            result = cursor.fetchone()
            
            conn.close()
            return result[0] if result else "-"
            
        except Exception:
            return "-"
    
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
        # Ajout des types de congés mentionnés
        types_conge = [
            "Congé annuel",
            "Congé annuel cumulé", # Ajout pour prendre en compte votre confusion
            "Congé maladie", 
            "Congé maternité",
            "Congé paternité",
            "Congé formation",
            "Congé pour éducation",
            "Permission d'absence", # <= 20 jours, non cumulable avec congé spécial
            "Autorisation d'absence ordinaire (3 jours max)", # Événements familiaux
            "Autorisation d'absence spéciale", # Hospitalisation, élections, syndical
        ]
        self.combo_type_conge = ctk.CTkComboBox(form1, values=types_conge, corner_radius=8,
                                               font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.combo_type_conge.set("Congé annuel")
        self.create_form_row(form1, "Type de congé/absence :", self.combo_type_conge, row)
        row += 1
        
        # Dates (optionnelles)
        date_debut_frame, self.entry_date_debut = self.create_date_input_group(form1, "Date de début (jj/mm/aaaa)")
        self.create_form_row(form1, "Date de début :", date_debut_frame, row)
        row += 1
        
        date_fin_frame, self.entry_date_fin = self.create_date_input_group(form1, "Date de fin (jj/mm/aaaa)")
        self.create_form_row(form1, "Date de fin :", date_fin_frame, row)
        row += 1
        
        # Motif (champ texte multiligne)
        self.entry_motif = ctk.CTkTextbox(form1, height=100, corner_radius=8,
                                         font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.create_form_row(form1, "Motif :", self.entry_motif, row)
        row += 1
        
        # --- DEUXIÈME BLOC: Résumé du personnel ---
        card2, form2 = self.create_card_frame(parent, "👤 Résumé du Demandeur et de la Demande")
        card2.pack(fill="x", padx=5, pady=(0, 20))
        
        # Cadre pour le résumé (sera rempli dynamiquement)
        self.resume_frame = ctk.CTkFrame(form2, fg_color="transparent")
        self.resume_frame.pack(fill="x", pady=10)
        
        # Message initial
        ctk.CTkLabel(self.resume_frame, 
                     text="Veuillez rechercher un personnel pour afficher ses informations et valider la demande.",
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