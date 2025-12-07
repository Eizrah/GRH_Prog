# Calcul du congé annuel cumulé pour le personnel
import datetime
import math # Pour utiliser math.floor pour arrondir

# --- FONCTION ORIGINALEMENT FOURNIE (RENOMMÉE POUR CLARTÉ) ---

def calculer_conge_cumule_simplifie(date_entree: datetime.date, date_demande: datetime.date, jours_par_an: int = 15, silent: bool = False) -> int:
    """
    [Logique Simplifiée] Calcule le congé cumulé en jours entre deux dates, en appliquant 
    une règle de cumul maximale de 5 années glissantes sur la totalité (jours_par_an).
    
    Args:
        date_entree (datetime.date): La date d'entrée en service (début du cumul).
        date_demande (datetime.date): La date à laquelle le solde est demandé.
        jours_par_an (int): Le nombre de jours de congé attribué par année complète.
        silent (bool): Si True, supprime les messages de débogage.

    Returns:
        int: Le solde de congé cumulé total en jours.
    """
    
    # 1. Initialisation
    conges_par_annee = {} 
    annee_debut_cumul = date_entree.year + 1
    annee_fin_cumul = date_demande.year
    
    if annee_fin_cumul <= annee_debut_cumul:
        if not silent:
            print("Aucune année complète de service n'est écoulée pour le cumul de congés.")
        return 0

    # 2. Boucle de Cumul Annuel (Logique du code original)
    if not silent:
        print(f"\n--- Calcul des Congés Cumulés (Simplifié) entre {annee_debut_cumul} et {annee_fin_cumul} ---")
    
    for annee_courante in range(annee_debut_cumul, annee_fin_cumul + 1):
        
        # A. Ajout du congé pour l'année courante
        conges_par_annee[annee_courante] = jours_par_an
        if not silent:
            print(f"✅ ANNEE {annee_courante}: {jours_par_an} jours ajoutés.")
        
        # B. Application de la règle de 5 ans glissants
        if len(conges_par_annee) > 5:
            annees_triees = sorted(conges_par_annee.keys())
            annee_a_supprimer = annees_triees[0] 
            jours_retires = conges_par_annee.pop(annee_a_supprimer)
            
            if not silent:
                print(f"❌ RÈGLE DES 5 ANS: L'année {annee_a_supprimer} est supprimée. Retrait de {jours_retires} jours.")
            
        # C. Affichage du solde de l'année
        solde_actuel = sum(conges_par_annee.values())
        if not silent:
            print(f"   --> SOLDE À FIN {annee_courante}: {solde_actuel} jours.")

    # 3. Résultat Final
    solde_final = sum(conges_par_annee.values())
    if not silent:
        print("---------------------------------------------------------")
        print(f"**CONGÉ CUMULÉ TOTAL final au {date_demande.strftime('%Y-%m-%d')}: {solde_final} jours**")
        print("---------------------------------------------------------")
    
    return solde_final


# --- NOUVELLE FONCTION BASÉE SUR L'ARTICLE 8 ---

def calculer_conge_cumule_article_8(
    date_entree: datetime.date, 
    date_demande: datetime.date, 
    jours_fraction_cumulable: int = 15, 
    permissions_absence_total: int = 0, # Total des jours de permission d'absence sur les 6 ans
    silent: bool = False
) -> int:
    """
    [Article 8] Calcule le congé cumulé spécial basé sur la deuxième fraction de 15 jours,
    pour un bénéfice après six années de service (6 fractions de 15 jours).

    Args:
        date_entree (datetime.date): La date d'entrée en service.
        date_demande (datetime.date): La date à laquelle le solde est demandé.
        jours_fraction_cumulable (int): La taille de la fraction cumulable (par défaut 15 jours).
        permissions_absence_total (int): Jours de permission d'absence sur les 6 ans.
        silent (bool): Si True, supprime les messages de débogage.

    Returns:
        int: Le solde de congé cumulé total spécial en jours (0, 60, ou 80).
    """
    
    # Nombre de jours dans 2 mois (4 semaines de 5 jours ouvrables = 40 jours)
    # Dans un contexte de congé légal (souvent 5 jours/semaine), 2 mois civils est souvent 60 jours
    # (30 jours * 2 mois) ou 40 jours ouvrables. Le décret parle de "mois", prenons 30 jours/mois.
    # 2 mois = 60 jours. 2 mois et 20 jours = 80 jours.
    PLAFOND_2_MOIS = 60  # Jours (Article 8.1 : 2 mois)
    PLAFOND_2_MOIS_20_J = 80 # Jours (Article 8.2 : 2 mois et 20 jours)
    PERIODE_DE_CUMUL_ANNEES = 6 # Le cumul spécial est acquis APRES six années

    # 1. Calculer le nombre d'années complètes de service
    annee_debut_cumul = date_entree.year + 1
    annee_fin_cumul = date_demande.year
    nombre_annees_service = max(0, annee_fin_cumul - annee_debut_cumul + 1)
    
    if not silent:
        print(f"\n--- Calcul des Congés Cumulés (Article 8) ---")
        print(f"Période de service complète calculée : {annee_debut_cumul} à {annee_fin_cumul} ({nombre_annees_service} années)")


    # 2. Vérifier si les 6 années de service sont atteintes
    if nombre_annees_service < PERIODE_DE_CUMUL_ANNEES:
        if not silent:
            print(f"Service insuffisant. Le congé cumulé Article 8 est acquis après {PERIODE_DE_CUMUL_ANNEES} années.")
        return 0
    
    # 3. Calculer le cumul maximal théorique
    # Le cumul théorique est de 6 fractions de 15 jours = 90 jours
    cumul_theorique = PERIODE_DE_CUMUL_ANNEES * jours_fraction_cumulable
    
    # 4. Déterminer le plafond applicable (Article 8.1 et 8.2)
    
    # Article 8.1 : Permissions n'excédant pas 20 jours -> Plafond de 2 mois (60 jours)
    if permissions_absence_total > 0 and permissions_absence_total <= 20:
        solde_final = PLAFOND_2_MOIS # 60 jours
        if not silent:
            print(f"Conditions de l'Article 8.1 remplies (Permissions <= 20 jours: {permissions_absence_total} jours).")
            print(f"→ Plafond appliqué : **{PLAFOND_2_MOIS} jours** (Deux mois).")

    # Article 8.2 : Aucune permission d'absence -> Plafond de 2 mois et 20 jours (80 jours)
    elif permissions_absence_total == 0:
        solde_final = PLAFOND_2_MOIS_20_J # 80 jours
        if not silent:
            print(f"Conditions de l'Article 8.2 remplies (Aucune permission d'absence).")
            print(f"→ Plafond appliqué : **{PLAFOND_2_MOIS_20_J} jours** (Deux mois et vingt jours).")

    # Si les permissions dépassent 20 jours, l'éligibilité au dispositif spécial de cumul pourrait être perdue.
    else:
        solde_final = 0
        if not silent:
            print(f"Permissions d'absence ({permissions_absence_total} jours) > 20 jours. Le droit au congé cumulé spécial Article 8 semble perdu.")
            
    # La règle du délai de route (5 jours max aller-retour) est une donnée informative et de
    # transport (Article 9), elle n'est pas utilisée dans le calcul du solde final en jours.
    
    if not silent:
        print("---------------------------------------------------------")
        print(f"**CONGÉ CUMULÉ SPÉCIAL (Article 8) final au {date_demande.strftime('%Y-%m-%d')}: {solde_final} jours**")
        print("---------------------------------------------------------")
        
    return solde_final

# 4. Exemple d'utilisation
#--------------------------------------------------------------------------------

if __name__ == "__main__":
    import os
    os.system('cls')
    
    # --- Exemples de la logique Simplifiée (votre code initial) ---
    print("\n\n#####################################################")
    print("## UTILISATION DE LA LOGIQUE SIMPLIFIÉE (5 ans glissants) ##")
    print("#####################################################")
    
    date_entrer_ex1 = datetime.date(2020, 10, 21)
    date_dmd_ex1 = datetime.date(2022, 5, 29) # Années complètes : 2021, 2022.
    print("\n### EXEMPLE S1 : Cumul simple ###")
    conge_total_ex1 = calculer_conge_cumule_simplifie(date_entrer_ex1, date_dmd_ex1)

    date_entrer_ex2 = datetime.date(2018, 1, 1) # Entrée en 2018
    date_dmd_ex2 = datetime.date(2025, 1, 1)   # Années : 2019, 2020, 2021, 2022, 2023, 2024 (6 ans)
    print("\n### EXEMPLE S2 : Cas de suppression (A1 sera supprimé) ###")
    conge_total_ex2 = calculer_conge_cumule_simplifie(date_entrer_ex2, date_dmd_ex2)


    # --- Exemples de la logique Article 8 ---
    print("\n\n#####################################################")
    print("## UTILISATION DE LA LOGIQUE SPÉCIALE (Article 8) ##")
    print("#####################################################")
    
    # Cas A : Moins de 6 ans de service
    date_entrer_a = datetime.date(2021, 1, 1)
    date_dmd_a = datetime.date(2025, 1, 1) # 4 ans complets (2022, 2023, 2024)
    print("\n### EXEMPLE A : Moins de 6 ans de service ###")
    conge_total_a = calculer_conge_cumule_article_8(date_entrer_a, date_dmd_a, permissions_absence_total=0)
    
    # Cas B : 6 ans et aucune permission d'absence -> 2 mois et 20 jours (80 jours)
    date_entrer_b = datetime.date(2018, 1, 1)
    date_dmd_b = datetime.date(2025, 1, 1) # 6 ans complets (2019 à 2024)
    print("\n### EXEMPLE B : 6 ans et 0 jour de permission ###")
    conge_total_b = calculer_conge_cumule_article_8(date_entrer_b, date_dmd_b, permissions_absence_total=0)

    # Cas C : 6 ans et permissions <= 20 jours -> 2 mois (60 jours)
    date_entrer_c = datetime.date(2018, 1, 1)
    date_dmd_c = datetime.date(2025, 1, 1) # 6 ans complets (2019 à 2024)
    print("\n### EXEMPLE C : 6 ans et 15 jours de permission ###")
    conge_total_c = calculer_conge_cumule_article_8(date_entrer_c, date_dmd_c, permissions_absence_total=15)
    
    # Cas D : 6 ans et permissions > 20 jours -> Perte du bénéfice spécial (0 jour)
    date_entrer_d = datetime.date(2018, 1, 1)
    date_dmd_d = datetime.date(2025, 1, 1) # 6 ans complets (2019 à 2024)
    print("\n### EXEMPLE D : 6 ans et 25 jours de permission ###")
    conge_total_d = calculer_conge_cumule_article_8(date_entrer_d, date_dmd_d, permissions_absence_total=25)