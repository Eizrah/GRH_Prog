import customtkinter as ctk
# Importation des vues
from .frame.NavBar import NavBar 
from .frame.Dashboard import DashboardView
from .frame.AddPers import AjoutPersonnelView
from .frame.Dmd import Dmd  # Ajout de cette importation
from .frame.AdminFrame import AdminFrame
# COULEURS (Subset)
COLORS = {
    "BG_LIGHT_GREY": "#F0F2F5",
    "CARD_WHITE": "#FFFFFF",
}

class Fenetreprincpale(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("blue")
        
        # paramètres de la fenêtre principale
        self.title("Application RH - Gestion du Personnel")
        self.geometry("1200x750")
        self.resizable(True, True)
        
        self.configure(fg_color=COLORS['BG_LIGHT_GREY'])
        
        # Configuration de la grille
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)  # Colonne 0 (NavBar) : Taille fixe
        self.grid_columnconfigure(1, weight=1)  # Colonne 1 (Contenu) : S'étend
        
        # --- Dictionnaire pour stocker les vues ---
        self.frames = {}
        
        # --- 1. PLACEMENT DE LA BARRE DE NAVIGATION (Colonne 0) ---
        # On passe 'self' (l'instance de Fenetreprincpale) comme contrôleur
        self.nav_bar = NavBar(master=self, controller=self)
        self.nav_bar.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # --- 2. CADRE CONTENEUR DE VUES (Colonne 1) ---
        self.container = ctk.CTkFrame(self, fg_color=COLORS['BG_LIGHT_GREY'])
        self.container.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # --- 3. CRÉATION ET ENREGISTREMENT DES VUES ---
        # Liste des classes de vues à instancier (AJOUT DE Dmd)
        views = [DashboardView, AjoutPersonnelView, Dmd,AdminFrame]
        
        for F in views:
            # Le nom de la vue est le nom de la classe
            frame_name = F.__name__
            # Instanciation de la vue dans le container
            frame = F(master=self.container, controller=self)
            # Enregistrement dans le dictionnaire
            self.frames[frame_name] = frame
            # Placement de la frame pour qu'elle remplisse tout le container (mais elle est cachée initialement)
            frame.grid(row=0, column=0, sticky="nsew")

        # --- 4. Afficher la vue par défaut ---
        self.show_frame("DashboardView")
        
        # --- 5. Connecter les boutons de la NavBar ---
        self.connect_navbar_buttons()

    def connect_navbar_buttons(self):
        """Connecte les boutons de la navbar aux méthodes correspondantes"""
        if hasattr(self.nav_bar, 'dashboard'):
            self.nav_bar.dashboard.configure(command=lambda: self.show_frame("DashboardView"))
        
        if hasattr(self.nav_bar, 'addPers'):
            self.nav_bar.addPers.configure(command=lambda: self.show_frame("AjoutPersonnelView"))
        
        # Ajout du bouton Demande
        if hasattr(self.nav_bar, 'DemandeBtn'):
            self.nav_bar.DemandeBtn.configure(command=lambda: self.show_frame("Dmd"))
        
        # CORRECTION ICI : AdminFrame au lieu de DeconnexionBtn
        if hasattr(self.nav_bar, 'ValidationAdmin'):
            self.nav_bar.ValidationAdmin.configure(command=lambda: self.show_frame("AdminFrame"))  # Correction
        
        # Bouton de déconnexion
        if hasattr(self.nav_bar, 'DeconnexionBtn'):
            self.nav_bar.DeconnexionBtn.configure(command=self.quitter_application)

    def quitter_application(self):
        """Méthode pour quitter l'application"""
        self.destroy()

    def show_frame(self, page_name):
        """ 
        Affiche la frame passée en argument et masque les autres.
        :param page_name: Nom de la classe de la vue à afficher (e.g., "DashboardView").
        """
        frame = self.frames.get(page_name)
        if frame:
            # Remonter la frame en haut de la pile (la rendre visible)
            frame.tkraise()
            
            # Mettre à jour le bouton actif dans la navbar
            if hasattr(self.nav_bar, 'set_active_button'):
                if page_name == "DashboardView":
                    self.nav_bar.set_active_button('dashboard')
                elif page_name == "AjoutPersonnelView":
                    self.nav_bar.set_active_button('addPers')
                elif page_name == "Dmd":  # Ajout pour Dmd
                    self.nav_bar.set_active_button('DemandeBtn')
                elif page_name == "AdminFrame":  # Correction ici
                    self.nav_bar.set_active_button('ValidationAdmin')  # Utilisez le bon nom de bouton
                # Ajoutez d'autres correspondances au besoin
        else:
            print(f"Erreur: La vue '{page_name}' n'existe pas.")
    
    def add_personnel(self, data):
        """
        Méthode pour ajouter un personnel (appelée par AjoutPersonnelView)
        À implémenter avec votre logique de sauvegarde
        """
        print(f"Données reçues pour ajout de personnel: {data}")
        # Ici vous devrez implémenter la logique de sauvegarde dans votre base de données
        # Par exemple: sauvegarde en base de données, fichier, etc.
    
    def ajouter_demande(self, data):
        """
        Méthode pour ajouter une demande de congé (appelée par Dmd)
        À implémenter avec votre logique de sauvegarde
        """
        print(f"Données reçues pour demande de congé: {data}")
        # Ici vous devrez implémenter la logique de sauvegarde des demandes