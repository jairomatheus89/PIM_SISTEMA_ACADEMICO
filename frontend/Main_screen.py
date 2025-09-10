
from tkinter import * 
from backend.api import *

class MainScreen:
    def __init__(self, master, professor):
        self.master = master
        self.professor = professor  # dicionário com id, nome , materia
        
        master.title(f"PROFESSOR - {professor['nome']}")
        master.geometry("700x600")  

        # Label de boas-vindas
        self.welcome_label = Label(master, text=f"Bem-vindo, {professor['nome']}", font=("Calibri", 14, "bold"))
        self.welcome_label.pack(pady=10)

        # Exemplo: mostrar ID do professor
        self.id_label = Label(master, text=f"Materia do Professor: {professor['materia']}", font=("Calibri", 12))
        self.id_label.pack(pady=5)

        # Botão para listar turmas
        self.listar_turmas_btn = Button(master, text="Listar minhas turmas", command=self.mostrar_turmas)
        self.listar_turmas_btn.pack(pady=20)


        ####
        # Frame para turmas com scrollbar
        frame_turmas = Frame(master)
        frame_turmas.pack(fill=BOTH, expand=False, padx=20, pady=5)

        self.scrollbar_turmas = Scrollbar(frame_turmas)
        self.scrollbar_turmas.pack(side=RIGHT, fill=Y)

        self.listbox_turmas = Listbox(frame_turmas, yscrollcommand=self.scrollbar_turmas.set, height=8)
        self.listbox_turmas.pack(side=LEFT, fill=BOTH, expand=True)
        self.listbox_turmas.bind("<<ListboxSelect>>", self.turma_selecionada)

        self.scrollbar_turmas.config(command=self.listbox_turmas.yview)

        # Frame para alunos com scrollbar
        frame_alunos = Frame(master)
        frame_alunos.pack(fill=BOTH, expand=False, padx=20, pady=5)

        self.scrollbar_alunos = Scrollbar(frame_alunos)
        self.scrollbar_alunos.pack(side=RIGHT, fill=Y)

        self.listbox_alunos = Listbox(frame_alunos, yscrollcommand=self.scrollbar_alunos.set, height=10)
        self.listbox_alunos.pack(side=LEFT, fill=BOTH, expand=True)

        self.scrollbar_alunos.config(command=self.listbox_alunos.yview)
        


    def listar_turmas(self):
        resultado = listar_turmas_api(self.professor["id"])
        
        # Limpa o frame antes de mostrar as turmas
        for widget in self.frame_turmas.winfo_children():
            widget.destroy()

        if resultado["sucesso"]:
            for turma in resultado["turmas"]:
                Label(self.frame_turmas, text=turma["nome_turma"]).pack()
        else:
            Label(self.frame_turmas, text="Não foi possível carregar as turmas", fg="red").pack()

    def mostrar_turmas(self):
        resultado = listar_turmas_api(self.professor["id"])
        self.listbox_turmas.delete(0, END)
        self.listbox_alunos.delete(0, END)

        if resultado["sucesso"]:
            self.turmas = resultado["turmas"]
            for turma in self.turmas:
                self.listbox_turmas.insert(END, turma["nome_turma"])
        else:
            self.listbox_turmas.insert(END, "Não foi possível carregar as turmas")

    def turma_selecionada(self, event):
        if not self.listbox_turmas.curselection():
            return
        index = self.listbox_turmas.curselection()[0]
        turma_selecionada = self.turmas[index]

        resultado = listar_alunos_api(turma_selecionada["id_turma"])
        self.listbox_alunos.delete(0, END)

        if resultado["sucesso"]:
            for aluno in resultado["alunos"]:
                self.listbox_alunos.insert(END, f"{aluno['nome']} (RA: {aluno['ra']})")
        else:
            self.listbox_alunos.insert(END, "Não foi possível carregar os alunos")

if __name__ == "__main__":
    root = Tk()
    MainScreen(root)
    root.mainloop()