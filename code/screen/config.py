"""
Configuration de l'application RH Legal Pro
"""

# --- Configuration Globale ---
APP_NAME = "RH Legal Pro"
APP_VERSION = "2.0"
DEFAULT_FONT_FAMILY = "Segoe UI"
FONT_SECONDARY = "Arial"

# --- Configuration selon les lois et décrets ---
CONFIG_LOIS = {
    "CONGE_ANNUEL_BASE": 30,
    "ANCIENNETE_MIN_CONGES": 1,
    "MAX_CONGE_CONSECUTIF": 20,
    "AUTO_ADVANCEMENT_ECHELON": 2,
    "PERMISSION_MAX_JOURS": 20,
    "CONGE_MATERNITE": 14 * 7,
    "CONGE_PATERNITE": 15,
    "CADRES": ["A", "B", "C", "D"],
    "ECHELLES": {
        "A": ["A1", "A2", "A3"],
        "B": ["B1", "B2"],
        "C": ["C1", "C2"],
        "D": ["D1", "D2", "D3"]
    },
    "CLASSES": {
        "exceptionnelle": {"echelons": 2, "ordre": 1},
        "principale": {"echelons": 3, "ordre": 2},
        "premiere": {"echelons": 3, "ordre": 3},
        "deuxieme": {"echelons": 3, "ordre": 4}
    },
    "CATEGORIES_PERSONNEL": [
        "Fonctionnaire",
        "EFA (Emplois normalement dévolus aux fonctionnaires)",
        "ELD (Emplois de longue durée)",
        "ECD (Emplois de courte durée)",
        "EMO (Main d'œuvre)",
        "ES (Emplois spéciaux)"
    ],
    "POSITIONS_REGLEMENTAIRES": [
        "En activité",
        "En détachement",
        "Hors cadre",
        "Sous les drapeaux",
        "En disponibilité"
    ]
}

def get_types_absence_map():
    return {
        'CONGE_ANNUEL': {'nom': 'Congé Annuel', 'duree_max': 30, 'solde_imputable': True},
        'CONGE_ANNUEL_CUMULE': {'nom': 'Congé Annuel Cumulé', 'duree_max': 60, 'solde_imputable': True},
        'CONGE_MALADIE': {'nom': 'Congé de Maladie', 'duree_max': 180, 'solde_imputable': False},
        'CONGE_MATERNITE': {'nom': 'Congé de Maternité', 'duree_max': 98, 'solde_imputable': False},
        'CONGE_PATERNITE': {'nom': 'Congé de Paternité', 'duree_max': 15, 'solde_imputable': False},
        'CONGE_FORMATION': {'nom': 'Congé pour Formation', 'duree_max': 365, 'solde_imputable': True},
        'CONGE_EDUCATION': {'nom': 'Congé pour Éducation', 'duree_max': 30, 'solde_imputable': True},
        'PERMISSION_ABSENCE': {'nom': 'Permission d\'absence', 'duree_max': 20, 'solde_imputable': False},
        'AUTORISATION_ORDINAIRE': {'nom': 'Autorisation d\'absence ordinaire', 'duree_max': 5, 'solde_imputable': False},
        'AUTORISATION_SPECIALE': {'nom': 'Autorisation Spéciale', 'duree_max': 10, 'solde_imputable': False}
    }

# --- Base de données des utilisateurs ---
USERS_DB = {
    "admin": {
        "password": "admin123",
        "data": {
            'id': '0', 'role': 'admin', 'nom_complet': 'Administrateur Système',
            'personnel_id': '0', 'matricule': 'ADM001'
        }
    },
    "rh": {
        "password": "rh123",
        "data": {
            'id': '1', 'role': 'rh', 'nom_complet': 'Responsable RH',
            'personnel_id': '1', 'matricule': 'RH001'
        }
    },
    "rakoto.jp": {
        "password": "personnel",
        "data": {
            'id': '2', 'role': 'personnel', 'nom_complet': 'RAKOTO Jean Pierre',
            'personnel_id': '2', 'matricule': 'MAT001'
        }
    },
    "razafy.ms": {
        "password": "personnel",
        "data": {
            'id': '3', 'role': 'personnel', 'nom_complet': 'RAZAFY Marie Solange',
            'personnel_id': '3', 'matricule': 'MAT002'
        }
    }
}

# Palette de couleurs professionnelle
COLORS = {
    "PRIMARY": "#2C3E50",
    "SECONDARY": "#3498DB",
    "ACCENT_GREEN": "#27AE60",
    "ACCENT_RED": "#E74C3C",
    "ACCENT_ORANGE": "#E67E22",
    "BG_LIGHT": "#ECF0F1",
    "BG_WHITE": "#FFFFFF",
    "TEXT_DARK": "#2C3E50",
    "TEXT_LIGHT": "#7F8C8D",
    "BORDER": "#BDC3C7",
    "HOVER": "#D5DBDB",
    "HEADER": "#34495E",
    "SUCCESS": "#2ECC71",
    "WARNING": "#F1C40F",
    "SIDEBAR": "#2C3E50",
    "INFO": "#3498DB",
}