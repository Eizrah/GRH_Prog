# Classe enfant de Pause pour les autorisations d'absence
import Pause
import uuid
from datetime import datetime


class Autorisation(Pause.Pause):
    """
    Classe représentant une autorisation d'absence d'un fonctionnaire.
    Une autorisation peut être de différents types (ordinaire, hospitalisation, élections, syndical).
    """

    # Types d'autorisation possibles
    TYPES_AUTORISATION = {
        'ordinaire': 'Autorisation absence ordinaire',
        'hospitalisation': 'Autorisation spéciale en cas d\'hospitalisation du conjoint ou de son enfant à charge',
        'elections': 'Autorisation spéciale d\'absence des fonctionnaires candidats à des élections politiques',
        'syndical': 'Autorisation spéciale d\'absence des fonctionnaires occupant des fonctions publiques électives ou syndicales'
    }

    def __init__(self, type, duree, validation, id_fonctionnaire=None, motif=None,
                 date_debut=None, date_fin=None, jours_demandes=0, jours_accordes=0,
                 decision=None, date_demande=None, date_decision=None):
        """
        Initialise une nouvelle autorisation d'absence.

        Args:
            type (str): Type d'autorisation (ordinaire, hospitalisation, elections, syndical)
            duree (int): Durée de l'autorisation en jours
            validation (str): Statut de validation ('en_attente', 'accepté', 'refusé')
            id_fonctionnaire (str): Identifiant du fonctionnaire concerné
            motif (str): Motif de l'autorisation
            date_debut (str): Date de début au format YYYY-MM-DD
            date_fin (str): Date de fin au format YYYY-MM-DD
            jours_demandes (int): Nombre de jours demandés
            jours_accordes (int): Nombre de jours accordés
            decision (str): Motif de la décision du supérieur
            date_demande (str): Date de la demande
            date_decision (str): Date de la décision
        """
        # Appel au constructeur de la classe parent Pause
        super().__init__(duree, validation)

        # Génération d'un identifiant unique
        self._id_aut = str(uuid.uuid4())
        self._type = type
        self._id_fonctionnaire = id_fonctionnaire
        self._motif = motif
        self._date_debut = date_debut or datetime.now().date().isoformat()
        self._date_fin = date_fin
        self._jours_demandes = jours_demandes
        self._jours_accordes = jours_accordes
        self._decision = decision
        self._date_demande = date_demande or datetime.now().isoformat()
        self._date_decision = date_decision

    # ============================================
    # PROPRIÉTÉS (GETTERS) - Permettent d'accéder aux attributs privés
    # ============================================

    @property
    def type(self):
        """Retourne le type d'autorisation"""
        return self._type

    @property
    def id_aut(self):
        """Retourne l'identifiant unique de l'autorisation"""
        return self._id_aut

    @property
    def id_fonctionnaire(self):
        """Retourne l'identifiant du fonctionnaire"""
        return self._id_fonctionnaire

    @property
    def motif(self):
        """Retourne le motif de l'autorisation"""
        return self._motif

    @property
    def date_debut(self):
        """Retourne la date de début"""
        return self._date_debut

    @property
    def date_fin(self):
        """Retourne la date de fin"""
        return self._date_fin

    @property
    def jours_demandes(self):
        """Retourne le nombre de jours demandés"""
        return self._jours_demandes

    @property
    def jours_accordes(self):
        """Retourne le nombre de jours accordés"""
        return self._jours_accordes

    @property
    def decision(self):
        """Retourne la décision du supérieur"""
        return self._decision

    @property
    def date_demande(self):
        """Retourne la date de la demande"""
        return self._date_demande

    @property
    def date_decision(self):
        """Retourne la date de la décision"""
        return self._date_decision

    # ============================================
    # SETTERS - Permettent de modifier les attributs privés
    # ============================================

    @type.setter
    def type(self, valeur):
        """Modifie le type d'autorisation"""
        self._type = valeur

    @id_fonctionnaire.setter
    def id_fonctionnaire(self, valeur):
        """Modifie l'identifiant du fonctionnaire"""
        self._id_fonctionnaire = valeur

    @motif.setter
    def motif(self, valeur):
        """Modifie le motif de l'autorisation"""
        self._motif = valeur

    @date_debut.setter
    def date_debut(self, valeur):
        """Modifie la date de début"""
        self._date_debut = valeur

    @date_fin.setter
    def date_fin(self, valeur):
        """Modifie la date de fin"""
        self._date_fin = valeur

    @jours_demandes.setter
    def jours_demandes(self, valeur):
        """Modifie le nombre de jours demandés"""
        self._jours_demandes = valeur

    @jours_accordes.setter
    def jours_accordes(self, valeur):
        """Modifie le nombre de jours accordés"""
        self._jours_accordes = valeur

    @decision.setter
    def decision(self, valeur):
        """Modifie la décision du supérieur"""
        self._decision = valeur

    @date_demande.setter
    def date_demande(self, valeur):
        """Modifie la date de la demande"""
        self._date_demande = valeur

    @date_decision.setter
    def date_decision(self, valeur):
        """Modifie la date de la décision"""
        self._date_decision = valeur

    # ============================================
    # MÉTHODES PUBLIQUES
    # ============================================

    def obtenir_libelle_type(self):
        """
        Retourne le libellé complet du type d'autorisation.

        Returns:
            str: Libellé complet du type
        """
        return self.TYPES_AUTORISATION.get(self._type, self._type)

    def convertir_en_dictionnaire(self):
        """
        Convertit l'objet en dictionnaire pour la base de données.

        Returns:
            dict: Dictionnaire contenant tous les attributs
        """
        return {
            'id_aut': self._id_aut,
            'type': self._type,
            'duree': self._duree,
            'validation': self._validation,
            'id_fonctionnaire': self._id_fonctionnaire,
            'motif': self._motif,
            'date_debut': self._date_debut,
            'date_fin': self._date_fin,
            'jours_demandes': self._jours_demandes,
            'jours_accordes': self._jours_accordes,
            'decision': self._decision,
            'date_demande': self._date_demande,
            'date_decision': self._date_decision
        }

    @classmethod
    def creer_apres_dictionnaire(cls, donnees):
        """
        Crée un objet Autorisation à partir d'un dictionnaire.

        Args:
            donnees (dict): Dictionnaire contenant les données

        Returns:
            Autorisation: Nouvel objet créé
        """
        return cls(
            type=donnees['type'],
            duree=donnees['duree'],
            validation=donnees['validation'],
            id_fonctionnaire=donnees['id_fonctionnaire'],
            motif=donnees.get('motif'),
            date_debut=donnees.get('date_debut'),
            date_fin=donnees.get('date_fin'),
            jours_demandes=donnees.get('jours_demandes', 0),
            jours_accordes=donnees.get('jours_accordes', 0),
            decision=donnees.get('decision'),
            date_demande=donnees.get('date_demande'),
            date_decision=donnees.get('date_decision')
        )

    def __str__(self):
        """
        Retourne une représentation textuelle de l'autorisation.

        Returns:
            str: Description de l'autorisation
        """
        return f"Autorisation: {self.obtenir_libelle_type()} ({self._duree} jours) - Statut: {self._validation}"
"""  
Note

type :  autorisation absence ordinaire
        autorisation speciale en cas d'hospitalisation du conjoint ou de son enfant à charge
        autorisation special  d'absence des fonctionaires candidats à des "lections politiques
"""