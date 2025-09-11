from tkinter import *
from tkinter import ttk
from backend.api import listar_atividades_aluno_api  # você ainda vai criar no backend

class AlunoScreen(Frame):
    def __init__(self, master, voltar_callback):
        super().__init__(master)
        self.master = master
        self.voltar_callback = voltar_callback
        self.pack(expand=True, fill="both")

        Label(self, text="Consultar Aluno", font=("Calibri", 20, "bold")).pack(pady=20)

        # Campo RA
        self.ra_label = Label(self, text="Digite seu RA:")
        self.ra_label.pack()
        self.ra_entry = Entry(self, width=30)
        self.ra_entry.pack(pady=5)

        # Botão Buscar
        self.buscar_btn = Button(self, text="Buscar Atividades", command=self.buscar_atividades)
        self.buscar_btn.pack(pady=10)
        
        # Botão voltar
        self.voltar_btn = Button(self, text="Voltar", command=self.voltar_callback)
        self.voltar_btn.pack(pady=10)

        # Tabela (Treeview)
        self.tree = ttk.Treeview(self, columns=("atividade", "nota", "status", "data_entrega"), show="headings")

        # Configurando cabeçalhos
        self.tree.heading("atividade", text="Atividade")
        self.tree.heading("nota", text="Nota")
        self.tree.heading("status", text="Status")
        self.tree.heading("data_entrega", text="Data de Entrega")

        # Definindo largura das colunas
        self.tree.column("atividade", width=200, anchor="w") 
        self.tree.column("nota", width=100, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        self.tree.column("data_entrega", width=100, anchor="center")

        self.tree.pack(expand=True, fill="both", pady=20)

        
    
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
