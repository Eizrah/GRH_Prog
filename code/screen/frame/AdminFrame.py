import customtkinter
from tkinter import ttk

class AdminFrame(customtkinter.CTkFrame):
    def __init__(self, master, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Stocker le contrôleur pour y accéder plus tard
        self.controller = controller
        
        # Titre de la section
        self.title_label = customtkinter.CTkLabel(
            self, 
            text="Gestion des Demandes de Congé",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=20)
        
        # Création du tableau (Treeview)
        self.create_table()
        
        # Dictionnaire pour stocker les boutons par item_id
        self.action_buttons = {}
        
        # Ajout de données d'exemple (à remplacer par vos données réelles)
        self.add_sample_data()
    
    def create_table(self):
        # Cadre pour le tableau avec défilement
        table_frame = customtkinter.CTkFrame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Configuration du style pour Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=40,  # Augmenté pour accommoder les boutons
                        fieldbackground="#2a2d2e",
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        
        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat")
        style.map("Treeview.Heading", background=[('active', '#3484F0')])
        
        # Création du Treeview
        columns = (
            "matricule", "nom_prenom", "date_entree", "statut", 
            "corps", "grade", "solde_conge", "actions"
        )
        
        self.tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show="headings",
            height=15,
            selectmode="extended"
        )
        
        # Définition des en-têtes
        headers = [
            ("Matricule", 100),
            ("Nom & Prénom", 150),
            ("Date d'entrée", 120),
            ("Statut", 120),
            ("Corps", 120),
            ("Grade", 120),
            ("Solde Congé", 100),
            ("Actions", 250)  # Augmenté pour les boutons
        ]
        
        for i, (header, width) in enumerate(headers):
            self.tree.heading(columns[i], text=header)
            self.tree.column(columns[i], width=width, anchor="center")
        
        # Barre de défilement verticale
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        # Barre de défilement horizontale
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=hsb.set)
        
        # Placement des éléments
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Configuration du redimensionnement
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Boutons d'action globaux
        self.create_action_buttons()
        
        # Lier l'événement de sélection pour mettre à jour l'affichage des boutons
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
    
    def create_action_buttons(self):
        """Crée les boutons d'action globaux"""
        button_frame = customtkinter.CTkFrame(self)
        button_frame.pack(pady=10)
        
        customtkinter.CTkButton(
            button_frame,
            text="Actualiser",
            command=self.refresh_table,
            width=120,
            height=35
        ).pack(side="left", padx=5)
        
        customtkinter.CTkButton(
            button_frame,
            text="Exporter",
            command=self.export_data,
            width=120,
            height=35
        ).pack(side="left", padx=5)
    
    def add_row(self, matricule, nom_prenom, date_entree, statut, corps, grade, solde_conge):
        """Ajoute une ligne au tableau"""
        # Insertion de la ligne avec les données
        item_id = self.tree.insert(
            "", 
            "end", 
            values=(
                matricule, 
                nom_prenom, 
                date_entree, 
                statut, 
                corps, 
                grade, 
                solde_conge,
                "Accepter | Refuser | Détails"  # Texte descriptif
            )
        )
        
        # Stocker les données de la ligne pour référence
        self.action_buttons[item_id] = {
            'matricule': matricule,
            'nom_prenom': nom_prenom,
            'date_entree': date_entree,
            'statut': statut,
            'corps': corps,
            'grade': grade,
            'solde_conge': solde_conge
        }
    
    def on_tree_select(self, event):
        """Gère la sélection d'une ligne dans le tableau"""
        selection = self.tree.selection()
        if selection:
            item_id = selection[0]
            # Afficher une fenêtre d'action quand une ligne est sélectionnée
            self.show_action_dialog(item_id)
    
    def show_action_dialog(self, item_id):
        """Affiche une boîte de dialogue pour les actions"""
        if item_id not in self.action_buttons:
            return
        
        data = self.action_buttons[item_id]
        
        # Création d'une fenêtre modale pour les actions
        action_window = customtkinter.CTkToplevel(self)
        action_window.title(f"Actions pour {data['nom_prenom']}")
        action_window.geometry("400x250")
        action_window.grab_set()  # Rend la fenêtre modale
        
        # Titre
        title_label = customtkinter.CTkLabel(
            action_window,
            text=f"Actions pour: {data['nom_prenom']}",
            font=customtkinter.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Informations de base
        info_text = f"""
        Matricule: {data['matricule']}
        Grade: {data['grade']}
        Solde Congé: {data['solde_conge']} jours
        """
        
        info_label = customtkinter.CTkLabel(
            action_window,
            text=info_text,
            font=customtkinter.CTkFont(size=14),
            justify="left"
        )
        info_label.pack(pady=10)
        
        # Frame pour les boutons d'action
        button_frame = customtkinter.CTkFrame(action_window)
        button_frame.pack(pady=20)
        
        # Bouton Accepter
        accept_btn = customtkinter.CTkButton(
            button_frame,
            text="✓ Accepter",
            width=100,
            height=35,
            fg_color="green",
            hover_color="dark green",
            command=lambda: self.accept_request(item_id, action_window)
        )
        accept_btn.pack(side="left", padx=5)
        
        # Bouton Refuser
        reject_btn = customtkinter.CTkButton(
            button_frame,
            text="✗ Refuser",
            width=100,
            height=35,
            fg_color="red",
            hover_color="dark red",
            command=lambda: self.reject_request(item_id, action_window)
        )
        reject_btn.pack(side="left", padx=5)
        
        # Bouton Voir Détails
        detail_btn = customtkinter.CTkButton(
            button_frame,
            text="👁️ Détails",
            width=100,
            height=35,
            command=lambda: self.view_details(item_id, action_window)
        )
        detail_btn.pack(side="left", padx=5)
        
        # Bouton Annuler
        cancel_btn = customtkinter.CTkButton(
            action_window,
            text="Annuler",
            width=120,
            height=35,
            command=action_window.destroy
        )
        cancel_btn.pack(pady=10)
    
    def accept_request(self, item_id, parent_window=None):
        """Gère l'acceptation d'une demande"""
        if item_id in self.action_buttons:
            data = self.action_buttons[item_id]
            matricule = data['matricule']
            print(f"Demande acceptée pour le matricule: {matricule}")
            
            # Si un contrôleur est disponible, on peut l'utiliser
            if self.controller:
                print(f"Contrôleur disponible pour AdminFrame - Acceptation")
            
            # Mettre à jour l'affichage dans le tableau
            self.tree.item(item_id, tags=("accepted",))
            self.tree.tag_configure("accepted", background="lightgreen")
            
            # Afficher un message de confirmation
            self.show_message("Demande acceptée", f"La demande de {data['nom_prenom']} a été acceptée.")
        
        if parent_window:
            parent_window.destroy()
    
    def reject_request(self, item_id, parent_window=None):
        """Gère le refus d'une demande"""
        if item_id in self.action_buttons:
            data = self.action_buttons[item_id]
            matricule = data['matricule']
            print(f"Demande refusée pour le matricule: {matricule}")
            
            # Si un contrôleur est disponible, on peut l'utiliser
            if self.controller:
                print(f"Contrôleur disponible pour AdminFrame - Refus")
            
            # Mettre à jour l'affichage dans le tableau
            self.tree.item(item_id, tags=("rejected",))
            self.tree.tag_configure("rejected", background="lightcoral")
            
            # Afficher un message de confirmation
            self.show_message("Demande refusée", f"La demande de {data['nom_prenom']} a été refusée.")
        
        if parent_window:
            parent_window.destroy()
    
    def view_details(self, item_id, parent_window=None):
        """Affiche les détails d'une personne"""
        if item_id in self.action_buttons:
            data = self.action_buttons[item_id]
            
            # Création d'une fenêtre modale pour afficher les détails
            detail_window = customtkinter.CTkToplevel(self)
            detail_window.title(f"Détails - {data['nom_prenom']}")
            detail_window.geometry("450x350")
            detail_window.grab_set()  # Rend la fenêtre modale
            
            # Affichage des informations complètes
            info_text = f"""
            Informations détaillées:
            
            Matricule: {data['matricule']}
            Nom & Prénom: {data['nom_prenom']}
            Date d'entrée: {data['date_entree']}
            Statut: {data['statut']}
            Corps: {data['corps']}
            Grade: {data['grade']}
            Solde de Congé: {data['solde_conge']} jours
            
            Historique des demandes:
            - En attente: 1 demande
            - Acceptées: 3 demandes
            - Refusées: 0 demande
            """
            
            detail_label = customtkinter.CTkLabel(
                detail_window,
                text=info_text,
                font=customtkinter.CTkFont(size=14),
                justify="left"
            )
            detail_label.pack(padx=20, pady=20)
            
            # Bouton de fermeture
            customtkinter.CTkButton(
                detail_window,
                text="Fermer",
                command=detail_window.destroy
            ).pack(pady=10)
        
        if parent_window:
            parent_window.destroy()
    
    def show_message(self, title, message):
        """Affiche un message d'information"""
        msg_window = customtkinter.CTkToplevel(self)
        msg_window.title(title)
        msg_window.geometry("300x150")
        msg_window.grab_set()
        
        msg_label = customtkinter.CTkLabel(
            msg_window,
            text=message,
            font=customtkinter.CTkFont(size=14)
        )
        msg_label.pack(pady=20)
        
        customtkinter.CTkButton(
            msg_window,
            text="OK",
            command=msg_window.destroy
        ).pack(pady=10)
    
    def add_sample_data(self):
        """Ajoute des données d'exemple au tableau"""
        sample_data = [
            ("EMP001", "Dupont Jean", "15/01/2020", "Fonctionnaire", "Informatique", "Ingénieur", "25"),
            ("EMP002", "Martin Sophie", "20/03/2019", "Contractuel", "RH", "Assistant", "18"),
            ("EMP003", "Leroy Pierre", "10/05/2018", "Fonctionnaire", "Finances", "Contrôleur", "30"),
            ("EMP004", "Moreau Alice", "05/11/2021", "Contractuel", "Marketing", "Chargé", "15"),
            ("EMP005", "Garcia Carlos", "12/07/2017", "Fonctionnaire", "Direction", "Directeur", "35"),
        ]
        
        for data in sample_data:
            self.add_row(*data)
    
    def refresh_table(self):
        """Actualise le tableau"""
        # Si un contrôleur est disponible, on peut l'utiliser
        if self.controller:
            print(f"Contrôleur disponible pour AdminFrame - rafraîchissement")
        # Ici, vous pouvez ajouter la logique pour rafraîchir les données
        print("Tableau actualisé")
        
        # Effacer les données actuelles
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Réinitialiser le dictionnaire
        self.action_buttons.clear()
        
        # Recharger les données
        self.add_sample_data()
    
    def export_data(self):
        """Exporte les données du tableau"""
        # Si un contrôleur est disponible, on peut l'utiliser
        if self.controller:
            print(f"Contrôleur disponible pour AdminFrame - exportation")
        
        # Collecter les données
        export_data = []
        for item_id in self.action_buttons:
            data = self.action_buttons[item_id]
            export_data.append(data)
        
        # Ici, vous pouvez ajouter la logique d'exportation (CSV, Excel, etc.)
        print(f"Données exportées: {len(export_data)} lignes")
        for data in export_data:
            print(f"  - {data['matricule']}: {data['nom_prenom']}")

if __name__ == "__main__":
    # Code de test pour afficher le frame seul
    app = customtkinter.CTk()
    app.geometry("1200x600")
    app.title("Test Admin Frame")
    
    admin_frame = AdminFrame(app)
    admin_frame.pack(fill="both", expand=True)
    
    app.mainloop()