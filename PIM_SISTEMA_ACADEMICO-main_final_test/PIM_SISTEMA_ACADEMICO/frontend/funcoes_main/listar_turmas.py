from tkinter import *
from tkinter import ttk
from backend.api import *

# Cores
BG_COLOR = "#1E2A38"        # Fundo azul escuro
BTN_COLOR = "#D4A017"       # Botão mostarda escuro
BTN_FG = "black"             # Texto do botão
LABEL_FG = "white"           # Texto labels
ENTRY_BG = "#2E3C4E"         # Fundo dos Entry
ENTRY_FG = "white"

def criar_frame_turmas(self, frame):
    frame.config(bg=BG_COLOR)
    
    Label(frame, text="Selecione a turma:", bg=BG_COLOR, fg=LABEL_FG).pack(anchor=W, padx=5, pady=5)
    
    self.combo_turmas = ttk.Combobox(frame, state="readonly")
    self.combo_turmas.pack(fill=X, padx=5, pady=5)
    self.combo_turmas.bind("<<ComboboxSelected>>", lambda e: turma_selecionada(self, e))

    frame_alunos = Frame(frame, bg=BG_COLOR)
    frame_alunos.pack(fill=BOTH, expand=True, padx=20, pady=5)

    colunas = ("nome", "ra")
    self.tree_alunos_turmas = ttk.Treeview(frame_alunos, columns=colunas, show="headings", height=10)
    self.tree_alunos_turmas.heading("nome", text="Nome do Aluno")
    self.tree_alunos_turmas.heading("ra", text="RA")
    self.tree_alunos_turmas.column("nome", width=150, anchor=CENTER)
    self.tree_alunos_turmas.column("ra", width=100, anchor=CENTER)

    scrollbar = Scrollbar(frame_alunos, orient=VERTICAL, command=self.tree_alunos_turmas.yview)
    self.tree_alunos_turmas.configure(yscrollcommand=scrollbar.set)
    self.tree_alunos_turmas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

def mostrar_turmas(self):
    resultado = listar_turmas_api(self.professor["id"])
    
    self.combo_turmas.set("")
    self.combo_turmas["values"] = []
    self.tree_alunos_turmas.delete(*self.tree_alunos_turmas.get_children())

    if resultado.get("sucesso"):
        self.turmas = resultado.get("turmas", [])
        nomes_turmas = [t["nome_turma"] for t in self.turmas]
        nomes_turmas.insert(0, "Todas as turmas")
        self.combo_turmas["values"] = nomes_turmas
        if nomes_turmas:
            self.combo_turmas.current(0)
            turma_selecionada(self, None)
    else:
        self.combo_turmas["values"] = ["Não foi possível carregar as turmas"]
        self.combo_turmas.current(0)

def turma_selecionada(self, event):
    nome_turma = self.combo_turmas.get()
    self.tree_alunos_turmas.delete(*self.tree_alunos_turmas.get_children())

    if not nome_turma or nome_turma == "Não foi possível carregar as turmas":
        return

    if nome_turma == "Todas as turmas":
        for turma in self.turmas:
            resultado = listar_alunos_api(turma["id_turma"])
            if resultado.get("sucesso"):
                for aluno in resultado.get("alunos", []):
                    self.tree_alunos_turmas.insert("", END, values=(aluno["nome"], aluno["ra"]))
            else:
                self.tree_alunos_turmas.insert("", END, values=(f"Erro ao carregar alunos ({turma['nome_turma']})", ""))
    else:
        turma = next((t for t in self.turmas if t["nome_turma"] == nome_turma), None)
        if not turma:
            return
        resultado = listar_alunos_api(turma["id_turma"])
        if resultado.get("sucesso"):
            for aluno in resultado.get("alunos", []):
                self.tree_alunos_turmas.insert("", END, values=(aluno["nome"], aluno["ra"]))
        else:
            self.tree_alunos_turmas.insert("", END, values=("Não foi possível carregar os alunos", ""))
