# Classe enfant de Pause pour les permissions d'absence
import Pause
import uuid
from datetime import datetime


class Permission(Pause.Pause):
    """
    Classe représentant une permission d'absence d'un fonctionnaire.
    Une permission est une absence autorisée de courte durée (max 20 jours).
    """

    def __init__(self, motif, duree, validation, id_fonctionnaire=None, date_debut=None,
                 date_fin=None, lieu=None, jours_demandes=0, jours_accordes=0,
                 decision=None, date_demande=None, date_decision=None):
        """
        Initialise une nouvelle permission d'absence.

        Args:
            motif (str): Motif de la permission (ex: rendez-vous médical, urgence familiale)
            duree (int): Durée de la permission en jours
            validation (str): Statut de validation ('en_attente', 'accepté', 'refusé')
            id_fonctionnaire (str): Identifiant du fonctionnaire concerné
            date_debut (str): Date de début au format YYYY-MM-DD
            date_fin (str): Date de fin au format YYYY-MM-DD
            lieu (str): Lieu où sera passée la permission
            jours_demandes (int): Nombre de jours demandés
            jours_accordes (int): Nombre de jours accordés
            decision (str): Motif de la décision du supérieur
            date_demande (str): Date de la demande
            date_decision (str): Date de la décision
        """
        # Appel au constructeur de la classe parent Pause
        super().__init__(duree, validation)

        # Génération d'un identifiant unique
        self._id_permission = str(uuid.uuid4())
        self._motif = motif
        self._id_fonctionnaire = id_fonctionnaire
        self._date_debut = date_debut or datetime.now().date().isoformat()
        self._date_fin = date_fin
        self._lieu = lieu
        self._jours_demandes = jours_demandes
        self._jours_accordes = jours_accordes
        self._decision = decision
        self._date_demande = date_demande or datetime.now().isoformat()
        self._date_decision = date_decision

    # ============================================
    # PROPRIÉTÉS (GETTERS)
    # ============================================

    @property
    def motif(self):
        """Retourne le motif de la permission"""
        return self._motif

    @property
    def id_permission(self):
        """Retourne l'identifiant unique de la permission"""
        return self._id_permission

    @property
    def id_fonctionnaire(self):
        """Retourne l'identifiant du fonctionnaire"""
        return self._id_fonctionnaire

    @property
    def date_debut(self):
        """Retourne la date de début"""
        return self._date_debut

    @property
    def date_fin(self):
        """Retourne la date de fin"""
        return self._date_fin

    @property
    def lieu(self):
        """Retourne le lieu de la permission"""
        return self._lieu

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
    # SETTERS
    # ============================================

    @motif.setter
    def motif(self, valeur):
        """Modifie le motif de la permission"""
        self._motif = valeur

    @id_fonctionnaire.setter
    def id_fonctionnaire(self, valeur):
        """Modifie l'identifiant du fonctionnaire"""
        self._id_fonctionnaire = valeur

    @date_debut.setter
    def date_debut(self, valeur):
        """Modifie la date de début"""
        self._date_debut = valeur

    @date_fin.setter
    def date_fin(self, valeur):
        """Modifie la date de fin"""
        self._date_fin = valeur

    @lieu.setter
    def lieu(self, valeur):
        """Modifie le lieu de la permission"""
        self._lieu = valeur

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
    # MÉTHODES DE LA CLASSE PARENT (PAUSE) - IMPLÉMENTATION
    # ============================================

    @property
    def duree(self):
        """Retourne la durée de la permission (héritée de Pause)"""
        return self._duree

    @property
    def validation(self):
        """Retourne le statut de validation (héritée de Pause)"""
        return self._validation

    @duree.setter
    def duree(self, valeur):
        """Modifie la durée de la permission (héritée de Pause)"""
        self._duree = valeur

    @validation.setter
    def validation(self, valeur):
        """Modifie le statut de validation (héritée de Pause)"""
        self._validation = valeur

    # ============================================
    # MÉTHODES PUBLIQUES
    # ============================================

    def convertir_en_dictionnaire(self):
        """
        Convertit l'objet en dictionnaire pour la base de données.

        Returns:
            dict: Dictionnaire contenant tous les attributs
        """
        return {
            'id_permission': self._id_permission,
            'motif': self._motif,
            'duree': self._duree,
            'validation': self._validation,
            'id_fonctionnaire': self._id_fonctionnaire,
            'date_debut': self._date_debut,
            'date_fin': self._date_fin,
            'lieu': self._lieu,
            'jours_demandes': self._jours_demandes,
            'jours_accordes': self._jours_accordes,
            'decision': self._decision,
            'date_demande': self._date_demande,
            'date_decision': self._date_decision
        }

    @classmethod
    def creer_apres_dictionnaire(cls, donnees):
        """
        Crée un objet Permission à partir d'un dictionnaire.

        Args:
            donnees (dict): Dictionnaire contenant les données

        Returns:
            Permission: Nouvel objet créé
        """
        return cls(
            motif=donnees['motif'],
            duree=donnees['duree'],
            validation=donnees['validation'],
            id_fonctionnaire=donnees['id_fonctionnaire'],
            date_debut=donnees.get('date_debut'),
            date_fin=donnees.get('date_fin'),
            lieu=donnees.get('lieu'),
            jours_demandes=donnees.get('jours_demandes', 0),
            jours_accordes=donnees.get('jours_accordes', 0),
            decision=donnees.get('decision'),
            date_demande=donnees.get('date_demande'),
            date_decision=donnees.get('date_decision')
        )

    def __str__(self):
        """
        Retourne une représentation textuelle de la permission.

        Returns:
            str: Description de la permission
        """
        return f"Permission: {self._motif} ({self._duree} jours) - Statut: {self._validation}"