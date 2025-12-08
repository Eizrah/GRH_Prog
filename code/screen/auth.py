"""
Module d'authentification et page de connexion
"""
import customtkinter as ctk
from tkinter import messagebox
from config import USERS_DB, DEFAULT_FONT_FAMILY, COLORS
from global_state import global_state

class ModernLoginPage(ctk.CTk):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager

        # Stocker le data_manager dans l'état global
        global_state.set_data_manager(data_manager)

        # Configuration de la fenêtre
        self.title("RH Legal Pro - Connexion")
        self.geometry("1000x600")
        self.configure(fg_color=COLORS['BG_LIGHT'])
        self.resizable(False, False)

        # Centrer la fenêtre
        self.update_idletasks()
        width = 1000
        height = 600
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.create_modern_login_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_modern_login_ui(self):
        """Crée l'interface de connexion moderne"""
        main_container = ctk.CTkFrame(self, fg_color=COLORS['BG_WHITE'], corner_radius=20)
        main_container.grid(row=0, column=0, padx=50, pady=50, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        # Deux colonnes
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)

        # --- Colonne de gauche : Logo et informations ---
        left_frame = ctk.CTkFrame(main_container, fg_color=COLORS['PRIMARY'], corner_radius=15)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=20)

        self.create_left_panel(left_frame)

        # --- Colonne de droite : Formulaire de connexion ---
        right_frame = ctk.CTkFrame(main_container, fg_color=COLORS['BG_WHITE'], corner_radius=15)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=20)

        self.create_login_form(right_frame)

        # Lier la touche Entrée
        self.bind('<Return>', lambda event: self.attempt_login())

    def create_left_panel(self, parent):
        """Crée le panneau gauche avec logo et infos"""
        logo_frame = ctk.CTkFrame(parent, fg_color="transparent")
        logo_frame.pack(pady=60, padx=30)

        # Logo
        ctk.CTkLabel(logo_frame, text="⚖️",
                    font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=72),
                    text_color=COLORS['BG_WHITE']).pack()

        ctk.CTkLabel(logo_frame, text="RH Legal Pro",
                    font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=32, weight="bold"),
                    text_color=COLORS['BG_WHITE']).pack(pady=(10, 5))

        ctk.CTkLabel(logo_frame, text="Gestion conforme aux lois",
                    font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14),
                    text_color=COLORS['BG_WHITE']).pack()

    def create_login_form(self, parent):
        """Crée le formulaire de connexion"""
        ctk.CTkLabel(parent, text="Connexion sécurisée",
                    font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=28, weight="bold"),
                    text_color=COLORS['PRIMARY']).pack(pady=(50, 30))

        # Champ utilisateur
        user_frame = ctk.CTkFrame(parent, fg_color="transparent")
        user_frame.pack(pady=10, padx=40, fill="x")

        ctk.CTkLabel(user_frame, text="Identifiant",
                    font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=12, weight="bold"),
                    text_color=COLORS['TEXT_DARK']).pack(anchor="w")

        self.username_entry = ctk.CTkEntry(user_frame,
                                          placeholder_text="ex: admin, rh, rakoto.jp, razafy.ms",
                                          height=45,
                                          corner_radius=8,
                                          border_width=1,
                                          border_color=COLORS['BORDER'],
                                          fg_color=COLORS['BG_WHITE'],
                                          text_color=COLORS['TEXT_DARK'],
                                          font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.username_entry.pack(fill="x", pady=(5, 0))
        self.username_entry.insert(0, "admin")

        # Champ mot de passe
        password_frame = ctk.CTkFrame(parent, fg_color="transparent")
        password_frame.pack(pady=15, padx=40, fill="x")

        ctk.CTkLabel(password_frame, text="Mot de passe",
                    font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=12, weight="bold"),
                    text_color=COLORS['TEXT_DARK']).pack(anchor="w")

        self.password_entry = ctk.CTkEntry(password_frame,
                                          placeholder_text="Votre mot de passe",
                                          show="•",
                                          height=45,
                                          corner_radius=8,
                                          border_width=1,
                                          border_color=COLORS['BORDER'],
                                          fg_color=COLORS['BG_WHITE'],
                                          text_color=COLORS['TEXT_DARK'],
                                          font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.password_entry.pack(fill="x", pady=(5, 0))
        self.password_entry.insert(0, "admin123")

        # Bouton de connexion
        login_button = ctk.CTkButton(parent,
                                    text="SE CONNECTER",
                                    command=self.attempt_login,
                                    height=50,
                                    corner_radius=8,
                                    fg_color=COLORS['PRIMARY'],
                                    hover_color=COLORS['SECONDARY'],
                                    font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=16, weight="bold"))
        login_button.pack(pady=30, padx=40, fill="x")

    def attempt_login(self):
        """Tente de connecter l'utilisateur"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
            return

        if username in USERS_DB and USERS_DB[username]["password"] == password:
            # Stocker l'utilisateur dans l'état global
            user_data = USERS_DB[username]["data"].copy()
            global_state.set_current_user(user_data)

            print(f"Connexion réussie: {user_data['nom_complet']}")

            # Fermer la fenêtre de connexion et ouvrir l'application principale
            self.destroy()
            from main_app import ModernGestionCongeApp
            app = ModernGestionCongeApp(self.data_manager)
            app.mainloop()
        else:
            messagebox.showerror("Erreur d'authentification",
                               "Identifiants incorrects. Veuillez réessayer.")
            self.password_entry.delete(0, 'end')

    def on_closing(self):
        """Gère la fermeture de la fenêtre"""
        self.data_manager.close()
        self.destroy()