#cadre = corps
#classe pere de la classe  Grade
class Cadre:
    def __init__(self,id_cadre,classe_corps,chef_grade,nbr_grade,id_grade):
        self.__id_cadre = id_cadre
        self.__classe_corps = classe_corps
        self.__chef_grade = chef_grade
        self.__nbr_grade = nbr_grade
        self.__id_grade = id_grade
    
    
    
    #getter
    @property
    def id_cadre(self):
        return self.__id_cadre
    @property
    def classe_corps(self):
        return self.__classe_corps
    @property
    def chef_grade(self):
        return self.__chef_grade
    @property
    def nbr_grade(self):
        return self.__nbr_grade
    @property
    def id_grade(self):
        return self.__id_grade
    
    #setter
    @property.setter
    def id_cadre(self,id_cadre):
        self.__id_cadre = id_cadre
        
    @property.setter
    def classe_corps(self,classe_corps):
        self.__classe_corps = classe_corps
    @property.setter
    def chef_grade(self,classe_grade):
        self.__chef_grade = classe_grade
    @property.setter
    def nbr_grade(self,nbr_grade):
        self.__nbr_grade = nbr_grade
    @property.setter
    def id_grade(self,id_grade):
        self.__id_grade = id_grade
        
        
"""  
Note: 
chef_grade = grade le plus elevé d  ns le corps (cadre)
nbr_grade = nombre de grade dans le corps (cadre)
id_grade =  clet etrangere vers la table grade
"""