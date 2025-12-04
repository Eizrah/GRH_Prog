#classe abstraite 
from abc import ABC, abstractmethod
class Personnel(ABC):  
    def __init__(self, num_matricule, nom, prenom, date_naissance, lieu_naissance, date_entree, date_sortie, objet_depart, position):
        self._num_matricule = num_matricule
        self._nom = nom
        self._prenom = prenom
        self._date_naissance = date_naissance
        self._lieu_naissance = lieu_naissance
        self._date_entree = date_entree
        self._date_sortie = date_sortie
        self._objet_depart = objet_depart
        self._position = position
        
    
    
    
    
    @property
    @abstractmethod
    def num_matricule(self):
        return self._num_matricule
    
    
    @num_matricule.setter
    @abstractmethod  
    def num_matricule(self, value):
        self._num_matricule = value
    
    @property
    @abstractmethod
    def nom(self):
        return self._nom
    
    @nom.setter
    @abstractmethod
    def nom(self, value):
        self._nom = value
    
    @property
    @abstractmethod
    def prenom(self):
        return self._prenom
    
    @prenom.setter
    @abstractmethod
    def prenom(self, value):
        self._prenom = value
    
    @property
    @abstractmethod
    def date_naissance(self):
        return self._date_naissance
    
    @date_naissance.setter
    @abstractmethod
    def date_naissance(self, value):
        self._date_naissance = value
    
    @property
    @abstractmethod
    def lieu_naissance(self):
        return self._lieu_naissance
    
    @lieu_naissance.setter
    @abstractmethod
    def lieu_naissance(self, value):
        self._lieu_naissance = value
    
    @property
    @abstractmethod
    def date_entree(self):
        return self._date_entree
    
    @date_entree.setter
    @abstractmethod
    def date_entree(self, value):
        self._date_entree = value
    
    @property
    @abstractmethod
    def date_sortie(self):
        return self._date_sortie
    
    @date_sortie.setter
    @abstractmethod
    def date_sortie(self, value):
        self._date_sortie = value
    
    @property
    @abstractmethod
    def objet_depart(self):
        return self._objet_depart
    
    @objet_depart.setter
    @abstractmethod
    def objet_depart(self, value):
        self._objet_depart = value
   
    @property
    @abstractmethod
    def position(self):
        return self._position
   
    @position.setter
    @abstractmethod
    def position(self, value):
        self._position = value


  
    @abstractmethod
    def calcSoldeConge(self):
        pass
""" 
NOTE:
Position  peut prendre les valeurs suivantes:
  -en activité
  -en detachement
  -hors cadre
  -sous le drapeau 
  -en disponibilité

calcSoldeConge : methode pour calculer le solde de congé
"""