#classe enfant de Pause
import Pause
import uuid
class Autorisation(Pause.Pause):
    def __init__(self ,type,duree, validation, ):
        super().__init__(duree, validation)
        self._id_aut =uuid.uuid4()
        self._type = type
       
    @property
    def duree(self):
        return self._duree
       
    @duree.setter
    def duree(self, value):
        self._duree = value
       
    @property
    def validation(self):
        return self._validation
       
    @validation.setter
    def validation(self, value):
        self._validation = value
       
    @property
    def type(self):
        return self._type
       
    @type.setter
    def type(self, value):
        self._type = value
        

"""  
Note

type :  autorisation absence ordinaire
        autorisation speciale en cas d'hospitalisation du conjoint ou de son enfant à charge
        autorisation special  d'absence des fonctionaires candidats à des "lections politiques
"""