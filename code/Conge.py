class Conge:
    def __init__(self, id_conge, sorte_conge,duree,validation):
        self._id_conge = id_conge
        self._sorte_conge = sorte_conge
        self._duree = duree
        self._validation = validation
        
        
    @property
    def id_conge(self):
        return self._id_conge
    @id_conge.setter
    def id_conge(self, id_conge):
        self._id_conge = id_conge
        
    @property
    def sorte_conge(self):
        return self._sorte_conge
    @sorte_conge.setter
    def sorte_conge(self, sorte_conge):
        self._sorte_conge = sorte_conge
    
    @property
    def duree(self):
        return self._duree
    @duree.setter
    def duree(self, duree):
        self._duree = duree
    @property
    def validation(self):
        return self._validation
    @validation.setter
    def validation(self, validation):
        self._validation = validation
   
"""  
sorte_conge : type de congé et absence : conge annuel , conge pour formation, autorisation d'absence ordinaire , etc
validation : choix entre "en attente", "accepté", "refusé"
   
"""