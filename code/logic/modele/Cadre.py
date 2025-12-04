#cadre = corps
#classe pere de la classe  Grade
import uuid
class Cadre:
    def __init__(self, classe_corps, chef_grade,echelle):
        self.__id_cadre = uuid.uuid4()
        self.__classe_corps = classe_corps
        self.__chef_grade = chef_grade
        self.__echelle = echelle
    @property
    def id_cadre(self):
        return self.__id_cadre
    
    @id_cadre.setter
    def id_cadre(self, value):
        self.__id_cadre = value
        
    @property
    def classe_corps(self):
        return self.__classe_corps
    
    @classe_corps.setter
    def classe_corps(self, value):
        self.__classe_corps = value
        
    @property
    def chef_grade(self):
        return self.__chef_grade
    
    @chef_grade.setter
    def chef_grade(self, value):
        self.__chef_grade = value
        

    @property
    def echelle(self):
        return self.__echelle
    @echelle.setter
    def echelle(self,value):
        self.__echelle = value
        
        
"""  
Note: 
chef_grade = grade le plus elevé d  ns le corps (cadre)

class_corps : A,B,C,D
Echelle pour classe A : A1,A2,A3
        pour classe B : B1,B2
        pour classe C : C1,C2
        pour classe D : D1,D2,D3
"""

