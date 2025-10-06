from tkinter import *
from tkinter import ttk
from backend.api import *
from frontend.funcoes_main.atividades import *
from frontend.funcoes_main.listar_turmas import *
from frontend.funcoes_main.notas import *
from frontend.funcoes_main.relatorios import*

class MainScreen:
    def __init__(self, master, professor):
        self.master = master
        self.professor = professor
        self.turmas = []

        master.title(f"PROFESSOR - {professor['nome']}")
        master.geometry("800x800")
        master.configure(bg="#0D1B2A")  # Fundo azul escuro

        # Labels
        self.welcome_label = Label(master, text=f"Bem-vindo, {professor['nome']}", font=("Calibri", 14, "bold"), bg="#0D1B2A", fg="#F0F0F0")
        self.welcome_label.pack(pady=10)

        self.id_label = Label(master, text=f"Matéria do Professor: {professor['materia']}", font=("Calibri", 12), bg="#0D1B2A", fg="#F0F0F0")
        self.id_label.pack(pady=5)

        # Frame dos botões do menu
        self.menu_frame = Frame(master, bg="#0D1B2A")
        self.menu_frame.pack(pady=10)

        # Função auxiliar para criar botão estilizado
        def criar_botao(texto, comando):
            return Button(self.menu_frame, text=texto, width=15, bg="#D4A017", fg="#0D1B2A", font=("Arial", 12, "bold"),
                          activebackground="#e6b800", command=comando)

        self.btn_turmas = criar_botao("Minhas Turmas", lambda: self.mostrar_frame("turmas"))
        self.btn_turmas.grid(row=0, column=0, padx=5)

        self.btn_atividades = criar_botao("Atividades", lambda: self.mostrar_frame("atividades"))
        self.btn_atividades.grid(row=0, column=1, padx=5)

        self.btn_add_notas = criar_botao("Adicionar Notas", lambda: self.mostrar_frame("notas"))
        self.btn_add_notas.grid(row=0, column=2, padx=5)

        self.btn_relatorios = criar_botao("Relatórios", lambda: self.mostrar_frame("relatorios"))
        self.btn_relatorios.grid(row=0, column=3, padx=5)

        # Frames de conteúdo
        self.frames = {}
        self.frames["turmas"] = Frame(master, bg="#0D1B2A")
        criar_frame_turmas(self, self.frames["turmas"])

        self.frames["atividades"] = Frame(master, bg="#0D1B2A")
        Label(self.frames["atividades"], text="Gerenciar Atividades", bg="#0D1B2A", fg="#F0F0F0", font=("Calibri", 14, "bold")).pack()

        self.frames["notas"] = Frame(master, bg="#0D1B2A")
        Label(self.frames["notas"], text="Gerenciar Notas", bg="#0D1B2A", fg="#F0F0F0", font=("Calibri", 14, "bold")).pack()

        self.frames["relatorios"] = Frame(master, bg="#0D1B2A")
        Label(self.frames["relatorios"], text="Gerenciar Relatórios", bg="#0D1B2A", fg="#F0F0F0", font=("Calibri", 14, "bold")).pack()

        # Oculta frames inicialmente
        for f in self.frames.values():
            f.pack_forget()

        # Treeview Style global
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#f9f9f9", foreground="black", rowheight=25, fieldbackground="#f9f9f9", font=("Calibri", 10))
        self.style.map("Treeview", background=[("selected", "#D4A017")], foreground=[("selected", "#0D1B2A")])
        self.style.configure("Treeview.Heading", font=("Calibri", 11, "bold"), background="#D4A017", foreground="#0D1B2A")

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
        elif chave == "relatorios":
            mostrar_relatorios(self)

if __name__ == "__main__":
    root = Tk()
    MainScreen(root, {"nome": "Professor Teste", "materia": "Matemática"})
    root.mainloop()
