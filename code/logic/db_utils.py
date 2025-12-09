import os
import sys
import shutil

def get_database_path():
    """
    Retourne le chemin vers la base de données.
    Si exécuté via PyInstaller, utilise le dossier AppData/Local/GRH_App
    pour garantir que la DB est accessible en écriture et persistante.
    """
    if getattr(sys, 'frozen', False):
        # --- MODE EXÉCUTABLE POOL ---
        # On ne peut PAS écrire dans sys._MEIPASS (dossier temporaire)
        # On va donc placer la DB dans %LOCALAPPDATA%/GRH_App
        
        base_dir = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), 'GRH_App')
        os.makedirs(base_dir, exist_ok=True)
        
        db_path = os.path.join(base_dir, 'db.sqlite3')
        
        # Si la DB n'existe pas encore dans AppData, on la copie depuis le bundle
        if not os.path.exists(db_path):
            # Dans le bundle, la DB est incluse via --add-data
            # sys._MEIPASS/database/db.sqlite3
            bundled_db_path = os.path.join(sys._MEIPASS, 'database', 'db.sqlite3')
            
            if os.path.exists(bundled_db_path):
                try:
                    shutil.copy2(bundled_db_path, db_path)
                    print(f"Initialisation: Copie de la DB vers {db_path}")
                except Exception as e:
                    print(f"Erreur copie DB: {e}")
            else:
                print(f"ERREUR CRITIQUE: Base de données source introuvable dans {bundled_db_path}")

        return db_path
        
    else:
        # --- MODE DÉVELOPPEMENT ---
        # Trouver le répertoire racine du projet (où se trouve main.py)
        if __file__:
            # Si ce fichier est dans logic/
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)  # Remonter d'un niveau
        else:
            project_root = os.getcwd()
        
        db_path = os.path.join(project_root, 'database', 'db.sqlite3')
        
        # Vérifier que la base de données existe
        if not os.path.exists(db_path):
            print(f"ATTENTION: Base de données non trouvée: {db_path}")
        
        return db_path


def get_connection():
    """
    Retourne une connexion SQLite à la base de données.
    """
    import sqlite3
    db_path = get_database_path()
    return sqlite3.connect(db_path)


if __name__ == "__main__":
    # Test
    print(f"Chemin de la base de données: {get_database_path()}")

