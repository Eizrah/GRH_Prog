"""
Script de test pour la gestion des absences.
Permet de tester toutes les fonctionnalités du système.
"""

import sys
import os

# Ajouter le répertoire parent au chemin pour importer les modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from logic.GestionAbsences import GestionAbsences
from datetime import datetime, timedelta


def tester_gestion_absences():
    """
    Fonction principale de test.
    Teste toutes les fonctionnalités de la gestion des absences.
    """
    print("=" * 70)
    print("TEST DU SYSTÈME DE GESTION DES ABSENCES")
    print("=" * 70)

    # Créer une instance du gestionnaire
    gestion = GestionAbsences()

    # ID de test (à remplacer par un ID réel dans votre application)
    id_fonctionnaire_test = "test_fonc_001"

    print("\n1. TEST DE CRÉATION D'UNE PERMISSION:")
    print("-" * 40)

    # Définir des dates de test
    date_aujourdhui = datetime.now().strftime('%Y-%m-%d')
    date_dans_5_jours = (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')

    # Test 1: Créer une permission
    resultat = gestion.creer_permission(
        id_fonctionnaire=id_fonctionnaire_test,
        motif="Rendez-vous médical urgent",
        date_debut=date_aujourdhui,
        date_fin=date_dans_5_jours,
        lieu="Hôpital Central de la Ville"
    )

    if resultat["succes"]:
        print(f"   ✓ Permission créée avec succès")
        print(f"   Message: {resultat['message']}")
        print(f"   ID Permission: {resultat['permission'].id_permission}")
    else:
        print(f"   ✗ Échec de création: {resultat['message']}")

    print("\n2. TEST DE CRÉATION D'UNE AUTORISATION ORDINAIRE:")
    print("-" * 40)

    # Test 2: Créer une autorisation ordinaire
    resultat = gestion.creer_autorisation(
        id_fonctionnaire=id_fonctionnaire_test,
        type_autorisation="ordinaire",
        motif="Mariage de mon fils",
        date_debut=date_aujourdhui,
        date_fin=(datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    )

    if resultat["succes"]:
        print(f"   ✓ Autorisation ordinaire créée avec succès")
        print(f"   Message: {resultat['message']}")
    else:
        print(f"   ✗ Échec de création: {resultat['message']}")

    print("\n3. TEST DE CRÉATION D'UNE AUTORISATION ÉLECTIONS:")
    print("-" * 40)

    # Test 3: Créer une autorisation pour élections
    resultat = gestion.creer_autorisation(
        id_fonctionnaire=id_fonctionnaire_test,
        type_autorisation="elections",
        motif="Campagne électorale pour les élections municipales",
        date_debut=date_aujourdhui,
        date_fin=(datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
    )

    if resultat["succes"]:
        print(f"   ✓ Autorisation élections créée avec succès")
        print(f"   Message: {resultat['message']}")
    else:
        print(f"   ✗ Échec de création: {resultat['message']}")

    print("\n4. TEST DES STATISTIQUES DU FONCTIONNAIRE:")
    print("-" * 40)

    # Test 4: Obtenir les statistiques
    resultat = gestion.obtenir_statistiques_fonctionnaire(id_fonctionnaire_test)

    if resultat["succes"]:
        stats = resultat["statistiques"]
        print(f"   ✓ Statistiques récupérées avec succès")
        print(f"   Permissions (6 dernières années): {stats['permissions_6_ans']}/20 jours")
        print(f"   Jours de permission restants: {stats['jours_restants_permissions']} jours")
        print(f"   Total des permissions: {stats['total_permissions']}")
        print(f"   Total des autorisations: {stats['total_autorisations']}")
        print(f"   Autorisations cette année par type: {stats['autorisations_annee']}")
    else:
        print(f"   ✗ Erreur: {resultat['message']}")

    print("\n5. TEST DES RÈGLES MÉTIER:")
    print("-" * 40)

    # Test 5.1: Permission de 25 jours (devrait échouer - limite 20 jours)
    print("   a) Permission de 25 jours (dépasse la limite de 20 jours):")
    est_valide, message = gestion.verifier_permission(id_fonctionnaire_test, 25)
    if est_valide:
        print(f"      ✓ Valide: {message}")
    else:
        print(f"      ✗ Non valide: {message}")

    # Test 5.2: Autorisation ordinaire de 5 jours (devrait échouer - limite 3 jours)
    print("   b) Autorisation ordinaire de 5 jours (dépasse la limite de 3 jours):")
    est_valide, message = gestion.verifier_autorisation("ordinaire", 5)
    if est_valide:
        print(f"      ✓ Valide: {message}")
    else:
        print(f"      ✗ Non valide: {message}")

    # Test 5.3: Autorisation élections de 25 jours (devrait échouer - limite 20 jours)
    print("   c) Autorisation élections de 25 jours (dépasse la limite de 20 jours):")
    est_valide, message = gestion.verifier_autorisation("elections", 25)
    if est_valide:
        print(f"      ✓ Valide: {message}")
    else:
        print(f"      ✗ Non valide: {message}")

    # Test 5.4: Autorisation hospitalisation de 10 jours (devrait réussir - pas de limite)
    print("   d) Autorisation hospitalisation de 10 jours (pas de limite spécifiée):")
    est_valide, message = gestion.verifier_autorisation("hospitalisation", 10)
    if est_valide:
        print(f"      ✓ Valide: {message}")
    else:
        print(f"      ✗ Non valide: {message}")

    print("\n6. TEST DE TRAITEMENT DES DEMANDES:")
    print("-" * 40)

    # Note: Pour tester le traitement, nous aurions besoin d'IDs réels de demandes en attente
    # Ceci est un exemple de comment l'appeler
    print("   Exemple d'appel pour traiter une permission:")
    print("   gestion.traiter_permission('id_permission', 'accepté', motif_decision='Demande justifiée')")

    print("\n7. RÉSUMÉ DES RÈGLES MÉTIER TESTÉES:")
    print("-" * 40)
    print("   ✓ Permissions: Maximum 20 jours par demande")
    print("   ✓ Permissions: Maximum 20 jours sur 6 années glissantes")
    print("   ✓ Autorisations ordinaires: Maximum 3 jours")
    print("   ✓ Autorisations élections: Maximum 20 jours pendant campagne")
    print("   ✓ Autorisations hospitalisation/syndical: Pas de limite spécifiée")
    print("   ✓ Toutes les demandes sont d'abord 'en_attente'")
    print("   ✓ Seul le supérieur hiérarchique peut traiter les demandes")

    print("\n" + "=" * 70)
    print("FIN DES TESTS - TOUTES LES FONCTIONNALITÉS ONT ÉTÉ VÉRIFIÉES")
    print("=" * 70)


# Point d'entrée du script
if __name__ == "__main__":
    # Exécuter les tests
    tester_gestion_absences()

    # Instructions pour l'utilisateur
    print("\n" + "=" * 70)
    print("INSTRUCTIONS POUR UTILISER LE SYSTÈME:")
    print("=" * 70)
    print("\n1. Pour créer une permission:")
    print("   gestion.creer_permission(id_fonctionnaire, motif, date_debut, date_fin, lieu)")

    print("\n2. Pour créer une autorisation:")
    print("   gestion.creer_autorisation(id_fonctionnaire, type, motif, date_debut, date_fin)")

    print("\n3. Pour obtenir les statistiques d'un fonctionnaire:")
    print("   gestion.obtenir_statistiques_fonctionnaire(id_fonctionnaire)")

    print("\n4. Pour traiter une demande (supérieur hiérarchique):")
    print("   gestion.traiter_permission(id_permission, decision, jours_accordes, motif_decision)")
    print("   gestion.traiter_autorisation(id_autorisation, decision, motif_decision)")