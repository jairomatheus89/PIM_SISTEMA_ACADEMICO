from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from datetime import date

from backend.api import *

def atualizar_tree_atividades(self, turma_selecionada="Todas as turmas"):
    # Limpa a Treeview
    for item in self.tree_atividades.get_children():
        self.tree_atividades.delete(item)

    # Chama a API para listar atividades do professor
    resultado = listar_atividades_api(self.professor["id"])

    if resultado.get("sucesso"):
        atividades = resultado["atividades"]

        # Filtra atividades por turma selecionada, se necessário
        if turma_selecionada != "Todas as turmas":
            atividades = [
                a for a in atividades
                if turma_selecionada in [t["nome_turma"] for t in a.get("turmas", [])]
            ]

        # Insere atividades filtradas na Treeview
        for atividade in atividades:
            self.tree_atividades.insert("", "end", values=(
                atividade["nome_atividade"],
                atividade.get("descricao", ""),
                ", ".join([t["nome_turma"] for t in atividade.get("turmas", [])]),
                atividade.get("data_entrega", "N/A")
            ))
    else:
        self.tree_atividades.insert("", "end", values=("Erro", resultado.get("mensagem", ""), "", ""))


def mostrar_atividades(self):
    # Limpa o frame de atividades antes de criar
    for widget in self.frames["atividades"].winfo_children():
        widget.destroy()

    frame = self.frames["atividades"]

    # === Frame para seleção de turma ===
    Label(frame, text="Selecione a turma:").pack(anchor="center", padx=5, pady=5)

    # Chama a API para listar turmas do professor
    resultado_turmas = listar_turmas_api(self.professor["id"])
    self.turmas = resultado_turmas.get("turmas", []) if resultado_turmas.get("sucesso") else []
    turmas_nomes = ["Todas as turmas"] + [t["nome_turma"] for t in self.turmas]  # opção "Todas as turmas"

    self.combo_turmas_atividades = ttk.Combobox(frame, values=turmas_nomes, state="readonly", width=110)
    self.combo_turmas_atividades.current(0)
    self.combo_turmas_atividades.pack( padx=5, pady=5)

    # Atualiza Treeview ao selecionar uma turma
    self.combo_turmas_atividades.bind(
        "<<ComboboxSelected>>",
        lambda e: atualizar_tree_atividades(self, self.combo_turmas_atividades.get())
    )

    # === Frame para Treeview ===
    self.frame_tree_atividades = Frame(frame)
    self.frame_tree_atividades.pack(fill=X, pady=10, padx=20)

    self.tree_atividades = ttk.Treeview(
        self.frame_tree_atividades,
        columns=("nome", "descricao", "turma", "data_entrega"),
        show="headings",
        height=8
    )

    self.tree_atividades.heading("nome", text="Nome")
    self.tree_atividades.heading("descricao", text="Descrição")
    self.tree_atividades.heading("turma", text="Turma")
    self.tree_atividades.heading("data_entrega", text="Data de Entrega")

    self.tree_atividades.column("nome", width=150, anchor=W, stretch=False)
    self.tree_atividades.column("descricao", width=200, anchor=W, stretch=False)
    self.tree_atividades.column("turma", width=200, anchor=W, stretch=False)
    self.tree_atividades.column("data_entrega", width=100, anchor=W, stretch=False)

    self.tree_atividades.pack()

    # === Frame para botões principais (ficando embaixo da Treeview) ===
    botoes_frame = Frame(frame)
    botoes_frame.pack(pady=10)

    botoes_interno = Frame(botoes_frame)
    botoes_interno.pack()

    Button(botoes_interno, text="Criar Atividade", command=lambda: criar_atividade_widgets(self)).grid(row=0, column=0, padx=5)
    Button(botoes_interno, text="Editar Atividade", command=lambda: editar_atividade_widgets(self)).grid(row=0, column=1, padx=5)
    Button(botoes_interno, text="Excluir Atividade", command=lambda: excluir_atividade_widgets(self)).grid(row=0, column=2, padx=5)

    # Atualiza todas as atividades inicialmente
    atualizar_tree_atividades(self, "Todas as turmas")


def criar_atividade_widgets(self):
    # Limpa todo o frame de atividades
    for widget in self.frames["atividades"].winfo_children():
        widget.destroy()

    # Cria o frame do formulário
    self.form_atividade_frame = Frame(self.frames["atividades"])
    self.form_atividade_frame.pack(fill=X, pady=10)

    # Listar turmas para o combobox
    resultado = listar_turmas_api(self.professor["id"])
    self.turmas = resultado.get("turmas", []) if resultado.get("sucesso") else []

    Label(self.form_atividade_frame, text="Selecione a turma:").pack(anchor=W, padx=5, pady=5)
    turmas_nomes = ["Todas as turmas"] + [t["nome_turma"] for t in self.turmas]
    self.combo_turma_atividade = ttk.Combobox(
        self.form_atividade_frame, 
        values=turmas_nomes, 
        state="readonly", 
        width=100
    )
    self.combo_turma_atividade.current(0)
    self.combo_turma_atividade.pack(pady=5)

    # Campos do formulário
    Label(self.form_atividade_frame, text="Nome da Atividade:").pack(anchor="center", padx=5, pady=5)
    self.nome_atividade_entry = Entry(self.form_atividade_frame, width=100)
    self.nome_atividade_entry.pack(pady=5)

    Label(self.form_atividade_frame, text="Descrição:").pack(anchor="center", padx=5, pady=5)
    self.descricao_atividade_entry = Entry(self.form_atividade_frame, width=100)
    self.descricao_atividade_entry.pack(pady=5)

    Label(self.form_atividade_frame, text="Data de Entrega:").pack(anchor="center", padx=5, pady=5)
    self.data_entrega_entry = DateEntry(
        self.form_atividade_frame,
        date_pattern='yyyy-mm-dd',
        background='darkblue',
        foreground='white',
        borderwidth=2,
        width=20,
        font=("Calibri", 12)
    )
    self.data_entrega_entry.pack(pady=5)

    # Botão criar atividade
    Button(
        self.form_atividade_frame, 
        text="CRIAR ATIVIDADE", 
        command=lambda: criar_atividade(self)
    ).pack(pady=10)


def criar_atividade(self):
    # Pega os dados do formulário
    nome = self.nome_atividade_entry.get().strip()
    descricao = self.descricao_atividade_entry.get().strip()
    turma_selecionada = self.combo_turma_atividade.get()
    data_entrega = self.data_entrega_entry.get_date()  # DateEntry retorna datetime.date

    # Validação de campos obrigatórios
    if not nome or not descricao or not turma_selecionada:
        messagebox.showerror("Erro", "Preencha todos os campos")
        return

    # Verifica a data 
    hoje = date.today()
    if data_entrega < hoje:
        messagebox.showerror("Erro", "A data de entrega inválida ")
        return

    # Confirmação antes de criar
    confirmar = messagebox.askyesno("Confirmação", "Tem certeza que deseja criar esta atividade?")
    if not confirmar:
        return  # Sai da função se o usuário clicar em "Não"

    # Seleção de turmas
    if turma_selecionada == "Todas as turmas":
        turmas_ids = [t["id_turma"] for t in self.turmas]
    else:
        turma = next((t for t in self.turmas if t["nome_turma"] == turma_selecionada), None)
        turmas_ids = [turma["id_turma"]] if turma else []

    # Monta o payload para a API
    payload = {
        "nome_atividade": nome,
        "descricao": descricao,
        "turmas": turmas_ids,
        "data_entrega": data_entrega.strftime("%Y-%m-%d"),
        "professor_id": self.professor["id"]
    }

    # Chama a API
    resultado = criar_atividade_api(payload)

    # Atualiza a Treeview caso sucesso
    if resultado.get("sucesso"):
        messagebox.showinfo("Sucesso", "Atividade criada com sucesso!")
        mostrar_atividades(self)
    else:
        messagebox.showerror("Erro", "Falha ao criar atividade!")


def editar_atividade_widgets(self):
    # Limpar tela
    for widget in self.frames["atividades"].winfo_children():
        widget.destroy()

    self.form_editar_atividade_frame = Frame(self.frames["atividades"])
    self.form_editar_atividade_frame.pack(fill=X, pady=10)

    # === ComboBox de turmas ===
    Label(self.form_editar_atividade_frame, text="Selecione a Atividade:").pack(anchor=W, padx=5, pady=5)

    resultado_turmas = listar_turmas_api(self.professor["id"])
    self.turmas = resultado_turmas.get("turmas", []) if resultado_turmas.get("sucesso") else []
    turmas_nomes = ["Todas as Atividades"] + [t["nome_turma"] for t in self.turmas]

    self.combo_turmas_editar = ttk.Combobox(
        self.form_editar_atividade_frame, values=turmas_nomes, state="readonly"
    )
    self.combo_turmas_editar.current(0)
    self.combo_turmas_editar.pack(fill=X, padx=5, pady=5)

    # === Listbox de atividades ===
    frame_atividades = Frame(self.form_editar_atividade_frame)
    frame_atividades.pack(fill=BOTH, expand=True, padx=20, pady=5)

    self.scrollbar_atividades = Scrollbar(frame_atividades)
    self.scrollbar_atividades.pack(side=RIGHT, fill=Y)

    self.listbox_atividades = Listbox(frame_atividades, yscrollcommand=self.scrollbar_atividades.set, height=10)
    self.listbox_atividades.pack(side=LEFT, fill=BOTH, expand=True)
    self.scrollbar_atividades.config(command=self.listbox_atividades.yview)

    # Atualizar atividades ao selecionar a turma
    def carregar_atividades(event=None):
        nome_turma = self.combo_turmas_editar.get()
        self.listbox_atividades.delete(0, END)
        self.atividades_filtradas = []

        resultado = listar_atividades_api(self.professor["id"])
        if resultado.get("sucesso"):
            for atividade in resultado["atividades"]:
                if nome_turma == "Todas as Atividades" or nome_turma in [t["nome_turma"] for t in atividade.get("turmas", [])]:
                    self.atividades_filtradas.append(atividade)
                    self.listbox_atividades.insert(END, atividade["nome_atividade"])
        else:
            self.listbox_atividades.insert(END, "Erro ao carregar atividades")

    self.combo_turmas_editar.bind("<<ComboboxSelected>>", carregar_atividades)
    carregar_atividades()

    # === Formulário para visualizar e editar ===
    self.form_edicao_frame = Frame(self.form_editar_atividade_frame)
    self.form_edicao_frame.pack(fill=X, pady=10)

    #Labels de visualização (bloqueados)
    Label(self.form_edicao_frame, text="Nome da Atividade (ATUAL):").pack(anchor=W)
    self.nome_atividade_label = Label(self.form_edicao_frame, text="", relief="sunken", anchor=W, width=200)
    self.nome_atividade_label.pack(pady=5)

    Label(self.form_edicao_frame, text="Nome da Atividade (NOVO):").pack(anchor=W)
    self.nome_atividade_entry_editar = Entry(self.form_edicao_frame, width=200)
    self.nome_atividade_entry_editar.pack(pady=5)

    Label(self.form_edicao_frame, text="Descrição (ATUAL):").pack(anchor=W)
    self.descricao_atividade_label = Label(self.form_edicao_frame, text="", relief="sunken", anchor=W, width=200)
    self.descricao_atividade_label.pack(pady=5)

    Label(self.form_edicao_frame, text="Descrição (NOVO):").pack(anchor=W)
    self.descricao_atividade_entry_editar = Entry(self.form_edicao_frame, width=200)
    self.descricao_atividade_entry_editar.pack(pady=5)

    Label(self.form_edicao_frame, text="Data de Entrega (ATUAL):").pack(anchor=W)
    self.data_entrega_label = Label(self.form_edicao_frame, text="", relief="sunken", anchor=W, width=200)
    self.data_entrega_label.pack(pady=5)

    Label(self.form_edicao_frame, text="Data de Entrega (NOVO):").pack(anchor=W)
    self.data_entrega_entry_editar = DateEntry(
        self.form_edicao_frame,
        date_pattern='yyyy-mm-dd',
        background='darkblue',
        foreground='white',
        borderwidth=2,
        width=20,  # DateEntry usa número de caracteres, width=20 é suficiente
        font=("Calibri", 12)
    )
    self.data_entrega_entry_editar.pack(pady=5, anchor=W)

    # Atualizar formulário de edição ao selecionar atividade
    def atividade_selecionada(event=None):
        idx = self.listbox_atividades.curselection()
        if not idx:
            return
        atividade = self.atividades_filtradas[idx[0]]

        # Preencher labels
        self.nome_atividade_label.config(text=atividade["nome_atividade"])
        self.descricao_atividade_label.config(text=atividade.get("descricao", ""))
        self.data_entrega_label.config(text=atividade.get("data_entrega", ""))

        # Preencher inputs editáveis
        self.nome_atividade_entry_editar.delete(0, END)
        self.nome_atividade_entry_editar.insert(0, atividade["nome_atividade"])

        self.descricao_atividade_entry_editar.delete(0, END)
        self.descricao_atividade_entry_editar.insert(0, atividade.get("descricao", ""))

        if atividade.get("data_entrega"):
            self.data_entrega_entry_editar.set_date(atividade["data_entrega"])

        # Guardar id da atividade para salvar edição
        self.id_atividade_editar = atividade["id_atividade"]

    self.listbox_atividades.bind("<<ListboxSelect>>", atividade_selecionada)

    # Seleciona automaticamente a primeira atividade (se houver)
    if self.listbox_atividades.size() > 0:
        self.listbox_atividades.selection_set(0)
        atividade_selecionada(None)

    # Botão para salvar edição
    Button(self.form_edicao_frame, text="Salvar Edição", command=lambda: editar_atividade(self)).pack(pady=10)


def editar_atividade(self):
    # Pega os dados dos inputs de edição
    nome = self.nome_atividade_entry_editar.get().strip()
    descricao = self.descricao_atividade_entry_editar.get().strip()
    data_entrega = self.data_entrega_entry_editar.get_date()
    

    # Validação básica dos campos
    if not nome or not descricao:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return

    if data_entrega < date.today():
        messagebox.showwarning("Atenção", "Data de entrega inválida.")
        return

    
    # Verifica se existe uma atividade selecionada
    if not hasattr(self, "id_atividade_editar") or self.id_atividade_editar is None:
        messagebox.showwarning("Atenção", "Selecione uma atividade para editar.")
        return

    # Monta payload para API
    payload = {
        "id_atividade": self.id_atividade_editar,  # id da atividade selecionada
        "nome_atividade": nome,
        "descricao": descricao,
        "data_entrega": data_entrega.strftime("%Y-%m-%d"),
        "professor_id": self.professor["id"]
    }

    # Confirmação antes de salvar
    confirmar = messagebox.askyesno("Confirmar", "Deseja realmente salvar a edição desta atividade?")
    if not confirmar:
        return

    # Chama API para salvar edição
    resultado = editar_atividade_api(payload)

    if resultado.get("sucesso"):
        messagebox.showinfo("Sucesso", "Atividade editada com sucesso!")
        mostrar_atividades(self)  # Atualiza Treeview
    else:
        messagebox.showerror(
            "Erro",
            f"Não foi possível editar a atividade: {resultado.get('mensagem','Erro desconhecido')}"
        )


def excluir_atividade_widgets(self):
    # Limpar tela
    for widget in self.frames["atividades"].winfo_children():
        widget.destroy()

    self.form_excluir_atividade_frame = Frame(self.frames["atividades"])
    self.form_excluir_atividade_frame.pack(fill=X, pady=10)

    # === ComboBox de turmas ===
    Label(self.form_excluir_atividade_frame, text="Selecione a Atividade:").pack(anchor=W, padx=5, pady=5)

    resultado_turmas = listar_turmas_api(self.professor["id"])
    self.turmas = resultado_turmas.get("turmas", []) if resultado_turmas.get("sucesso") else []
    turmas_nomes = ["Todas as Atividades"] + [t["nome_turma"] for t in self.turmas]

    self.combo_turmas_excluir = ttk.Combobox(
        self.form_excluir_atividade_frame, values=turmas_nomes, state="readonly"
    )
    self.combo_turmas_excluir.current(0)
    self.combo_turmas_excluir.pack(fill=X, padx=5, pady=5)

    # === Listbox de atividades ===
    frame_atividades = Frame(self.form_excluir_atividade_frame)
    frame_atividades.pack(fill=BOTH, expand=True, padx=20, pady=5)

    self.scrollbar_atividades = Scrollbar(frame_atividades)
    self.scrollbar_atividades.pack(side=RIGHT, fill=Y)

    self.listbox_atividades = Listbox(frame_atividades, yscrollcommand=self.scrollbar_atividades.set, height=10)
    self.listbox_atividades.pack(side=LEFT, fill=BOTH, expand=True)
    self.scrollbar_atividades.config(command=self.listbox_atividades.yview)

    # Atualizar atividades ao selecionar a turma
    def carregar_atividades(event=None):
        nome_turma = self.combo_turmas_excluir.get()
        self.listbox_atividades.delete(0, END)
        self.atividades_filtradas = []

        resultado = listar_atividades_api(self.professor["id"])
        if resultado.get("sucesso"):
            for atividade in resultado["atividades"]:
                if nome_turma == "Todas as Atividades" or nome_turma in [t["nome_turma"] for t in atividade.get("turmas", [])]:
                    self.atividades_filtradas.append(atividade)
                    self.listbox_atividades.insert(END, atividade["nome_atividade"])
        else:
            self.listbox_atividades.insert(END, "Erro ao carregar atividades")

    self.combo_turmas_excluir.bind("<<ComboboxSelected>>", carregar_atividades)
    carregar_atividades()

    # === Formulário para visualizar atividade ===
    self.form_visualizacao_frame = Frame(self.form_excluir_atividade_frame)
    self.form_visualizacao_frame.pack(fill=X, pady=10)

    Label(self.form_visualizacao_frame, text="Nome da Atividade:").pack(anchor=W)
    self.nome_atividade_label = Label(self.form_visualizacao_frame, text="", relief="sunken", anchor=W, width=200)
    self.nome_atividade_label.pack(pady=5)

    Label(self.form_visualizacao_frame, text="Descrição:").pack(anchor=W)
    self.descricao_atividade_label = Label(self.form_visualizacao_frame, text="", relief="sunken", anchor=W, width=200)
    self.descricao_atividade_label.pack(pady=5)

    Label(self.form_visualizacao_frame, text="Data de Entrega:").pack(anchor=W)
    self.data_entrega_label = Label(self.form_visualizacao_frame, text="", relief="sunken", anchor=W, width=200)
    self.data_entrega_label.pack(pady=5)

    # Atualizar formulário ao selecionar atividade
    def atividade_selecionada(event=None):
        idx = self.listbox_atividades.curselection()
        if not idx:
            return
        atividade = self.atividades_filtradas[idx[0]]

        # Preencher labels
        self.nome_atividade_label.config(text=atividade["nome_atividade"])
        self.descricao_atividade_label.config(text=atividade.get("descricao", ""))
        self.data_entrega_label.config(text=atividade.get("data_entrega", ""))

        # Guardar id da atividade para exclusão
        self.id_atividade_excluir = atividade["id_atividade"]

    self.listbox_atividades.bind("<<ListboxSelect>>", atividade_selecionada)

    # Seleciona automaticamente a primeira atividade (se houver)
    if self.listbox_atividades.size() > 0:
        self.listbox_atividades.selection_set(0)
        atividade_selecionada(None)

    # Botão para excluir
    Button(self.form_visualizacao_frame, text="Excluir Atividade", command=lambda: excluir_atividade_confirmar(self)).pack(pady=10)


def excluir_atividade_confirmar(self):
    # Verifica se alguma atividade foi selecionada
    if not hasattr(self, "id_atividade_excluir") or not self.id_atividade_excluir:
        messagebox.showwarning("Atenção", "Selecione uma atividade para excluir.")
        return

    # Confirmação antes de excluir
    confirmar = messagebox.askyesno(
        "Confirmar Exclusão",
        "Deseja realmente excluir a atividade selecionada?"
    )
    if not confirmar:
        return

    # Monta payload para API
    payload = {
        "id_atividade": self.id_atividade_excluir,
        "professor_id": self.professor["id"]
    }

    # Chama API para excluir atividade
    resultado = excluir_atividade_api(payload)

    if resultado.get("sucesso"):
        messagebox.showinfo("Sucesso", "Atividade excluída com sucesso!")
        mostrar_atividades(self)  # Atualiza Treeview
    else:
        messagebox.showerror(
            "Erro",
            f"Não foi possível excluir a atividade: {resultado.get('mensagem','Erro desconhecido')}"
        )
