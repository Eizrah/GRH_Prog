#classe eenfant de Pause
import Pause
import uuid
class Permission(Pause.Pause):
    def __init__(self, motif, duree, validation, ):
        super().__init__(duree, validation)
        self._id_permission = uuid.uuid4()
        self._motif = motif
       
    @property
    def motif(self):
        return self._motif
    @property
    def id_permission(self):
        return self._id_permission
    @motif.setter
    def motif(self, value):
        self._motif = value
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
Note

motif : raison de la permission (ex: rendez-vous médical, urgence familiale, etc.)

"""