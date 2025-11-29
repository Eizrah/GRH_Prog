#classe d'association entre Personnel et Emplois

from . import Personnel,Emplois

class Affectation:
    def __init__(self,id_affectation,date_debut,date_fin,personnel:Personnel,emplois:Emplois):
        self._id_affectation = id_affectation
        self._date_debut = date_debut
        self._date_fin = date_fin
        self._personnel = personnel
        self._emplois = emplois
        
    @property
    def id_affectation(self):
        return self._id_affectation
    @id_affectation.setter
    def id_affectation(self, value):
        self._id_affectation = value
    
    @property
    def date_debut(self):
        return self._date_debut
    @date_debut.setter
    def date_debut(self, value):
        self._date_debut = value
    
    @property
    def date_fin(self):
        return self._date_fin
    @date_fin.setter
    def date_fin(self, value):
        self._date_fin = value
    
    @property
    def personnel(self):
        return self._personnel
    @personnel.setter
    def personnel(self, value):
        self._personnel = value
    @property
    def emplois(self):
        return self._emplois
    @emplois.setter
    def emplois(self, value):
        self._emplois = value
        
    
    """ 
    personnel: cle etrangere vers Personnel
    emplois: cle etrangere vers Emplois
    """