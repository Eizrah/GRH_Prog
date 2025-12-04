#CODE GEMINI    
def calculer_conge_cumule_fonctionnaire_mg(annees_service_completes, mois_service_annee_courante, conges_pris_total):
    """
    Calcule le droit aux congés annuels et le solde cumulable d'un fonctionnaire
    à Madagascar, en intégrant la règle de report glissant sur 5 ans.

    Args:
        annees_service_completes (int): Nombre d'années de service complètes (N).
        mois_service_annee_courante (int): Nombre de mois de service dans l'année en cours (0-11).
        conges_pris_total (float): Total des jours de congés déjà pris pendant toute la période.

    Returns:
        dict: Détails des congés acquis, du plafond de cumul, et du solde restant.
    """
    
    # 1. Constantes
    JOURS_PAR_MOIS = 2.5                    # 30 jours / 12 mois
    JOURS_REPORTABLES_PAR_AN = 15.0         # Le maximum cumulable par année complète
    
    # 2. Calcul du Droit Acquis Total (inclut l'année en cours)
    total_mois_service = (annees_service_completes * 12) + mois_service_annee_courante
    conges_acquis_total = total_mois_service * JOURS_PAR_MOIS

    # 3. Gestion du PLAFOND GLISSANT de Report (5 ANS)
    
    # Le droit de report n'est conservé que pour les 5 dernières années complètes.
    
    # Nombre d'années reportables (maximum 5)
    annees_reportables_retenues = min(annees_service_completes, 5)
    
    # 4. Calcul du Stock Reportable Maximum (Plafond Théorique)
    stock_reportable_max = annees_reportables_retenues * JOURS_REPORTABLES_PAR_AN

    # 5. Déduction des Congés déjà pris
    
    # 5.1. Congés Obligatoires (la partie non-reportable)
    # On suppose que 15 jours/an (la partie obligatoire) doivent être pris chaque année.
    conges_obligatoires_theoriques = annees_service_completes * 15.0
    
    # 5.2. Jours pris au-delà de la fraction obligatoire
    # Ce sont ces jours qui entament le stock cumulable reporté.
    prise_au_dela_obligatoire = max(0.0, conges_pris_total - conges_obligatoires_theoriques)
    
    # 6. Calcul du Solde Cumulable Restant
    
    solde_cumulable_restant = stock_reportable_max - prise_au_dela_obligatoire
    
    # 7. Calcul du Solde Total Restant (Acquis total - Pris)
    solde_conges_restant_brut = conges_acquis_total - conges_pris_total

    # 8. Indicateur de Dépassement
    depassement_annee = 0
    if annees_service_completes > 5:
        # Si N > 5, le droit de l'Année N-5 (la plus ancienne) est perdu.
        depassement_annee = annees_service_completes - 5
        
    return {
        "annees_service_completes": annees_service_completes,
        "conges_acquis_total_jours": round(conges_acquis_total, 2),
        "conges_pris_total_jours": conges_pris_total,
        "annees_reportables_retenues": annees_reportables_retenues,
        "stock_reportable_max_jours": round(stock_reportable_max, 2),
        "solde_cumulable_restant_jours": round(max(0.0, solde_cumulable_restant), 2),
        "solde_conges_restant_brut_jours": round(solde_conges_restant_brut, 2),
        "avertissement_depassement": f"L'Année {depassement_annee} est 'effacée' du stock de report glissant." if depassement_annee > 0 else "Aucun dépassement du plafond de 5 ans."
    }

# --- EXEMPLE D'UTILISATION ---

# Scénario 1 : 4 ans complets. Le cumul est OK.
print("## 📝 Scénario 1 : 4 Années (Dans le Plafond)")
resultat_4ans = calculer_conge_cumule_fonctionnaire_mg(4, 0, 10.0) # 4 ans complets, 10 jours pris
print(f"Années reportables retenues : {resultat_4ans['annees_reportables_retenues']} ans")
print(f"Stock cumulable max (15j x 4) : {resultat_4ans['stock_reportable_max_jours']} jours")
print(f"Solde cumulable restant : {resultat_4ans['solde_cumulable_restant_jours']} jours")
print(f"Avertissement : {resultat_4ans['avertissement_depassement']}")
print("-" * 20)

# Scénario 2 : 7 ans complets. Le cumul de l'Année 2 (N-5) est effacé.
print("## 📝 Scénario 2 : 7 Années (Dépassement de 5 ans)")
resultat_7ans = calculer_conge_cumule_fonctionnaire_mg(7, 0, 105.0) # 7 ans complets, 105 jours pris (7 * 15j)
print(f"Années reportables retenues : {resultat_7ans['annees_reportables_retenues']} ans (Seulement les 5 dernières sont comptées)")
print(f"Stock cumulable max (15j x 5) : {resultat_7ans['stock_reportable_max_jours']} jours")
print(f"Solde cumulable restant : {resultat_7ans['solde_cumulable_restant_jours']} jours")
print(f"Avertissement : {resultat_7ans['avertissement_depassement']}")  

