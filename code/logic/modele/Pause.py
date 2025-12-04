#classe abstraitre
from abc import ABC, abstractmethod
class Pause(ABC):
    def __init__(self,  duree, validation):
       
        self._duree = duree
        self._validation = validation
       
        
   
    
    @property
    @abstractmethod
    def duree(self):
        pass
    
    @duree.setter
    @abstractmethod
    def duree(self, value):
        pass
       
    @property
    @abstractmethod
    def validation(self):
        pass
    
    @validation.setter
    @abstractmethod
    def validation(self, value):
        pass  
    
  
"""  
validation : choix entre "en attente", "accepté", "refusé"
   
"""