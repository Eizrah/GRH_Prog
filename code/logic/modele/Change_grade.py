#classe fils entre Grade et Personnel/Fonctionnaire ou Personnel/Agent_contractuel en gros classe d'association
""" 
Note:
date_av = date d'avancement à un nouveau grade
nouveau_grade = nouveau grade
ancien_grade = ancien grade

À revoir ici
id_fonc = identifiant du fonctionnaire (pas son num_mat)
id_agent = identifiant de l'agent contractuel (pas son numero de matricule)
id_grade = cle primaire de la classe Grade
"""
from uuid import uuid4

class ChangeGrade:
    def __init__(self, date_av, nouveau_grade, ancien_grade, id_grade, id_fonc, id_ag):
        self._id_changement = uuid4()
        self._date_av = date_av
        self._nouveau_grade = nouveau_grade
        self._ancien_grade = ancien_grade
        self._id_grade = id_grade
        self._id_fonc = id_fonc
        self._id_ag = id_ag
        
    #getter
    @property
    def id_changement(self):
        return self._id_changement
    
    @property
    def date_av(self):
        return self._date_av
    
    @property 
    def nouveau_grade(self):
        return self._nouveau_grade
    
    @property
    def ancien_grade(self):
        return self._ancien_grade
        
    @property
    def id_grade(self):
        return self._id_grade

    @property
    def id_fonc(self):
        return self._id_fonc
        
    @property
    def id_ag(self):
        return self._id_ag
    
    
    #setter
    @date_av.setter
    def date_av(self,value):
        self._date_av = value
        
    @nouveau_grade.setter
    def nouveau_grade(self,value):
        self._nouveau_grade = value
        
    @ancien_grade.setter
    def ancien_grade(self,value):
        self._ancien_grade=value
        
    @id_grade.setter
    def id_grade(self, value):
        self._id_grade = value

    @id_fonc.setter
    def id_fonc(self, value):
        self._id_fonc = value
        
    @id_ag.setter
    def id_ag(self, value):
        self._id_ag = value
    