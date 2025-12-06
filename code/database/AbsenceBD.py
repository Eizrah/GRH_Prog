"""
Module pour gérer la base de données des absences
"""
import sqlite3
import os
import json
from datetime import datetime, timedelta


class AbsenceDB:
    """Classe pour gérer la base de données des permissions et autorisations"""

    def __init__(self, db_path=None):
        if db_path is None:
            # Chemin par défaut
            db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'db.sqlite3')
        self.db_path = db_path
        self.init_tables()

    def get_connection(self):
        """Obtient une connexion à la base de données"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_tables(self):
        """Initialise les tables si elles n'existent pas"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Table des permissions
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS permissions (
            id_permission TEXT PRIMARY KEY,
            motif TEXT NOT NULL,
            duree INTEGER NOT NULL,
            validation TEXT NOT NULL,
            id_fonctionnaire TEXT NOT NULL,
            date_debut DATE NOT NULL,
            date_fin DATE NOT NULL,
            lieu TEXT,
            jours_demandes INTEGER NOT NULL,
            jours_accordes INTEGER DEFAULT 0,
            decision TEXT,
            date_demande DATETIME NOT NULL,
            date_decision DATETIME,
            FOREIGN KEY (id_fonctionnaire) REFERENCES fonctionnaires(id_fonc)
        )
        ''')

        # Table des autorisations
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS autorisations (
            id_aut TEXT PRIMARY KEY,
            type TEXT NOT NULL,
            duree INTEGER NOT NULL,
            validation TEXT NOT NULL,
            id_fonctionnaire TEXT NOT NULL,
            motif TEXT,
            date_debut DATE NOT NULL,
            date_fin DATE NOT NULL,
            jours_demandes INTEGER NOT NULL,
            jours_accordes INTEGER DEFAULT 0,
            decision TEXT,
            date_demande DATETIME NOT NULL,
            date_decision DATETIME,
            FOREIGN KEY (id_fonctionnaire) REFERENCES fonctionnaires(id_fonc),
            CHECK (type IN ('ordinaire', 'hospitalisation', 'elections', 'syndical'))
        )
        ''')

        # Index pour optimiser les recherches
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_permissions_fonctionnaire ON permissions(id_fonctionnaire)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_permissions_validation ON permissions(validation)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_permissions_date ON permissions(date_debut)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_autorisations_fonctionnaire ON autorisations(id_fonctionnaire)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_autorisations_validation ON autorisations(validation)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_autorisations_type ON autorisations(type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_autorisations_date ON autorisations(date_debut)')

        conn.commit()
        conn.close()

    def sauvegarder_permission(self, permission):
        """Sauvegarde une permission dans la base de données"""
        conn = self.get_connection()
        cursor = conn.cursor()

        data = permission.to_dict()

        cursor.execute('''
        INSERT INTO permissions (
            id_permission, motif, duree, validation, id_fonctionnaire,
            date_debut, date_fin, lieu, jours_demandes, jours_accordes,
            decision, date_demande, date_decision
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['id_permission'], data['motif'], data['duree'],
            data['validation'], data['id_fonctionnaire'], data['date_debut'],
            data['date_fin'], data['lieu'], data['jours_demandes'],
            data['jours_accordes'], data['decision'], data['date_demande'],
            data['date_decision']
        ))

        conn.commit()
        conn.close()

    def sauvegarder_autorisation(self, autorisation):
        """Sauvegarde une autorisation dans la base de données"""
        conn = self.get_connection()
        cursor = conn.cursor()

        data = autorisation.to_dict()

        cursor.execute('''
        INSERT INTO autorisations (
            id_aut, type, duree, validation, id_fonctionnaire, motif,
            date_debut, date_fin, jours_demandes, jours_accordes,
            decision, date_demande, date_decision
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['id_aut'], data['type'], data['duree'], data['validation'],
            data['id_fonctionnaire'], data['motif'], data['date_debut'],
            data['date_fin'], data['jours_demandes'], data['jours_accordes'],
            data['decision'], data['date_demande'], data['date_decision']
        ))

        conn.commit()
        conn.close()

    def get_permissions_fonctionnaire(self, id_fonctionnaire, validation=None):
        """Récupère les permissions d'un fonctionnaire"""
        conn = self.get_connection()
        cursor = conn.cursor()

        if validation:
            cursor.execute('''
            SELECT * FROM permissions 
            WHERE id_fonctionnaire = ? AND validation = ?
            ORDER BY date_demande DESC
            ''', (id_fonctionnaire, validation))
        else:
            cursor.execute('''
            SELECT * FROM permissions 
            WHERE id_fonctionnaire = ?
            ORDER BY date_demande DESC
            ''', (id_fonctionnaire,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_autorisations_fonctionnaire(self, id_fonctionnaire, validation=None):
        """Récupère les autorisations d'un fonctionnaire"""
        conn = self.get_connection()
        cursor = conn.cursor()

        if validation:
            cursor.execute('''
            SELECT * FROM autorisations 
            WHERE id_fonctionnaire = ? AND validation = ?
            ORDER BY date_demande DESC
            ''', (id_fonctionnaire, validation))
        else:
            cursor.execute('''
            SELECT * FROM autorisations 
            WHERE id_fonctionnaire = ?
            ORDER BY date_demande DESC
            ''', (id_fonctionnaire,))

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_permissions_en_attente(self):
        """Récupère toutes les permissions en attente"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM permissions 
        WHERE validation = 'en_attente'
        ORDER BY date_demande
        ''')

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def get_autorisations_en_attente(self):
        """Récupère toutes les autorisations en attente"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
        SELECT * FROM autorisations 
        WHERE validation = 'en_attente'
        ORDER BY date_demande
        ''')

        rows = cursor.fetchall()
        conn.close()

        return [dict(row) for row in rows]

    def update_permission(self, permission):
        """Met à jour une permission dans la base de données"""
        conn = self.get_connection()
        cursor = conn.cursor()

        data = permission.to_dict()

        cursor.execute('''
        UPDATE permissions SET
            motif=?, duree=?, validation=?, id_fonctionnaire=?,
            date_debut=?, date_fin=?, lieu=?, jours_demandes=?,
            jours_accordes=?, decision=?, date_demande=?, date_decision=?
        WHERE id_permission=?
        ''', (
            data['motif'], data['duree'], data['validation'],
            data['id_fonctionnaire'], data['date_debut'], data['date_fin'],
            data['lieu'], data['jours_demandes'], data['jours_accordes'],
            data['decision'], data['date_demande'], data['date_decision'],
            data['id_permission']
        ))

        conn.commit()
        conn.close()

    def update_autorisation(self, autorisation):
        """Met à jour une autorisation dans la base de données"""
        conn = self.get_connection()
        cursor = conn.cursor()

        data = autorisation.to_dict()

        cursor.execute('''
        UPDATE autorisations SET
            type=?, duree=?, validation=?, id_fonctionnaire=?, motif=?,
            date_debut=?, date_fin=?, jours_demandes=?, jours_accordes=?,
            decision=?, date_demande=?, date_decision=?
        WHERE id_aut=?
        ''', (
            data['type'], data['duree'], data['validation'],
            data['id_fonctionnaire'], data['motif'], data['date_debut'],
            data['date_fin'], data['jours_demandes'], data['jours_accordes'],
            data['decision'], data['date_demande'], data['date_decision'],
            data['id_aut']
        ))

        conn.commit()
        conn.close()

    def calculer_permissions_6_ans(self, id_fonctionnaire):
        """Calcule le total des permissions sur les 6 dernières années"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Date limite: aujourd'hui - 6 ans
        date_limite = (datetime.now() - timedelta(days=6 * 365)).strftime('%Y-%m-%d')

        cursor.execute('''
        SELECT SUM(jours_accordes) as total_jours
        FROM permissions
        WHERE id_fonctionnaire = ? 
          AND validation = 'accepté'
          AND date_debut >= ?
        ''', (id_fonctionnaire, date_limite))

        result = cursor.fetchone()
        conn.close()

        return result['total_jours'] or 0 if result else 0

    def calculer_autorisations_annee(self, id_fonctionnaire):
        """Calcule les autorisations par type pour l'année en cours"""
        conn = self.get_connection()
        cursor = conn.cursor()

        annee_courante = datetime.now().year

        cursor.execute('''
        SELECT type, SUM(jours_accordes) as total_jours
        FROM autorisations
        WHERE id_fonctionnaire = ? 
          AND validation = 'accepté'
          AND strftime('%Y', date_debut) = ?
        GROUP BY type
        ''', (id_fonctionnaire, str(annee_courante)))

        rows = cursor.fetchall()
        conn.close()

        result = {}
        for row in rows:
            result[row['type']] = row['total_jours']

        return result