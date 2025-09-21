from tkinter import *
from tkinter import ttk
from backend.api import *

def criar_frame_turmas(self, frame):
    # Label e Combobox de turmas
    Label(frame, text="Selecione a turma:").pack(anchor=W, padx=5, pady=5)
    self.combo_turmas = ttk.Combobox(frame, state="readonly")
    self.combo_turmas.pack(fill=X, padx=5, pady=5)
    self.combo_turmas.bind("<<ComboboxSelected>>", lambda e: turma_selecionada(self, e))

    # Listbox de alunos
    frame_alunos = Frame(frame)
    frame_alunos.pack(fill=BOTH, expand=True, padx=20, pady=5)

    self.scrollbar_alunos = Scrollbar(frame_alunos)
    self.scrollbar_alunos.pack(side=RIGHT, fill=Y)

    self.listbox_alunos = Listbox(frame_alunos, yscrollcommand=self.scrollbar_alunos.set, height=10)
    self.listbox_alunos.pack(side=LEFT, fill=BOTH, expand=True)

    self.scrollbar_alunos.config(command=self.listbox_alunos.yview)


def mostrar_turmas(self):
    resultado = listar_turmas_api(self.professor["id"])
    
    self.combo_turmas.set("")
    self.combo_turmas["values"] = []
    self.listbox_alunos.delete(0, END)

    if resultado.get("sucesso"):
        self.turmas = resultado.get("turmas", [])
        nomes_turmas = [t["nome_turma"] for t in self.turmas]
        nomes_turmas.insert(0, "Todas as turmas")  # adiciona a opção "Todas as turmas"
        self.combo_turmas["values"] = nomes_turmas

        if nomes_turmas:
            self.combo_turmas.current(0)
            turma_selecionada(self, None)
    else:
        self.combo_turmas["values"] = ["Não foi possível carregar as turmas"]
        self.combo_turmas.current(0)


def turma_selecionada(self, event):
    nome_turma = self.combo_turmas.get()
    self.listbox_alunos.delete(0, END)

    if not nome_turma or nome_turma == "Não foi possível carregar as turmas":
        return

    if nome_turma == "Todas as turmas":
        # Listar alunos de todas as turmas
        for turma in self.turmas:
            resultado = listar_alunos_api(turma["id_turma"])
            if resultado.get("sucesso"):
                for aluno in resultado.get("alunos", []):
                    self.listbox_alunos.insert(END, f"{aluno['nome']} (RA: {aluno['ra']})")
            else:
                self.listbox_alunos.insert(END, f"Erro ao carregar alunos da turma {turma['nome_turma']}")
    else:
        # Listar alunos da turma selecionada
        turma = next((t for t in self.turmas if t["nome_turma"] == nome_turma), None)
        if not turma:
            return

        resultado = listar_alunos_api(turma["id_turma"])
        if resultado.get("sucesso"):
            for aluno in resultado.get("alunos", []):
                self.listbox_alunos.insert(END, f"{aluno['nome']} (RA: {aluno['ra']})")
        else:
            self.listbox_alunos.insert(END, "Não foi possível carregar os alunos")
