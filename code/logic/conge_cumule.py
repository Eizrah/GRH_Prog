# The lines `import datetime` and `import os` are used to import the `datetime` module and the `os`
# module in Python, respectively.
import datetime
import os 
os.system('cls')


# date_entrer = datetime.date(2020, 10, 21)
# date_dmd = datetime.date(2025, 5, 29)
# #------------------
# i = 1  # compteur d'années
# conge_cumule_total = 0  # Total cumulé
# #------------------

# # Calcul du nombre d'années entre les dates
# duree = date_dmd.year - date_entrer.year
# print(f"Différence en années : {duree}")

# # Boucle pour chaque année complète
# annees_completes = duree   # 2020-2022 donne 2 ans mais seulement 1 année complète (2021)

# while i <= annees_completes:
#     date = date_entrer.year + i
#     conge_cumule_total += 15  # Correction : += pas =+
#     print(f"Année {i}:  {date}: 15 jours ajoutés , total :{conge_cumule_total} jours")
#     i += 1  # Correction : += pas =+

# print(f"Congé cumulé total durant ces {annees_completes} années : {conge_cumule_total} jours")

def calculer_conge_cumule(date_entree: datetime.date, date_demande: datetime.date, jours_par_an: int = 15) -> int:
    """
    Calcule le congé cumulé en jours entre deux dates, en appliquant une règle de 
    cumul maximale de 5 années glissantes.

    Args:
        date_entree (datetime.date): La date d'entrée en service (début du cumul).
        date_demande (datetime.date): La date à laquelle le solde est demandé.
        jours_par_an (int): Le nombre de jours de congé attribué par année complète.

    Returns:
        int: Le solde de congé cumulé total en jours.
    """
    
    # 1. Initialisation
    
    # Stocke les jours de congé par année. La clé est l'année (int), la valeur est le congé (int).
    conges_par_annee = {} 
    
    # L'année de départ du calcul est l'année suivant l'entrée.
    annee_debut_cumul = date_entree.year + 1
    annee_fin_cumul = date_demande.year
    
    # Si la date d'entrée et la date de demande sont dans la même année, il n'y a pas
    # d'années complètes pour le cumul.
    if annee_fin_cumul <= annee_debut_cumul:
        print("Aucune année complète de service n'est écoulée pour le cumul de congés.")
        return 0

    # 2. Boucle de Cumul Annuel
    
    print(f"\n--- Calcul des Congés Cumulés entre {annee_debut_cumul} et {annee_fin_cumul} ---")
    
    for annee_courante in range(annee_debut_cumul, annee_fin_cumul + 1):
        
        # A. Ajout du congé pour l'année courante
        
        # Si on est en 2025, on ajoute les 15 jours pour 2025 (qui est la dernière année complète)
        conges_par_annee[annee_courante] = jours_par_an
        print(f"✅ ANNEE {annee_courante}: {jours_par_an} jours ajoutés.")
        
        # B. Application de la règle de 5 ans glissants
        
        # Le nombre maximum d'années à conserver est 5. Si la taille dépasse 5, on supprime.
        
        if len(conges_par_annee) > 5:
            # On trie les années pour s'assurer que l'on supprime la plus ancienne
            annees_triees = sorted(conges_par_annee.keys())
            annee_a_supprimer = annees_triees[0] # L'année la plus ancienne dans le dictionnaire
            
            # On stocke les jours à retirer pour l'affichage
            jours_retires = conges_par_annee.pop(annee_a_supprimer)
            
            print(f"❌ RÈGLE DES 5 ANS: L'année {annee_a_supprimer} est supprimée. Retrait de {jours_retires} jours.")
            
        # C. Affichage du solde de l'année
        
        solde_actuel = sum(conges_par_annee.values())
        print(f"   --> SOLDE À FIN {annee_courante}: {solde_actuel} jours.")

    # 3. Résultat Final
    solde_final = sum(conges_par_annee.values())
    print("---------------------------------------------------------")
    print(f"**CONGÉ CUMULÉ TOTAL final au {date_demande.strftime('%Y-%m-%d')}: {solde_final} jours**")
    print("---------------------------------------------------------")
    
    return solde_final

# 4. Exemple d'utilisation (Reprise de votre cas initial)
#--------------------------------------------------------------------------------

date_entrer_ex1 = datetime.date(2020, 10, 21)
date_dmd_ex1 = datetime.date(2022, 5, 29) # La dernière année complète est 2024 (2020->2021->2022->2023->2024)

print("\n### EXEMPLE 1 : Cas sur 5 ans (2021 à 2024) ###")
conge_total_ex1 = calculer_conge_cumule(date_entrer_ex1, date_dmd_ex1)

# 5. Exemple illustrant la règle des 5 ans (Cumul qui dépasse les 5 ans)
#--------------------------------------------------------------------------------

date_entrer_ex2 = datetime.date(2018, 1, 1) # Entrée en 2018
date_dmd_ex2 = datetime.date(2025, 1, 1)   # Solde demandé en 2025

# Années de cumul complètes : 2019, 2020, 2021, 2022, 2023, 2024 (6 années)

print("\n### EXEMPLE 2 : Cas de suppression (A1 sera supprimé) ###")
conge_total_ex2 = calculer_conge_cumule(date_entrer_ex2, date_dmd_ex2)

# Le calcul en détail pour l'exemple 2 serait :
# 2019 (Ajout, Solde=15)
# 2020 (Ajout, Solde=30)
# 2021 (Ajout, Solde=45)
# 2022 (Ajout, Solde=60)
# 2023 (Ajout, Solde=75)
# 2024 (Ajout, Solde=90. Année 2019 est supprimée -> Solde = 90 - 15 = 75)
# Résultat final : 75 jours (conges pour 2020, 2021, 2022, 2023, 2024)

