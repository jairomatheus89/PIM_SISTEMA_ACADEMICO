from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from backend.api import *  # listar_turmas_api, listar_atividades_api, listar_alunos_api, salvar_nota_api

def mostrar_notas(self):
    """Cria a interface de notas: turmas, atividades, Treeview de alunos e frame do aluno."""
    # Limpa o frame principal
    for widget in self.frames["notas"].winfo_children():
        widget.destroy()
    frame = self.frames["notas"]

    # === ComboBox de Turmas ===
    Label(frame, text="Selecione a turma:").pack(anchor=W, padx=5, pady=5)
    resultado_turmas = listar_turmas_api(self.professor["id"])
    self.turmas = resultado_turmas.get("turmas", []) if resultado_turmas.get("sucesso") else []
    turmas_nomes = ["Selecione uma turma"] + [t["nome_turma"] for t in self.turmas]

    self.combo_turmas_notas = ttk.Combobox(frame, values=turmas_nomes, state="readonly", width=50)
    self.combo_turmas_notas.current(0)
    self.combo_turmas_notas.pack(pady=5)

    # === ComboBox de Atividades ===
    Label(frame, text="Selecione a atividade:").pack(anchor=W, padx=5, pady=5)
    self.combo_atividades_notas = ttk.Combobox(frame, values=["Selecione uma turma primeiro"], state="readonly", width=50)
    self.combo_atividades_notas.current(0)
    self.combo_atividades_notas.pack(pady=5)

    # === Treeview de Alunos ===
    self.frame_alunos_notas = Frame(frame)
    self.frame_alunos_notas.pack(fill=X, padx=20, pady=5)

    columns = ("ra", "nome")
    self.tree_alunos = ttk.Treeview(self.frame_alunos_notas, columns=columns, show="headings", height=8)
    self.tree_alunos.heading("ra", text="RA")
    self.tree_alunos.heading("nome", text="Nome")
    self.tree_alunos.column("ra", width=100)
    self.tree_alunos.column("nome", width=250)
    self.tree_alunos.pack(side=LEFT, fill=X, expand=True)

    scrollbar = Scrollbar(self.frame_alunos_notas, orient=VERTICAL, command=self.tree_alunos.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    self.tree_alunos.configure(yscrollcommand=scrollbar.set)

    # === Frame do aluno selecionado (sempre visível) ===
    self.frame_aluno_selecionado = Frame(frame)
    self.frame_aluno_selecionado.pack(fill=X, padx=20, pady=10)
    criar_frame_aluno(self)

    # === Binds de eventos ===
    self.combo_turmas_notas.bind("<<ComboboxSelected>>", lambda e: carregar_atividades(self))
    self.combo_atividades_notas.bind("<<ComboboxSelected>>", lambda e: carregar_alunos(self))
    self.tree_alunos.bind("<<TreeviewSelect>>", lambda e: atualizar_dados_aluno(self))


def criar_frame_aluno(self):
    """Cria widgets do frame do aluno selecionado."""
    Label(self.frame_aluno_selecionado, text="Aluno:").grid(row=0, column=0, sticky=W, padx=5, pady=2)
    self.label_nome_aluno = Label(self.frame_aluno_selecionado, text="")
    self.label_nome_aluno.grid(row=0, column=1, sticky=W, padx=5, pady=2)

    Label(self.frame_aluno_selecionado, text="RA:").grid(row=1, column=0, sticky=W, padx=5, pady=2)
    self.label_ra_aluno = Label(self.frame_aluno_selecionado, text="")
    self.label_ra_aluno.grid(row=1, column=1, sticky=W, padx=5, pady=2)

    Label(self.frame_aluno_selecionado, text="Atividade:").grid(row=2, column=0, sticky=W, padx=5, pady=2)
    self.label_atividade = Label(self.frame_aluno_selecionado, text="")
    self.label_atividade.grid(row=2, column=1, sticky=W, padx=5, pady=2)

    Label(self.frame_aluno_selecionado, text="Nota:").grid(row=3, column=0, sticky=W, padx=5, pady=2)
    self.nota_entry_aluno = Entry(self.frame_aluno_selecionado, width=10)
    self.nota_entry_aluno.grid(row=3, column=1, sticky=W, padx=5, pady=2)

    Label(self.frame_aluno_selecionado, text="Status de entrega:").grid(row=4, column=0, sticky=W, padx=5, pady=2)
    self.status_entrega_combo = ttk.Combobox(
        self.frame_aluno_selecionado,
        values=["Entregue", "Não entregue"],
        state="readonly",
        width=15
    )
    self.status_entrega_combo.grid(row=4, column=1, sticky=W, padx=5, pady=2)
    self.status_entrega_combo.set("Não entregue")

    self.botao_salvar_aluno = Button(
        self.frame_aluno_selecionado,
        text="Salvar",
        command=lambda: salvar_nota_aluno(self, getattr(self, "aluno_selecionado", None))
    )
    self.botao_salvar_aluno.grid(row=5, column=0, columnspan=2, pady=10)


def carregar_atividades(self):
    """Carrega atividades da turma selecionada."""
    turma_nome = self.combo_turmas_notas.get()
    # Reset
    self.combo_atividades_notas["values"] = ["Selecione uma turma primeiro"]
    self.combo_atividades_notas.current(0)
    for item in self.tree_alunos.get_children():
        self.tree_alunos.delete(item)
    self.label_nome_aluno.config(text="")
    self.label_ra_aluno.config(text="")
    self.label_atividade.config(text="")
    self.nota_entry_aluno.delete(0, END)
    self.status_entrega_combo.set("Não entregue")

    if turma_nome == "Selecione uma turma":
        return

    turma = next((t for t in self.turmas if t["nome_turma"] == turma_nome), None)
    if not turma:
        return

    resultado = listar_atividades_api(self.professor["id"])
    todas_atividades = resultado.get("atividades", []) if resultado.get("sucesso") else []

    self.atividades = [a for a in todas_atividades if any(t["id_turma"] == turma["id_turma"] for t in a.get("turmas", []))]
    nomes_atividades = ["Selecione uma atividade"] + [a["nome_atividade"] for a in self.atividades]
    self.combo_atividades_notas["values"] = nomes_atividades
    self.combo_atividades_notas.current(0)


def carregar_alunos(self):
    """Carrega alunos da atividade selecionada."""
    for item in self.tree_alunos.get_children():
        self.tree_alunos.delete(item)

    atividade_nome = self.combo_atividades_notas.get()
    if atividade_nome == "Selecione uma atividade":
        return

    self.atividade_selecionada = next((a for a in self.atividades if a["nome_atividade"] == atividade_nome), None)
    if not self.atividade_selecionada:
        return

    turma_id = self.atividade_selecionada["turmas"][0]["id_turma"]
    resultado = listar_alunos_api(turma_id)
    self.alunos = resultado.get("alunos", []) if resultado.get("sucesso") else []

    for aluno in self.alunos:
        self.tree_alunos.insert("", END, values=(aluno["ra"], aluno["nome"]))


def atualizar_dados_aluno(self):
    """Atualiza os campos do frame do aluno selecionado quando ele é clicado na Treeview."""
    selecionado = self.tree_alunos.selection()
    if not selecionado:
        return
    idx = self.tree_alunos.index(selecionado[0])
    aluno = self.alunos[idx]
    self.aluno_selecionado = aluno

    resultado = listar_atividades_aluno_api(aluno["ra"])
    atividades_aluno = resultado.get("atividades", []) if resultado.get("sucesso") else []

    nota = 0
    entregue = "Não entregue"
    for a in atividades_aluno:
        if a["nome_atividade"] == self.atividade_selecionada["nome_atividade"]:
            nota = a.get("nota") or 0
            entregue = "Entregue" if a.get("entregue") else "Não entregue"
            break

    self.label_nome_aluno.config(text=aluno["nome"])
    self.label_ra_aluno.config(text=aluno["ra"])
    self.label_atividade.config(text=self.atividade_selecionada["nome_atividade"])
    self.nota_entry_aluno.delete(0, END)
    self.nota_entry_aluno.insert(0, str(nota))
    self.status_entrega_combo.set(entregue)


def salvar_nota_aluno(self, aluno):
    """Salva ou atualiza a nota e o status de entrega do aluno selecionado."""
    if not aluno:
        messagebox.showwarning("Atenção", "Nenhum aluno selecionado.")
        return

    nota_str = self.nota_entry_aluno.get().strip()
    status = self.status_entrega_combo.get()

    try:
        nota_valor = float(nota_str)
        if nota_valor < 0 or nota_valor > 10:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Atenção", "Digite uma nota válida (0 a 10).")
        return

    entregue = True if status == "Entregue" else False

    payload = {
        "id_aluno": aluno["id_aluno"],
        "id_atividade": self.atividade_selecionada["id_atividade"],
        "nota": nota_valor,
        "entregue": entregue,
        "professor_id": self.professor["id"]
    }

    resultado = salvar_nota_api(payload)
    if resultado.get("sucesso"):
        messagebox.showinfo("Sucesso", f"Nota do aluno {aluno['nome']} salva com sucesso!")
    else:
        messagebox.showerror("Erro", resultado.get("mensagem", "Erro ao salvar nota"))
