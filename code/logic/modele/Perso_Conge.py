#classe d'associaton entre Personnel et Conge
from uuid import uuid4
class PersoConge:
    def __init__(self, date_depart, date_fin, id_personne, id_conge):
        self.__id_pc = uuid4()
        self.__date_depart = date_depart
        self.__date_fin = date_fin
        self.__id_personne = id_personne
        self.__id_conge = id_conge
        
    @property
    def id_pc(self):
        return self.__id_pc
    
  
        
    @property
    def date_depart(self):
        return self.__date_depart
    
    @date_depart.setter
    def date_depart(self, value):
        self.__date_depart = value
        
    @property
    def date_fin(self):
        return self.__date_fin
    
    @date_fin.setter   
    def date_fin(self, value):
        self.__date_fin = value
        
    @property
    def id_personne(self):
        return self.__id_personne
    
    @id_personne.setter
    def id_personne(self, value):
        self.__id_personne = value
        
    @property
    def id_conge(self):
        return self.__id_conge
    
    @id_conge.setter
    def id_conge(self, value):
        self.__id_conge = value
            
    
"""   
id_pc = id de Perso_Conge
id_personne = cle primaire de Personnel
id_conge = cle primaire de Conge
"""

