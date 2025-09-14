from tkinter import *
from tkinter import ttk

from backend.api import *
from frontend.funcoes_main.atividades import mostrar_atividades
from frontend.funcoes_main.listar_turmas import *

class MainScreen:
    def __init__(self, master, professor):
        self.master = master
        self.professor = professor
        self.turmas = []

        master.title(f"PROFESSOR - {professor['nome']}")
        master.geometry("800x800")

        # Label de boas-vindas
        self.welcome_label = Label(master, text=f"Bem-vindo, {professor['nome']}", font=("Calibri", 14, "bold"))
        self.welcome_label.pack(pady=10)

        # Matéria do professor
        self.id_label = Label(master, text=f"Matéria do Professor: {professor['materia']}", font=("Calibri", 12))
        self.id_label.pack(pady=5)

        # Frame para os botões do menu
        self.menu_frame = Frame(master)
        self.menu_frame.pack(pady=10)

        self.btn_turmas = Button(self.menu_frame, text="Minhas Turmas", command=lambda: self.mostrar_frame("turmas"))
        self.btn_turmas.grid(row=0, column=0, padx=5)

        self.btn_outra1 = Button(self.menu_frame, text="Atividades", command=lambda: self.mostrar_frame("atividades"))
        self.btn_outra1.grid(row=0, column=1, padx=5)

        self.btn_outra2 = Button(self.menu_frame, text="Adicionar Notas", command=lambda: self.mostrar_frame("notas"))
        self.btn_outra2.grid(row=0, column=2, padx=5)

        self.btn_outra3 = Button(self.menu_frame, text="Pjota gay", command=lambda: self.mostrar_frame("outra3"))
        self.btn_outra3.grid(row=0, column=3, padx=5)

        # Frames de conteúdo
        self.frames = {}

        # Frame Turmas
        self.frames["turmas"] = Frame(master)
        criar_frame_turmas(self, self.frames["turmas"])

        # Frame Atividades
        self.frames["atividades"] = Frame(master)
        Label(self.frames["atividades"], text="Gerenciar Atividades").pack()

        # Outras funcionalidades
        self.frames["notas"] = Frame(master)
        Label(self.frames["notas"], text="Gerenciar Notas").pack()

        self.frames["outra3"] = Frame(master)
        Label(self.frames["outra3"], text="pjota gay sim senhor").pack()

        # Inicialmente não mostra nenhum frame
        for f in self.frames.values():
            f.pack_forget()


    def mostrar_frame(self, chave):
        for f in self.frames.values():
            f.pack_forget()

        self.frames[chave].pack(fill=BOTH, expand=True)

        if chave == "turmas":
            mostrar_turmas(self)
        elif chave == "atividades":
            mostrar_atividades(self) 
        elif chave == "notas":
            mostrar_notas(self)
    




if __name__ == "__main__":
    root = Tk()
    MainScreen(root)
    root.mainloop()
