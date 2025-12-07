# -*- coding: utf-8 -*-
"""
Module de Gestion des Absences (Congés, Permissions, Autorisations)
Basé sur le décret malgache de gestion des fonctionnaires
"""

from datetime import datetime, date, timedelta
from typing import Tuple, Dict, Any

class GestionAbsences:
    """
    Classe pour gérer toutes les absences des fonctionnaires :
    - Congés (annuel, cumulé, maladie, maternité, paternité, formation, etc.)
    - Permissions d'absence
    - Autorisations d'absence
    """
    
    def __init__(self):
        """Initialise le gestionnaire d'absences"""
        self.types_conge = {
            "Congé annuel": self.valider_conge_annuel,
            "Congé maladie": self.valider_conge_maladie,
            "Congé maternité": self.valider_conge_maternite,
            "Congé paternité": self.valider_conge_paternite,
            "Congé sans solde": self.valider_conge_sans_solde,
            "Congé pour événements familiaux": self.valider_conge_evenements,
            "Congé formation": self.valider_conge_formation,
            "Congé pour éducation": self.valider_conge_education,
            "Congé pour éducation dans les domaines social, civique et syndical": self.valider_conge_education,
            "Absence exceptionnelle": self.valider_autorisation_ordinaire,
            "Permission d'absence": self.valider_permission,
            "Autorisation d'absence ordinaire (3 jours max)": self.valider_autorisation_ordinaire,
            "Autorisation d'absence spéciale": self.valider_autorisation_election
        }
    
    def calculer_duree_absence(self, date_debut: str, date_fin: str) -> int:
        """
        Calcule la durée en jours entre deux dates
        
        Args:
            date_debut (str): Date de début au format DD/MM/YYYY
            date_fin (str): Date de fin au format DD/MM/YYYY
        
        Returns:
            int: Nombre de jours
        """
        try:
            debut = datetime.strptime(date_debut, '%d/%m/%Y').date()
            fin = datetime.strptime(date_fin, '%d/%m/%Y').date()
            duree = (fin - debut).days + 1  # +1 pour inclure le dernier jour
            return duree
        except ValueError:
            return 0
    
    def valider_demande(self, type_absence: str, solde_disponible: int, 
                       date_debut: str, date_fin: str, **kwargs) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Valide une demande d'absence selon son type
        
        Args:
            type_absence (str): Type de congé/permission/autorisation
            solde_disponible (int): Solde de congé annuel disponible
            date_debut (str): Date de début
            date_fin (str): Date de fin
            **kwargs: Paramètres supplémentaires spécifiques au type
        
        Returns:
            Tuple[bool, str, Dict]: (Validé, Message, Informations complémentaires)
        """
        duree = self.calculer_duree_absence(date_debut, date_fin)
        
        if duree <= 0:
            return False, "Erreur : La date de fin doit être postérieure à la date de début", {}
        
        if type_absence in self.types_conge:
            return self.types_conge[type_absence](solde_disponible, duree, date_debut, date_fin, **kwargs)
        else:
            return False, "Type d'absence non reconnu", {}
    
    # ========== CONGÉS ==========
    
    def valider_conge_annuel(self, solde: int, duree: int, date_debut: str, date_fin: str, **kwargs) -> Tuple[bool, str, Dict]:
        """
        Valide un congé annuel
        Article 4 : 30 jours/an (2,5 jours/mois)
        - Première fraction de 15 jours obligatoire sans interruption
        - Deuxième fraction peut être échelonnée
        """
        if duree > solde:
            return False, f"Solde insuffisant : vous demandez {duree} jours mais vous n'avez que {solde} jours disponibles", {
                "duree_demandee": duree,
                "solde_disponible": solde,
                "solde_apres": solde - duree
            }
        
        # Vérification de la première fraction (15 jours minimum sans interruption)
        if duree >= 15:
            infos = {
                "type_fraction": "Première fraction (15 jours minimum obligatoire)",
                "duree": duree,
                "solde_apres": solde - duree
            }
            return True, f"Congé annuel validé : {duree} jours (solde restant : {solde - duree} jours)", infos
        else:
            infos = {
                "type_fraction": "Deuxième fraction ou fraction partielle",
                "duree": duree,
                "solde_apres": solde - duree,
                "note": "Soumis à l'échelonnement selon les nécessités de service"
            }
            return True, f"Congé annuel validé : {duree} jours (solde restant : {solde - duree} jours). Note : Soumis à validation selon les nécessités de service.", infos
    
    def valider_conge_maladie(self, solde: int, duree: int, date_debut: str, date_fin: str, **kwargs) -> Tuple[bool, str, Dict]:
        """
        Valide un congé de maladie
        Article 16 : 1 mois max, renouvelable jusqu'à 3 mois total sur 12 mois
        """
        conges_maladie_annee = kwargs.get('conges_maladie_precedents', 0)
        total_avec_demande = conges_maladie_annee + duree
        
        if duree > 30:
            return False, f"Erreur : Un congé de maladie ne peut excéder 30 jours (1 mois) à la fois. Vous demandez {duree} jours.", {
                "duree_max_par_demande": 30
            }
        
        if total_avec_demande > 90:
            return False, f"Erreur : Vous avez déjà pris {conges_maladie_annee} jours de congé maladie sur les 12 derniers mois. Le maximum total est de 90 jours (3 mois). Cette demande de {duree} jours dépasserait la limite.", {
                "conges_deja_pris": conges_maladie_annee,
                "duree_demandee": duree,
                "limite_annuelle": 90
            }
        
        justificatif_requis = duree > 3
        
        infos = {
            "duree": duree,
            "conges_deja_pris_12mois": conges_maladie_annee,
            "total_avec_demande": total_avec_demande,
            "justificatif_medical_requis": justificatif_requis,
            "note": "Certificat médical requis" if justificatif_requis else "Certificat médical recommandé"
        }
        
        message = f"Congé de maladie validé : {duree} jours."
        if justificatif_requis:
            message += " ⚠️ CERTIFICAT MÉDICAL OBLIGATOIRE (durée > 3 jours)"
        
        return True, message, infos
    
    def valider_conge_maternite(self, solde: int, duree: int, date_debut: str, date_fin: str, **kwargs) -> Tuple[bool, str, Dict]:
        """
        Valide un congé de maternité
        Article 31 : 3 mois (90 jours), non cumulable
        """
        if duree != 90:
            return False, f"Erreur : Le congé de maternité est fixé à 90 jours (3 mois). Vous demandez {duree} jours.", {
                "duree_reglementaire": 90
            }
        
        infos = {
            "duree": 90,
            "periode": "4 semaines avant à 2 semaines avant la date présumée d'accouchement",
            "note": "Non cumulable avec d'autres congés"
        }
        
        return True, "Congé de maternité validé : 90 jours (3 mois). ⚠️ Justificatif médical requis.", infos
    
    def valider_conge_paternite(self, solde: int, duree: int, date_debut: str, date_fin: str, **kwargs) -> Tuple[bool, str, Dict]:
        """
        Valide un congé de paternité
        Article 32 : 15 jours à partir de la date d'accouchement
        """
        if duree > 15:
            return False, f"Erreur : Le congé de paternité est limité à 15 jours. Vous demandez {duree} jours.", {
                "duree_max": 15
            }
        
        infos = {
            "duree": duree,
            "duree_reglementaire": 15,
            "periode": "À partir de la date d'accouchement",
            "note": "Non cumulable avec d'autres congés"
        }
        
        return True, f"Congé de paternité validé : {duree} jours. ⚠️ Justificatif requis (acte de naissance).", infos
    
    def valider_conge_formation(self, solde: int, duree: int, date_debut: str, date_fin: str, **kwargs) -> Tuple[bool, str, Dict]:
        """
        Valide un congé pour formation
        Article 10-11 : Accord du Ministre chargé de la Fonction Publique requis
        """
        infos = {
            "duree": duree,
            "autorite_concedante": "Ministre chargé de la Fonction Publique",
            "prerequis": "Avis favorable du Ministre employeur",
            "note": "Non cumulable avec d'autres congés"
        }
        
        return True, f"Congé de formation validé : {duree} jours. ⚠️ Requiert l'accord du Ministre de la Fonction Publique après avis favorable du Ministre employeur.", infos
    
    def valider_conge_education(self, solde: int, duree: int, date_debut: str, date_fin: str, **kwargs) -> Tuple[bool, str, Dict]:
        """
        Valide un congé pour éducation sociale, civique et syndicale
        Article 12-13 : Accord du Ministre employeur requis
        """
        infos = {
            "duree": duree,
            "autorite_concedante": "Ministre employeur",
            "domaines": "Social, civique et syndical",
            "note": "Non cumulable avec d'autres congés"
        }
        
        return True, f"Congé pour éducation validé : {duree} jours (domaines social, civique et syndical). ⚠️ Requiert l'accord du Ministre employeur.", infos
    
    def valider_conge_sans_solde(self, solde: int, duree: int, date_debut: str, date_fin: str, **kwargs) -> Tuple[bool, str, Dict]:
        """
        Valide un congé sans solde
        """
        infos = {
            "duree": duree,
            "type": "Congé sans solde",
            "note": "Aucune rémunération pendant cette période"
        }
        
        return True, f"Congé sans solde validé : {duree} jours. ⚠️ Aucun traitement ne sera versé pendant cette période.", infos
    
    def valider_conge_evenements(self, solde: int, duree: int, date_debut: str, date_fin: str, **kwargs) -> Tuple[bool, str, Dict]:
        """
        Valide un congé pour événements familiaux
        """
        infos = {
            "duree": duree,
            "evenements_concernes": "Mariage, décès familial, naissance, etc.",
            "note": "Justificatifs requis"
        }
        
        return True, f"Congé pour événements familiaux validé : {duree} jours. ⚠️ Justificatifs requis.", infos
    
    # ========== PERMISSIONS ==========
    
    def valider_permission(self, solde: int, duree: int, date_debut: str, date_fin: str, **kwargs) -> Tuple[bool, str, Dict]:
        """
        Valide une permission d'absence
        Article 36-38 : Durée ≤ 20 jours, max 20 jours sur 6 ans consécutifs
        Uniquement pour ceux qui optent pour congés annuels cumulés
        """
        if duree > 20:
            return False, f"Erreur : Une permission d'absence ne peut excéder 20 jours. Vous demandez {duree} jours.", {
                "duree_max": 20
            }
        
        permissions_6ans = kwargs.get('permissions_6_ans', 0)
        total_avec_demande = permissions_6ans + duree
        
        if total_avec_demande > 20:
            return False, f"Erreur : Vous avez déjà pris {permissions_6ans} jours de permission sur les 6 dernières années. Le maximum est de 20 jours. Cette demande dépasserait la limite.", {
                "permissions_deja_prises": permissions_6ans,
                "duree_demandee": duree,
                "limite_6ans": 20
            }
        
        infos = {
            "duree": duree,
            "permissions_deja_prises_6ans": permissions_6ans,
            "total_avec_demande": total_avec_demande,
            "prerequis": "Option pour congés annuels cumulés",
            "note": "L'octroi est subordonné aux nécessités du service"
        }
        
        return True, f"Permission d'absence validée : {duree} jours. Total sur 6 ans : {total_avec_demande}/20 jours.", infos
    
    # ========== AUTORISATIONS ==========
    
    def valider_autorisation_ordinaire(self, solde: int, duree: int, date_debut: str, date_fin: str, **kwargs) -> Tuple[bool, str, Dict]:
        """
        Valide une autorisation d'absence ordinaire
        Article 40 : Événements familiaux, max 3 jours
        """
        if duree > 3:
            return False, f"Erreur : Une autorisation d'absence ordinaire ne peut excéder 3 jours. Vous demandez {duree} jours. Au-delà de 3 jours, il s'agit d'une fraction de congé annuel.", {
                "duree_max": 3,
                "alternative": "Utiliser le congé annuel pour une durée supérieure"
            }
        
        evenement = kwargs.get('evenement', 'Non spécifié')
        
        infos = {
            "duree": duree,
            "evenement": evenement,
            "evenements_valides": ["Naissance d'un enfant", "Mariage du fonctionnaire ou de son enfant", 
                                  "Décès du conjoint, père, mère ou enfant", "Maladie grave du conjoint ou enfant"],
            "note": "Avec solde entière"
        }
        
        return True, f"Autorisation d'absence ordinaire validée : {duree} jours pour {evenement}. ⚠️ Justificatif requis.", infos
    
    def valider_autorisation_election(self, solde: int, duree: int, date_debut: str, date_fin: str, **kwargs) -> Tuple[bool, str, Dict]:
        """
        Valide une autorisation spéciale pour candidats aux élections
        Article 41 : Max 20 jours pendant la campagne électorale
        """
        if duree > 20:
            return False, f"Erreur : L'autorisation pour campagne électorale ne peut excéder 20 jours. Vous demandez {duree} jours.", {
                "duree_max": 20
            }
        
        infos = {
            "duree": duree,
            "type": "Candidat aux élections politiques",
            "periode": "Pendant la campagne électorale",
            "note": "Pour impossibilité d'assurer les fonctions normales"
        }
        
        return True, f"Autorisation spéciale (élections) validée : {duree} jours. ⚠️ Justificatif de candidature requis.", infos
    
    def valider_autorisation_syndicale(self, solde: int, duree: int, date_debut: str, date_fin: str, **kwargs) -> Tuple[bool, str, Dict]:
        """
        Valide une autorisation pour représentants syndicaux
        Article 42 : Durée = durée des réunions (délai de route non compris)
        """
        duree_reunion = kwargs.get('duree_reunion', duree)
        
        infos = {
            "duree": duree,
            "duree_reunion": duree_reunion,
            "type": "Représentant syndical mandaté",
            "occasions": "Congrès professionnel, syndical, fédéral ou international",
            "note": "Délai de route non compris dans la durée"
        }
        
        return True, f"Autorisation syndicale validée : {duree} jours. ⚠️ Mandat et convocation requis.", infos


# Pour tests
if __name__ == "__main__":
    gestionnaire = GestionAbsences()
    
    print("=== Tests de Validation ===\n")
    
    # Test congé annuel
    print("1. Congé annuel (20 jours, solde: 45)")
    valide, message, infos = gestionnaire.valider_demande(
        "Congé annuel", 45, "01/01/2026", "20/01/2026"
    )
    print(f"   Valide: {valide}")
    print(f"   Message: {message}\n")
    
    # Test congé maladie
    print("2. Congé maladie (10 jours)")
    valide, message, infos = gestionnaire.valider_demande(
        "Congé maladie", 45, "01/02/2026", "10/02/2026",
        conges_maladie_precedents=15
    )
    print(f"   Valide: {valide}")
    print(f"   Message: {message}\n")
    
    # Test permission
    print("3. Permission (5 jours, déjà 10 jours pris)")
    valide, message, infos = gestionnaire.valider_demande(
        "Permission d'absence", 45, "01/03/2026", "05/03/2026",
        permissions_6_ans=10
    )
    print(f"   Valide: {valide}")
    print(f"   Message: {message}\n")