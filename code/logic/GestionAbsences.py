"""
Module de logique pour la gestion des permissions et autorisations d'absence.
Contient toutes les règles métier selon les articles 36-42 du décret.
"""

from datetime import datetime, timedelta
from modele.Fonctionnaire import Fonctionnaire
from modele.Permission import Permission
from modele.Autorisation import Autorisation
from database.AbsenceBD import AbsenceBD


class GestionAbsences:
    """
    Classe principale pour gérer la logique des absences.
    S'occupe de la validation, création et traitement des demandes d'absence.
    """

    def __init__(self):
        """Initialise le gestionnaire avec une connexion à la base de données"""
        self.base_donnees = AbsenceDB()

    def verifier_permission(self, id_fonctionnaire, jours_demandes):
        """
        Vérifie si une permission peut être accordée selon les règles.

        Règles vérifiées:
        1. Durée maximale de 20 jours par demande
        2. Maximum 20 jours sur 6 ans glissants
        3. Fonctionnaire doit avoir le régime de congés cumulés

        Args:
            id_fonctionnaire (str): Identifiant du fonctionnaire
            jours_demandes (int): Nombre de jours demandés

        Returns:
            tuple: (est_valide, message) - Si la permission est valide et un message explicatif
        """
        # Règle 1: Durée maximale de 20 jours par demande (Article 36)
        if jours_demandes > 20:
            return False, "La durée d'une permission ne peut excéder 20 jours"

        # Règle 2: Calculer les permissions sur les 6 dernières années
        permissions_6_ans = self.base_donnees.calculer_permissions_6_ans(id_fonctionnaire)

        # Vérifier si on dépasse la limite de 20 jours sur 6 ans
        if permissions_6_ans + jours_demandes > 20:
            message = f"Dépassement de la limite des 20 jours sur 6 ans. "
            message += f"Déjà utilisé: {permissions_6_ans} jours. "
            message += f"Restant: {20 - permissions_6_ans} jours."
            return False, message

        # Règle 3: Vérifier le régime de congés cumulés (Article 37)
        # Note: À adapter selon votre modèle de fonctionnaire
        # fonctionnaire = Fonctionnaire.trouver_par_id(id_fonctionnaire)
        # if not fonctionnaire or not fonctionnaire.regime_conges_cumules:
        #     return False, "Les permissions sont réservées aux fonctionnaires avec régime de congés cumulés"

        return True, "Permission valide selon les règles"

    def verifier_autorisation(self, type_autorisation, jours_demandes):
        """
        Vérifie si une autorisation peut être accordée selon les règles.

        Règles vérifiées selon le type:
        - Ordinaire: maximum 3 jours
        - Élections: maximum 20 jours pendant la campagne
        - Hospitalisation/Syndical: pas de limite spécifiée

        Args:
            type_autorisation (str): Type d'autorisation
            jours_demandes (int): Nombre de jours demandés

        Returns:
            tuple: (est_valide, message) - Si l'autorisation est valide et un message
        """
        # Règle pour les autorisations ordinaires (Article 40)
        if type_autorisation == 'ordinaire' and jours_demandes > 3:
            return False, "Les autorisations ordinaires ne peuvent excéder 3 jours"

        # Règle pour les autorisations d'élections (Article 41)
        if type_autorisation == 'elections' and jours_demandes > 20:
            return False, "Les autorisations pour élections ne peuvent excéder 20 jours"

        return True, "Autorisation valide selon les règles"

    def creer_permission(self, id_fonctionnaire, motif, date_debut, date_fin, lieu):
        """
        Crée et enregistre une demande de permission d'absence.

        Args:
            id_fonctionnaire (str): ID du fonctionnaire
            motif (str): Motif de la permission
            date_debut (str): Date de début (format YYYY-MM-DD)
            date_fin (str): Date de fin (format YYYY-MM-DD)
            lieu (str): Lieu où sera passée la permission

        Returns:
            dict: Résultat de l'opération avec clés 'succes', 'message', 'permission'
        """
        try:
            # Calculer le nombre de jours entre les dates
            debut = datetime.strptime(date_debut, '%Y-%m-%d')
            fin = datetime.strptime(date_fin, '%Y-%m-%d')
            jours_demandes = (fin - debut).days + 1

            # Vérifier si la permission est valide selon les règles
            est_valide, message = self.verifier_permission(id_fonctionnaire, jours_demandes)

            if not est_valide:
                return {"succes": False, "message": message}

            # Créer l'objet Permission
            permission = Permission(
                motif=motif,
                duree=jours_demandes,
                validation="en_attente",  # Par défaut en attente
                id_fonctionnaire=id_fonctionnaire,
                date_debut=date_debut,
                date_fin=date_fin,
                lieu=lieu,
                jours_demandes=jours_demandes
            )

            # Sauvegarder dans la base de données
            self.base_donnees.sauvegarder_permission(permission)

            return {
                "succes": True,
                "message": "Demande de permission soumise avec succès",
                "permission": permission
            }

        except ValueError as e:
            # Erreur de format de date
            return {"succes": False, "message": f"Erreur de format de date: {str(e)}"}
        except Exception as e:
            # Autre erreur
            return {"succes": False, "message": f"Erreur lors de la création: {str(e)}"}

    def creer_autorisation(self, id_fonctionnaire, type_autorisation, motif, date_debut, date_fin):
        """
        Crée et enregistre une demande d'autorisation d'absence.

        Args:
            id_fonctionnaire (str): ID du fonctionnaire
            type_autorisation (str): Type d'autorisation
            motif (str): Motif de l'autorisation
            date_debut (str): Date de début (format YYYY-MM-DD)
            date_fin (str): Date de fin (format YYYY-MM-DD)

        Returns:
            dict: Résultat de l'opération avec clés 'succes', 'message', 'autorisation'
        """
        try:
            # Calculer le nombre de jours entre les dates
            debut = datetime.strptime(date_debut, '%Y-%m-%d')
            fin = datetime.strptime(date_fin, '%Y-%m-%d')
            jours_demandes = (fin - debut).days + 1

            # Vérifier si l'autorisation est valide selon les règles
            est_valide, message = self.verifier_autorisation(type_autorisation, jours_demandes)

            if not est_valide:
                return {"succes": False, "message": message}

            # Créer l'objet Autorisation
            autorisation = Autorisation(
                type=type_autorisation,
                duree=jours_demandes,
                validation="en_attente",  # Par défaut en attente
                id_fonctionnaire=id_fonctionnaire,
                motif=motif,
                date_debut=date_debut,
                date_fin=date_fin,
                jours_demandes=jours_demandes
            )

            # Sauvegarder dans la base de données
            self.base_donnees.sauvegarder_autorisation(autorisation)

            return {
                "succes": True,
                "message": "Demande d'autorisation soumise avec succès",
                "autorisation": autorisation
            }

        except ValueError as e:
            return {"succes": False, "message": f"Erreur de format de date: {str(e)}"}
        except Exception as e:
            return {"succes": False, "message": f"Erreur lors de la création: {str(e)}"}

    def traiter_permission(self, id_permission, decision, jours_accordes=None, motif_decision=None):
        """
        Traite une demande de permission (pour le supérieur hiérarchique).

        Args:
            id_permission (str): ID de la permission à traiter
            decision (str): Décision ('accepté', 'refusé', 'fractionnee', 'reduite')
            jours_accordes (int): Nombre de jours accordés (si fractionnée ou réduite)
            motif_decision (str): Motif de la décision

        Returns:
            dict: Résultat de l'opération avec clés 'succes' et 'message'
        """
        try:
            # Récupérer toutes les permissions en attente
            permissions_attente = self.base_donnees.get_permissions_en_attente()

            # Chercher la permission par son ID
            donnees_permission = None
            for p in permissions_attente:
                if p['id_permission'] == id_permission:
                    donnees_permission = p
                    break

            if not donnees_permission:
                return {"succes": False, "message": "Permission non trouvée ou déjà traitée"}

            # Créer l'objet Permission à partir des données
            permission = Permission.creer_apres_dictionnaire(donnees_permission)

            # Mettre à jour les attributs selon la décision
            permission.validation = decision
            permission.date_decision = datetime.now().isoformat()
            permission.decision = motif_decision

            if decision == 'accepté':
                # Accorder tous les jours demandés
                permission.jours_accordes = permission.jours_demandes
            elif decision in ['fractionnee', 'reduite'] and jours_accordes is not None:
                # Accorder un nombre réduit de jours
                permission.jours_accordes = jours_accordes
                permission.duree = jours_accordes
            else:
                # Refuser = 0 jour accordé
                permission.jours_accordes = 0

            # Mettre à jour dans la base de données
            self.base_donnees.update_permission(permission)

            return {"succes": True, "message": f"Demande {decision} avec succès"}

        except Exception as e:
            return {"succes": False, "message": f"Erreur lors du traitement: {str(e)}"}

    def traiter_autorisation(self, id_autorisation, decision, motif_decision=None):
        """
        Traite une demande d'autorisation (pour le supérieur hiérarchique).

        Args:
            id_autorisation (str): ID de l'autorisation à traiter
            decision (str): Décision ('accepté', 'refusé')
            motif_decision (str): Motif de la décision

        Returns:
            dict: Résultat de l'opération avec clés 'succes' et 'message'
        """
        try:
            # Récupérer toutes les autorisations en attente
            autorisations_attente = self.base_donnees.get_autorisations_en_attente()

            # Chercher l'autorisation par son ID
            donnees_autorisation = None
            for a in autorisations_attente:
                if a['id_aut'] == id_autorisation:
                    donnees_autorisation = a
                    break

            if not donnees_autorisation:
                return {"succes": False, "message": "Autorisation non trouvée ou déjà traitée"}

            # Créer l'objet Autorisation à partir des données
            autorisation = Autorisation.creer_apres_dictionnaire(donnees_autorisation)

            # Mettre à jour les attributs selon la décision
            autorisation.validation = decision
            autorisation.date_decision = datetime.now().isoformat()
            autorisation.decision = motif_decision

            if decision == 'accepté':
                # Accorder tous les jours demandés
                autorisation.jours_accordes = autorisation.jours_demandes
            else:
                # Refuser = 0 jour accordé
                autorisation.jours_accordes = 0

            # Mettre à jour dans la base de données
            self.base_donnees.update_autorisation(autorisation)

            return {"succes": True, "message": f"Demande {decision} avec succès"}

        except Exception as e:
            return {"succes": False, "message": f"Erreur lors du traitement: {str(e)}"}

    def obtenir_statistiques_fonctionnaire(self, id_fonctionnaire):
        """
        Calcule les statistiques d'absence pour un fonctionnaire.

        Args:
            id_fonctionnaire (str): ID du fonctionnaire

        Returns:
            dict: Statistiques détaillées avec clés 'succes', 'statistiques', 'permissions', 'autorisations'
        """
        try:
            # 1. Permissions sur 6 ans (Article 38)
            permissions_6_ans = self.base_donnees.calculer_permissions_6_ans(id_fonctionnaire)
            jours_restants_permissions = max(0, 20 - permissions_6_ans)

            # 2. Autorisations par type pour l'année en cours
            autorisations_annee = self.base_donnees.calculer_autorisations_annee(id_fonctionnaire)

            # 3. Liste complète des permissions et autorisations
            permissions = self.base_donnees.get_permissions_fonctionnaire(id_fonctionnaire)
            autorisations = self.base_donnees.get_autorisations_fonctionnaire(id_fonctionnaire)

            return {
                "succes": True,
                "statistiques": {
                    "permissions_6_ans": permissions_6_ans,
                    "limite_permissions": 20,
                    "jours_restants_permissions": jours_restants_permissions,
                    "autorisations_annee": autorisations_annee,
                    "total_permissions": len(permissions),
                    "total_autorisations": len(autorisations)
                },
                "permissions": permissions,
                "autorisations": autorisations
            }

        except Exception as e:
            return {"succes": False, "message": str(e)}