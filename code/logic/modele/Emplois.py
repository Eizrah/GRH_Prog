class Emplois:
    def __init__(self,id_emploi,nom_poste,duree):
        self._id_emploi = id_emploi
        self._nom_poste = nom_poste
        self._duree = duree
        
    #getter
    @property
    def id_emploi(self):
        return self._id_emploi
    
    @property
    def nom_poste(self):
        return self._nom_poste
    @property
    def duree(self):
        return self._duree
    
    #setter
    @id_emploi.setter
    def id_emploi(self, value):
        self._id_emploi = value

    @nom_poste.setter
    def nom_poste(self, value):
        self._nom_poste = value
    @duree.setter
    def duree(self, value):
        self._duree = value
        