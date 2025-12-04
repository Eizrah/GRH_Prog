import customtkinter


COLORS = {
    "ACCENT_RED": "#EF4444",
    "BG_LIGHT_GREY": "#F0F2F5", 
    "CARD_WHITE": "#FFFFFF", 
    "TEXT_DARK": "#374151", 
}
HOVER_DECONNEXION = "#c83f3f" 
HOVER_INACTIVE = COLORS['BG_LIGHT_GREY']
TEXT_COLOR_INACTIVE = COLORS['TEXT_DARK']
TEXT_COLOR_ACTIVE = "#4A90E2"  # Couleur pour l'élément actif

class NavBar(customtkinter.CTkFrame):
    def __init__(self, master, controller=None, **kwargs):
        super().__init__(master, width=220, corner_radius=15, fg_color=COLORS['CARD_WHITE'], **kwargs)
        
        self.controller = controller  # Stocker la référence au contrôleur
        
        # NOUVELLE CONFIGURATION INTERNE DE LA GRILLE (3 Rangées)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)    # Rangée 0 : Titre
        self.grid_rowconfigure(1, weight=1)    # Rangée 1 : Liens de navigation
        self.grid_rowconfigure(2, weight=0)    # Rangée 2 : Bouton Déconnexion

        # Label en forme de titre
        self.labTitre = customtkinter.CTkLabel(self,
                                                text="RH.App - Gestion des Congés",
                                                font=customtkinter.CTkFont(family="Arial", size=16, weight="bold"),
                                                text_color=COLORS['TEXT_DARK']) 
        
        self.labTitre.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="new")
        
        # Cadre pour les liens de navigation
        self.nav_links_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.nav_links_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(10, 5))
        self.nav_links_frame.grid_columnconfigure(0, weight=1)

        # Bouton Dashboard (actif par défaut)
        self.dashboard = customtkinter.CTkButton(self.nav_links_frame,
                                                 text="📊 Tableau de bord",
                                                 fg_color="transparent",
                                                 text_color=TEXT_COLOR_ACTIVE,  # Couleur active
                                                 hover_color=HOVER_INACTIVE,
                                                 anchor="w", 
                                                 corner_radius=8,
                                                 font=customtkinter.CTkFont(family="Arial", size=14, weight="bold"))
        self.dashboard.grid(row=0, column=0, padx=10, pady=4, sticky="new")
        
        # Bouton Ajouter Personne
        self.addPers = customtkinter.CTkButton(self.nav_links_frame, 
                                                 text="👤 Ajouter Personne",
                                                 fg_color="transparent", 
                                                 text_color=TEXT_COLOR_INACTIVE, 
                                                 hover_color=HOVER_INACTIVE, 
                                                 anchor="w", 
                                                 corner_radius=8,
                                                 font=customtkinter.CTkFont(family="Arial", size=14, weight="bold"))
        self.addPers.grid(row=1, column=0, padx=10, pady=4, sticky="new")
        
        # Bouton Demande de Congé
        self.DemandeBtn = customtkinter.CTkButton(self.nav_links_frame, 
                                                 text="📝 Demande de Congé",
                                                 fg_color="transparent", 
                                                 text_color=TEXT_COLOR_INACTIVE, 
                                                 hover_color=HOVER_INACTIVE, 
                                                 anchor="w", 
                                                 corner_radius=8,
                                                 font=customtkinter.CTkFont(family="Arial", size=14, weight="bold"))
        self.DemandeBtn.grid(row=2, column=0, padx=10, pady=4, sticky="new")
        
        # Bouton Liste des demandes
        self.ValidationAdmin = customtkinter.CTkButton(self.nav_links_frame, 
                                                 text="📋 Liste des demandes",
                                                 fg_color="transparent", 
                                                 text_color=TEXT_COLOR_INACTIVE, 
                                                 hover_color=HOVER_INACTIVE, 
                                                 anchor="w", 
                                                 corner_radius=8,
                                                 font=customtkinter.CTkFont(family="Arial", size=14, weight="bold"))
        self.ValidationAdmin.grid(row=3, column=0, padx=10, pady=4, sticky="new")
        
        # Bouton Déconnexion
        self.DeconnexionBtn = customtkinter.CTkButton(self, 
                                                     text="Déconnexion", 
                                                     corner_radius=8, 
                                                     fg_color=COLORS['ACCENT_RED'],
                                                     hover_color=HOVER_DECONNEXION,
                                                     font=customtkinter.CTkFont(family="Arial", size=14, weight="bold"))
        self.DeconnexionBtn.grid(row=2, column=0, padx=20, pady=20, sticky="sew")
    
    def set_active_button(self, button_name):
        """Change la couleur du bouton actif"""
        # Réinitialiser tous les boutons à la couleur inactive
        buttons = {
            'dashboard': self.dashboard,
            'addPers': self.addPers,
            'DemandeBtn': self.DemandeBtn,
            'ValidationAdmin': self.ValidationAdmin
        }
        
        for name, button in buttons.items():
            if name == button_name:
                button.configure(text_color=TEXT_COLOR_ACTIVE)
            else:
                button.configure(text_color=TEXT_COLOR_INACTIVE)