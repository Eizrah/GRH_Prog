import sqlite3
import os
from datetime import date
# Import de votre fonction existante
from logic.conge_cumule import calculer_conge_cumule
# pour savoir combien de jours de cong on a 
def obtenir_solde_reel(id_personne, type_personne, date_entree):
    """
    Calcule le solde disponible = (Droits acquis) - (Congés validés pris)
    
    Args:
        id_personne (str): id_fonc ou id_ag
        type_personne (str): "fonc" ou "agent"
        date_entree (date): La date d'embauche
    """
    
    # 1. Calculer le total acquis (La poche pleine)
    # On compare la date d'entrée à aujourd'hui pour savoir combien on a gagné
    jours_acquis = calculer_conge_cumule(date_entree, date.today(), silent=True)
    
    # 2. Calculer le total consommé (Ce qu'on a déjà mangé)
    jours_pris = 0
    
    try:
        # Chemin DB (à adapter selon votre structure de dossier)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, 'database', 'db.sqlite3')
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # La requête change légèrement selon si c'est un fonctionnaire ou un agent
        colonne_id = "id_fonc" if type_personne == "fonc" else "id_ag"
        
        # On somme les durées des congés qui sont "Accepté" ET qui sont de type "Congé annuel..."
        query = f"""
            SELECT SUM(c.duree)
            FROM Conge c
            JOIN PersoConge pc ON c.id_conge = pc.id_conge
            WHERE pc.{colonne_id} = ? 
            AND c.validation = 'Accepté'
            AND (c.type LIKE 'Congé annuel%') 
        """
        # Note: LIKE 'Congé annuel%' permet de capturer "Congé annuel" et "Congé annuel cumulé"
        
        cursor.execute(query, (id_personne,))
        result = cursor.fetchone()
        
        if result and result[0]:
            jours_pris = result[0]
            
        conn.close()
        
    except Exception as e:
        print(f"Erreur calcul jours pris: {e}")
        return 0 # Par sécurité en cas d'erreur
        
    # 3. Le résultat final
    solde_reel = jours_acquis - jours_pris
    
    return solde_reel