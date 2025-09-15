from tkinter import *
from tkinter import ttk, messagebox

from backend.api import listar_atividades_aluno_api, listar_materias_aluno_api

class AlunoScreen(Frame):
    def __init__(self, master, voltar_callback):
        super().__init__(master)
        self.master = master
        self.voltar_callback = voltar_callback
        self.pack(expand=True, fill="both", padx=10, pady=10)

        Label(self, text="Consultar RA", font=("Calibri", 18, "bold")).pack(pady=10)

        # Campo RA
        frame_ra = Frame(self)
        frame_ra.pack(fill=X, pady=5)
        Label(frame_ra, text="Digite seu RA:", width=15, anchor=W).pack(side=LEFT)
        self.ra_entry = Entry(frame_ra)
        self.ra_entry.pack(side=LEFT, fill=X, expand=True, padx=5)

        # Frame para os botões do menu
        self.menu_frame = Frame(self)
        self.menu_frame.pack(pady=10)

        # Botões
        self.btn_atividades = Button(self.menu_frame, text="Atividades", width=15,
                                     command=lambda: self.mostrar_frame("listar_atividades"))
        self.btn_atividades.grid(row=0, column=0, padx=5)

        self.btn_notas = Button(self.menu_frame, text="Notas", width=15,
                                command=lambda: self.mostrar_frame("listar_notas"))
        self.btn_notas.grid(row=0, column=1, padx=5)

        self.btn_voltar = Button(self.menu_frame, text="Voltar", width=15,
                                 command=self.voltar_elimpar)
        self.btn_voltar.grid(row=0, column=2, padx=5)

        # Frame principal para os conteúdos
        self.content_frame = Frame(self)
        self.content_frame.pack(fill=BOTH, expand=True)

        self.frames = {
            "listar_atividades": Frame(self.content_frame),
            "listar_notas": Frame(self.content_frame)
        }

        # Esconde tudo no início
        for f in self.frames.values():
            f.pack_forget()

        # Inicializa dados
        self.atividades_completas = []
        self.materias_ids = []
        self.materias_nomes = []

    def mostrar_frame(self, chave):
        ra_digitado = self.ra_entry.get().strip()
        if not ra_digitado:
            messagebox.showwarning("Atenção", "Digite o RA antes de continuar!")
            return

        for f in self.frames.values():
            f.pack_forget()

        self.frames[chave].pack(fill=BOTH, expand=True)

        if chave == "listar_atividades":
            self.listar_atividades()
        elif chave == "listar_notas":
            # Aqui você pode adicionar listar_notas()
            pass

    # ==================== Funções de Atividades ====================
    def listar_atividades(self):
        frame_atividades = self.frames["listar_atividades"]

        # Limpa frame antes de reconstruir
        for widget in frame_atividades.winfo_children():
            widget.destroy()

        # Frame para Combobox de matérias
        frame_materia = Frame(frame_atividades)
        frame_materia.pack(fill=X, pady=5)
        Label(frame_materia, text="Selecione a Matéria:", width=15, anchor=W).pack(side=LEFT)
        self.materia_combobox = ttk.Combobox(frame_materia, state="readonly", width=25)
        self.materia_combobox.pack(side=LEFT, fill=X, expand=True, padx=5)
        self.materia_combobox.bind("<<ComboboxSelected>>", lambda e: self.atualizar_tabela())

        # Frame para Treeview
        self.tree_frame = Frame(frame_atividades)
        self.tree_frame.pack(fill=BOTH, expand=True, pady=10)

        colunas = ("atividade", "nota", "status", "data_entrega")
        self.tree = ttk.Treeview(self.tree_frame, columns=colunas, show="headings", height=10, selectmode="browse")
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

        # Estilo Treeview
        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=25, font=("Calibri", 10))
        self.style.map("Treeview", background=[("selected", "#347083")])
        self.style.configure("Treeview.Heading", font=("Calibri", 11, "bold"))

        # Busca atividades do aluno
        self.buscar_atividades()

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

        idx = self.materia_combobox.current()
        if idx == 0 or not self.materias_ids:
            id_professor_selecionado = None
        else:
            id_professor_selecionado = int(self.materias_ids[idx - 1])

        for i, atividade in enumerate(self.atividades_completas):
            if id_professor_selecionado and int(atividade.get("id_professor", 0)) != id_professor_selecionado:
                continue

            status = "Entregue" if atividade.get("entregue") else "Pendente"
            cor_fundo = "#f9f9f9" if i % 2 == 0 else "#e6f2ff"
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
        for row in self.tree.get_children():
            self.tree.delete(row)

    def voltar_elimpar(self):
        # Limpa RA
        self.ra_entry.delete(0, END)
        # Limpa combobox
        self.materias_ids = []
        self.materias_nomes = []
        # Limpa tabela
        self.limpar_tabela()
        # Esconde frames de conteúdo
        for f in self.frames.values():
            f.pack_forget()
        # Chama callback original
        self.voltar_callback()
