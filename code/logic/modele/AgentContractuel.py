"""  
NOTE 
status : EFA , ELD, ECD, EMO, ES 
id_cadre : clé etrangere de la classe Crade

"""
from . import Personnel
import uuid
class AgentContractuel(Personnel.Personnel):
    def __init__(self, num_matricule, nom, prenom, date_naissance, lieu_naissance, date_entree, date_sortie, objet_depart, position,statut,id_cadre):
        super().__init__(num_matricule, nom, prenom, date_naissance, lieu_naissance, date_entree, date_sortie, objet_depart, position)
       
        self._statut = statut
        self._id_cadre = id_cadre
        self.id_ag = uuid.uuid4()
    #setter
    @property
    def statut(self):
        return self._statut
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
  #setter
    @statut.setter
    def statut(self,value):
        self._statut = value
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


