class Personnel:  
    def __init__(self, num_matricule, nom, prenom, date_naissance, lieu_naissance, date_entree, date_sortie, objet_depart, position):
        self._num_matricule = num_matricule
        self._nom = nom
        self._prenom = prenom
        self._date_naissance = date_naissance
        self._lieu_naissance = lieu_naissance
        self._date_entree = date_entree
        self._date_sortie = date_sortie
        self._objet_depart = objet_depart
        self._position = position
        
    
    
    @property
    def num_matricule(self):
        """Obtient le numéro de matricule."""
        return self._num_matricule
    
    @num_matricule.setter  
    def num_matricule(self, value):
        """Définit le numéro de matricule."""
        self._num_matricule = value

    
    @property
    def nom(self):
        """Obtient le nom."""
        return self._nom
    
    @nom.setter
    def nom(self, value):
        """Définit le nom."""
        self._nom = value

    
    @property
    def prenom(self):
        return self._prenom
    
    @prenom.setter
    def prenom(self, value):
        self._prenom = value

    
    @property
    def date_naissance(self):
        return self._date_naissance
    
    @date_naissance.setter
    def date_naissance(self, value):
        self._date_naissance = value

    
    @property
    def lieu_naissance(self):
        return self._lieu_naissance
    
    @lieu_naissance.setter
    def lieu_naissance(self, value):
        self._lieu_naissance = value

 
    @property
    def date_entree(self):
        return self._date_entree
    
    @date_entree.setter
    def date_entree(self, value):
        self._date_entree = value

    
    @property
    def date_sortie(self):
        return self._date_sortie
    
    @date_sortie.setter
    def date_sortie(self, value):
        self._date_sortie = value

    
    @property
    def objet_depart(self):
        return self._objet_depart
    
    @objet_depart.setter
    def objet_depart(self, value):
        self._objet_depart = value

    
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value):
        self._position = value

    


    def __str__(self):
         return f"Matricule: {self.num_matricule}, Nom: {self.nom}, Prénom: {self.prenom}"
       


""" 
NOTE:
Position  peut prendre les valeurs suivantes:
  -en activité
  -en detachement
  -hors cadre
  -sous le drapeau 
  -en disponibilité

"""