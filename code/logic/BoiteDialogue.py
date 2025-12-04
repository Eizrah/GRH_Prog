from tkinter import messagebox

# pour l'enregistrement dans la bd
def pannel_erreur():
    messagebox.showerror("Message erreur","erreur lors de l'enregistrement ")

def pannel_succes():
    messagebox.showinfo("Message succes","Enregistrement réussi ")

# pour l'erreur de type 
def pannel_type_err():
    messagebox.showerror("Message erreur","Type non valable ")
