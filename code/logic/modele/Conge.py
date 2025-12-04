#classe enfant de Pause
import Pause
import uuid
class Conge(Pause.Pause):
    def __init__(self,  type_conge,duree, validation):
        super().__init__(duree, validation)
        self._id_conge = uuid.uuid4()
        self._type_conge = type_conge
       
    @property
    def type_conge(self):
        return self._type_conge
    @property
    def id_conge(self):
        return self._id_conge
    @type_conge.setter
    def type_conge(self, value):
        self._type_conge = value
    #implementation getter
    @property
    def duree(self):
        return self._duree
    @property
    def validation(self):
        return self._validation
    #implementation setter
    @duree.setter
    def duree(self, value):
        self._duree = value
    @validation.setter
    def validation(self, value):
        self._validation = value


"""  
type de conge: 
             - congé annuel
             - congé annuel cumulé
             - congé formation
             - congé pour education dans le domaine social, civique et syndical
             - congé maladie
             - congé maternité
             - congé paternité


"""