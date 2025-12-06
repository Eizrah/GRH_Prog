"""  
NOTE
id_fonc: identifiant unique du fonctionnaire
diplome: diplome du fonctionnaire
id_cadre : clé etrangere de la classe Crade
"""
from .Personnel import Personnel
import uuid
class Fonctionnaire(Personnel):
    def __init__(self, num_matricule, nom, prenom, date_naissance, lieu_naissance, date_entree, date_sortie, objet_depart, position,diplome,id_cadre):
        super().__init__(num_matricule, nom, prenom, date_naissance, lieu_naissance, date_entree, date_sortie, objet_depart, position)
        self._diplome = diplome
        self._id_cadre = id_cadre
        self.id_fonc = uuid.uuid4()

    # Dans la classe Fonctionnaire, ajoutez:

    from logic.GestionAbsences import GestionAbsences

    class Fonctionnaire(Personnel):
        # ... code existant ...

        def demander_permission(self, motif, date_debut, date_fin, lieu):
            """Méthode pour demander une permission d'absence"""
            gestion = GestionAbsences()
            return gestion.creer_permission(
                id_fonctionnaire=self.id_fonc,
                motif=motif,
                date_debut=date_debut,
                date_fin=date_fin,
                lieu=lieu
            )

        def demander_autorisation(self, type_auth, motif, date_debut, date_fin):
            """Méthode pour demander une autorisation d'absence"""
            gestion = GestionAbsences()
            return gestion.creer_autorisation(
                id_fonctionnaire=self.id_fonc,
                type_auth=type_auth,
                motif=motif,
                date_debut=date_debut,
                date_fin=date_fin
            )

        def get_statistiques_absences(self):
            """Récupère les statistiques d'absence du fonctionnaire"""
            gestion = GestionAbsences()
            return gestion.get_statistiques_fonctionnaire(self.id_fonc)
        
     
     #setter   
  
    @property
    def diplome(self):
        
        return self._diplome
    
    @property 
    def id_cadre(self):
        return self._id_cadre
    @property
    def num_matricule(self):
        return self._num_matricule
    @property
    def nom(self):
        return self._nom
    @property
    def prenom(self):
        return self._prenom
    @property
    def date_naissance(self):
        return self._date_naissance
    @property
    def lieu_naissance(self):
        return self._lieu_naissance
    @property
    def date_entree(self):
        return self._date_entree
    @property
    def date_sortie(self):
        return self._date_sortie
    @property
    def objet_depart(self):
        return self._objet_depart
    @property
    def position(self):
        return self._position
    #getter
    @diplome.setter
    def diplome(self, value):
        self._diplome = value
    @id_cadre.setter
    def id_cadre(self, value):
        self._id_cadre = value
    @nom.setter
    def nom(self,value):
        self._nom = value
    @prenom.setter
    def prenom(self,value):
        self._prenom = value
    @date_naissance.setter
    def date_naissance(self,value):
        self._date_naissance = value
    @lieu_naissance.setter
    def lieu_naissance(self,value):
        self._lieu_naissance = value
    @date_entree.setter
    def date_entree(self,value):
        self._date_entree = value
    @date_sortie.setter
    def date_sortie(self,value):
        self._date_sortie = value
    @objet_depart.setter
    def objet_depart(self,value):
        self._objet_depart = value
    @position.setter
    def position(self,value):
        self._position = value
    
    def calcSoldeConge(self):
        print("Calcul du solde de congé pour le fonctionnaire")

F1 = Fonctionnaire("01F0X","Vegeta","DBZ","12/02/1990","Planet vegeta","17/05/2001","null","null","en_activite","Master en Destruction",1)
print(F1.nom)
