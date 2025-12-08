import datetime

def calculer_conge_cumule(date_entree: datetime.date, date_demande: datetime.date, jours_par_an: int = 15, silent: bool = False) -> int:
    """
    Calcule le congé cumulé en jours entre deux dates, en appliquant une règle de 
    cumul maximale de 5 années glissantes.
    
    IMPORTANT: Le solde ne commence qu'à partir de l'année suivante l'entrée.
    Si la date_demande est dans la même année que date_entree, le solde est 0.
    """
    
    # 1. Vérification que la date_demande est après la date_entree
    if date_demande <= date_entree:
        if not silent:
            print("La date de demande doit être postérieure à la date d'entrée.")
        return 0
    
    # 2. Initialisation
    conges_par_annee = {}
    
    # L'année de départ du calcul est l'année SUIVANTE l'entrée
    annee_debut_cumul = date_entree.year + 1
    annee_fin_cumul = date_demande.year
    
    # Si l'année de début est supérieure à l'année de fin, solde = 0
    if annee_debut_cumul > annee_fin_cumul:
        if not silent:
            print(f"Aucune année complète de service: entrée {date_entree.year}, demande {date_demande.year}")
        return 0
    
    # 3. Boucle de cumul
    if not silent:
        print(f"\n--- Calcul des Congés Cumulés entre {annee_debut_cumul} et {annee_fin_cumul} ---")
    
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
    
    # 4. Résultat Final
    solde_final = sum(conges_par_annee.values())
    
    # Le solde inclut toutes les années accumulées, y compris l'année en cours
    # car les congés se cumulent progressivement
    
    if not silent:
        print("---------------------------------------------------------")
        print(f"**CONGÉ CUMULÉ TOTAL final au {date_demande.strftime('%Y-%m-%d')}: {solde_final} jours**")
        print("---------------------------------------------------------")
    
    return max(0, solde_final)  # Garantir que le solde n'est pas négatif

# Ajout d'une fonction pour calculer le solde initial (0 jours)
def solde_initial(date_entree: datetime.date, date_aujourdhui: datetime.date = None) -> int:
    """
    Retourne 0 si moins d'un an de service, sinon calcule normalement
    """
    if date_aujourdhui is None:
        date_aujourdhui = datetime.date.today()
    
    # Si moins d'un an, solde = 0
    if (date_aujourdhui - date_entree).days < 365:
        return 0
    
    return calculer_conge_cumule(date_entree, date_aujourdhui, silent=True)