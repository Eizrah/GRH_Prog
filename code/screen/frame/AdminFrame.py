import customtkinter
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime
from logic.gestion_solde import obtenir_solde_reel

class AdminFrame(customtkinter.CTkFrame):
    def __init__(self, master, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.controller = controller
        # Dictionnaire pour stocker les infos complètes par id_pc
        self.requests_data = {} 
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Titre Global
        customtkinter.CTkLabel(
            self, 
            text="Gestion des Demandes de Congé",
            font=customtkinter.CTkFont(size=20, weight="bold")
        ).pack(pady=(10, 5))

        # Container principal
        self.main_container = customtkinter.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- PARTIE 1: TABLEAU FONCTIONNAIRES ---
        self.frame_fonc = customtkinter.CTkFrame(self.main_container)
        self.frame_fonc.pack(fill="both", expand=True, pady=(0, 10))
        
        customtkinter.CTkLabel(self.frame_fonc, text="Requêtes Fonctionnaires", 
                               font=customtkinter.CTkFont(size=18, weight="bold")).pack(pady=5)
                               
        self.tree_fonc = self.create_treeview(self.frame_fonc)
        self.tree_fonc.bind("<<TreeviewSelect>>", lambda e: self.on_select(e, "fonc"))
        
        # --- PARTIE 2: TABLEAU AGENTS CONTRACTUELS ---
        self.frame_agent = customtkinter.CTkFrame(self.main_container)
        self.frame_agent.pack(fill="both", expand=True, pady=(10, 0))
        
        customtkinter.CTkLabel(self.frame_agent, text="Requêtes Agents Contractuels", 
                               font=customtkinter.CTkFont(size=18, weight="bold")).pack(pady=5)
                               
        self.tree_agent = self.create_treeview(self.frame_agent)
        self.tree_agent.bind("<<TreeviewSelect>>", lambda e: self.on_select(e, "agent"))

        # Bouton Actualiser Global
        customtkinter.CTkButton(self, text="Actualiser Tout", command=self.refresh_table).pack(pady=10)
        
        # Initialisation
        self.refresh_table()

    def create_treeview(self, parent):
        # Frame pour Treeview + Scrollbars
        container = customtkinter.CTkFrame(parent, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("matricule", "nom_prenom", "type", "dates", "conge_restant", "action")
        headers = ["Matricule", "Nom & Prénom", "Type Demande", "Dates", "Solde Actuel", "Action"]
        widths = [100, 150, 150, 180, 100, 100]
        
        tree = ttk.Treeview(container, columns=columns, show="headings", selectmode="browse", height=6)
        
        for col, h, w in zip(columns, headers, widths):
            tree.heading(col, text=h)
            tree.column(col, width=w, anchor="center")
            
        # Scrollbars
        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        tree.pack(side="left", fill="both", expand=True)
        
        return tree

    def refresh_table(self):
        """Récupère les données et les sépare dans les deux tableaux"""
        
        # Import local pour conge_cumule pour éviter les soucis de path au top-level si possible
        try:
            from logic.conge_cumule import calculer_conge_cumule
        except ImportError:
            # Fallback si le path n'est pas encore bon (ex: run direct)
            import sys
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            project_root = os.path.dirname(parent_dir)
            sys.path.append(os.path.join(project_root, 'code'))
            from logic.conge_cumule import calculer_conge_cumule

        # Vider les tableaux
        for item in self.tree_fonc.get_children(): self.tree_fonc.delete(item)
        for item in self.tree_agent.get_children(): self.tree_agent.delete(item)
        self.requests_data.clear()
        
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            project_root = os.path.dirname(parent_dir)
            db_path = os.path.join(project_root, 'database', 'db.sqlite3')
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Fetch PersoConge
            cursor.execute("SELECT id_pc, date_depart, date_fin, id_conge, id_permission, id_aut, id_fonc, id_ag FROM PersoConge")
            rows = cursor.fetchall()
            
            for row in rows:
                id_pc, d_dep_str, d_fin_str, id_c, id_p, id_a, id_f, id_ag = row
                
                # --- 1. Identifier la Personne et Date Entrée ---
                person_type = None 
                person_info = {}
                person_id = None
                date_entree_str = None
                
                # Check Fonctionnaire
                cursor.execute("SELECT num_matricule, nom, prenom, date_entre FROM Fonctionnaire WHERE id_fonc = ?", (id_f,))
                res_f = cursor.fetchone()
                if res_f:
                    person_type = "fonc"
                    person_id = id_f
                    person_info = {"matricule": res_f[0], "nom": res_f[1], "prenom": res_f[2]}
                    date_entree_str = res_f[3]
                else:
                    # Check Agent
                    cursor.execute("SELECT num_matricule, nom, prenom, date_entre FROM AgentContractuel WHERE id_ag = ?", (id_ag,))
                    res_ag = cursor.fetchone()
                    if res_ag:
                        person_type = "agent"
                        person_id = id_ag
                        person_info = {"matricule": res_ag[0], "nom": res_ag[1], "prenom": res_ag[2]}
                        date_entree_str = res_ag[3]
                
                if not person_type: continue 
                
                # --- 2. Identifier la Demande & Motif ---
                req_type = "Inconnu"
                req_detail = "" 
                validation = "Inconnu"
                
                # Conge
                cursor.execute("SELECT type, duree, validation FROM Conge WHERE id_conge = ?", (id_c,))
                res_c = cursor.fetchone()
                if res_c:
                    req_type = "Congé"
                    req_detail = res_c[0] 
                    validation = res_c[2]
                else:
                    # Permission
                    cursor.execute("SELECT motif, duree, validation FROM Permission WHERE id_permission = ?", (id_p,))
                    res_p = cursor.fetchone()
                    if res_p:
                        req_type = "Permission d'absence"
                        req_detail = res_p[0]  # Le motif
                        validation = res_p[2]
                    else:
                        # Autorisation
                        cursor.execute("SELECT type, duree, validation, motif FROM Autorisation WHERE id_aut = ?", (id_a,))
                        res_a = cursor.fetchone()
                        if res_a:
                            req_type = res_a[0]  # Type exact de l'autorisation
                            req_detail = res_a[3] if res_a[3] else "-"  # Le motif
                            validation = res_a[2]

                # --- 3. Récupérer Détails Avancés (Poste, Grade, Solde) ---
                
                # Calcul Solde
                solde = "N/A"
                if date_entree_str: # On a besoin de la date d'entrée et de l'ID
                    try:
                        # Parsing de la date d'entrée
                        d_entree = None
                        for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                            try:
                                d_entree = datetime.strptime(date_entree_str, fmt).date()
                                break
                            except ValueError: pass
                        
                        if d_entree:
                            # Appel de la fonction qui fait (Acquis - Consommé)
                            # person_id a été défini plus haut dans votre code (id_f ou id_ag)
                            # person_type a été défini plus haut ("fonc" ou "agent")
                            val_solde = obtenir_solde_reel(person_id, person_type, d_entree)
                            
                            solde = f"{val_solde} jours"
                            
                    except Exception as e:
                        print(f"Erreur calcul solde: {e}")
                
                # Poste 
                
                # Poste (via Affectation -> id_emploi -> Emplois.nom_poste)
                nom_poste = "Non défini"
                if person_type == "fonc":
                    cursor.execute("SELECT id_emploi FROM Affectation WHERE id_fonc = ?", (person_id,))
                else:
                    cursor.execute("SELECT id_emploi FROM Affectation WHERE id_ag = ?", (person_id,))
                res_aff = cursor.fetchone()
                if res_aff:
                    cursor.execute("SELECT nom_poste FROM Emplois WHERE id_emploi = ?", (res_aff[0],))
                    res_emp = cursor.fetchone()
                    if res_emp: nom_poste = res_emp[0]
                
                # Grade/Classe (via Change_grade -> Grade)
                classe = "Non défini"
                echelon = "Non défini"
                if person_type == "fonc":
                    cursor.execute("SELECT id_grade FROM Change_grade WHERE id_fonc = ?", (person_id,))
                else:
                     cursor.execute("SELECT id_grade FROM Change_grade WHERE id_ag = ?", (person_id,))
                res_cg = cursor.fetchone() 
                if res_cg:
                    cursor.execute("SELECT classe, echelon FROM Grade WHERE id_grade = ?", (res_cg[0],))
                    res_gr = cursor.fetchone()
                    if res_gr:
                        classe = res_gr[0]
                        echelon = res_gr[1]

                # --- 4. Stocker et Afficher ---
                full_data = {
                    "id_pc": id_pc,
                    "person_type": person_type,
                    "matricule": person_info['matricule'],
                    "nom_prenom": f"{person_info['nom']} {person_info['prenom']}",
                    "poste": nom_poste,
                    "classe": classe,
                    "echelon": echelon,
                    "solde": solde,
                    "req_type": req_type,
                    "req_detail": req_detail, # Nom conge ou Motif
                    "validation": validation,
                    "dates": f"{d_dep_str} à {d_fin_str}",
                    "id_conge": id_c if req_type == "Congé" else (id_p if req_type=="Permission" else id_a)
                }
                
                self.requests_data[id_pc] = full_data
                
                # Affichage
                vals = (person_info['matricule'], f"{person_info['nom']} {person_info['prenom']}", 
                        req_type, f"{d_dep_str} au {d_fin_str}", solde, "Voir Détails")
                
                # Tags pour couleur
                tag = "pending"
                if validation == "Accepté": tag = "accepted"
                elif validation == "Refusé": tag = "rejected"

                if person_type == "fonc":
                    self.tree_fonc.insert("", "end", iid=id_pc, values=vals, tags=(tag,))
                else:
                    self.tree_agent.insert("", "end", iid=id_pc, values=vals, tags=(tag,))
            
            # Couleurs
            for tree in [self.tree_fonc, self.tree_agent]:
                tree.tag_configure("accepted", background="#d1fae5", foreground="black")
                tree.tag_configure("rejected", background="#fee2e2", foreground="black")
                tree.tag_configure("pending", background="#2a2d2e", foreground="white")

            conn.close()
            
        except Exception as e:
            print(f"Erreur refresh: {e}")

    def on_select(self, event, tree_type):
        tree = self.tree_fonc if tree_type == "fonc" else self.tree_agent
        sel = tree.selection()
        if sel:
            item_id = sel[0]
            self.show_detail_dialog(item_id)
            try:
                tree.selection_remove(item_id)
            except: pass

    def show_detail_dialog(self, item_id):
        if item_id not in self.requests_data: return
        data = self.requests_data[item_id]
        
        dialog = customtkinter.CTkToplevel(self)
        dialog.title(f"Détails - {data['nom_prenom']}")
        dialog.geometry("500x600")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # --- Contenu non-éditable ---
        padding = {'padx': 20, 'pady': 5}
        
        ctk = customtkinter
        font_lbl = ctk.CTkFont(size=14, weight="bold")
        font_val = ctk.CTkFont(size=14)
        
        def add_info(label, value):
            row = ctk.CTkFrame(dialog, fg_color="transparent")
            row.pack(fill="x", **padding)
            ctk.CTkLabel(row, text=label, font=font_lbl, width=150, anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=str(value), font=font_val, anchor="w").pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(dialog, text="INFORMATIONS PERSONNEL", font=ctk.CTkFont(size=16, weight="bold", underline=True)).pack(pady=10)
        
        add_info("Matricule:", data['matricule'])
        add_info("Nom & Prénom:", data['nom_prenom'])
        add_info("Emploi:", data['poste'])
        add_info("Classe:", data['classe'])
        add_info("Echelon:", data['echelon'])
        add_info("Solde Congé:", data['solde'])
        
        ctk.CTkLabel(dialog, text="DÉTAILS DEMANDE", font=ctk.CTkFont(size=16, weight="bold", underline=True)).pack(pady=10)
        
        add_info("Type:", data['req_type'])
        add_info("Détail/Motif:", data['req_detail'])
        add_info("Dates:", data['dates'])
        add_info("Statut Actuel:", data['validation'])
        
        # --- Boutons Actions ---
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        if data['validation'] == "En Attente":
            ctk.CTkButton(btn_frame, text="ACCEPTER", fg_color="green", 
                          command=lambda: self.process_action(item_id, "Accepté", dialog)).pack(side="left", padx=10)
            
            ctk.CTkButton(btn_frame, text="REFUSER", fg_color="red", 
                          command=lambda: self.process_action(item_id, "Refusé", dialog)).pack(side="left", padx=10)
        
        ctk.CTkButton(btn_frame, text="Fermer", fg_color="gray", command=dialog.destroy).pack(side="left", padx=10)

    def process_action(self, item_id, decision, window):
        """Met à jour la validation dans la DB et ajuste le solde"""
        data = self.requests_data[item_id]
        import sqlite3
        
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            project_root = os.path.dirname(parent_dir)
            db_path = os.path.join(project_root, 'database', 'db.sqlite3')
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # 1. Mettre à jour la validation
            target_id = data['id_conge']
            updated = False
            
            # On essaye Conge
            cursor.execute("UPDATE Conge SET validation = ? WHERE id_conge = ?", (decision, target_id))
            if cursor.rowcount > 0: 
                updated = True
            
            if not updated:
                cursor.execute("UPDATE Permission SET validation = ? WHERE id_permission = ?", (decision, target_id))
                if cursor.rowcount > 0: 
                    updated = True
                
            if not updated:
                cursor.execute("UPDATE Autorisation SET validation = ? WHERE id_aut = ?", (decision, target_id))
                if cursor.rowcount > 0: 
                    updated = True
            
            # 2. Le solde sera automatiquement mis à jour car il est calculé en temps réel
            # à partir de la fonction obtenir_solde_reel() qui soustrait les congés acceptés
            
            conn.commit()
            conn.close()
            
            if updated:
                window.destroy()
                self.refresh_table() 
            else:
                messagebox.showerror("Erreur", "Impossible de mettre à jour la demande.")
                
        except Exception as e:
            print(f"Erreur update: {e}")
            if 'conn' in locals() and conn:
                conn.close()

if __name__ == "__main__":
    app = customtkinter.CTk()
    app.geometry("1000x800")
    f = AdminFrame(app)
    f.pack(fill="both", expand=True)
    app.mainloop()