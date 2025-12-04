import customtkinter as ctk

# --- COULEURS ET POLICES (pour la cohérence avec rh_frontend.py) ---
# En production, ces couleurs seraient importées depuis un fichier de configuration
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

# --- DONNÉES DE DÉMONSTRATION ---
PERSONNEL_DATA = [
    {
        "matricule": "001", "nom": "Dupont", "prenom": "Alice", "email": "alice.dupont@rh.app",
        "type": "Fonctionnaire", "classe": "A", "echelle": "A3", "corps": "Administration",
        "statut": "En activité",
    },
    {
        "matricule": "002", "nom": "Lefevre", "prenom": "Marc", "email": "marc.lefevre@rh.app",
        "type": "Contractuel", "classe": "B", "echelle": "B1", "corps": "Technique",
        "statut": "En congé",
    },
    {
        "matricule": "003", "nom": "Martin", "prenom": "Sophie", "email": "sophie.martin@rh.app",
        "type": "Fonctionnaire", "classe": "C", "echelle": "C2", "corps": "Éducation",
        "statut": "En détachement",
    },
    {
        "matricule": "004", "nom": "Dubois", "prenom": "Pierre", "email": "pierre.dubois@rh.app",
        "type": "Fonctionnaire", "classe": "D", "echelle": "D3", "corps": "Sécurité",
        "statut": "Hors cadre",
    },
    {
        "matricule": "005", "nom": "Petit", "prenom": "Jeanne", "email": "jeanne.petit@rh.app",
        "type": "Contractuel", "classe": "A", "echelle": "A1", "corps": "Finances",
        "statut": "En disponibilité",
    },
]

class Bilan(ctk.CTkFrame):
    """
    Affiche la synthèse des données clés (cartes de statistiques)
    en haut du tableau de bord.
    """
    def __init__(self, master, personnel_data, **kwargs):
        # Définir la couleur par défaut seulement si elle n'est pas déjà spécifiée
        if 'fg_color' not in kwargs:
            kwargs['fg_color'] = COLORS['BG_LIGHT_GREY']
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="bilan_cols")
        
        # Données de synthèse (simulées)
        total_personnel = len(personnel_data)
        conges_approuves = 15 # Simulé
        conges_en_attente = 3 # Simulé

        # Création et placement des cartes
        self.create_card(0, "👤 Personnel Total", str(total_personnel), COLORS['PRIMARY_BLUE'])
        self.create_card(1, "✅ Congés Approuvés", str(conges_approuves), COLORS['ACCENT_GREEN'])
        self.create_card(2, "⏳ Congés en Attente", str(conges_en_attente), COLORS['ACCENT_RED'])
        
    def create_card(self, column, title, value, color):
        """ Crée une carte de statistique individuelle. """
        card = ctk.CTkFrame(self, fg_color=COLORS['CARD_WHITE'], corner_radius=12, height=120)
        card.grid(row=0, column=column, padx=(10, 0) if column > 0 else 0, pady=15, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        
        # Titre/Description
        title_label = ctk.CTkLabel(card, text=title, text_color=COLORS['TEXT_GREY'], anchor="w",
                                    font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"))
        title_label.grid(row=0, column=0, padx=15, pady=(15, 0), sticky="w")
        
        # Valeur/Nombre
        value_label = ctk.CTkLabel(card, text=value, text_color=color, anchor="w",
                                    font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=36, weight="bold"))
        value_label.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="w")


class TableauDashboard(ctk.CTkFrame):
    """
    Affiche la liste du personnel dans un tableau scrollable.
    """
    def __init__(self, master, personnel_data, **kwargs):
        # Définir la couleur par défaut seulement si elle n'est pas déjà spécifiée
        if 'fg_color' not in kwargs:
            kwargs['fg_color'] = COLORS['CARD_WHITE']
        if 'corner_radius' not in kwargs:
            kwargs['corner_radius'] = 15
            
        super().__init__(master, **kwargs)
        self.data = personnel_data
        self.grid_columnconfigure(0, weight=1)

        # Titre de la section
        table_title = ctk.CTkLabel(self, text="📋 Liste Complète du Personnel", text_color=COLORS['TEXT_DARK'], anchor="w",
                                    font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=18, weight="bold"))
        table_title.pack(fill="x", padx=20, pady=(15, 5))

        # Cadre Scrollable pour le contenu du tableau
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        
        self.setup_table()

    def setup_table(self):
        """ Configure les en-têtes et remplit le tableau avec les données. """
        
        headers = ("Matricule", "Nom & Email", "Type", "Classe", "Échelle", "Corps", "Statut", "Action")
        
        # Poids des colonnes pour un affichage proportionnel
        col_weights = [1, 3, 1, 1, 1, 2, 2, 2] 
        
        for i, header_text in enumerate(headers):
            # Configuration du poids de la colonne
            self.scroll_frame.grid_columnconfigure(i, weight=col_weights[i])
            
            # Création de l'en-tête
            header = ctk.CTkLabel(self.scroll_frame, text=header_text, 
                                fg_color=COLORS['HEADER_BG'], corner_radius=8,
                                text_color=COLORS['TEXT_DARK'], 
                                font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"))
            header.grid(row=0, column=i, sticky="nsew", padx=(5, 0) if i > 0 else 0, pady=5)


        # Remplissage des lignes de données
        for row_index, record in enumerate(self.data):
            row = row_index + 1  # La première rangée (row=0) est réservée aux en-têtes
            
            # Style de ligne alterné (comme dans un tableau)
            bg_color = COLORS['BG_LIGHT_GREY'] if row_index % 2 == 1 else COLORS['CARD_WHITE']
            text_color = COLORS['TEXT_DARK']

            # Matricule
            ctk.CTkLabel(self.scroll_frame, text=record["matricule"], text_color=text_color, 
                        fg_color=bg_color, anchor="w", corner_radius=0).grid(row=row, column=0, sticky="nsew", padx=(5, 0))

            # Nom, Prénom, Email et Initiales (Colonne 1)
            name_frame = ctk.CTkFrame(self.scroll_frame, fg_color=bg_color, corner_radius=0)
            name_frame.grid(row=row, column=1, sticky="nsew", padx=(5, 0))
            self.create_name_cell(name_frame, record, bg_color)
            
            # Type (Fonctionnaire/Contractuel)
            ctk.CTkLabel(self.scroll_frame, text=record["type"], text_color=text_color, 
                        fg_color=bg_color, anchor="w", corner_radius=0).grid(row=row, column=2, sticky="nsew", padx=(5, 0))
            
            # Classe
            ctk.CTkLabel(self.scroll_frame, text=record["classe"], text_color=text_color, 
                        fg_color=bg_color, anchor="w", corner_radius=0).grid(row=row, column=3, sticky="nsew", padx=(5, 0))
            
            # Échelle
            ctk.CTkLabel(self.scroll_frame, text=record["echelle"], text_color=text_color, 
                        fg_color=bg_color, anchor="w", corner_radius=0).grid(row=row, column=4, sticky="nsew", padx=(5, 0))
            
            # Corps
            ctk.CTkLabel(self.scroll_frame, text=record["corps"], text_color=text_color, 
                        fg_color=bg_color, anchor="w", corner_radius=0).grid(row=row, column=5, sticky="nsew", padx=(5, 0))
            
            # Statut (avec couleur contextuelle)
            statut_frame = ctk.CTkFrame(self.scroll_frame, fg_color=bg_color, corner_radius=0)
            statut_frame.grid(row=row, column=6, sticky="nsew", padx=(5, 0))
            self.create_statut_cell(statut_frame, record["statut"])
            
            # Action (Boutons Modifier/Supprimer)
            action_frame = ctk.CTkFrame(self.scroll_frame, fg_color=bg_color, corner_radius=0)
            action_frame.grid(row=row, column=7, sticky="nsew", padx=(5, 5))
            self.create_action_buttons(action_frame, record["matricule"])
            
    def create_name_cell(self, master, record, bg_color):
        """ Crée la cellule Nom & Email avec le bloc initiales. """
        master.grid_columnconfigure(0, weight=0) # Pour les initiales (taille fixe)
        master.grid_columnconfigure(1, weight=1) # Pour le texte (étirable)
        master.grid_rowconfigure((0, 1), weight=1)
        
        # Bloc Initiales
        initials_frame = self.get_initials_frame(master, record["prenom"], record["nom"])
        initials_frame.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky="w")
        
        # Nom complet
        name_label = ctk.CTkLabel(master, text=f"{record['nom'].upper()} {record['prenom']}", 
                                text_color=COLORS['TEXT_DARK'], anchor="w", fg_color=bg_color,
                                font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"))
        name_label.grid(row=0, column=1, sticky="w")

        # Email
        email_label = ctk.CTkLabel(master, text=record['email'], text_color=COLORS['TEXT_GREY'], 
                                anchor="w", fg_color=bg_color,
                                font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=12))
        email_label.grid(row=1, column=1, sticky="w")


    def get_initials_frame(self, master, first_name, last_name):
        """ Crée le petit bloc carré avec les initiales. """
        initials = first_name[0].upper() + last_name[0].upper()
        initials_frame = ctk.CTkFrame(master, width=30, height=30, fg_color=COLORS['PRIMARY_BLUE'], corner_radius=8)
        initials_frame.grid_propagate(False)
        
        initials_label = ctk.CTkLabel(initials_frame, text=initials, text_color=COLORS['CARD_WHITE'],
                                    font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=12, weight="bold"))
        initials_label.place(relx=0.5, rely=0.5, anchor="center") # Centrer le texte dans le bloc
        return initials_frame
        
    def create_statut_cell(self, master, statut):
        """ Crée la cellule de statut avec un indicateur de couleur. """
        
        # Logique de couleur pour le statut
        if statut in ("En activité", "Sous le drapeau"):
            color = COLORS['ACCENT_GREEN']
        elif statut in ("En congé", "En détachement", "Hors cadre"):
            color = COLORS['PRIMARY_BLUE']
        else: # En disponibilité, En attente, etc.
            color = COLORS['ACCENT_RED']
            
        # Cadre pour aligner verticalement
        statut_label = ctk.CTkLabel(master, text=statut, text_color=color, 
                                    font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                                    anchor="w")
        statut_label.pack(side="left", padx=5, pady=5)


    def create_action_buttons(self, master, matricule):
        """ Crée les boutons Modifier et Supprimer avec des icônes. """
        # Utilisation d'un cadre transparent pour centrer les boutons dans la cellule
        action_frame = ctk.CTkFrame(master, fg_color="transparent")
        action_frame.pack(expand=True, padx=5, pady=5)

        # Bouton Modifier (Edit icon: ✏️)
        edit_btn = ctk.CTkButton(action_frame, text="✏️", width=30, height=30, corner_radius=6,
                                fg_color=COLORS['PRIMARY_BLUE'], hover_color=COLORS['PRIMARY_BLUE'],
                                command=lambda m=matricule: print(f"Modifier {m}")) # Placeholder command
        edit_btn.pack(side="left", padx=(0, 5))
        
        # Bouton Supprimer (Delete icon: 🗑️)
        delete_btn = ctk.CTkButton(action_frame, text="🗑️", width=30, height=30, corner_radius=6,
                                fg_color=COLORS['ACCENT_RED'], hover_color="#c83f3f",
                                command=lambda m=matricule: print(f"Supprimer {m}")) # Placeholder command
        delete_btn.pack(side="left")


class DashboardView(ctk.CTkFrame):
    """ Conteneur principal pour le tableau de bord, combinant le Bilan et le Tableau. """
    def __init__(self, master=None, controller=None, **kwargs):
        # Utilisation d'un fond clair pour le contenu
        super().__init__(master, fg_color=COLORS['BG_LIGHT_GREY'], **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Rendre la rangée du tableau étirable

        # 1. Titre de la page (Tableau de bord)
        title_label = ctk.CTkLabel(self, text="Tableau de bord", text_color=COLORS['TEXT_DARK'], anchor="w",
                                font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=25, pady=(20, 5), sticky="w")

        # 2. Bilan (Synthèse des cartes)
        self.bilan_frame = Bilan(self, PERSONNEL_DATA)
        self.bilan_frame.grid(row=1, column=0, padx=20, pady=0, sticky="new")
        
        # 3. Tableau du Personnel
        self.tableau_frame = TableauDashboard(self, PERSONNEL_DATA)
        self.tableau_frame.grid(row=2, column=0, padx=20, pady=(10, 20), sticky="nsew")