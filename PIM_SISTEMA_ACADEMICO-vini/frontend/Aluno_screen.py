import customtkinter as ctk
from tkinter import ttk
from backend.api import listar_atividades_aluno_api


class AlunoScreen(ctk.CTkFrame):
    def __init__(self, master, voltar_callback, fg_color="royalblue4"):
        super().__init__(master, fg_color=fg_color)
        self.master = master
        self.voltar_callback = voltar_callback
        self.pack(expand=True, fill="both")

        # Título
        ctk.CTkLabel(
            self,
            text="Consultar Aluno",
            font=("Calibri", 20, "bold"),
            text_color="white"
        ).pack(pady=20)

        # Campo RA
        self.ra_label = ctk.CTkLabel(
            self,
            text="Digite seu RA:",
            text_color="white"
        )
        self.ra_label.pack()

        self.ra_entry = ctk.CTkEntry(self, width=250)
        self.ra_entry.pack(pady=5)

        # Botão Buscar
        self.buscar_btn = ctk.CTkButton(
            self,
            text="Buscar Atividades",
            fg_color="deepskyblue4",
            text_color="white",
            command=self.buscar_atividades
        )
        self.buscar_btn.pack(pady=10)
        
        # Botão Voltar
        self.voltar_btn = ctk.CTkButton(
            self,
            text="Voltar",
            command=self.voltar_callback
        )
        self.voltar_btn.pack(pady=10)

        # Frame para a tabela (Treeview do ttk)
        tabela_frame = ctk.CTkFrame(self, fg_color="white")
        tabela_frame.pack(expand=True, fill="both", pady=20, padx=10)

        self.tree = ttk.Treeview(
            tabela_frame,
            columns=("atividade", "nota", "status", "data_entrega"),
            show="headings"
        )

        # Configurando cabeçalhos
        self.tree.heading("atividade", text="Atividade")
        self.tree.heading("nota", text="Nota")
        self.tree.heading("status", text="Status")
        self.tree.heading("data_entrega", text="Data de Entrega")

        # Definindo largura das colunas
        self.tree.column("atividade", width=200, anchor="w") 
        self.tree.column("nota", width=100, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        self.tree.column("data_entrega", width=120, anchor="center")

        self.tree.pack(expand=True, fill="both")

    # ---------------- Buscar atividades ----------------
    def buscar_atividades(self):
        ra = self.ra_entry.get().strip()
        if not ra:
            return

        resultado = listar_atividades_aluno_api(ra)  # chamada na API

        # Limpa a tabela
        for row in self.tree.get_children():
            self.tree.delete(row)

        if resultado["sucesso"]:
            for atividade in resultado["atividades"]:
                self.tree.insert("", "end", values=(
                    atividade["nome_atividade"],
                    atividade["nota"] if atividade.get("nota") is not None else "N/A",
                    "Entregue" if atividade.get("entregue") else "Pendente",
                    atividade.get("data_entrega", "N/A")
                ))
        else:
            self.tree.insert("", "end", values=("Erro", resultado.get("mensagem", ""), "", ""))
