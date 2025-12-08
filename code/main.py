from logic.modele.Cadre import Cadre
from logic.modele.Grade import Grade
from logic.modele.Fonctionnaire import Fonctionnaire
from screen.auth import ModernLoginPage


if __name__ == "__main__":
    # Démarrer avec la page de connexion
    login_app = ModernLoginPage()
    login_app.mainloop()
