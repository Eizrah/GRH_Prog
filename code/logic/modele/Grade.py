#classe fils de Cadre
from . import  Emplois
class Grade:
    def __init__(self,id_grade,titre,classe,echelon):
        self.__id_grade = id_grade
        self.__titre = titre
        self.__classe = classe
        self.__echelon = echelon
    
    
        
      
    #getter
    @property
    def id_grade(self):
        return self.__id_grade
    @property
    def titre(self):
        return self.__titre
    @property
    def classe(self):
        return self.__classe
    @property
    def echelon(self):
        return self.__echelon
    
    #setter
    @property.setter
    def id_grade(self,id_grade):
        self.__id_grade = id_grade
    @property.setter
    def titre(self,titre):
        self.__titre = titre
    @property.setter
    def classe(self,classe):
        self.__classe = classe
    @property.setter
    def echelon(self,echelon):
        self.__echelon = echelon
    
    #methode
    def AvancementEchelon(self, duree :Emplois):
        duree = Emplois.duree
        
        if duree > 2:
            self.__echelon += 1
            print(f"Felicitation! Vous etes promu au echelon {self.__echelon}")
        else:
            print("Desole! Vous ne pouvez pas etre promu d'echelon")
     

    def AvancementClasse(self, duree :Emplois):
        duree = Emplois.duree
        
        if duree > 5:
            if self.__classe == "classe exceptionnelle":
                print("Desole! Vous etes deja au plus haut niveau de classe")
            elif self.__classe == "classe principal":
                self.__classe = "classe exceptionnelle"
                print(f"Felicitation! Vous etes promu a la {self.__classe}")
            elif self.__classe == "premiere classe":
                self.__classe = "classe principal"
                print(f"Felicitation! Vous etes promu a la {self.__classe}")
            elif self.__classe == "deuxieme classe":
                self.__classe = "premiere classe"
                print(f"Felicitation! Vous etes promu a la {self.__classe}")
        else:
            print("Desole! Vous ne pouvez pas etre promu de classe")

""" 
classe  : classe exceptionnelle, classe principal, premiere classe, deuxieme classe
"""      