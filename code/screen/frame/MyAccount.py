import customtkinter as ctk
from datetime import datetime

# Couleurs
COLORS = {
    "BG_LIGHT_GREY": "#F0F2F5",
    "CARD_WHITE": "#FFFFFF",
    "TEXT_DARK": "#374151",
    "TEXT_GREY": "#9CA3AF",
    "ACCENT_BLUE": "#4A90E2",
    "HEADER_BG": "#E5F0FF",
}

class MyAccount(ctk.CTkFrame):
    """Frame pour afficher les informations du compte utilisateur"""
    
    def __init__(self, master, controller=None, **kwargs):
        super().__init__(master, fg_color=COLORS['BG_LIGHT_GREY'], **kwargs)
        self.controller = controller
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Cadre scrollable pour le contenu
        self.scrollable_content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scrollable_content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.scrollable_content.grid_columnconfigure(0, weight=1)
        
        self.create_account_view()
    
    def create_account_view(self):
        """Crée la vue du compte utilisateur"""
        
        # === EN-TÊTE ===
        header_frame = ctk.CTkFrame(self.scrollable_content, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="👤 Mon compte",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            text_color=COLORS['TEXT_DARK'],
            anchor="w"
        )
        title_label.pack(side="left", padx=5)
        
        # === SECTION PROFIL UTILISATEUR ===
        profile_frame = ctk.CTkFrame(self.scrollable_content, fg_color=COLORS['CARD_WHITE'], corner_radius=15)
        profile_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        profile_frame.grid_columnconfigure(1, weight=1)
        
        # Avatar
        avatar_label = ctk.CTkLabel(
            profile_frame,
            text="R",
            font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
            text_color=COLORS['CARD_WHITE'],
            fg_color=COLORS['ACCENT_BLUE'],
            width=80,
            height=80,
            corner_radius=40
        )
        avatar_label.grid(row=0, column=0, rowspan=3, padx=30, pady=30, sticky="w")
        
        # Nom
        name_label = ctk.CTkLabel(
            profile_frame,
            text="Responsable RH",
            font=ctk.CTkFont(family="Arial", size=22, weight="bold"),
            text_color=COLORS['TEXT_DARK'],
            anchor="w"
        )
        name_label.grid(row=0, column=1, sticky="w", padx=10, pady=(30, 5))
        
        # Matricule et type
        info1_label = ctk.CTkLabel(
            profile_frame,
            text="Matricule: RH001 | Fonctionnaire",
            font=ctk.CTkFont(family="Arial", size=13),
            text_color=COLORS['TEXT_GREY'],
            anchor="w"
        )
        info1_label.grid(row=1, column=1, sticky="w", padx=10, pady=2)
        
        # Poste et grade
        info2_label = ctk.CTkLabel(
            profile_frame,
            text="Poste: Responsable RH | Grade: Chef de service",
            font=ctk.CTkFont(family="Arial", size=13),
            text_color=COLORS['TEXT_GREY'],
            anchor="w"
        )
        info2_label.grid(row=2, column=1, sticky="w", padx=10, pady=(2, 30))
        
        # === GRILLE DE CARTES D'INFORMATIONS ===
        cards_container = ctk.CTkFrame(self.scrollable_content, fg_color="transparent")
        cards_container.grid(row=2, column=0, sticky="ew")
        cards_container.grid_columnconfigure(0, weight=1)
        cards_container.grid_columnconfigure(1, weight=1)
        
        # Carte 1: Date de naissance
        self.create_info_card(
            cards_container,
            "📅 Date de naissance",
            "1980-01-01",
            "Antananarivo",
            row=0, col=0
        )
        
        # Carte 2: Date d'entrée
        self.create_info_card(
            cards_container,
            "📆 Date d'entrée",
            "2010-01-01",
            "Ancienneté: 15 an(s) et 11 mois",
            row=0, col=1
        )
        
        # Carte 3: Position
        self.create_info_card(
            cards_container,
            "💼 Position",
            "En activité",
            "Cadre: A",
            row=1, col=0
        )
        
        # Carte 4: Grade/Classe
        self.create_info_card(
            cards_container,
            "📊 Grade/Classe",
            "exceptionnelle",
            "Échelon: 2",
            row=1, col=1
        )
        
        # Carte 5: Corps/Échelle
        self.create_info_card(
            cards_container,
            "🏢 Corps/Échelle",
            "Administration",
            "Échelle: A1",
            row=2, col=0
        )
        
        # Carte 6: Indice de solde
        self.create_info_card(
            cards_container,
            "💰 Indice de solde",
            "800",
            "",
            row=2, col=1
        )
    
    def create_info_card(self, parent, title, main_value, sub_value, row, col):
        """Crée une carte d'information"""
        card = ctk.CTkFrame(parent, fg_color=COLORS['CARD_WHITE'], corner_radius=12)
        card.grid(row=row, column=col, sticky="ew", padx=10, pady=10)
        
        # Titre avec icône
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(family="Arial", size=12),
            text_color=COLORS['TEXT_GREY'],
            anchor="w"
        )
        title_label.pack(anchor="w", padx=20, pady=(15, 5))
        
        # Valeur principale
        main_label = ctk.CTkLabel(
            card,
            text=main_value,
            font=ctk.CTkFont(family="Arial", size=18, weight="bold"),
            text_color=COLORS['TEXT_DARK'],
            anchor="w"
        )
        main_label.pack(anchor="w", padx=20, pady=(0, 5))
        
        # Sous-valeur (si présente)
        if sub_value:
            sub_label = ctk.CTkLabel(
                card,
                text=sub_value,
                font=ctk.CTkFont(family="Arial", size=11),
                text_color=COLORS['TEXT_GREY'],
                anchor="w"
            )
            sub_label.pack(anchor="w", padx=20, pady=(0, 15))
        else:
            # Padding si pas de sous-valeur
            ctk.CTkLabel(card, text="", height=5).pack()


if __name__ == "__main__":
    # Test de la frame
    app = ctk.CTk()
    app.geometry("1000x700")
    app.title("Test MyAccount")
    
    frame = MyAccount(app)
    frame.pack(fill="both", expand=True)
    
    app.mainloop()
