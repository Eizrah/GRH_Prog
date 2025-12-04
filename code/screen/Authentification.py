import customtkinter as ctk
from tkinter import messagebox
from .FenetrePrincipal import Fenetreprincpale
""" 
NOTE
À revoir l'authentification pour savoir c'est l'admin ou le RH qui se connecte
"""

COLORS = {
    "PRIMARY_BLUE": "#4A90E2",
    "ACCENT_GREEN": "#10B981",
    "ACCENT_RED": "#EF4444",
    "BG_LIGHT_GREY": "#F0F2F5",
    "CARD_WHITE": "#FFFFFF",
    "TEXT_DARK": "#374151",
    "TEXT_GREY": "#9CA3AF",
    "HEADER_BG": "#E5F0FF",
    "ACTIVE_SIDEBAR": "#1E40AF",
    "TEXT_BLACK": "#000000"
}


class LoginPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Connexion RH.App")
        self.geometry("800x500")
        self.configure(fg_color=COLORS['BG_LIGHT_GREY'])
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.create_login_ui()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_login_ui(self):
        # ... (Création des cadres et labels de design) ...
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['BG_LIGHT_GREY'])
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        login_card_frame = ctk.CTkFrame(main_frame, fg_color=COLORS['CARD_WHITE'], corner_radius=15, width=700, height=450)
        login_card_frame.grid(row=0, column=0, sticky="")
        login_card_frame.grid_columnconfigure(0, weight=1)
        login_card_frame.grid_columnconfigure(1, weight=1)

        form_frame = ctk.CTkFrame(login_card_frame, fg_color=COLORS['CARD_WHITE'])
        form_frame.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        form_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(form_frame, text="LOG IN PLEASE",
                     font=ctk.CTkFont( size=28, weight="bold"),
                     text_color=COLORS['TEXT_DARK']).grid(row=0, column=0, pady=(30, 40), sticky="s")

        self.username_entry = ctk.CTkEntry(form_frame, placeholder_text="📧 Utilisateur (Ex: admin, rakoto.jp, rh)",
                                           width=300, height=45, corner_radius=8,
                                           font=ctk.CTkFont( size=15))
        self.username_entry.grid(row=1, column=0, pady=15, padx=20, sticky="ew")
        self.username_entry.insert(0, "admin")

        self.password_entry = ctk.CTkEntry(form_frame,
                                           placeholder_text="🔑 Mot de passe (Ex: admin123, rh123, personnel)",
                                           show="*", width=300, height=45, corner_radius=8,
                                           font=ctk.CTkFont( size=15))
        self.password_entry.grid(row=2, column=0, pady=15, padx=20, sticky="ew")
        self.password_entry.insert(0, "admin123")

        options_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        options_frame.grid(row=3, column=0, pady=(5, 30), padx=20, sticky="ew")
        options_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkCheckBox(options_frame, text="Se souvenir de moi", corner_radius=5, text_color=COLORS['TEXT_DARK'],
                        font=ctk.CTkFont( size=12)).pack(side="left")
        ctk.CTkButton(options_frame, text="Mot de passe oublié ?", fg_color="transparent",
                      text_color=COLORS['PRIMARY_BLUE'], hover_color=COLORS['CARD_WHITE'],
                      font=ctk.CTkFont(size=12, weight="bold")).pack(side="right")

        ctk.CTkButton(form_frame, text="LOG IN", command=self.attempt_login,
                      width=150, height=40, corner_radius=8,
                      font=ctk.CTkFont( size=18, weight="bold"),
                      fg_color=COLORS['PRIMARY_BLUE'], hover_color="#3670B3").grid(row=4, column=0, pady=(0, 30))
        self.bind('<Return>', lambda event: self.attempt_login())

        # Design partie droite
        design_frame = ctk.CTkFrame(login_card_frame, fg_color=COLORS['PRIMARY_BLUE'], corner_radius=15)
        design_frame.grid(row=0, column=1, sticky="nsew")
        design_content = ctk.CTkFrame(design_frame, fg_color="transparent")
        design_content.grid(row=0, column=0, sticky="nsew")
        design_content.grid_columnconfigure(0, weight=1)
        design_content.grid_rowconfigure(0, weight=1)

        ctk.CTkLabel(design_content, text="BIENVENUE !",
                     font=ctk.CTkFont( size=34, weight="bold"),
                     text_color=COLORS['CARD_WHITE']).pack(pady=(120, 10))

        ctk.CTkLabel(design_content, text="Connectez-vous à votre espace RH",
                     font=ctk.CTkFont( size=16),
                     text_color=COLORS['CARD_WHITE']).pack(pady=(0, 30))

        ctk.CTkButton(design_content, text="S'INSCRIRE", fg_color="transparent", border_width=2,
                      border_color=COLORS['CARD_WHITE'], hover_color="#3670B3",
                      width=100, height=35, corner_radius=8,
                      font=ctk.CTkFont( size=14, weight="bold")).pack()


    def attempt_login(self):
        """Fonction de connexion simulée (Frontend uniquement)."""
        username = self.username_entry.get().strip()
        # Simulation d'une connexion réussie pour lancer l'app principale
        if username in ["admin", "rakoto.jp", "rh"]:
            self.destroy()
            app = Fenetreprincpale()
            app.mainloop()
        else:
            messagebox.showerror("Erreur de Connexion", "Identifiants invalides (Simulés). Veuillez réessayer.")
            self.password_entry.delete(0, 'end')

    def on_closing(self):
        self.destroy()