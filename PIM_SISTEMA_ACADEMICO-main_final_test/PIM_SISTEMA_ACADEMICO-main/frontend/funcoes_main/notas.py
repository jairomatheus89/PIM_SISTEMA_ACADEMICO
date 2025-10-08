from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from backend.api import *

# Cores
TREE_BG = "#0F1A2B"          # fundo azul escuro
TREE_FG = "#FFFFFF"           # texto branco
LABEL_HIGHLIGHT = "#FFD966"   # amarelo mostarda
ENTRY_BG = "#1E2A40"          # fundo de entry e combobox
ENTRY_FG = "#FFFFFF"
BTN_BG = "#0F1A2B"            # botão azul escuro
BTN_FG = "#FFD966"             # texto botão amarelo

def mostrar_notas(self):
    for widget in self.frames["notas"].winfo_children():
        widget.destroy()
    frame = self.frames["notas"]
    frame.config(bg=TREE_BG)

    Label(frame, text="Selecione a turma:", fg=LABEL_HIGHLIGHT, bg=TREE_BG, font=("Calibri", 11, "bold")).pack(anchor=W, padx=5, pady=5)
    resultado_turmas = listar_turmas_api(self.professor["id"])
    self.turmas = resultado_turmas.get("turmas", []) if resultado_turmas.get("sucesso") else []
    turmas_nomes = ["Selecione uma turma"] + [t["nome_turma"] for t in self.turmas]

    self.combo_turmas_notas = ttk.Combobox(frame, values=turmas_nomes, state="readonly", width=50)
    self.combo_turmas_notas.current(0)
    self.combo_turmas_notas.pack(pady=5)

    Label(frame, text="Selecione a atividade:", fg=LABEL_HIGHLIGHT, bg=TREE_BG, font=("Calibri", 11, "bold")).pack(anchor=W, padx=5, pady=5)
    self.combo_atividades_notas = ttk.Combobox(frame, values=["Selecione uma turma primeiro"], state="readonly", width=50)
    self.combo_atividades_notas.current(0)
    self.combo_atividades_notas.pack(pady=5)

    self.frame_alunos_notas = Frame(frame, bg=TREE_BG)
    self.frame_alunos_notas.pack(fill=X, padx=20, pady=5)

    columns = ("ra", "nome", "nota", "status")
    
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background=TREE_BG,
                    foreground=TREE_FG,
                    fieldbackground=TREE_BG,
                    rowheight=25,
                    font=("Calibri", 11))
    style.map('Treeview', background=[('selected', '#334466')], foreground=[('selected', '#FFFFFF')])
    
    self.tree_alunos_notas = ttk.Treeview(self.frame_alunos_notas, columns=columns, show="headings", height=8)
    for col in columns:
        self.tree_alunos_notas.heading(col, text=col.capitalize())
        self.tree_alunos_notas.column(col, anchor=CENTER, width=100)
    self.tree_alunos_notas.column("nome", width=200)
    self.tree_alunos_notas.pack(side=LEFT, fill=X, expand=True)

    scrollbar = Scrollbar(self.frame_alunos_notas, orient=VERTICAL, command=self.tree_alunos_notas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    self.tree_alunos_notas.configure(yscrollcommand=scrollbar.set)

    self.frame_aluno_selecionado = Frame(frame, bg=TREE_BG)
    self.frame_aluno_selecionado.pack(fill=X, padx=20, pady=10)
    criar_frame_aluno(self)

    self.combo_turmas_notas.bind("<<ComboboxSelected>>", lambda e: carregar_atividades(self))
    self.combo_atividades_notas.bind("<<ComboboxSelected>>", lambda e: carregar_alunos(self))
    self.tree_alunos_notas.bind("<<TreeviewSelect>>", lambda e: atualizar_dados_aluno(self))


def criar_frame_aluno(self):
    self.frame_aluno_selecionado.columnconfigure(0, weight=1)
    self.frame_aluno_selecionado.columnconfigure(1, weight=1)

    Label(self.frame_aluno_selecionado, text="Aluno:", fg=LABEL_HIGHLIGHT, bg=TREE_BG).grid(row=0, column=0, sticky=E, padx=5, pady=2)
    self.label_nome_aluno = Label(self.frame_aluno_selecionado, text="", width=30, anchor=CENTER, fg=TREE_FG, bg=TREE_BG)
    self.label_nome_aluno.grid(row=0, column=1, sticky=W, padx=5, pady=2)

    Label(self.frame_aluno_selecionado, text="RA:", fg=LABEL_HIGHLIGHT, bg=TREE_BG).grid(row=1, column=0, sticky=E, padx=5, pady=2)
    self.label_ra_aluno = Label(self.frame_aluno_selecionado, text="", width=30, anchor=CENTER, fg=TREE_FG, bg=TREE_BG)
    self.label_ra_aluno.grid(row=1, column=1, sticky=W, padx=5, pady=2)

    Label(self.frame_aluno_selecionado, text="Atividade:", fg=LABEL_HIGHLIGHT, bg=TREE_BG).grid(row=2, column=0, sticky=E, padx=5, pady=2)
    self.label_atividade = Label(self.frame_aluno_selecionado, text="", width=30, anchor=CENTER, fg=TREE_FG, bg=TREE_BG)
    self.label_atividade.grid(row=2, column=1, sticky=W, padx=5, pady=2)

    Label(self.frame_aluno_selecionado, text="Nota:", fg=LABEL_HIGHLIGHT, bg=TREE_BG).grid(row=3, column=0, sticky=E, padx=5, pady=2)
    self.nota_entry_aluno = Entry(self.frame_aluno_selecionado, width=10, justify=CENTER, fg=ENTRY_FG, bg=ENTRY_BG)
    self.nota_entry_aluno.grid(row=3, column=1, sticky=W, padx=5, pady=2)

    Label(self.frame_aluno_selecionado, text="Status de entrega:", fg=LABEL_HIGHLIGHT, bg=TREE_BG).grid(row=4, column=0, sticky=E, padx=5, pady=2)
    self.status_entrega_combo = ttk.Combobox(self.frame_aluno_selecionado, values=["Entregue","Não entregue"], state="readonly", width=15)
    self.status_entrega_combo.set("Não entregue")
    self.status_entrega_combo.grid(row=4, column=1, sticky=W, padx=5, pady=2)
    
    self.botao_salvar_aluno = Button(self.frame_aluno_selecionado, text="Salvar", bg=BTN_BG, fg=BTN_FG, font=("Calibri", 11, "bold"), command=lambda: salvar_nota_aluno(self, getattr(self,"aluno_selecionado", None)))
    self.botao_salvar_aluno.grid(row=5, column=0, columnspan=2, pady=10)


def carregar_atividades(self):
    turma_nome = self.combo_turmas_notas.get()
    self.combo_atividades_notas["values"] = ["Selecione uma turma primeiro"]
    self.combo_atividades_notas.current(0)
    self.tree_alunos_notas.delete(*self.tree_alunos_notas.get_children())
    self.label_nome_aluno.config(text="")
    self.label_ra_aluno.config(text="")
    self.label_atividade.config(text="")
    self.nota_entry_aluno.delete(0, END)
    if hasattr(self, "status_entrega_combo"):
        try:
            self.status_entrega_combo.set("")
        except Exception:
            pass
    if turma_nome == "Selecione uma turma":
        return

    turma = next((t for t in self.turmas if t["nome_turma"] == turma_nome), None)
    if not turma:
        return

    resultado = listar_atividades_api(self.professor["id"])
    todas_atividades = resultado.get("atividades", []) if resultado.get("sucesso") else []
    self.atividades = [a for a in todas_atividades if any(t["id_turma"]==turma["id_turma"] for t in a.get("turmas",[]))]
    nomes_atividades = ["Selecione uma atividade"] + [a["nome_atividade"] for a in self.atividades]
    self.combo_atividades_notas["values"] = nomes_atividades
    self.combo_atividades_notas.current(0)


def carregar_alunos(self):
    # limpa tree e painel do aluno ao trocar de atividade
    self.tree_alunos_notas.delete(*self.tree_alunos_notas.get_children())

    # Limpa painel/seleção do aluno (caso um aluno anterior esteja carregado)
    if hasattr(self, "label_nome_aluno"):
        self.label_nome_aluno.config(text="")
    if hasattr(self, "label_ra_aluno"):
        self.label_ra_aluno.config(text="")
    if hasattr(self, "label_atividade"):
        self.label_atividade.config(text="")
    if hasattr(self, "nota_entry_aluno"):
        try:
            self.nota_entry_aluno.delete(0, END)
        except Exception:
            pass
    if hasattr(self, "status_entrega_combo"):
        try:
            self.status_entrega_combo.set("")
        except Exception:
            pass

    # limpa seleção interna e variável do aluno selecionado
    try:
        for sel in self.tree_alunos_notas.selection():
            self.tree_alunos_notas.selection_remove(sel)
    except Exception:
        pass
    self.aluno_selecionado = None
    atividade_nome = self.combo_atividades_notas.get()
    turma_nome = self.combo_turmas_notas.get()
    if atividade_nome == "Selecione uma atividade" or turma_nome=="Selecione uma turma":
        return

    turma = next((t for t in self.turmas if t["nome_turma"] == turma_nome), None)
    if not turma:
        return

    self.atividade_selecionada = next((a for a in self.atividades if a["nome_atividade"]==atividade_nome), None)
    if not self.atividade_selecionada:
        return

    if not any(t["id_turma"]==turma["id_turma"] for t in self.atividade_selecionada.get("turmas",[])):
        messagebox.showwarning("Atenção","A atividade não pertence à turma selecionada.")
        return

    resultado = listar_alunos_api(turma["id_turma"])
    self.alunos = resultado.get("alunos", []) if resultado.get("sucesso") else []

    for aluno in self.alunos:
        resultado_nota = listar_atividades_aluno_api(aluno["ra"])
        atividades_aluno = resultado_nota.get("atividades", []) if resultado_nota.get("sucesso") else []
        nota = 0
        status = "Não entregue"
        for a in atividades_aluno:
            if a["nome_atividade"] == self.atividade_selecionada["nome_atividade"]:
                nota = a.get("nota") or 0
                status = "Entregue" if a.get("entregue") else "Não entregue"
                break
        self.tree_alunos_notas.insert("", END, values=(aluno["ra"], aluno["nome"], nota, status))


def atualizar_dados_aluno(self):
    selecionado = self.tree_alunos_notas.selection()
    if not selecionado:
        return
    idx = self.tree_alunos_notas.index(selecionado[0])
    aluno = self.alunos[idx]
    self.aluno_selecionado = aluno

    resultado = listar_atividades_aluno_api(aluno["ra"])
    atividades_aluno = resultado.get("atividades", []) if resultado.get("sucesso") else []
    nota = 0
    entregue = "Entregue"
    for a in atividades_aluno:
        if a["nome_atividade"] == self.atividade_selecionada["nome_atividade"]:
            nota = a.get("nota") or 0            
            break

    self.label_nome_aluno.config(text=aluno["nome"])
    self.label_ra_aluno.config(text=aluno["ra"])
    self.label_atividade.config(text=self.atividade_selecionada["nome_atividade"])
    self.nota_entry_aluno.delete(0, END)
    self.nota_entry_aluno.insert(0, str(nota))
    self.status_entrega_combo.set(entregue)


def salvar_nota_aluno(self, aluno):
    if not aluno:
        messagebox.showwarning("Atenção","Nenhum aluno selecionado.")
        return

    nota_str = self.nota_entry_aluno.get().strip()
    status = self.status_entrega_combo.get()
    try:
        nota_valor = float(nota_str)
        if nota_valor<0 or nota_valor>10:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Atenção","Digite uma nota válida (0 a 10).")
        return

    entregue = True if status=="Entregue" else False
    payload = {
        "id_aluno": aluno["id_aluno"],
        "id_atividade": self.atividade_selecionada["id_atividade"],
        "nota": nota_valor,
        "entregue": entregue,
        "professor_id": self.professor["id"]
    }

    resultado = salvar_nota_api(payload)
    if resultado.get("sucesso"):
        messagebox.showinfo("Sucesso",f"Nota do aluno {aluno['nome']} salva com sucesso!")
        carregar_alunos(self)  # atualiza Treeview de notas
    else:
        messagebox.showerror("Erro",resultado.get("mensagem","Erro ao salvar nota"))
