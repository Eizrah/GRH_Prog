#classe d'association entre Personnel et Emplois
from uuid import uuid4
class Affectation:
    def __init__(self, date_debut, date_fin, id_emploi, id_fonc=None, id_ag=None):
        self._id_affectation = uuid4()
        self._date_debut = date_debut
        self._date_fin = date_fin
        self._id_emploi = id_emploi
        self._id_fonc = id_fonc
        self._id_ag = id_ag
        
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
    def id_fonc(self):
        return self._id_fonc
    
    @id_fonc.setter
    def id_fonc(self, value):
        self._id_fonc = value

    @property
    def id_ag(self):
        return self._id_ag
    
    @id_ag.setter
    def id_ag(self, value):
        self._id_ag = value
        
    @property
    def id_emploi(self):
        return self._id_emploi
    
    @id_emploi.setter
    def id_emploi(self, value):
        self._id_emploi = value
    
    """ 
    id_fonc: cle etrangere vers Fonctionnaire (peut etre null)
    id_ag: cle etrangere vers AgentContractuel (peut etre null)
    id_emploi: cle etrangere vers Emplois
    """