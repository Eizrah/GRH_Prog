# rh_backend.py
import sqlite3
import uuid
from datetime import datetime, timedelta

# --- Configuration Globale & COULEURS (DOIT ÊTRE DANS LE FRONTEND NORMALEMENT, MAIS GARDÉ ICI POUR LES CONSTANTES) ---
# NOTE: Ces constantes seraient idéalement dans un fichier de configuration séparé ou dans le Frontend,
# mais sont regroupées ici avec les utilitaires pour la simplicité de la séparation.
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

# --- Rôles et Données Utilitaires GLOBALES ---
USERS_DB = {
    "rakoto.jp": {
        "password": "personnel",
        "data": {
            'id': '1', 'role': 'personnel', 'nom_complet': 'RAKOTO Jean Pierre', 'personnel_id': '1'
        }
    },
    "razafy.ms": {
        "password": "personnel",
        "data": {
            'id': '2', 'role': 'personnel', 'nom_complet': 'RAZAFY Marie Solange', 'personnel_id': '2'
        }
    },
    "admin": {
        "password": "admin123",
        "data": {
            'id': '0', 'role': 'admin', 'nom_complet': 'Administrateur Général', 'personnel_id': '0'
        }
    },
    "rh": {
        "password": "rh123",
        "data": {
            'id': '3', 'role': 'rh', 'nom_complet': 'RH Responsable', 'personnel_id': '0'
        }
    }
}
CURRENT_USER = None # Variable globale gérée par l'application pour l'utilisateur connecté

def get_types_absence_map():
    """Mappe les codes internes des types d'absence à leur libellé affichable."""
    return {
        'CONGE_ANNUEL': 'Congé Annuel',
        'CONGE_ANNUEL_CUMULE': 'Congé Annuel Cumulé',
        'CONGE_MALADIE': 'Congé de Maladie',
        'CONGE_MATERNITE': 'Congé de Maternité',
        'CONGE_FORMATION': 'Congé pour Formation',
        'CONGE_EDUCATION': 'Congé pour Éducation',
        'PERMISSION_ABSENCE': 'Permission d\'absence',
        'AUTORISATION_ORDINAIRE': 'Autorisation d\'absence ordinaire',
        'AUTORISATION_SPECIALE_HOSP': 'Autorisation Spéciale (Hospitalisation)',
        'AUTORISATION_SPECIALE_FAM': 'Autorisation Spéciale (Événement familial)'
    }

def calculate_working_days(start_date_str: str, end_date_str: str) -> int:
    """
    Calcule le nombre de jours ouvrés (exclut Samedi et Dimanche) entre deux dates.
    
    Args:
        start_date_str (str): Date de début (format YYYY-MM-DD).
        end_date_str (str): Date de fin (format YYYY-MM-DD).
        
    Returns:
        int: Nombre de jours ouvrés.
    """
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        return 0
        
    if start_date > end_date:
        return 0

    delta = end_date - start_date
    days = 0
    # On inclut la date de fin dans le décompte (+1)
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        # 0=Lundi, ..., 4=Vendredi, 5=Samedi, 6=Dimanche
        if day.weekday() < 5:
            days += 1
    return days


# =================================================================
# --- DATA MANAGER (GESTION SQLITE & LOGIQUE GRH) ---
# =================================================================
class SQLiteDataManager:

    def __init__(self, db_name='gestion_conges.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables()
        self._seed_data()

    def _connect(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f"Erreur de connexion à SQLite: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()

    def _create_tables(self):
        try:
            # ... (Définition de la table personnel) ...
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS personnel (
                    id TEXT PRIMARY KEY,
                    numeroMatricule TEXT UNIQUE NOT NULL,
                    nom TEXT NOT NULL,
                    prenoms TEXT,
                    dateEntree TEXT,
                    emploi TEXT,
                    dateNaissance TEXT,
                    lieuNaissance TEXT,
                    categorie TEXT,
                    corps TEXT,
                    cadre TEXT,
                    classe TEXT,
                    echelon INTEGER,
                    positionReglementaire TEXT
                )
            """)
            # ... (Définition de la table absences) ...
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS absences (
                    id TEXT PRIMARY KEY,
                    personnelId TEXT,
                    numeroDecision TEXT,
                    type TEXT NOT NULL,
                    dateDebut TEXT NOT NULL,
                    dateFin TEXT NOT NULL,
                    duree INTEGER NOT NULL,
                    statut TEXT NOT NULL,
                    accordePar TEXT,
                    motif TEXT,
                    FOREIGN KEY (personnelId) REFERENCES personnel (id)
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors de la création des tables: {e}")
            self.conn.rollback()

    def _seed_data(self):
        # ... (Insertion des données initiales) ...
        if self.cursor.execute("SELECT COUNT(*) FROM personnel").fetchone()[0] == 0:
            personnels_data = [
                ('1', 'MAT001', 'RAKOTO', 'Jean Pierre', '2010-01-10', 'Chef de Service',
                 '1980-05-15', 'Antananarivo', 'Fonctionnaire', 'Admin. Général', 'A', 'Principal', 3, 'Activité'),
                ('2', 'MAT002', 'RAZAFY', 'Marie Solange', '2015-09-01', 'Technicien Informatique',
                 '1990-11-20', 'Fianarantsoa', 'Agent Contractuel', 'Technique', 'C', 'Deuxième Classe', 1, 'Activité')
            ]
            self.cursor.executemany("""
                INSERT INTO personnel VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, personnels_data)
            absences_data = [
                ('1', '1', 'DEC-2024-001', 'CONGE_ANNUEL', '2024-11-01', '2024-11-15', 15, 'APPROUVE', 'Directeur RH',
                 'Congés annuels 2024'),
                ('4', '1', 'DEM-2025-001', 'CONGE_ANNUEL', '2025-02-01', '2025-02-05', 5, 'EN_ATTENTE', 'N/A',
                 'Vacances Hiver'),
                ('2', '1', 'DEC-2024-015', 'PERMISSION_ABSENCE', '2024-10-10', '2024-10-12', 3, 'TERMINE',
                 'Chef de Service', 'Absence pour cause personnelle'),
                ('5', '1', 'DEC-2024-016', 'AUTORISATION_ORDINAIRE', '2024-09-01', '2024-09-01', 1, 'APPROUVE',
                 'Chef de Service', 'Participation à une formation'),
                ('3', '2', 'DEM-2025-002', 'CONGE_ANNUEL', '2025-01-20', '2025-01-27', 8, 'EN_ATTENTE',
                 'Chef de Service', 'Voyage personnel')
            ]
            self.cursor.executemany("""
                INSERT INTO absences VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, absences_data)
            self.conn.commit()

    # --- Méthodes de Récupération de Données ---

    def get_personnel_by_id(self, personnel_id):
        self.cursor.execute("SELECT * FROM personnel WHERE id = ?", (personnel_id,))
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def get_all_personnels(self):
        self.cursor.execute("SELECT * FROM personnel")
        return [dict(row) for row in self.cursor.fetchall()]

    def get_absences(self, personnel_id=None):
        if personnel_id and personnel_id != '0':
            self.cursor.execute("SELECT * FROM absences WHERE personnelId = ? ORDER BY dateDebut DESC", (personnel_id,))
        else:
            self.cursor.execute("SELECT * FROM absences ORDER BY dateDebut DESC")
        return [dict(row) for row in self.cursor.fetchall()]

    # --- Méthodes de Modification de Données ---

    def add_absence(self, absence_data):
        global CURRENT_USER
        if not CURRENT_USER or CURRENT_USER['role'] != 'personnel':
            raise PermissionError("Opération non autorisée. Utilisateur non connecté ou non personnel.")
            
        new_id = str(uuid.uuid4())
        data_to_insert = (
            new_id, CURRENT_USER['personnel_id'],
            f"DEM-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            absence_data['type'], absence_data['dateDebut'], absence_data['dateFin'],
            absence_data['duree'], 'EN_ATTENTE', 'N/A', absence_data['motif']
        )
        try:
            self.cursor.execute("""
                INSERT INTO absences (id, personnelId, numeroDecision, type, dateDebut, dateFin, duree, statut, accordePar, motif)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data_to_insert)
            self.conn.commit()
            self.cursor.execute("SELECT * FROM absences WHERE id = ?", (new_id,))
            return dict(self.cursor.fetchone())
        except sqlite3.Error as e:
            print(f"Erreur lors de l'insertion de l'absence: {e}")
            self.conn.rollback()
            return None

    def update_absence_status(self, absence_id, new_status, accorde_par):
        try:
            self.cursor.execute("""
                UPDATE absences SET statut = ?, accordePar = ? WHERE id = ?
            """, (new_status, accorde_par, absence_id))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour du statut d'absence: {e}")
            self.conn.rollback()
            return False

    # --- Logique GRH ---

    def get_anciennete_en_annees(self, personnel_id: str) -> int:
        """Calcule l'ancienneté en années complètes."""
        personnel = self.get_personnel_by_id(personnel_id)
        if not personnel:
            return 0
        try:
            date_entree = datetime.strptime(personnel['dateEntree'], "%Y-%m-%d")
            # Une année complète est 365.25 jours (pour les bissextiles)
            return (datetime.now() - date_entree).days // 365
        except ValueError:
            return 0

    def a_droit_au_conge_annuel(self, personnel_id: str) -> bool:
        """Vérifie si le droit au congé annuel est acquis (après 12 mois de service effectif)."""
        return self.get_anciennete_en_annees(personnel_id) >= 1

    def calculer_solde_conges(self, personnel_id: str):
        """Calcule le solde de congé annuel disponible."""
        JOURS_CREDIT_ANNUEL = 30 # Crédit annuel par défaut

        if not self.a_droit_au_conge_annuel(personnel_id):
            jours_credit = 0
        else:
            jours_credit = JOURS_CREDIT_ANNUEL

        CONGES_IMPUTABLES = ['CONGE_ANNUEL', 'CONGE_ANNUEL_CUMULE']

        # Jours validés / pris
        query_valides = f"""
            SELECT SUM(duree) FROM absences
            WHERE personnelId = ? AND type IN ({','.join(['?'] * len(CONGES_IMPUTABLES))}) AND statut IN ('APPROUVE', 'TERMINE')
        """
        params_valides = [personnel_id] + CONGES_IMPUTABLES
        self.cursor.execute(query_valides, params_valides)
        jours_valides = self.cursor.fetchone()[0] or 0

        # Jours en attente de validation
        query_attente = f"""
            SELECT SUM(duree) FROM absences
            WHERE personnelId = ? AND type IN ({','.join(['?'] * len(CONGES_IMPUTABLES))}) AND statut = 'EN_ATTENTE'
        """
        params_attente = [personnel_id] + CONGES_IMPUTABLES
        self.cursor.execute(query_attente, params_attente)
        jours_en_attente = self.cursor.fetchone()[0] or 0

        # Solde réel disponible
        jours_restants = jours_credit - jours_valides - jours_en_attente

        return {
            'joursTotal': jours_credit,
            'joursValides': jours_valides,
            'joursEnAttente': jours_en_attente,
            'joursRestants': jours_restants
        }