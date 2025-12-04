#calcul conge pour fonctionnaire
# This code snippet seems to be calculating the duration between two dates and checking if a certain
# condition is met to determine if a person can take a leave of absence. Here's a breakdown of what
# the code is doing:
import datetime
from typing import Type
import os
# #def calcul_solde_conge(self, nom_fonc, etat_demande,duree,date_debut,date_dmd):#solde de conge_annuel_cumule
# date_debut = datetime.date(1990,2,15)
# date_dmd = datetime.date(1991,3,1)
# dmd_etat = input("Veuiller entrer l'etat de la demande")
# dmd_etat.lower
# nom_fonc = "Jean"
# duree = date_dmd - date_debut
# strd = str(duree)
# x = strd.split(' ')
# duree = int(x[0])
# print(duree)
# if duree > 365  and dmd_etat == " valide" :
#     print(f"{nom_fonc} peut prendre un congé de 30jours dont 15 jours obligatoire")
# elif duree > 365  and dmd_etat == "en attente":
#     print(f"{nom_fonc} doit attendre la validation de son boss")
# elif duree > 365  and dmd_etat == "echec":
#     print(f"{nom_fonc} ne peut pas prendre de congé")
# else:
#     print("dsl vous n'avez pas encore atteint 1 ans effctif")
        



#CODE PAR MOI 
# date_entrer_en_service = datetime.date(2020,5,10)
# date_demande = datetime.date(2024,6,15)
# duree_service = date_demande - date_entrer_en_service
# duree_service = str(duree_service)
# duree_service = duree_service.split(' ')
# duree_service=duree_service[0]
# duree_service=float(duree_service)
# print(duree_service)
# if duree_service >= 365:
#     pass
os.system('cls')



#  Calcul de la durée de service précise (Années et Mois complets) 
def calculer_duree_service_precise(date_entree, date_demande):
    """
    Calcule le nombre d'années complètes de service et le nombre de mois restants.
    
    """
    if date_demande < date_entree:
        return 0, 0, 0 # Service négatif
                        #util dans le cas ou la date de demande = 10/01/2021 la date d'entrée en service = 10/12/2020
        
    # Calculer le nombre total de mois
    total_mois = (date_demande.year - date_entree.year) * 12 + date_demande.month - date_entree.month
    """  
    (date_demande.year - date_entree.year) * 12 :calcule la duree d'entrer en service(calculer en mois)
    date_demande.month - date_entree.month: calcule le mois en cours après avoir verifier qu'il a effectuer 1 ans complet 
       
    """
    
    # Ajustement si le jour de demande est avant le jour d'entrée (le mois n'est pas complet)
    if date_demande.day < date_entree.day:
        total_mois -= 1
        
    annee_service_completes = total_mois // 12
    mois_restants = total_mois % 12
    
    # Pour le calcul des congés, on travaille avec les mois complets
    return annee_service_completes, mois_restants, total_mois

#Calcul du Congé Cumulable (avec règle des 5 ans)
def calcul_conge_cumul(annee_service_completes, mois_service_annee_courante, jrs_conge_pris):
    """
    

    annee_service_completes: Nombre d'années complètes de service (N).
    mois_service_annee_courante: Nombre de mois dans l'année incomplète (0-11) mais après 1 ans complet.
    jrs_conge_pris: Total des jours de congés déjà pris.
    """ 
    
    # 1. Constantes
    JOURS_PAR_MOIS = 2.5                    # Jours de congé acquis par mois (30/12)
    JOURS_REPORTABLES_PAR_AN = 15.0         # Jours maximum cumulables par année complète

    if annee_service_completes < 1 and mois_service_annee_courante < 1:
        return {
            "Statut": "Pas de droit de congé annuel (Moins d'un an de service effectif).",
            "Solde cumulable restant": 0.0
        }

    # 2. Gestion du PLAFOND GLISSANT de Report (5 ANS)
    # Le droit de report n'est conservé que pour les 5 dernières années complètes.
    annees_reportables_retenues = min(annee_service_completes, 5)
    
    # 3. Calcul du Stock Reportable Maximum (Plafond Théorique)
    # Ceci est le stock maximum qui PEUT être cumulé à un instant T (max 75 jours).
    stock_reportable_max = annees_reportables_retenues * JOURS_REPORTABLES_PAR_AN

    # 4. Calcul du Droit Acquis Total
    total_mois_service = (annee_service_completes * 12) + mois_service_annee_courante
    conges_acquis_total = total_mois_service * JOURS_PAR_MOIS
    
    # 5. Déduction des Congés déjà pris
    
    # 5.1. Congés Obligatoires (la partie non-reportable : 15 jours/an)
    conges_obligatoires_theoriques = annee_service_completes * 15.0
    
    # 5.2. Jours pris au-delà de la fraction obligatoire
    # Ce sont ces jours qui entament le stock cumulable reporté.
    prise_au_dela_obligatoire = max(0.0, jrs_conge_pris - conges_obligatoires_theoriques)
    
    # 6. Solde Cumulable Restant
    solde_cumulable_restant = max(0.0, stock_reportable_max - prise_au_dela_obligatoire)
    
    # 7. Solde Total Restant (utile pour info)
    solde_conges_restant_brut = max(0.0, conges_acquis_total - jrs_conge_pris)

    return {
        "Total_mois_service": total_mois_service,
        "Conges_Acquis_Total": round(conges_acquis_total, 2),
        "Conges_Pris": jrs_conge_pris,
        "Stock_Reportable_Max": round(stock_reportable_max, 2),
        "Solde_Cumulable_Restant": round(solde_cumulable_restant, 2),
        "Solde_Total_Restant_Brut": round(solde_conges_restant_brut, 2),
        "Avertissement_Plafond": f"Le droit de report est plafonné aux 5 dernières années complètes." if annee_service_completes > 5 else "Plafond de 5 ans non atteint."
    }



date_entrer_en_service = datetime.date(2020, 10, 15)
date_demande = datetime.date(2022, 5, 20)
jours_conge_deja_pris = 40.0 # Exemple de jours pris

# Calcul de la durée de service précise
annee_comp, mois_rest, total_mois = calculer_duree_service_precise(date_entrer_en_service, date_demande)

print(f"## ⏱️ Durée de Service Précise")
print(f"Date d'entrée: {date_entrer_en_service}")
print(f"Date de la demande: {date_demande}")
print(f"Période de service: **{annee_comp} ans**, **{mois_rest} mois** (total {total_mois} mois)")
print('-'*40)

# Calcul du Congé Cumulable
resultats = calcul_conge_cumul(annee_comp, mois_rest, jours_conge_deja_pris)

print("## 🧮 Résultats du Calcul des Congés Cumulables")
print(f"* Jours de congés acquis total: **{resultats['Conges_Acquis_Total']} jours**")
print(f"* Jours de congés déjà pris: **{resultats['Conges_Pris']} jours**")
print(f"* Stock reportable MAX (sur 5 ans): **{resultats['Stock_Reportable_Max']} jours**")
print(f"\n**SOLDE DE CONGÉ CUMULABLE RESTANT:** **{resultats['Solde_Cumulable_Restant']} jours**")
print(f"\n* Solde total de congés (toutes fractions): {resultats['Solde_Total_Restant_Brut']} jours")
print(f"* Note: {resultats['Avertissement_Plafond']}")