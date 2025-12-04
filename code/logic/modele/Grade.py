import uuid
class Grade:
    def __init__(self,  titre, classe, echelon,id_cadre):
        self.__id_grade = uuid.uuid4()
        self.__titre = titre
        self.__classe = classe
        self.__echelon = echelon
        self.__id_cadre = id_cadre
        
    @property
    def id_cadre(self):
        return self.__id_cadre
    
    @property
    def id_grade(self):
        return self.__id_grade
    
    @id_grade.setter
    def id_grade(self, value):
        self.__id_grade = value
        
    @property
    def titre(self):
        return self.__titre
    
    @titre.setter
    def titre(self, value):
        self.__titre = value
        
    @property
    def classe(self):
        return self.__classe
    
    @classe.setter
    def classe(self, value):
        self.__classe = value
        
    @property
    def echelon(self):
        return self.__echelon
    
    @echelon.setter
    def echelon(self, value):
        self.__echelon = value
    
    def avancement_echelon(self, emplois):
        if emplois.duree > 2:
            self.__echelon += 1
            print(f"Félicitation! Vous êtes promu au échelon {self.__echelon}")
        else:
            print("Désolé! Vous ne pouvez pas être promu d'échelon")
     
    def avancement_classe(self, emplois):
        if emplois.duree > 5:
            if self.__classe == "classe exceptionnelle":
                print("Désolé! Vous êtes déjà au plus haut niveau de classe")
            elif self.__classe == "classe principal":
                self.__classe = "classe exceptionnelle"
                print(f"Félicitation! Vous êtes promu à la {self.__classe}")
            elif self.__classe == "premiere classe":
                self.__classe = "classe principal"
                print(f"Félicitation! Vous êtes promu à la {self.__classe}")
            elif self.__classe == "deuxieme classe":
                self.__classe = "premiere classe"
                print(f"Félicitation! Vous êtes promu à la {self.__classe}")
        else:
            print("Désolé! Vous ne pouvez pas être promu de classe")
""" 
classe  : classe exceptionnelle, classe principal, premiere classe, deuxieme classe
"""      

