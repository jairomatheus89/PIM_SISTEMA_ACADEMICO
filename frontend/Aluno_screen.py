from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from backend.api import listar_atividades_aluno_api, listar_materias_aluno_api

class AlunoScreen(Frame):
    def __init__(self, master, voltar_callback):
        super().__init__(master)
        self.master = master
        self.voltar_callback = voltar_callback
        self.pack(expand=True, fill="both", padx=10, pady=10)

        Label(self, text="Consultar Aluno", font=("Calibri", 18, "bold")).pack(pady=10)

        # Campo RA
        frame_ra = Frame(self)
        frame_ra.pack(fill=X, pady=5)
        Label(frame_ra, text="Digite seu RA:", width=15, anchor=W).pack(side=LEFT)
        self.ra_entry = Entry(frame_ra)
        self.ra_entry.pack(side=LEFT, fill=X, expand=True, padx=5)

        # Botão Buscar
        self.buscar_btn = Button(self, text="Buscar Atividades", command=self.buscar_atividades, width=20)
        self.buscar_btn.pack(pady=5)

        # Combobox para selecionar a matéria
        frame_materia = Frame(self)
        frame_materia.pack(fill=X, pady=5)
        Label(frame_materia, text="Selecione a Matéria:", width=15, anchor=W).pack(side=LEFT)
        self.materia_combobox = ttk.Combobox(frame_materia, state="readonly", width=25)
        self.materia_combobox.pack(side=LEFT, fill=X, expand=True, padx=5)
        self.materia_combobox.bind("<<ComboboxSelected>>", lambda e: self.atualizar_tabela())

        # Treeview (Tabela) menor e compacta
        self.tree_frame = Frame(self)
        self.tree_frame.pack(fill=BOTH, expand=True, pady=10)

        colunas = ("atividade", "nota", "status", "data_entrega")
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=colunas,
            show="headings",
            height=10,
            selectmode="browse"
        )
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        # Cabeçalhos
        self.tree.heading("atividade", text="Atividade")
        self.tree.heading("nota", text="Nota")
        self.tree.heading("status", text="Status")
        self.tree.heading("data_entrega", text="Data de Entrega")

        # Largura das colunas
        self.tree.column("atividade", width=150, anchor=CENTER)
        self.tree.column("nota", width=50, anchor=CENTER)
        self.tree.column("status", width=80, anchor=CENTER)
        self.tree.column("data_entrega", width=100, anchor=CENTER)

        # Scrollbar vertical
        scrollbar = Scrollbar(self.tree_frame, orient=VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Armazena atividades e matérias
        self.atividades_completas = []
        self.materias_ids = []
        self.materias_nomes = []

        # Estilo
        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=25, font=("Calibri", 10))
        self.style.map("Treeview", background=[("selected", "#347083")])
        self.style.configure("Treeview.Heading", font=("Calibri", 11, "bold"))

        # Botão Voltar no final
        self.voltar_btn = Button(self, text="Voltar", command=self.voltar_elimpar, width=15)
        self.voltar_btn.pack(pady=5, side=BOTTOM)

    def buscar_atividades(self):
        ra = self.ra_entry.get().strip()
        if not ra:
            return

        # Busca matérias do aluno
        materias_resp = listar_materias_aluno_api(ra)
        if not materias_resp["sucesso"]:
            messagebox.showerror("Erro", f"Aluno com RA {ra} não encontrado.")
            self.limpar_tabela()
            return

        materias = materias_resp["materias"]
        self.materias_nomes = [m["materia"] for m in materias]
        self.materias_ids = [m["id_professor"] for m in materias]
        self.materia_combobox["values"] = ["Todas"] + self.materias_nomes
        self.materia_combobox.current(0)

        # Busca atividades do aluno
        resultado = listar_atividades_aluno_api(ra)
        if resultado["sucesso"]:
            self.atividades_completas = resultado["atividades"]
        else:
            self.atividades_completas = []

        self.atualizar_tabela()

    def atualizar_tabela(self):
        self.limpar_tabela()

        # ID do professor selecionado
        idx = self.materia_combobox.current()
        if idx == 0 or not self.materias_ids:
            id_professor_selecionado = None
        else:
            id_professor_selecionado = int(self.materias_ids[idx - 1])

        # Adiciona linhas com efeito zebra e cores de status
        for i, atividade in enumerate(self.atividades_completas):
            if id_professor_selecionado and int(atividade.get("id_professor", 0)) != id_professor_selecionado:
                continue

            status = "Entregue" if atividade.get("entregue") else "Pendente"
            cor_fundo = "#f9f9f9" if i % 2 == 0 else "#e6f2ff"  # efeito zebra
            cor_texto = "green" if status == "Entregue" else "red"

            item = self.tree.insert("", "end", values=(
                atividade["nome_atividade"],
                atividade["nota"] if atividade.get("nota") is not None else "-",
                status,
                atividade.get("data_entrega", "-")
            ))

            self.tree.tag_configure(f"linha_{i}", background=cor_fundo, foreground="black")
            self.tree.item(item, tags=(f"linha_{i}", f"status_{i}"))
            self.tree.tag_configure(f"status_{i}", foreground=cor_texto)

    def limpar_tabela(self):
        # Limpa a tabela
        for row in self.tree.get_children():
            self.tree.delete(row)

    def voltar_elimpar(self):
        # Limpa RA
        self.ra_entry.delete(0, END)
        # Limpa combobox
        self.materia_combobox["values"] = ["Todas"]
        self.materia_combobox.current(0)
        self.materias_ids = []
        self.materias_nomes = []
        # Limpa tabela
        self.limpar_tabela()
        # Chama callback original
        self.voltar_callback()
