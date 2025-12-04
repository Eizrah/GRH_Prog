import customtkinter as ctk
from tkinter import messagebox

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
        
        # Bouton calendrier (simulé pour l'instant)
        ctk.CTkButton(frame, text="📅", width=40, fg_color=COLORS['ACCENT_GREEN'],
                      hover_color="#059669",
                      command=lambda: print("Ouvrir calendrier")).pack(side="right", padx=(5,0))
        return frame, entry
    
    def rechercher_personnel(self):
        """Méthode pour rechercher et afficher les informations du personnel"""
        matricule = self.entry_matricule.get()
        
        if not matricule:
            messagebox.showwarning("Attention", "Veuillez entrer un numéro de matricule")
            return
        
        # Simulation de la recherche - à remplacer par votre logique réelle
        # Exemple de données simulées
        donnees_simulees = {
            "001": {
                "nom": "Dupont",
                "prenom": "Alice",
                "type": "Fonctionnaire",
                "solde_conge": 25,
                "position": "En activité",
                "corps": "Administration",
                "grade": "A3",
                "date_embauche": "2020-05-15"
            },
            "002": {
                "nom": "Lefevre", 
                "prenom": "Marc",
                "type": "Agent Contractuel",
                "solde_conge": 18,
                "position": "En activité",
                "type_contrat": "CDI",
                "date_fin_contrat": "2025-12-31",
                "date_embauche": "2022-03-01"
            }
        }
        
        if matricule in donnees_simulees:
            data = donnees_simulees[matricule]
            self.afficher_resume_personnel(data)
        else:
            messagebox.showerror("Erreur", f"Personnel avec matricule {matricule} non trouvé")
    
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
        
        # Nom complet
        self.create_info_row(info_frame, "Nom complet:", f"{data['nom']} {data['prenom']}", row)
        row += 1
        
        # Type de personnel
        type_color = COLORS['PRIMARY_BLUE'] if data['type'] == "Fonctionnaire" else COLORS['ACCENT_GREEN']
        self.create_info_row(info_frame, "Type:", data['type'], row, type_color)
        row += 1
        
        # Solde de congé
        solde_color = COLORS['ACCENT_GREEN'] if data['solde_conge'] > 10 else COLORS['ACCENT_RED']
        self.create_info_row(info_frame, "Solde de congé:", f"{data['solde_conge']} jours", row, solde_color)
        row += 1
        
        # Position
        self.create_info_row(info_frame, "Position:", data['position'], row)
        row += 1
        
        # Informations spécifiques selon le type
        if data['type'] == "Fonctionnaire":
            self.create_info_row(info_frame, "Corps:", data.get('corps', 'Non spécifié'), row)
            row += 1
            self.create_info_row(info_frame, "Grade:", data.get('grade', 'Non spécifié'), row)
        else:
            self.create_info_row(info_frame, "Type de contrat:", data.get('type_contrat', 'Non spécifié'), row)
            row += 1
            self.create_info_row(info_frame, "Fin de contrat:", data.get('date_fin_contrat', 'Non spécifié'), row)
        
        row += 1
        self.create_info_row(info_frame, "Date d'embauche:", data.get('date_embauche', 'Non spécifié'), row)
    
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
        motif = self.entry_motif.get()
        date_debut = self.entry_date_debut.get() if hasattr(self, 'entry_date_debut') else ""
        date_fin = self.entry_date_fin.get() if hasattr(self, 'entry_date_fin') else ""
        
        if not all([matricule, type_conge, motif]):
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs obligatoires")
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
        self.create_form_row(form1, "Motif :", self.entry_motif, row)
        row += 1
        
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
