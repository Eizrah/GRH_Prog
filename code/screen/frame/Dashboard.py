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
    def __init__(self, master, personnel_data, stats=None, **kwargs):
        if 'fg_color' not in kwargs:
            kwargs['fg_color'] = COLORS['BG_LIGHT_GREY']
        super().__init__(master, **kwargs)
        self.grid_columnconfigure((0, 1, 2), weight=1, uniform="bilan_cols")
        
        # Stats par défaut si non fournies
        if not stats:
            stats = {"total": 0, "accepted": 0, "pending": 0}

        self.create_card(0, "📄 Demandes Totales", str(stats['total']), COLORS['PRIMARY_BLUE'])
        self.create_card(1, "✅ Congés Approuvés", str(stats['accepted']), COLORS['ACCENT_GREEN'])
        self.create_card(2, "⏳ Congés en Attente", str(stats['pending']), COLORS['ACCENT_RED'])
        
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
        
        # Récupération des stats réelles
        stats = self.fetch_stats()

        title_label = ctk.CTkLabel(self, text="Tableau de bord", text_color=COLORS['TEXT_DARK'], anchor="w",
                                font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=25, pady=(20, 5), sticky="w")
        
        # Bouton Actualiser
        refresh_btn = ctk.CTkButton(self, text="Actualiser", width=100, command=self.refresh_dashboard, fg_color=COLORS['PRIMARY_BLUE'])
        refresh_btn.grid(row=0, column=0, padx=25, pady=(20, 5), sticky="e")

        self.bilan_frame = Bilan(self, all_data, stats)
        self.bilan_frame.grid(row=1, column=0, padx=20, pady=0, sticky="new")
        
        self.tab_fonc = TableauDashboard(self, self.fonc_data, title="📋 Liste des Fonctionnaires")
        self.tab_fonc.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="nsew")

        self.tab_agent = TableauDashboard(self, self.agent_data, title="📋 Liste des Agents Contractuels")
        self.tab_agent.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="nsew")

    def refresh_dashboard(self):
        """Recharge toutes les données du dashboard"""
        self.fonc_data, self.agent_data = self.fetch_data()
        all_data = self.fonc_data + self.agent_data
        stats = self.fetch_stats()
        
        # Update Bilan
        # On recrée le bilan car c'est plus simple (ou on ajoute update_stats à Bilan)
        self.bilan_frame.destroy()
        self.bilan_frame = Bilan(self, all_data, stats)
        self.bilan_frame.grid(row=1, column=0, padx=20, pady=0, sticky="new")
        
        # Update Tables
        self.tab_fonc.update_data(self.fonc_data)
        self.tab_agent.update_data(self.agent_data)

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

    def fetch_stats(self):
        """Récupère les statistiques des demandes de congé"""
        try:
            db_path = os.path.join(project_root, 'database', 'db.sqlite3')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Compte pour chaque table
            tables = ['Conge', 'Permission', 'Autorisation']
            
            pending = 0
            accepted = 0
            
            for table in tables:
                # En Attente
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE validation = 'En Attente'")
                pending += cursor.fetchone()[0]
                
                # Accepté
                cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE validation = 'Accepté'")
                accepted += cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "total": pending + accepted, # Ou Count total rows si on veut aussi refusés
                "pending": pending,
                "accepted": accepted
            }
            
        except Exception as e:
            print(f"Erreur Fetch Stats: {e}")
            return {"total": 0, "pending": 0, "accepted": 0}

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

        self.setup_table()

    def update_data(self, new_data):
        self.data = new_data
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
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
            
            # Actions Frame
            action_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
            action_frame.grid(row=row, column=7, sticky="w", padx=5)
            
            # Bouton Modifier avec icône plus visible
            ctk.CTkButton(action_frame, text="✎ EDIT", width=50, fg_color=COLORS['PRIMARY_BLUE'],
                          hover_color="#3670B3",
                          font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=10, weight="bold"),
                          command=lambda m=record["matricule"]: self.edit_personnel(m)).pack(side="left", padx=2)
            
            # Bouton Supprimer avec icône plus visible
            ctk.CTkButton(action_frame, text="✖ DEL", width=50, fg_color=COLORS['ACCENT_RED'],
                          hover_color="#DC2626",
                          font=ctk.CTkFont(family=DEFAULT_FONT_FAMILY, size=10, weight="bold"),
                          command=lambda m=record["matricule"]: self.delete_personnel(m)).pack(side="left", padx=2)

    def edit_personnel(self, matricule):
        """Ouvre une boite de dialogue pour modifier le personnel"""
        try:
            # Création fenêtre modale
            win = ctk.CTkToplevel(self)
            win.title(f"Modifier Personnel - {matricule}")
            win.geometry("1000x800")
            win.grab_set() # Modale
            
            # Import différé pour éviter import circulaire
            from .AddPers import AjoutPersonnelView
            
            # Fonction de callback pour rafraichir le dashboard après modif
            def on_refresh():
                if hasattr(self.master, 'refresh_dashboard'):
                    self.master.refresh_dashboard()
            
            # Instantiation de la vue dans la fenêtre
            view = AjoutPersonnelView(
                win, 
                controller=self.master.controller if hasattr(self.master, 'controller') else None,
                close_callback=win.destroy,
                refresh_callback=on_refresh
            )
            view.pack(fill="both", expand=True)
            
            # Initialisation en mode édition
            view.on_show(edit_matricule=matricule)
            
        except ImportError:
            print("Erreur import AjoutPersonnelView")
        except Exception as e:
            print(f"Erreur ouverture dialog: {e}")

    def delete_personnel(self, matricule):
        """Supprime le personnel après confirmation"""
        from tkinter import messagebox
        if not messagebox.askyesno("Confirmer", f"Voulez-vous vraiment supprimer le personnel {matricule} ?"):
            return
            
        try:
             # Import local pour accès DB
            db_path = os.path.join(project_root, 'database', 'db.sqlite3')
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Essayer Fonctionnaire
            cursor.execute("DELETE FROM Fonctionnaire WHERE num_matricule = ?", (matricule,))
            cnt = cursor.rowcount
            if cnt == 0:
                cursor.execute("DELETE FROM AgentContractuel WHERE num_matricule = ?", (matricule,))
                cnt = cursor.rowcount
                
            conn.commit()
            conn.close()
            
            if cnt > 0:
                messagebox.showinfo("Succès", "Personnel supprimé.")
                # Refresh dashboard if possible
                if hasattr(self.master, 'fetch_data'):
                     # Re-fetch and update UI (Simplifié: on pourrait recharger toute la vue)
                     # Le plus simple est de rappeler __init__ ou une méthode refresh_view sur DashboardView
                     # Mais ici on est dans TableauDashboard. On peut demander au master.
                     
                     # Mais ici on est dans TableauDashboard. On peut demander au master.
                     if hasattr(self.master, 'refresh_dashboard'):
                        self.master.refresh_dashboard()
                     pass  
            else:
                messagebox.showwarning("Info", "Aucun enregistrement trouvé à supprimer.")
                
        except Exception as e:
            print(f"Erreur delete: {e}")
            messagebox.showerror("Erreur", f"Erreur lors de la suppression: {e}")