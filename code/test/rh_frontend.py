# rh_frontend.py - Interface Utilisateur Pure (Frontend)
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta # Utilisé uniquement pour les placeholders de date

# Assurez-vous d'avoir installé : pip install customtkinter tkcalendar
try:
    from tkcalendar import Calendar
except ImportError:
    # Classe de substitution si tkcalendar n'est pas installé
    class Calendar:
        def __init__(self, parent, *args, **kwargs):
            tk.Label(parent, text="tkcalendar non installé!").pack()
        def pack(self, *args, **kwargs): pass
        def grid(self, *args, **kwargs): pass
        def get_date(self): return datetime.now().strftime("%Y-%m-%d")

# --- Configuration Globale de CustomTkinter & COULEURS (Design) ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

DEFAULT_FONT_FAMILY = "Arial"

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

# =================================================================
# --- DONNÉES SIMULÉES (Mock Data pour le Frontend) ---
# (Non modifiées)
# =================================================================

MOCK_USER = {
    'id': '0', 'role': 'admin', 'nom_complet': 'Administrateur (Simulé)', 'personnel_id': '0'
}
MOCK_SOLDE_DATA = {
    'joursTotal': 30,
    'joursValides': 15,
    'joursEnAttente': 5,
    'joursRestants': 10
}
MOCK_TYPES_ABSENCE = {
    'CONGE_ANNUEL': 'Congé Annuel',
    'CONGE_MALADIE': 'Congé de Maladie',
    'PERMISSION_ABSENCE': 'Permission d\'absence',
}
MOCK_ABSENCES = [
    {'id': 'DEM-001', 'personnelId': '1', 'type': 'CONGE_ANNUEL', 'dateDebut': '2025-01-20', 'dateFin': '2025-01-27',
     'duree': 8, 'statut': 'EN_ATTENTE', 'accordePar': 'N/A', 'motif': 'Voyage personnel en attente.'},
    {'id': 'DEC-015', 'personnelId': '1', 'type': 'PERMISSION_ABSENCE', 'dateDebut': '2024-10-10', 'dateFin': '2024-10-12',
     'duree': 3, 'statut': 'TERMINE', 'accordePar': 'Chef Service', 'motif': 'Absence pour cause personnelle'},
    {'id': 'DEC-001', 'personnelId': '1', 'type': 'CONGE_ANNUEL', 'dateDebut': '2024-11-01', 'dateFin': '2024-11-15',
     'duree': 15, 'statut': 'APPROUVE', 'accordePar': 'Directeur RH', 'motif': 'Congés annuels 2024'},
]
MOCK_PERSONNELS = {
    '1': {'nom': 'RAKOTO', 'prenoms': 'Jean Pierre', 'numeroMatricule': 'MAT001'},
    '0': {'nom': 'ADMIN', 'prenoms': 'General', 'numeroMatricule': 'ADM000'},
}
CURRENT_MOCK_USER = MOCK_USER # Utilisateur courant simulé


# =================================================================
# --- PAGE DE CONNEXION (Design) ---
# (Non modifiée)
# =================================================================

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
                     font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=28, weight="bold"),
                     text_color=COLORS['TEXT_DARK']).grid(row=0, column=0, pady=(30, 40), sticky="s")

        self.username_entry = ctk.CTkEntry(form_frame, placeholder_text="📧 Utilisateur (Ex: admin, rakoto.jp, rh)",
                                           width=300, height=45, corner_radius=8,
                                           font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=15))
        self.username_entry.grid(row=1, column=0, pady=15, padx=20, sticky="ew")
        self.username_entry.insert(0, "admin")

        self.password_entry = ctk.CTkEntry(form_frame,
                                           placeholder_text="🔑 Mot de passe (Ex: admin123, rh123, personnel)",
                                           show="*", width=300, height=45, corner_radius=8,
                                           font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=15))
        self.password_entry.grid(row=2, column=0, pady=15, padx=20, sticky="ew")
        self.password_entry.insert(0, "admin123")

        options_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        options_frame.grid(row=3, column=0, pady=(5, 30), padx=20, sticky="ew")
        options_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkCheckBox(options_frame, text="Se souvenir de moi", corner_radius=5, text_color=COLORS['TEXT_DARK'],
                        font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=12)).pack(side="left")
        ctk.CTkButton(options_frame, text="Mot de passe oublié ?", fg_color="transparent",
                      text_color=COLORS['PRIMARY_BLUE'], hover_color=COLORS['CARD_WHITE'],
                      font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=12, weight="bold")).pack(side="right")

        ctk.CTkButton(form_frame, text="LOG IN", command=self.attempt_login,
                      width=150, height=40, corner_radius=8,
                      font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=18, weight="bold"),
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
                     font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=34, weight="bold"),
                     text_color=COLORS['CARD_WHITE']).pack(pady=(120, 10))

        ctk.CTkLabel(design_content, text="Connectez-vous à votre espace RH",
                     font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=16),
                     text_color=COLORS['CARD_WHITE']).pack(pady=(0, 30))

        ctk.CTkButton(design_content, text="S'INSCRIRE", fg_color="transparent", border_width=2,
                      border_color=COLORS['CARD_WHITE'], hover_color="#3670B3",
                      width=100, height=35, corner_radius=8,
                      font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold")).pack()


    def attempt_login(self):
        """Fonction de connexion simulée (Frontend uniquement)."""
        username = self.username_entry.get().strip()
        # Simulation d'une connexion réussie pour lancer l'app principale
        if username in ["admin", "rakoto.jp", "rh"]:
            self.destroy()
            app = GestionCongeApp()
            app.mainloop()
        else:
            messagebox.showerror("Erreur de Connexion", "Identifiants invalides (Simulés). Veuillez réessayer.")
            self.password_entry.delete(0, 'end')

    def on_closing(self):
        self.destroy()


# =================================================================
# --- APPLICATION PRINCIPALE (Design) ---
# =================================================================

class GestionCongeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RH.App - Gestion des Congés (Design)")
        self.geometry("1200x750")
        self.configure(fg_color=COLORS['BG_LIGHT_GREY'])
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Détermination de la vue initiale (Simulée)
        initial_view = "validation" if CURRENT_MOCK_USER['role'] in ['admin', 'rh'] else "soldes"
        self.current_view = ctk.StringVar(value=initial_view)

        self.create_widgets()
        self.show_view(self.current_view.get())

    # --- Widgets et Navigation (Design) ---

    def create_widgets(self):
        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=15, fg_color=COLORS['CARD_WHITE'])
        self.sidebar_frame.grid(row=0, column=0, sticky="nswe", padx=15, pady=15)
        self.sidebar_frame.grid_rowconfigure(len(self.get_sidebar_items()) + 2, weight=1)
        self.create_sidebar_content(self.sidebar_frame)

        # Content Frame
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nswe", padx=(0, 15), pady=15)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

    def get_sidebar_items(self):
        items = [
            ("Compteur(s) / Soldes", "soldes", "📊"),
            ("Nouvelle demande", "nouvelle_demande", "➕"),
            ("Calendrier", "calendrier", "📅"),
        ]
        # Affichage conditionnel basé sur le rôle simulé
        if CURRENT_MOCK_USER['role'] in ['admin', 'rh']:
            items.extend([
                ("Validation (Admin)", "validation", "✅"),
                # NOUVELLE ENTREE POUR L'AJOUT DE PERSONNEL
                ("Ajout Personnel", "ajout_personnel", "🧑‍💼"),
                ("Planning (GANTT)", "planning", "🗓️"),
                ("Extractions / Suivi", "extractions", "📎")
            ])
        return items

    def create_sidebar_content(self, parent):
        for widget in parent.winfo_children(): widget.destroy()

        self.logo_label = ctk.CTkLabel(parent, text="🟦 RH.App",
                                       font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.user_label = ctk.CTkLabel(parent, text=f"👤 {CURRENT_MOCK_USER['nom_complet']} ({CURRENT_MOCK_USER['role'].upper()})",
                                       font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=12, weight="normal"),
                                       text_color=COLORS['TEXT_GREY'])
        self.user_label.grid(row=1, column=0, padx=20, pady=(0, 30), sticky="w")

        self.sidebar_buttons = {}

        items = self.get_sidebar_items()
        for i, (text, view_name, icon) in enumerate(items):
            btn = ctk.CTkButton(parent, text=f"{icon} {text}",
                                command=lambda name=view_name: self.show_view(name),
                                font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                                fg_color="transparent", text_color=COLORS['TEXT_DARK'],
                                hover_color=COLORS['BG_LIGHT_GREY'], anchor="w", corner_radius=8)
            btn.grid(row=i + 2, column=0, sticky="ew", padx=10, pady=4)
            self.sidebar_buttons[view_name] = btn

        if self.current_view.get() in self.sidebar_buttons:
            self.sidebar_buttons[self.current_view.get()].configure(fg_color=COLORS['PRIMARY_BLUE'],
                                                                    text_color=COLORS['CARD_WHITE'],
                                                                    hover_color=COLORS['PRIMARY_BLUE'])

        self.logout_button = ctk.CTkButton(parent, text="Déconnexion", command=self.logout,
                                           fg_color=COLORS['ACCENT_RED'], hover_color="#c83f3f", corner_radius=8,
                                           font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"))
        self.logout_button.grid(row=99, column=0, padx=20, pady=20, sticky="s")

    def logout(self):
        """Déconnexion simulée (ferme l'app et relance la page de connexion)."""
        self.destroy()
        # NOTE: Le relancement est géré dans le bloc 'if __name__ == "__main__":'

    def create_breadcrumb(self, current_view_name):
        view_text = next((item[0] for item in self.get_sidebar_items() if item[1] == current_view_name), current_view_name)
        ctk.CTkLabel(self.content_frame, text=f"RH.App > {view_text}",
                     font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=12, weight="normal"),
                     text_color=COLORS['TEXT_GREY']).pack(anchor="w", pady=(0, 15))

    def create_card_frame(self, parent, title_text, large_title=True):
        """Crée un conteneur 'carte' (fond blanc, coins arrondis) avec un titre."""
        card_frame = ctk.CTkFrame(parent, fg_color=COLORS['CARD_WHITE'], corner_radius=15, border_width=1,
                                  border_color=COLORS['BG_LIGHT_GREY'])
        font_size = 22 if large_title else 18
        ctk.CTkLabel(card_frame, text=title_text,
                     font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=font_size, weight="bold"),
                     text_color=COLORS['ACTIVE_SIDEBAR']).pack(anchor="w", padx=25, pady=(20, 10))

        content_inner_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        content_inner_frame.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        return card_frame, content_inner_frame

    def show_view(self, view_name):
        # 1. Nettoyer le contenu précédent
        for widget in self.content_frame.winfo_children(): widget.destroy()

        # 2. Mettre à jour les boutons de la barre latérale (Design)
        self.current_view.set(view_name)
        for name, button in self.sidebar_buttons.items():
            is_active = (name == view_name)
            button.configure(
                fg_color=COLORS['PRIMARY_BLUE'] if is_active else "transparent",
                text_color=COLORS['CARD_WHITE'] if is_active else COLORS['TEXT_DARK'],
                hover_color=COLORS['PRIMARY_BLUE'] if is_active else COLORS['BG_LIGHT_GREY']
            )

        # 3. Créer le fil d'Ariane
        self.create_breadcrumb(view_name)

        # 4. Afficher le contenu de la vue
        view_content_frame = ctk.CTkScrollableFrame(self.content_frame, fg_color="transparent", label_text=None)
        view_content_frame.pack(fill="both", expand=True)

        if view_name == "soldes":
            self.create_soldes_view(view_content_frame)
        elif view_name == "nouvelle_demande":
            self.create_nouvelle_demande_view(view_content_frame)
        elif view_name == "calendrier":
            self.create_calendrier_view(view_content_frame)
        elif view_name == "validation":
            self.create_validation_view(view_content_frame)
        # NOUVEL APPEL DE LA VUE AJOUT PERSONNEL
        elif view_name == "ajout_personnel":
            self.create_ajout_personnel_view(view_content_frame)
        elif view_name == "planning":
            self.create_planning_view(view_content_frame)
        elif view_name == "extractions":
            self.create_extractions_view(view_content_frame)
        else:
            ctk.CTkLabel(view_content_frame, text=f"Vue '{view_name}' non implémentée.",
                         font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=20)).pack(pady=50)

    # ----------------------------------------------------
    # --- LOGIQUE DE TABLEAU CTK (Design) ---
    # (Non modifiée)
    # ----------------------------------------------------

    def create_ctk_table_header(self, parent_frame, columns, widths, row_num):
        """Crée l'en-tête d'un tableau simulé avec CTkLabel."""
        parent_frame.columnconfigure(tuple(range(len(columns))), weight=1)
        for i, (text, width) in enumerate(zip(columns, widths)):
            header_label = ctk.CTkLabel(parent_frame, text=text,
                                        font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=12, weight="bold"),
                                        text_color=COLORS['ACTIVE_SIDEBAR'],
                                        fg_color=COLORS['HEADER_BG'], corner_radius=0)
            if width:
                parent_frame.grid_columnconfigure(i, weight=0, minsize=width)
            else:
                parent_frame.grid_columnconfigure(i, weight=1)
            header_label.grid(row=row_num, column=i, sticky="nsew", padx=(1 if i > 0 else 0, 1), pady=(0, 1))

    def add_ctk_table_row(self, parent_frame, row_data, row_num, column_configs):
        """Ajoute une ligne de données à un tableau simulé avec CTkLabel."""
        bg_color = COLORS['BG_LIGHT_GREY'] if row_num % 2 != 0 else COLORS['CARD_WHITE']
        text_color = COLORS['TEXT_DARK']

        for i, (value, config) in enumerate(zip(row_data, column_configs)):

            if config.get('style') == 'status':
                statut = value
                fg_color_map = {
                    'EN_ATTENTE': "#F59E0B", 'APPROUVE': COLORS['ACCENT_GREEN'],
                    'TERMINE': COLORS['TEXT_GREY'], 'REFUSE': COLORS['ACCENT_RED']
                }
                label_color = fg_color_map.get(statut, COLORS['TEXT_GREY'])

                status_label = ctk.CTkLabel(parent_frame, text=statut.replace('_', ' ').capitalize(),
                                            font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=10, weight='bold'),
                                            text_color=COLORS['CARD_WHITE'], fg_color=label_color, corner_radius=5)

                cell_frame = ctk.CTkFrame(parent_frame, fg_color=bg_color, corner_radius=0)
                cell_frame.grid(row=row_num, column=i, sticky="nsew", padx=(1 if i > 0 else 0, 1), pady=(0, 1))
                cell_frame.grid_rowconfigure(0, weight=1)
                cell_frame.grid_columnconfigure(0, weight=1)
                status_label.grid(row=0, column=0, padx=5, pady=2, sticky="")

            else:
                cell_label = ctk.CTkLabel(parent_frame, text=str(value),
                                          font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=13, weight="normal"),
                                          text_color=text_color, fg_color=bg_color,
                                          anchor=config.get('anchor', 'w'), justify=config.get('justify', 'left'))
                cell_label.grid(row=row_num, column=i, sticky="nsew", padx=(1 if i > 0 else 0, 1), pady=(0, 1))

    def populate_historique_table(self, table_frame, is_admin_view):
        """Remplit le tableau avec des données simulées."""
        columns = ["ID Dmd", "Type", "Début", "Fin", "Durée (j)", "Statut", "Acc. par", "Motif"]
        widths = [80, 150, 100, 100, 60, 100, 100, None]
        column_configs = [
            {'anchor': 'w', 'style': 'text'}, {'anchor': 'w', 'style': 'text'},
            {'anchor': 'center', 'style': 'text'}, {'anchor': 'center', 'style': 'text'},
            {'anchor': 'center', 'style': 'text'}, {'anchor': 'center', 'style': 'status'},
            {'anchor': 'w', 'style': 'text'}, {'anchor': 'w', 'style': 'text'}
        ]

        if is_admin_view:
            columns.insert(1, "Demandeur")
            widths.insert(1, 150)
            column_configs.insert(1, {'anchor': 'w', 'style': 'text'})

        self.create_ctk_table_header(table_frame, columns, widths, 0)

        for i, absence in enumerate(MOCK_ABSENCES):
            row_data = [
                absence['id'], MOCK_TYPES_ABSENCE.get(absence['type'], 'INCONNU'),
                absence['dateDebut'], absence['dateFin'], absence['duree'],
                absence['statut'], absence['accordePar'] if absence['accordePar'] != 'N/A' else '-',
                absence['motif'] if len(absence['motif']) < 30 else absence['motif'][:27] + '...'
            ]
            if is_admin_view:
                nom_prenom = f"{MOCK_PERSONNELS.get(absence['personnelId'], {}).get('nom', 'Inconnu')} {MOCK_PERSONNELS.get(absence['personnelId'], {}).get('prenoms', '')}"
                row_data.insert(1, nom_prenom)
            self.add_ctk_table_row(table_frame, row_data, i + 1, column_configs)

    # ----------------------------------------------------
    # --- VUE SOLDES ET HISTORIQUE (Design) ---
    # (Non modifiée)
    # ----------------------------------------------------

    def create_soldes_view(self, parent):
        soldes = MOCK_SOLDE_DATA # Données simulées

        solde_card, solde_content = self.create_card_frame(parent, "📊 Votre Solde de Congés Annuel (CA)")
        solde_card.pack(fill="x", padx=5, pady=10)
        solde_content.grid_columnconfigure((0, 1, 2), weight=1)

        def create_metric(parent, title, value, unit, color, row, col):
            metric_frame = ctk.CTkFrame(parent, fg_color=COLORS['BG_LIGHT_GREY'], corner_radius=10)
            metric_frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

            ctk.CTkLabel(metric_frame, text=title, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                         text_color=COLORS['TEXT_DARK']).pack(anchor="w", padx=15, pady=(10, 0))

            ctk.CTkLabel(metric_frame, text=f"{value} {unit}",
                         font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=32, weight="bold"),
                         text_color=color).pack(anchor="w", padx=15, pady=(0, 10))

        solde_restant_color = COLORS['ACCENT_GREEN'] if soldes['joursRestants'] >= 0 else COLORS['ACCENT_RED']
        create_metric(solde_content, f"Solde CA disponible (sur {soldes['joursTotal']} jours)", soldes['joursRestants'],
                      "jours", solde_restant_color, 0, 0)
        create_metric(solde_content, "En attente de validation", soldes['joursEnAttente'], "jours",
                      COLORS['PRIMARY_BLUE'], 0, 1)
        create_metric(solde_content, "Congés déjà validés/pris", soldes['joursValides'], "jours",
                      COLORS['TEXT_GREY'], 0, 2)

        historique_card, historique_content = self.create_card_frame(parent, "📜 Historique de vos demandes d'absence",
                                                                     large_title=False)
        historique_card.pack(fill="both", expand=True, padx=5, pady=10)
        table_frame = ctk.CTkFrame(historique_content, fg_color=COLORS['CARD_WHITE'], corner_radius=5, border_width=1,
                                   border_color=COLORS['BG_LIGHT_GREY'])
        table_frame.pack(fill="both", expand=True)

        self.populate_historique_table(table_frame, is_admin_view=False)

    # --- SÉLECTEUR DE DATE (Design) ---

    def open_date_selector(self, entry_widget):
        top = tk.Toplevel(self)
        top.title("Sélectionner une date")
        top.configure(bg=COLORS['CARD_WHITE'])
        top.transient(self)
        top.grab_set()

        def grab_date():
            selected_date = cal.get_date()
            try:
                # La date vient en jj/mm/aaaa, on la formate en AAAA-MM-JJ
                date_obj = datetime.strptime(selected_date, '%d/%m/%Y')
                formatted_date = date_obj.strftime("%Y-%m-%d")
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, formatted_date)
            except ValueError:
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, selected_date)
            top.destroy()

        cal = Calendar(top, selectmode='day',
                       year=datetime.now().year, month=datetime.now().month, day=datetime.now().day,
                       date_pattern='dd/mm/yyyy', locale='fr_FR', showmonth=True,
                       background=COLORS['PRIMARY_BLUE'], selectbackground=COLORS['PRIMARY_BLUE'],
                       headersbackground=COLORS['HEADER_BG'])
        cal.pack(padx=20, pady=20)
        ctk.CTkButton(top, text="Confirmer", command=grab_date,
                      fg_color=COLORS['PRIMARY_BLUE'], corner_radius=8).pack(pady=(0, 10))

    # ----------------------------------------------------
    # --- VUE NOUVELLE DEMANDE (Design & Simulation) ---
    # (Non modifiée)
    # ----------------------------------------------------

    def create_nouvelle_demande_view(self, parent):
        card_frame, form_frame = self.create_card_frame(parent, "➕ Formulaire de Nouvelle Demande d'Absence")
        card_frame.pack(fill="x", padx=5, pady=10)
        form_frame.grid_columnconfigure(1, weight=1)

        def create_form_row(text, widget, row):
            ctk.CTkLabel(form_frame, text=text, anchor="w",
                         font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                         text_color=COLORS['TEXT_BLACK']).grid(row=row, column=0, padx=10,
                                                               pady=(15 if row == 0 else 5, 5), sticky="w")
            widget.grid(row=row, column=1, padx=10, pady=(15 if row == 0 else 5, 5), sticky="ew")

        types_absence_display = list(MOCK_TYPES_ABSENCE.values())
        self.type_absence_var = ctk.StringVar(value=types_absence_display[0])
        type_absence_menu = ctk.CTkOptionMenu(form_frame, values=types_absence_display, variable=self.type_absence_var,
                                              corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        create_form_row("Type d'absence :", type_absence_menu, 0)

        self.date_debut_entry = ctk.CTkEntry(form_frame, placeholder_text=datetime.now().strftime("%Y-%m-%d"),
                                             corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        create_form_row("Date de début :", self.date_debut_entry, 1)
        ctk.CTkButton(form_frame, text="📅", width=30, fg_color=COLORS['ACCENT_GREEN'],
                      command=lambda: self.open_date_selector(self.date_debut_entry)).grid(row=1, column=2, padx=(0, 10), pady=5, sticky="e")

        self.date_fin_entry = ctk.CTkEntry(form_frame,
                                           placeholder_text=(datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
                                           corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        create_form_row("Date de fin :", self.date_fin_entry, 2)
        ctk.CTkButton(form_frame, text="📅", width=30, fg_color=COLORS['ACCENT_GREEN'],
                      command=lambda: self.open_date_selector(self.date_fin_entry)).grid(row=2, column=2, padx=(0, 10), pady=5, sticky="e")

        ctk.CTkLabel(form_frame, text="Motif de la demande (détails) :", anchor="w",
                     font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                     text_color=COLORS['TEXT_BLACK']).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.motif_textbox = ctk.CTkTextbox(form_frame, height=100, corner_radius=8,
                                            font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        self.motif_textbox.grid(row=3, column=1, padx=10, pady=5, sticky="ew", columnspan=2)

        ctk.CTkButton(form_frame, text="Soumettre la demande (Simulée)",
                      command=self.submit_absence_request_mock,
                      font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=16, weight="bold"),
                      fg_color=COLORS['PRIMARY_BLUE'], hover_color="#3670B3", corner_radius=8).grid(row=4, column=1,
                                                                                                    pady=(20, 10),
                                                                                                    sticky="e")

    def submit_absence_request_mock(self):
        """Simulation de la soumission de la demande."""
        # Dans un vrai frontend, ici on construirait un JSON/objet et on l'enverrait au backend via API/Socket.
        date_debut_str = self.date_debut_entry.get() if self.date_debut_entry.get() else 'N/A'
        date_fin_str = self.date_fin_entry.get() if self.date_fin_entry.get() else 'N/A'

        messagebox.showinfo("Simulation de Soumission",
                            f"Demande soumise:\nType: {self.type_absence_var.get()}\nPériode: {date_debut_str} à {date_fin_str}\n"
                            f"Statut: EN_ATTENTE (Simulé).")
        self.show_view("soldes")

    # ----------------------------------------------------
    # --- VUE AJOUT PERSONNEL (NOUVELLE SECTION) ---
    # ----------------------------------------------------

    def create_ajout_personnel_view(self, parent):
        card_frame, form_frame = self.create_card_frame(parent, "🧑‍💼 Ajouter un Nouveau Personnel (Fonctionnaire ou Contractuel)")
        card_frame.pack(fill="x", padx=5, pady=10)
        
        # Configuration des colonnes pour un formulaire en deux colonnes
        form_frame.grid_columnconfigure((0, 2), weight=0)
        form_frame.grid_columnconfigure((1, 3), weight=1)

        # Helper pour créer une ligne de formulaire (Label et Widget)
        def create_form_row(text, widget, row, col, columnspan=1):
            ctk.CTkLabel(form_frame, text=text, anchor="w",
                         font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                         text_color=COLORS['TEXT_BLACK']).grid(row=row, column=col, padx=10, pady=(15, 5), sticky="w")
            widget.grid(row=row, column=col + 1, padx=10, pady=(15, 5), sticky="ew", columnspan=columnspan)
        
        # Helper pour les champs de date avec bouton calendrier
        def create_date_input_group(parent_frame, placeholder):
            entry = ctk.CTkEntry(parent_frame, placeholder_text=placeholder, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
            
            frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
            frame.grid_columnconfigure(0, weight=1)
            
            entry.pack(side="left", fill="x", expand=True)
            ctk.CTkButton(frame, text="📅", width=30, fg_color=COLORS['ACCENT_GREEN'],
                          command=lambda e=entry: self.open_date_selector(e)).pack(side="right", padx=(5,0))
            return frame, entry

        # --- SECTION 1: Champs de Personnel (Base) ---
        row = 0
        
        self.entry_matricule = ctk.CTkEntry(form_frame, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        create_form_row("Numéro Matricule :", self.entry_matricule, row, 0)
        
        self.entry_nom = ctk.CTkEntry(form_frame, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        create_form_row("Nom :", self.entry_nom, row, 2)
        row += 1

        self.entry_prenom = ctk.CTkEntry(form_frame, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        create_form_row("Prénom :", self.entry_prenom, row, 0)
        
        self.entry_lieu_naissance = ctk.CTkEntry(form_frame, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        create_form_row("Lieu de Naissance :", self.entry_lieu_naissance, row, 2)
        row += 1

        # Date de Naissance
        date_naissance_frame, self.entry_date_naissance = create_date_input_group(form_frame, "AAAA-MM-JJ")
        create_form_row("Date de Naissance :", date_naissance_frame, row, 0)
        
        # Date d'Entrée
        date_entree_frame, self.entry_date_entree = create_date_input_group(form_frame, "AAAA-MM-JJ")
        create_form_row("Date d'Entrée :", date_entree_frame, row, 2)
        row += 1

        # Position (Combobox)
        positions = ["en activite", "en detachement", "hors cadre", "sous le drapeau", "en disponibilite"]
        self.var_position = ctk.StringVar(value=positions[0])
        self.combo_position = ctk.CTkComboBox(form_frame, values=positions, variable=self.var_position, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        create_form_row("Position :", self.combo_position, row, 0)
        
        # Type de Personnel (Combobox) - Déclencheur du contenu dynamique
        types = ["Fonctionnaire", "Agent Contractuel"]
        self.var_type_personnel = ctk.StringVar(value=types[0])
        self.combo_type_personnel = ctk.CTkComboBox(form_frame, values=types, variable=self.var_type_personnel, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14),
                                                    command=self.update_personnel_type_fields)
        create_form_row("Type de Personnel :", self.combo_type_personnel, row, 2)
        row += 1
        
        # --- SECTION 2: Champs optionnels de Personnel (Sortie) ---
        
        # Date de Sortie (Optionnel)
        date_sortie_frame, self.entry_date_sortie = create_date_input_group(form_frame, "AAAA-MM-JJ (Optionnel)")
        create_form_row("Date de Sortie :", date_sortie_frame, row, 0)
        
        # Objet de Départ (Optionnel)
        self.entry_objet_depart = ctk.CTkEntry(form_frame, placeholder_text="(Optionnel)", corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        create_form_row("Objet de Départ :", self.entry_objet_depart, row, 2)
        row += 1
        
        # --- SECTION 3: Cadre Dynamique pour les Champs Spécifiques ---
        self.dynamic_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        self.dynamic_frame.grid(row=row, column=0, columnspan=4, sticky="ew", pady=(20, 0))
        # Initial call to set up the default fields (Fonctionnaire)
        self.update_personnel_type_fields(self.var_type_personnel.get())
        row += 1

        # --- SECTION 4: Bouton de Soumission ---
        ctk.CTkButton(form_frame, text="Créer le Personnel (Simulé)",
                      command=self.submit_personnel_mock,
                      font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=16, weight="bold"),
                      fg_color=COLORS['PRIMARY_BLUE'], hover_color="#3670B3", corner_radius=8).grid(row=row, column=0,
                                                                                                    columnspan=4,
                                                                                                    pady=(30, 10),
                                                                                                    sticky="e")

    def update_personnel_type_fields(self, choice):
        """Met à jour les champs dynamiques basés sur le type de personnel sélectionné."""
        # Nettoyer les widgets précédents dans le cadre dynamique
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        # Configurer les colonnes pour le cadre dynamique
        self.dynamic_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Champ ID du Cadre (Commun aux deux, mais placé dans le cadre dynamique pour l'alignement)
        self.entry_id_cadre = ctk.CTkEntry(self.dynamic_frame, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        ctk.CTkLabel(self.dynamic_frame, text="ID du Cadre :", anchor="w",
                     font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                     text_color=COLORS['TEXT_BLACK']).grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.entry_id_cadre.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

        if choice == "Fonctionnaire":
            # Champ Diplôme
            self.entry_diplome = ctk.CTkEntry(self.dynamic_frame, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
            ctk.CTkLabel(self.dynamic_frame, text="Diplôme :", anchor="w",
                         font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                         text_color=COLORS['TEXT_BLACK']).grid(row=0, column=0, padx=10, pady=5, sticky="w")
            self.entry_diplome.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        elif choice == "Agent Contractuel":
            # Champ Statut
            status_values = ["EFA", "ELD", "ECD", "EMO", "ED"]
            self.var_status_contractuel = ctk.StringVar(value=status_values[0])
            self.combo_status_contractuel = ctk.CTkComboBox(self.dynamic_frame, values=status_values, variable=self.var_status_contractuel, corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
            
            ctk.CTkLabel(self.dynamic_frame, text="Statut Contractuel :", anchor="w",
                         font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                         text_color=COLORS['TEXT_BLACK']).grid(row=0, column=0, padx=10, pady=5, sticky="w")
            self.combo_status_contractuel.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    def submit_personnel_mock(self):
        """Simulation de la soumission du nouveau personnel."""
        
        # Récupération des données communes
        data = {
            'type_personnel': self.var_type_personnel.get(),
            'matricule': self.entry_matricule.get(),
            'nom': self.entry_nom.get(),
            'prenom': self.entry_prenom.get(),
            'date_naissance': self.entry_date_naissance.get() or 'NULL',
            'lieu_naissance': self.entry_lieu_naissance.get(),
            'date_entree': self.entry_date_entree.get() or 'NULL',
            'date_sortie': self.entry_date_sortie.get() or 'NULL',
            'objet_depart': self.entry_objet_depart.get() or 'NULL',
            'position': self.var_position.get(),
            'id_cadre': self.entry_id_cadre.get() or 'NULL',
        }
        
        # Ajout des données spécifiques
        if data['type_personnel'] == "Fonctionnaire":
            # On vérifie si l'attribut a été créé par update_personnel_type_fields
            data['diplome'] = getattr(self, 'entry_diplome', ctk.CTkEntry(self)).get() if hasattr(self, 'entry_diplome') else 'N/A'
        elif data['type_personnel'] == "Agent Contractuel":
            data['statut_contractuel'] = self.var_status_contractuel.get() if hasattr(self, 'var_status_contractuel') else 'N/A'
        
        # Validation de base (Matricule, Nom, Prénom, Date Entrée obligatoires)
        if not all(data.get(k) and data.get(k) != 'NULL' for k in ['matricule', 'nom', 'prenom', 'date_entree']):
            messagebox.showerror("Erreur de Saisie", "Veuillez remplir les champs obligatoires : Matricule, Nom, Prénom et Date d'Entrée.")
            return

        messagebox.showinfo("Simulation de Création",
                            f"Personnel créé (Simulé):\nType: {data['type_personnel']}\nNom: {data['nom']} {data['prenom']}\nMatricule: {data['matricule']}\n"
                            f"Données: {data}")
        # Redirection vers la vue de validation (ou soldes) après soumission
        self.show_view("validation")

    # ----------------------------------------------------
    # --- VUE VALIDATION (Design & Simulation) ---
    # (Non modifiée)
    # ----------------------------------------------------

    def create_validation_view(self, parent):
        card_frame, content_frame = self.create_card_frame(parent, "✅ Demandes d'Absence en Attente de Validation")
        card_frame.pack(fill="both", expand=True, padx=5, pady=10)

        # Utilisation des demandes EN_ATTENTE simulées
        self.demandes_en_attente = [a for a in MOCK_ABSENCES if a['statut'] == 'EN_ATTENTE']
        self.current_demande_index = 0

        if not self.demandes_en_attente:
            ctk.CTkLabel(content_frame, text="Aucune demande en attente de validation.",
                         font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=16, slant="italic"),
                         text_color=COLORS['TEXT_BLACK']).pack(pady=50)
            return

        self.detail_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.detail_frame.pack(fill="x", pady=10)
        self.action_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        self.action_frame.pack(fill="x", pady=15)

        self.show_current_demand_details(self.detail_frame, self.action_frame)

    def show_current_demand_details(self, detail_frame, action_frame):
        # Nettoyer les cadres
        for widget in detail_frame.winfo_children(): widget.destroy()
        for widget in action_frame.winfo_children(): widget.destroy()

        if self.current_demande_index >= len(self.demandes_en_attente):
            ctk.CTkLabel(detail_frame, text="Toutes les demandes ont été traitées (Simulé).",
                         font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=16, slant="italic"),
                         text_color=COLORS['TEXT_BLACK']).pack(pady=20)
            return

        demand = self.demandes_en_attente[self.current_demande_index]
        personnel = MOCK_PERSONNELS.get(demand['personnelId'], {})
        type_display = MOCK_TYPES_ABSENCE.get(demand['type'], 'INCONNU')

        ctk.CTkLabel(detail_frame,
                     text=f"Demande {self.current_demande_index + 1} sur {len(self.demandes_en_attente)} en attente de : {personnel.get('nom', 'Inconnu')} {personnel.get('prenoms', '')}",
                     font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=16, weight="bold")).pack(anchor="w", pady=(0, 10))

        detail_text = (
            f"👤 Demandeur: {personnel.get('nom', 'Inconnu')} {personnel.get('prenoms', '')} (Matricule: {personnel.get('numeroMatricule', 'N/A')})\n"
            f"📝 Type: {type_display} \n"
            f"📅 Période: Du {demand['dateDebut']} au {demand['dateFin']} ({demand['duree']} jours)\n"
            f"❓ Motif:\n{demand['motif']}"
        )
        details_textbox = ctk.CTkTextbox(detail_frame, height=180, corner_radius=8,
                                         font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14))
        details_textbox.insert("0.0", detail_text)
        details_textbox.configure(state="disabled")
        details_textbox.pack(fill="x", pady=5)

        ctk.CTkButton(action_frame, text="✅ Approuver (Simulé)", fg_color=COLORS['ACCENT_GREEN'], hover_color="#059669",
                      corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                      command=lambda: self.process_demand_mock(demand['id'], 'APPROUVE')).pack(side="left", padx=10)

        ctk.CTkButton(action_frame, text="❌ Refuser (Simulé)", fg_color=COLORS['ACCENT_RED'], hover_color="#c83f3f",
                      corner_radius=8, font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                      command=lambda: self.process_demand_mock(demand['id'], 'REFUSE')).pack(side="left", padx=10)

    def process_demand_mock(self, absence_id, status):
        """Simulation de la validation de la demande."""
        action = "approuvée" if status == 'APPROUVE' else "refusée"
        messagebox.showinfo("Action réussie (Simulée)", f"Demande {absence_id} a été {action} par (Admin Simulé).")

        self.current_demande_index += 1
        # On relance la vue pour rafraîchir et passer à la demande suivante
        self.show_view("validation")

    # ----------------------------------------------------
    # --- VUES SIMPLES (Design) ---
    # (Non modifiées)
    # ----------------------------------------------------

    def create_calendrier_view(self, parent):
        card_frame, content_frame = self.create_card_frame(parent, "📅 Mon Calendrier de Congés")
        card_frame.pack(fill="x", padx=5, pady=10)

        ctk.CTkLabel(content_frame,
                     text="Cette vue intègre un calendrier interactif affichant les congés validés et en attente.",
                     justify="left", font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14)).pack(anchor="w", padx=10,
                                                                                                 pady=10)

        calendar_frame = tk.Frame(content_frame, bg=COLORS['CARD_WHITE'])
        calendar_frame.pack(pady=20, padx=10, fill="x", expand=False)

        cal = Calendar(calendar_frame, selectmode='day', year=datetime.now().year,
                       month=datetime.now().month, day=datetime.now().day,
                       date_pattern='dd/mm/yyyy', locale='fr_FR',
                       background=COLORS['PRIMARY_BLUE'], selectbackground=COLORS['PRIMARY_BLUE'])
        cal.pack(padx=20, pady=20)

    def create_planning_view(self, parent):
        card_frame, content_frame = self.create_card_frame(parent, "🗓️ Planning Global des Absences (Gantt Simulé)")
        card_frame.pack(fill="both", expand=True, padx=5, pady=10)

        ctk.CTkLabel(content_frame,
                     text="Cette vue afficherait un **diagramme de Gantt** simulé pour l'ensemble du personnel.",
                     justify="left", font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14)).pack(anchor="w", padx=10, pady=10)

        ctk.CTkLabel(content_frame, text="Fonctionnalité en cours de développement (Design Only)...",
                     font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=16, slant="italic"),
                     text_color=COLORS['TEXT_GREY']).pack(pady=50)

    def create_extractions_view(self, parent):
        card_frame, options_frame = self.create_card_frame(parent, "📎 Extractions / Suivi RH")
        card_frame.pack(fill="x", padx=5, pady=10)

        ctk.CTkLabel(options_frame, text="Sélectionner la période d'export :", anchor="w",
                     font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, weight="bold", size=14)).pack(padx=10, pady=(15, 5), anchor="w")

        ctk.CTkOptionMenu(options_frame, values=["Année 2024", "Mois dernier", "Personnalisé"], corner_radius=8,
                          font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14)).pack(padx=10, pady=5, anchor="w")

        ctk.CTkButton(options_frame, text="Exporter au format CSV (Simulé)", fg_color=COLORS['ACCENT_GREEN'],
                      hover_color="#059669", corner_radius=8,
                      font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"),
                      command=lambda: messagebox.showinfo("Export Simulation",
                                                          "Données exportées (Simulé).\nLe backend aurait généré le fichier.")).pack(padx=10, pady=(20, 15), anchor="w")


# =================================================================
# --- POINT D'ENTRÉE ---
# =================================================================

if __name__ == "__main__":
    # La gestion du backend est omise. On lance directement l'interface.
    # Pour simuler la persistance, le mainloop sera relancé après déconnexion.
    while True:
        login_app = LoginPage()
        login_app.mainloop()

        # Si LoginPage est détruit (par une connexion réussie ou fermeture), on vérifie si l'app principale doit être lancée.
        # Dans ce code frontend pur, on considère que si LoginPage se ferme, c'est pour lancer GestionCongeApp.
        # Si on revient à ce point après GestionCongeApp.logout(), on relance LoginPage.
        if not login_app.winfo_exists():
            # Si l'application principale a été lancée et fermée (via logout), on boucle pour relancer la connexion.
            # Si le script est terminé, la boucle s'arrête.
            pass
        else:
            break