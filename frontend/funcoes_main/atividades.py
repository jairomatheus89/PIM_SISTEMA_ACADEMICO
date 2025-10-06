from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import date
from backend.api import *

# ==================== Cores do tema ====================
BG_COLOR = "#1E2A38"      # Azul escuro
BTN_COLOR = "#D4A017"     # Mostarda escuro
BTN_TEXT_COLOR = "#000000" # Preto

# ==================== Funções auxiliares ====================
def get_turmas(self):
    resultado = listar_turmas_api(self.professor["id"])
    self.turmas = resultado.get("turmas", []) if resultado.get("sucesso") else []
    turmas_nomes = ["Todas as turmas"] + [t["nome_turma"] for t in self.turmas]
    return turmas_nomes

def get_atividades(self, turma_selecionada="Todas as turmas"):
    resultado = listar_atividades_api(self.professor["id"])
    if resultado.get("sucesso"):
        atividades = resultado["atividades"]
        if turma_selecionada != "Todas as turmas":
            atividades = [
                a for a in atividades
                if turma_selecionada in [t["nome_turma"] for t in a.get("turmas", [])]
            ]
        return atividades
    return []

# ==================== Atualizar Treeview ====================
def atualizar_tree_atividades(self, turma_selecionada="Todas as turmas"):
    for item in self.tree_atividades.get_children():
        self.tree_atividades.delete(item)

    atividades = get_atividades(self, turma_selecionada)

    if atividades:
        for atividade in atividades:
            self.tree_atividades.insert("", "end", iid=atividade["id_atividade"], values=(
                atividade["nome_atividade"],
                atividade.get("descricao", ""),
                ", ".join([t["nome_turma"] for t in atividade.get("turmas", [])]),
                atividade.get("data_entrega", "N/A")
            ))
    else:
        self.tree_atividades.insert("", "end", values=("Nenhuma atividade", "", "", ""))

# ==================== Mostrar atividades ====================
def mostrar_atividades(self):
    for widget in self.frames["atividades"].winfo_children():
        widget.destroy()

    frame = self.frames["atividades"]
    frame.config(bg=BG_COLOR)

    Label(frame, text="Selecione a turma:", bg=BG_COLOR, fg="white", font=("Arial", 12, "bold")).pack(anchor="center", padx=5, pady=5)

    turmas_nomes = get_turmas(self)
    self.combo_turmas_atividades = ttk.Combobox(frame, values=turmas_nomes, state="readonly", width=110)
    self.combo_turmas_atividades.current(0)
    self.combo_turmas_atividades.pack(padx=5, pady=5)
    self.combo_turmas_atividades.bind(
        "<<ComboboxSelected>>",
        lambda e: atualizar_tree_atividades(self, self.combo_turmas_atividades.get())
    )

    self.frame_tree_atividades = Frame(frame, bg=BG_COLOR)
    self.frame_tree_atividades.pack(fill=X, pady=10, padx=20)

    self.tree_atividades = ttk.Treeview(
        self.frame_tree_atividades,
        columns=("nome", "descricao", "turma", "data_entrega"),
        show="headings",
        height=8
    )
    for col, txt, w in [("nome", "Nome", 150), ("descricao", "Descrição", 200),
                         ("turma", "Turma", 200), ("data_entrega", "Data de Entrega", 100)]:
        self.tree_atividades.heading(col, text=txt)
        self.tree_atividades.column(col, width=w, anchor=CENTER, stretch=False)
    self.tree_atividades.pack()

    # Botões principais
    botoes_frame = Frame(frame, bg=BG_COLOR)
    botoes_frame.pack(pady=10)
    botoes_interno = Frame(botoes_frame, bg=BG_COLOR)
    botoes_interno.pack()

    Button(botoes_interno, text="Criar Atividade", bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
           command=lambda: criar_atividade_widgets(self), width=20).grid(row=0, column=0, padx=5)
    Button(botoes_interno, text="Editar Atividade", bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
           command=lambda: editar_atividade_tree(self), width=20).grid(row=0, column=1, padx=5)
    Button(botoes_interno, text="Excluir Atividade", bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
           command=lambda: excluir_atividade_tree(self), width=20).grid(row=0, column=2, padx=5)

    atualizar_tree_atividades(self, "Todas as turmas")

# ==================== Criar atividade ====================
def criar_atividade_widgets(self):
    for widget in self.frames["atividades"].winfo_children():
        widget.destroy()

    frame = self.frames["atividades"]
    frame.config(bg=BG_COLOR)
    self.form_atividade_frame = Frame(frame, bg=BG_COLOR)
    self.form_atividade_frame.pack(fill=X, pady=10)

    turmas_nomes = get_turmas(self)
    Label(self.form_atividade_frame, text="Selecione a turma:", bg=BG_COLOR, fg="white").pack(anchor=W, padx=5, pady=5)
    self.combo_turma_atividade = ttk.Combobox(self.form_atividade_frame, values=turmas_nomes, state="readonly", width=100)
    self.combo_turma_atividade.current(0)
    self.combo_turma_atividade.pack(pady=5)

    Label(self.form_atividade_frame, text="Nome da Atividade:", bg=BG_COLOR, fg="white").pack(anchor="center", padx=5, pady=5)
    self.nome_atividade_entry = Entry(self.form_atividade_frame, width=100)
    self.nome_atividade_entry.pack(pady=5)

    Label(self.form_atividade_frame, text="Descrição:", bg=BG_COLOR, fg="white").pack(anchor="center", padx=5, pady=5)
    self.descricao_atividade_entry = Entry(self.form_atividade_frame, width=100)
    self.descricao_atividade_entry.pack(pady=5)

    Label(self.form_atividade_frame, text="Data de Entrega:", bg=BG_COLOR, fg="white").pack(anchor="center", padx=5, pady=5)
    self.data_entrega_entry = DateEntry(self.form_atividade_frame, date_pattern='yyyy-mm-dd',
                                       background='darkblue', foreground='white', borderwidth=2, width=20, font=("Calibri", 12))
    self.data_entrega_entry.pack(pady=5)

    Button(self.form_atividade_frame, text="CRIAR ATIVIDADE", bg=BTN_COLOR, fg=BTN_TEXT_COLOR,
           command=lambda: criar_atividade(self)).pack(pady=10)

# ==================== Funções de criação, edição e exclusão ====================
def criar_atividade(self):
    nome = self.nome_atividade_entry.get().strip()
    descricao = self.descricao_atividade_entry.get().strip()
    turma_selecionada = self.combo_turma_atividade.get()
    data_entrega = self.data_entrega_entry.get_date()

    if not nome or not descricao or not turma_selecionada:
        messagebox.showerror("Erro", "Preencha todos os campos")
        return

    if data_entrega < date.today():
        messagebox.showerror("Erro", "A data de entrega é inválida")
        return

    if not messagebox.askyesno("Confirmação", "Tem certeza que deseja criar esta atividade?"):
        return

    turmas_ids = [t["id_turma"] for t in self.turmas] if turma_selecionada == "Todas as turmas" else [next(t["id_turma"] for t in self.turmas if t["nome_turma"] == turma_selecionada)]

    payload = {
        "nome_atividade": nome,
        "descricao": descricao,
        "turmas": turmas_ids,
        "data_entrega": data_entrega.strftime("%Y-%m-%d"),
        "professor_id": self.professor["id"]
    }

    resultado = criar_atividade_api(payload)
    if resultado.get("sucesso"):
        messagebox.showinfo("Sucesso", "Atividade criada com sucesso!")
        mostrar_atividades(self)
    else:
        messagebox.showerror("Erro", "Falha ao criar atividade!")

def editar_atividade_tree(self):
    selecionado = self.tree_atividades.focus()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione uma atividade na lista para editar.")
        return
    atividade = next((a for a in get_atividades(self) if a["id_atividade"] == int(selecionado)), None)
    if not atividade:
        messagebox.showerror("Erro", "Atividade não encontrada.")
        return

    criar_atividade_widgets(self)
    self.combo_turma_atividade.pack_forget()

    self.nome_atividade_entry.delete(0, END)
    self.nome_atividade_entry.insert(0, atividade["nome_atividade"])
    self.descricao_atividade_entry.delete(0, END)
    self.descricao_atividade_entry.insert(0, atividade.get("descricao", ""))
    self.data_entrega_entry.set_date(atividade.get("data_entrega", date.today()))
    self.id_atividade_editar = atividade["id_atividade"]

    for widget in self.form_atividade_frame.winfo_children():
        if isinstance(widget, Button):
            widget.config(text="SALVAR EDIÇÃO", command=lambda: editar_atividade(self))

def editar_atividade(self):
    nome = self.nome_atividade_entry.get().strip()
    descricao = self.descricao_atividade_entry.get().strip()
    data_entrega = self.data_entrega_entry.get_date()

    if not nome or not descricao:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return

    if data_entrega < date.today():
        messagebox.showwarning("Atenção", "Data de entrega inválida.")
        return

    payload = {
        "id_atividade": self.id_atividade_editar,
        "nome_atividade": nome,
        "descricao": descricao,
        "data_entrega": data_entrega.strftime("%Y-%m-%d"),
        "professor_id": self.professor["id"]
    }

    if not messagebox.askyesno("Confirmar", "Deseja realmente salvar a edição desta atividade?"):
        return

    resultado = editar_atividade_api(payload)
    if resultado.get("sucesso"):
        messagebox.showinfo("Sucesso", "Atividade editada com sucesso!")
        mostrar_atividades(self)
    else:
        messagebox.showerror("Erro", f"Não foi possível editar a atividade: {resultado.get('mensagem','Erro desconhecido')}")

def excluir_atividade_tree(self):
    selecionado = self.tree_atividades.focus()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione uma atividade no Treeview para excluir.")
        return

    atividade = next((a for a in get_atividades(self) if a["id_atividade"] == int(selecionado)), None)
    if not atividade:
        messagebox.showerror("Erro", "Atividade não encontrada.")
        return

    if not messagebox.askyesno("Confirmar Exclusão", "Deseja realmente excluir a atividade selecionada?"):
        return

    payload = {
        "id_atividade": atividade["id_atividade"],
        "professor_id": self.professor["id"]
    }

    resultado = excluir_atividade_api(payload)
    if resultado.get("sucesso"):
        messagebox.showinfo("Sucesso", "Atividade excluída com sucesso!")
        mostrar_atividades(self)
    else:
        messagebox.showerror("Erro", f"Não foi possível excluir a atividade: {resultado.get('mensagem','Erro desconhecido')}")
