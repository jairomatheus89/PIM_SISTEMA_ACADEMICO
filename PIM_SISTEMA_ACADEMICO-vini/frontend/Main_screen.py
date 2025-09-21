import customtkinter as ctk
from tkinter import ttk

from backend.api import *
from frontend.funcoes_main.atividades import mostrar_atividades
from frontend.funcoes_main.listar_turmas import *


class MainScreen(ctk.CTkFrame):
    def __init__(self, master, professor):
        super().__init__(master, fg_color="royalblue4")  # Frame principal com fundo azul
        self.pack(fill="both", expand=True)

        self.master = master
        self.professor = professor
        self.turmas = []

        try:
            master.iconbitmap('frontend/favicon.ico')
        except Exception as e:
            print("Não foi possível carregar ícone:", e)

        master.title(f"PROFESSOR - {professor['nome']}")
        master.geometry("800x800")
        master.resizable(False, False)

        # ---------------- Label de boas-vindas ----------------
        self.welcome_label = ctk.CTkLabel(
            self,
            text=f"Bem-vindo, {professor['nome']}",
            font=("Calibri", 14, "bold"),
            text_color="white"
        )
        self.welcome_label.pack(pady=10)

        # ---------------- Matéria do professor ----------------
        self.id_label = ctk.CTkLabel(
            self,
            text=f"Matéria do Professor: {professor['materia']}",
            font=("Calibri", 12),
            text_color="white"
        )
        self.id_label.pack(pady=5)

        # ---------------- Frame para os botões do menu ----------------
        self.menu_frame = ctk.CTkFrame(self, fg_color="royalblue4")
        self.menu_frame.pack(pady=10)

        self.btn_turmas = ctk.CTkButton(
            self.menu_frame,
            text="Minhas Turmas",
            fg_color="deepskyblue4",
            text_color="white",
            command=lambda: self.mostrar_frame("turmas")
        )
        self.btn_turmas.grid(row=0, column=0, padx=5)

        self.btn_outra1 = ctk.CTkButton(
            self.menu_frame,
            text="Atividades",
            fg_color="deepskyblue4",
            text_color="white",
            command=lambda: self.mostrar_frame("atividades")
        )
        self.btn_outra1.grid(row=0, column=1, padx=5)

        self.btn_outra2 = ctk.CTkButton(
            self.menu_frame,
            text="Adicionar Notas",
            fg_color="deepskyblue4",
            text_color="white",
            command=lambda: self.mostrar_frame("notas")
        )
        self.btn_outra2.grid(row=0, column=2, padx=5)

        self.btn_outra3 = ctk.CTkButton(
            self.menu_frame,
            text="Pjota gay",
            fg_color="deepskyblue4",
            text_color="white",
            command=lambda: self.mostrar_frame("outra3")
        )
        self.btn_outra3.grid(row=0, column=3, padx=5)

        # ---------------- Frames de conteúdo ----------------
        self.frames = {}

        # Frame Turmas
        self.frames["turmas"] = ctk.CTkFrame(self, fg_color="royalblue4")
        criar_frame_turmas(self, self.frames["turmas"])

        # Frame Atividades
        self.frames["atividades"] = ctk.CTkFrame(self, fg_color="royalblue4")
        ctk.CTkLabel(
            self.frames["atividades"],
            text="Gerenciar Atividades",
            text_color="white"
        ).pack(pady=10)

        # Frame Notas
        self.frames["notas"] = ctk.CTkFrame(self, fg_color="royalblue4")
        ctk.CTkLabel(
            self.frames["notas"],
            text="Gerenciar Notas",
            text_color="white"
        ).pack(pady=10)

        # Frame Outra3
        self.frames["outra3"] = ctk.CTkFrame(self, fg_color="royalblue4")
        ctk.CTkLabel(
            self.frames["outra3"],
            text="pjota gay sim senhor",
            text_color="white"
        ).pack(pady=10)

        # Inicialmente não mostra nenhum frame
        for f in self.frames.values():
            f.pack_forget()

    # ---------------- Controla troca de frame ----------------
    def mostrar_frame(self, chave):
        for f in self.frames.values():
            f.pack_forget()

        self.frames[chave].pack(fill="both", expand=True)

        if chave == "turmas":
            mostrar_turmas(self)
        elif chave == "atividades":
            mostrar_atividades(self)


if __name__ == "__main__":
    root = ctk.CTk()
    root.geometry("800x800")
    root.resizable(False, False)

    MainScreen(root, {"nome": "Professor Exemplo", "materia": "Matemática"})
    root.mainloop()
