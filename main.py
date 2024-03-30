import tkinter as tk
from tkinter import messagebox, simpledialog

class SystemeExpert:
    def __init__(self):
        self.base_de_connaissances = {}

    def ajouter_regles(self, symptomes, organe):
        self.base_de_connaissances[tuple(symptomes)] = organe

    def diagnostiquer(self, symptomes):
        organes_defectueux = []
        for regle, organe in self.base_de_connaissances.items():
            if all(symptome in symptomes for symptome in regle):
                organes_defectueux.append(organe)
        return organes_defectueux if organes_defectueux else ["Aucun organe défectueux détecté."]

    def ajouter_regle(self, symptomes, organe):
        self.base_de_connaissances[tuple(symptomes)] = organe

    def modifier_regle(self, anciens_symptomes, nouveaux_symptomes, organe):
        if tuple(anciens_symptomes) in self.base_de_connaissances:
            del self.base_de_connaissances[tuple(anciens_symptomes)]
            self.base_de_connaissances[tuple(nouveaux_symptomes)] = organe
            return True
        return False

    def supprimer_regle(self, symptomes):
        if tuple(symptomes) in self.base_de_connaissances:
            del self.base_de_connaissances[tuple(symptomes)]
            return True
        return False

class InterfaceUtilisateur(tk.Tk):
    def __init__(self, systeme_expert):
        super().__init__()
        self.systeme_expert = systeme_expert
        self.title("Système Expert de Diagnostic de Pannes d'Ordinateur")

        self.label = tk.Label(self, text="Bienvenue dans le système expert de diagnostic de pannes d'ordinateur")
        self.label.pack()

        self.symptomes_frame = tk.Frame(self)
        self.symptomes_frame.pack()

        self.symptomes = ["écran noir", "ventilateur ne tourne pas", "ordinateur ne démarre pas", "aucun bip sonore", "ordinateur surchauffe", "ventilateur fonctionne à pleine vitesse"]
        self.symptomes_vars = [tk.BooleanVar() for _ in range(len(self.symptomes))]
        for i, symptome in enumerate(self.symptomes):
            tk.Checkbutton(self.symptomes_frame, text=symptome, variable=self.symptomes_vars[i]).grid(row=i, sticky=tk.W)

        self.button_diagnostiquer = tk.Button(self, text="Diagnostiquer", command=self.diagnostiquer)
        self.button_diagnostiquer.pack()

        self.button_expert = tk.Button(self, text="Session Expert", command=self.ouvrir_session_expert)
        self.button_expert.pack()

    def diagnostiquer(self):
        symptomes_selectionnes = [self.symptomes[i] for i, var in enumerate(self.symptomes_vars) if var.get()]
        if len(symptomes_selectionnes) < 2:
            messagebox.showwarning("Attention", "Il est recommandé de sélectionner plus d'un symptôme pour un diagnostic précis.")
        else:
            organes_defectueux = self.systeme_expert.diagnostiquer(symptomes_selectionnes)
            result_window = ResultWindow(organes_defectueux)
            result_window.mainloop()

    def ouvrir_session_expert(self):
        if self.verifier_login():
            SessionExpertWindow(self.systeme_expert, self)

    def verifier_login(self):
        # Implémentez ici votre mécanisme de vérification de login
        # Par exemple, demandez à l'utilisateur d'entrer un mot de passe et vérifiez-le
        # Ici, je vais simplement autoriser l'accès en utilisant le mot de passe "admin"
        login = simpledialog.askstring("Login", "Entrez votre login :")
        if login == "admin":
            return True
        else:
            messagebox.showerror("Erreur", "Login incorrect.")
            return False

    def mise_a_jour_regles(self):
        self.destroy()
        InterfaceUtilisateur(self.systeme_expert)

class SessionExpertWindow(tk.Toplevel):
    def __init__(self, systeme_expert, interface_utilisateur):
        super().__init__()
        self.systeme_expert = systeme_expert
        self.interface_utilisateur = interface_utilisateur
        self.title("Session Expert")

        self.label = tk.Label(self, text="Bienvenue dans la session expert de gestion des règles")
        self.label.pack()

        self.choix_action = tk.StringVar()
        self.choix_action.set("ajouter")

        self.action_frame = tk.Frame(self)
        self.action_frame.pack()

        tk.Radiobutton(self.action_frame, text="Ajouter", variable=self.choix_action, value="ajouter", command=self.afficher_widgets).pack(anchor=tk.W)
        tk.Radiobutton(self.action_frame, text="Modifier", variable=self.choix_action, value="modifier", command=self.afficher_widgets).pack(anchor=tk.W)
        tk.Radiobutton(self.action_frame, text="Supprimer", variable=self.choix_action, value="supprimer", command=self.afficher_widgets).pack(anchor=tk.W)

        self.widgets_frame = tk.Frame(self)
        self.widgets_frame.pack()

        self.anciens_symptomes_label = tk.Label(self.widgets_frame, text="Anciens Symptômes:")
        self.anciens_symptomes_label.grid(row=0, column=0, sticky=tk.W)

        self.anciens_symptomes_entry = tk.Entry(self.widgets_frame, width=50)
        self.anciens_symptomes_entry.grid(row=0, column=1)

        self.nouveaux_symptomes_label = tk.Label(self.widgets_frame, text="Nouveaux Symptômes:")
        self.nouveaux_symptomes_label.grid(row=1, column=0, sticky=tk.W)

        self.nouveaux_symptomes_entry = tk.Entry(self.widgets_frame, width=50)
        self.nouveaux_symptomes_entry.grid(row=1, column=1)

        self.organe_label = tk.Label(self.widgets_frame, text="Organe:")
        self.organe_label.grid(row=2, column=0, sticky=tk.W)

        self.organe_entry = tk.Entry(self.widgets_frame, width=50)
        self.organe_entry.grid(row=2, column=1)

        self.afficher_widgets()

        self.button_executer = tk.Button(self, text="Exécuter", command=self.executer_action)
        self.button_executer.pack()
        
    def afficher_widgets(self):
        action = self.choix_action.get()
        if action == "ajouter":
            self.anciens_symptomes_label.grid_remove()
            self.anciens_symptomes_entry.grid_remove()
        else:
            self.anciens_symptomes_label.grid()
            self.anciens_symptomes_entry.grid()
        if action == "supprimer":
            self.nouveaux_symptomes_label.grid_remove()
            self.nouveaux_symptomes_entry.grid_remove()
            self.organe_label.grid_remove()
            self.organe_entry.grid_remove()
        else:
            self.nouveaux_symptomes_label.grid()
            self.nouveaux_symptomes_entry.grid()
            self.organe_label.grid()
            self.organe_entry.grid()

        if action == "modifier":
            self.organe_label.config(text="Nouvel Organe:")

    def executer_action(self):
        action = self.choix_action.get()
        if action == "ajouter":
            self.ajouter_regle()
        elif action == "modifier":
            self.modifier_regle()
        elif action == "supprimer":
            self.supprimer_regle()

    def ajouter_regle(self):
        nouveaux_symptomes = self.nouveaux_symptomes_entry.get().split(",")
        nouveaux_symptomes = [symptome.strip() for symptome in nouveaux_symptomes]
        organe = self.organe_entry.get()
        self.systeme_expert.ajouter_regle(nouveaux_symptomes, organe)
        messagebox.showinfo("Succès", "Règle ajoutée avec succès.")
        self.interface_utilisateur.mise_a_jour_regles()

    def modifier_regle(self):
        anciens_symptomes = self.anciens_symptomes_entry.get().split(",")
        anciens_symptomes = [symptome.strip() for symptome in anciens_symptomes]
        nouveaux_symptomes = self.nouveaux_symptomes_entry.get().split(",")
        nouveaux_symptomes = [symptome.strip() for symptome in nouveaux_symptomes]
        organe = self.organe_entry.get()
        if self.systeme_expert.modifier_regle(anciens_symptomes, nouveaux_symptomes, organe):
            messagebox.showinfo("Succès", "Règle modifiée avec succès.")
            self.interface_utilisateur.mise_a_jour_regles()
        else:
            messagebox.showerror("Erreur", "Impossible de trouver la règle à modifier.")

    def supprimer_regle(self):
        anciens_symptomes = self.anciens_symptomes_entry.get().split(",")
        anciens_symptomes = [symptome.strip() for symptome in anciens_symptomes]
        if self.systeme_expert.supprimer_regle(anciens_symptomes):
            messagebox.showinfo("Succès", "Règle supprimée avec succès.")
            self.interface_utilisateur.mise_a_jour_regles()
        else:
            messagebox.showerror("Erreur", "Impossible de trouver la règle à supprimer.")

class ResultWindow(tk.Toplevel):
    def __init__(self, organes_defectueux):
        super().__init__()
        self.title("Résultat du diagnostic")

        self.label = tk.Label(self, text="Organe(s) potentiellement défectueux :")
        self.label.pack()

        self.listbox = tk.Listbox(self)
        for organe in organes_defectueux:
            self.listbox.insert(tk.END, organe)
        self.listbox.pack()

# Création du système expert
se = SystemeExpert()

# Ajout de règles dans la base de connaissances
se.ajouter_regles(["écran noir", "ventilateur ne tourne pas"], "Carte mère")
se.ajouter_regles(["ordinateur ne démarre pas", "aucun bip sonore"], "Alimentation")
se.ajouter_regles(["ordinateur surchauffe", "ventilateur fonctionne à pleine vitesse"], "Ventilateur")

# Création de l'interface utilisateur
interface = InterfaceUtilisateur(se)
interface.mainloop()
