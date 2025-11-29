#classe d'associaton entre Personnel et Conge

class Perso_Conge:
    def __init__(self,id_pc,date_depart,date_fin,id_personne,id_conge):
        self.__id_pc = id_pc
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
    @property
    def date_fin(self):
        return self.__date_fin
    @property
    def id_personne(self):
        return self.__id_personne
    @property
    def id_conge(self):
        return self.__id_conge
    
    #setter
    @id_pc.setter
    def id_pc(self, value):
        self.__id_pc = value
    @date_depart.setter
    def date_depart(self, value):
        self.__date_depart = value
    @date_fin.setter   
    def date_fin(self, value):
        self.__date_fin = value
    @id_personne.setter
    def id_personne(self, value):
        self.__id_personne = value
    @id_conge.setter
    def id_conge(self, value):
        self.__id_conge = value
            
    
"""   
id_pc = id de Perso_Conge
id_personne = cle primaire de Personnel
id_conge = cle primaire de Conge
"""

