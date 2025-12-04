import uuid
class Emplois:
    def __init__(self, nom_poste, duree,lieu):
        self._id_emploi = uuid.uuid4()
        self._nom_poste = nom_poste
        self._duree = duree
        self._lieu = lieu
        
    @property
    def id_emploi(self):
        return self._id_emploi
    

    @property
    def nom_poste(self):
        return self._nom_poste
    
    @nom_poste.setter
    def nom_poste(self, value):
        self._nom_poste = value
        
    @property
    def duree(self):
        return self._duree
    
    @duree.setter
    def duree(self, value):
        self._duree = value