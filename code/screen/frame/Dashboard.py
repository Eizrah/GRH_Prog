import customtkinter as ctk
import sqlite3
import sys
import os
import re

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(parent_dir)
sys.path.append(project_root)

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


class Bilan(ctk.CTkFrame):
    def __init__(self, master, personnel_data, **kwargs):
        if 'fg_color' not in kwargs:
            kwargs['fg_color'] = COLORS['BG_LIGHT_GREY']
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="bilan_cols")
        
        total_personnel = len(personnel_data)
        conges_approuves = 15  # Simulé
        conges_en_attente = 3  # Simulé

        self.create_card(0, "👤 Personnel Total", str(total_personnel), COLORS['PRIMARY_BLUE'])
        self.create_card(1, "✅ Congés Approuvés", str(conges_approuves), COLORS['ACCENT_GREEN'])
        self.create_card(2, "⏳ Congés en Attente", str(conges_en_attente), COLORS['ACCENT_RED'])
        
    def create_card(self, column, title, value, color):
        card = ctk.CTkFrame(self, fg_color=COLORS['CARD_WHITE'], corner_radius=12, height=120)
        card.grid(row=0, column=column, padx=(10, 0) if column > 0 else 0, pady=15, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(card, text=title, text_color=COLORS['TEXT_GREY'], anchor="w",
                                    font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"))
        title_label.grid(row=0, column=0, padx=15, pady=(15, 0), sticky="w")
        
        value_label = ctk.CTkLabel(card, text=value, text_color=color, anchor="w",
                                    font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=36, weight="bold"))
        value_label.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="w")


class DashboardView(ctk.CTkFrame):
    def __init__(self, master=None, controller=None, **kwargs):
        super().__init__(master, fg_color=COLORS['BG_LIGHT_GREY'], **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)  # Bilan
        self.grid_rowconfigure(2, weight=1)  # Tab Fonctionnaire
        self.grid_rowconfigure(3, weight=1)  # Tab Agent
        
        self.fonc_data, self.agent_data = self.fetch_data()
        all_data = self.fonc_data + self.agent_data

        title_label = ctk.CTkLabel(self, text="Tableau de bord", text_color=COLORS['TEXT_DARK'], anchor="w",
                                font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=25, pady=(20, 5), sticky="w")

        self.bilan_frame = Bilan(self, all_data)
        self.bilan_frame.grid(row=1, column=0, padx=20, pady=0, sticky="new")
        
        self.tab_fonc = TableauDashboard(self, self.fonc_data, title="📋 Liste des Fonctionnaires")
        self.tab_fonc.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="nsew")

        self.tab_agent = TableauDashboard(self, self.agent_data, title="📋 Liste des Agents Contractuels")
        self.tab_agent.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")

    def fetch_data(self):
        try:
            db_path = os.path.join(project_root, 'database', 'db.sqlite3')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Fonctionnaires
            cursor.execute('''
                SELECT f.num_matricule, f.nom, f.prenom, f.position, 
                       g.classe, c.echelle, c.classe_corp
                FROM Fonctionnaire f
                LEFT JOIN Change_grade cg ON f.id_fonc = cg.id_fonc
                LEFT JOIN Grade g ON cg.id_grade = g.id_grade
                LEFT JOIN Cadre c ON f.id_cadre = c.id_cadre
            ''')
            rows_fonc = cursor.fetchall()
            fonc_list = []
            for r in rows_fonc:
                fonc_list.append({
                    "matricule": r[0] if r[0] else "-",
                    "nom": r[1] if r[1] else "-",
                    "prenom": r[2] if r[2] else "-",
                    "type": "Fonctionnaire",
                    "classe": r[4] if r[4] else "-",
                    "echelle": r[5] if r[5] else "-",
                    "corps": r[6] if r[6] else "-",
                    "statut": r[3] if r[3] else "-"
                })

            # Agents Contractuels
            cursor.execute('''
                SELECT a.num_matricule, a.nom, a.prenom, a.position, a.satut,
                       g.classe, c.echelle, c.classe_corp
                FROM AgentContractuel a
                LEFT JOIN Change_grade cg ON a.id_ag = cg.id_ag
                LEFT JOIN Grade g ON cg.id_grade = g.id_grade
                LEFT JOIN Cadre c ON a.id_cadre = c.id_cadre
            ''')
            rows_agent = cursor.fetchall()
            agent_list = []
            for r in rows_agent:
                full_statut = r[4] if r[4] else ""
                match = re.search(r'\((.*?)\)', full_statut)
                short_type = match.group(1) if match else "Agent"
                
                agent_list.append({
                    "matricule": r[0] if r[0] else "-",
                    "nom": r[1] if r[1] else "-",
                    "prenom": r[2] if r[2] else "-",
                    "type": short_type,
                    "classe": r[5] if r[5] else "-",
                    "echelle": r[6] if r[6] else "-",
                    "corps": r[7] if r[7] else "-",
                    "statut": r[3] if r[3] else "-"
                })
                
            conn.close()
            return fonc_list, agent_list
            
        except Exception as e:
            print(f"Erreur Fetch Data: {e}")
            return [], []

    def set_controller(self, controller):
        self.controller = controller


class TableauDashboard(ctk.CTkFrame):
    def __init__(self, master, personnel_data, title="Liste du Personnel", **kwargs):
        if 'fg_color' not in kwargs:
            kwargs['fg_color'] = COLORS['CARD_WHITE']
        if 'corner_radius' not in kwargs:
            kwargs['corner_radius'] = 15
            
        super().__init__(master, **kwargs)
        self.data = personnel_data
        self.grid_columnconfigure(0, weight=1)

        table_title = ctk.CTkLabel(self, text=title, text_color=COLORS['TEXT_DARK'], anchor="w",
                                    font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=18, weight="bold"))
        table_title.pack(fill="x", padx=20, pady=(15, 5))

        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0, height=200)
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.scroll_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)
        
        self.setup_table()

    def setup_table(self):
        headers = ("Matricule", "Nom", "Type", "Classe", "Échelle", "Corps", "Statut", "Action")
        col_weights = [1, 3, 1, 1, 1, 1, 2, 2] 
        
        for i, header_text in enumerate(headers):
            self.scroll_frame.grid_columnconfigure(i, weight=col_weights[i])
            header = ctk.CTkLabel(self.scroll_frame, text=header_text, 
                                fg_color=COLORS['HEADER_BG'], corner_radius=8,
                                text_color=COLORS['TEXT_DARK'], 
                                font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=14, weight="bold"))
            header.grid(row=0, column=i, sticky="nsew", padx=(5, 0) if i > 0 else 0, pady=5)

        for row_index, record in enumerate(self.data):
            row = row_index + 1
            bg_color = COLORS['BG_LIGHT_GREY'] if row_index % 2 == 1 else COLORS['CARD_WHITE']
            text_color = COLORS['TEXT_DARK']

            ctk.CTkLabel(self.scroll_frame, text=record["matricule"], text_color=text_color, fg_color=bg_color, anchor="w").grid(row=row, column=0, sticky="nsew", padx=(5,0))
            
            name_label = ctk.CTkLabel(self.scroll_frame, text=f"{record['nom'].upper()} {record['prenom']}", text_color=text_color, fg_color=bg_color, anchor="w", font=ctk.CTkFont(weight="bold"))
            name_label.grid(row=row, column=1, sticky="nsew", padx=(5,0))
            
            ctk.CTkLabel(self.scroll_frame, text=record["type"], text_color=text_color, fg_color=bg_color, anchor="w").grid(row=row, column=2, sticky="nsew", padx=(5,0))
            
            ctk.CTkLabel(self.scroll_frame, text=record["classe"], text_color=text_color, fg_color=bg_color, anchor="w").grid(row=row, column=3, sticky="nsew", padx=(5,0))
            
            ctk.CTkLabel(self.scroll_frame, text=record["echelle"], text_color=text_color, fg_color=bg_color, anchor="w").grid(row=row, column=4, sticky="nsew", padx=(5,0))
            
            ctk.CTkLabel(self.scroll_frame, text=record["corps"], text_color=text_color, fg_color=bg_color, anchor="w").grid(row=row, column=5, sticky="nsew", padx=(5,0))
            
            statut = record["statut"]
            color = COLORS['ACCENT_GREEN'] if statut in ("En activité", "Sous le drapeau") else COLORS['ACCENT_RED']
            ctk.CTkLabel(self.scroll_frame, text=statut, text_color=color, fg_color=bg_color, anchor="w", font=ctk.CTkFont(weight="bold")).grid(row=row, column=6, sticky="nsew", padx=(5,0))
            
            ctk.CTkButton(self.scroll_frame, text="✏️", width=30, fg_color=COLORS['PRIMARY_BLUE']).grid(row=row, column=7, sticky="w", padx=5)