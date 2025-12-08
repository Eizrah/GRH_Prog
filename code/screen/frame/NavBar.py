import customtkinter

# Couleurs inspirées du design RH Legal Pro
COLORS = {
    "NAV_BG": "#384456",  # Fond bleu-gris foncé (dark blue-gray)
    "TEXT_WHITE": "#FFFFFF",
    "TEXT_LIGHT_GRAY": "#B0B8C4",  # Gris clair pour sous-titre
    "ACCENT_BLUE": "#4A9FE7",  # Bleu pour le cercle utilisateur
    "ACCENT_GREEN": "#10B981",  # Vert pour le point d'administrateur
    "HOVER_COLOR": "#4A5C70",  # Couleur hover légèrement plus claire
    "ACTIVE_COLOR": "#2D3848",  # Couleur pour bouton actif
    "TEXT_ACTIVE": "#4A9FE7",
    "ACCENT_RED": "#EF4444",
    "HOVER_RED": "#c83f3f"
}

class NavBar(customtkinter.CTkFrame):
    def __init__(self, master, controller=None, user_data=None, **kwargs):
        super().__init__(master, width=280, corner_radius=0, fg_color=COLORS['NAV_BG'], **kwargs)
        
        self.controller = controller
        self.user_data = user_data or {}
        self.user_role = self.user_data.get('role', 'guest')
        self.user_name = self.user_data.get('nom_complet', 'Utilisateur')
        self.user_matricule = self.user_data.get('matricule', 'N/A')
        
        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # En-tête avec logo et titre
        self.grid_rowconfigure(1, weight=0)  # Info utilisateur
        self.grid_rowconfigure(2, weight=1)  # Boutons de navigation
        self.grid_rowconfigure(3, weight=0)  # Déconnexion
        
        # === EN-TÊTE AVEC LOGO ET TITRE ===
        header_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(30, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        # Logo (icône de balance de justice - simulé avec emoji)
        logo_label = customtkinter.CTkLabel(
            header_frame,
            text="⚖️",
            font=customtkinter.CTkFont(size=48),
            text_color=COLORS['TEXT_WHITE']
        )
        logo_label.grid(row=0, column=0, pady=(0, 10))
        
        # Titre principal
        title_label = customtkinter.CTkLabel(
            header_frame,
            text="RH Legal Pro",
            font=customtkinter.CTkFont(family="Arial", size=24, weight="bold"),
            text_color=COLORS['TEXT_WHITE']
        )
        title_label.grid(row=1, column=0)
        
        # Sous-titre
        subtitle_label = customtkinter.CTkLabel(
            header_frame,
            text="Gestion conforme aux lois",
            font=customtkinter.CTkFont(family="Arial", size=12),
            text_color=COLORS['TEXT_LIGHT_GRAY']
        )
        subtitle_label.grid(row=2, column=0, pady=(5, 0))
        
        # === INFO UTILISATEUR ===
        user_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        user_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(20, 30))
        user_frame.grid_columnconfigure(1, weight=1)
        
        # Cercle avec initiale (Avatar) - Première lettre du nom
        initial = self.user_name[0].upper() if self.user_name else "U"
        avatar_label = customtkinter.CTkLabel(
            user_frame,
            text=initial,
            font=customtkinter.CTkFont(family="Arial", size=20, weight="bold"),
            text_color=COLORS['TEXT_WHITE'],
            fg_color=COLORS['ACCENT_BLUE'],
            width=50,
            height=50,
            corner_radius=25
        )
        avatar_label.grid(row=0, column=0, rowspan=2, padx=(0, 12), sticky="w")
        
        # Nom de rôle
        role_label = customtkinter.CTkLabel(
            user_frame,
            text=self.user_name,
            font=customtkinter.CTkFont(family="Arial", size=14, weight="bold"),
            text_color=COLORS['TEXT_WHITE'],
            anchor="w"
        )
        role_label.grid(row=0, column=1, sticky="w")
        
        # Statut avec point vert
        status_text = f"● {self.user_matricule}"
        status_label = customtkinter.CTkLabel(
            user_frame,
            text=status_text,
            font=customtkinter.CTkFont(family="Arial", size=11),
            text_color=COLORS['ACCENT_GREEN'],
            anchor="w"
        )
        status_label.grid(row=1, column=1, sticky="w", pady=(2, 0))
        
        # === BOUTONS DE NAVIGATION ===
        self.nav_links_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.nav_links_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=(0, 10))
        self.nav_links_frame.grid_columnconfigure(0, weight=1)
        
        row_index = 0
        
        # Bouton Dashboard (toujours visible)
        self.dashboard = customtkinter.CTkButton(
            self.nav_links_frame,
            text="📊 Tableau de bord",
            fg_color=COLORS['ACTIVE_COLOR'],
            text_color=COLORS['TEXT_ACTIVE'],
            hover_color=COLORS['HOVER_COLOR'],
            anchor="w",
            corner_radius=8,
            height=45,
            font=customtkinter.CTkFont(family="Arial", size=14, weight="bold")
        )
        self.dashboard.grid(row=row_index, column=0, padx=5, pady=5, sticky="ew")
        row_index += 1
        
        # Boutons selon le rôle
        if self.user_role == 'admin':
            # Admin: AdminFrame
            self.ValidationAdmin = customtkinter.CTkButton(
                self.nav_links_frame,
                text="� Liste des demandes",
                fg_color="transparent",
                text_color=COLORS['TEXT_WHITE'],
                hover_color=COLORS['HOVER_COLOR'],
                anchor="w",
                corner_radius=8,
                height=45,
                font=customtkinter.CTkFont(family="Arial", size=14, weight="bold")
            )
            self.ValidationAdmin.grid(row=row_index, column=0, padx=5, pady=5, sticky="ew")
            row_index += 1
            
        elif self.user_role == 'rh':
            # RH: AddPers + Dmd
            self.addPers = customtkinter.CTkButton(
                self.nav_links_frame,
                text="� Ajouter Personne",
                fg_color="transparent",
                text_color=COLORS['TEXT_WHITE'],
                hover_color=COLORS['HOVER_COLOR'],
                anchor="w",
                corner_radius=8,
                height=45,
                font=customtkinter.CTkFont(family="Arial", size=14, weight="bold")
            )
            self.addPers.grid(row=row_index, column=0, padx=5, pady=5, sticky="ew")
            row_index += 1
            
            self.DemandeBtn = customtkinter.CTkButton(
                self.nav_links_frame,
                text="� Demande de Congé",
                fg_color="transparent",
                text_color=COLORS['TEXT_WHITE'],
                hover_color=COLORS['HOVER_COLOR'],
                anchor="w",
                corner_radius=8,
                height=45,
                font=customtkinter.CTkFont(family="Arial", size=14, weight="bold")
            )
            self.DemandeBtn.grid(row=row_index, column=0, padx=5, pady=5, sticky="ew")
            row_index += 1
        
        # Bouton Mon Compte (toujours visible)
        self.MonCompteBtn = customtkinter.CTkButton(
            self.nav_links_frame,
            text="👤 Mon Compte",
            fg_color="transparent",
            text_color=COLORS['TEXT_WHITE'],
            hover_color=COLORS['HOVER_COLOR'],
            anchor="w",
            corner_radius=8,
            height=45,
            font=customtkinter.CTkFont(family="Arial", size=14, weight="bold")
        )
        self.MonCompteBtn.grid(row=row_index, column=0, padx=5, pady=5, sticky="ew")
        
        # === BOUTON DÉCONNEXION ===
        self.DeconnexionBtn = customtkinter.CTkButton(
            self,
            text="⏻ Déconnexion",
            corner_radius=8,
            fg_color=COLORS['ACCENT_RED'],
            hover_color=COLORS['HOVER_RED'],
            height=45,
            font=customtkinter.CTkFont(family="Arial", size=14, weight="bold")
        )
        self.DeconnexionBtn.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
    
    def set_active_button(self, button_name):
        """Change la couleur du bouton actif"""
        buttons = {
            'dashboard': self.dashboard,
            'MonCompteBtn': self.MonCompteBtn
        }
        
        # Ajouter les boutons selon le rôle
        if hasattr(self, 'addPers'):
            buttons['addPers'] = self.addPers
        if hasattr(self, 'DemandeBtn'):
            buttons['DemandeBtn'] = self.DemandeBtn
        if hasattr(self, 'ValidationAdmin'):
            buttons['ValidationAdmin'] = self.ValidationAdmin
        
        for name, button in buttons.items():
            if name == button_name:
                button.configure(
                    fg_color=COLORS['ACTIVE_COLOR'],
                    text_color=COLORS['TEXT_ACTIVE']
                )
            else:
                button.configure(
                    fg_color="transparent",
                    text_color=COLORS['TEXT_WHITE']
                )