from tkinter import *
from tkinter import ttk, messagebox
from backend.api import listar_atividades_aluno_id_api, listar_materias_aluno_id_api, pegar_ra_id_alunos_api
from backend.src.algoritimo import merge_sort, busca_binaria  

class AlunoScreen(Frame):
    def __init__(self, master, voltar_callback):
        super().__init__(master, bg="#0D1B2A")
        self.master = master
        self.voltar_callback = voltar_callback
        self.pack(expand=True, fill="both", padx=10, pady=10)

        Label(self, text="Consultar RA", font=("Calibri", 18, "bold"), bg="#0D1B2A", fg="#F0F0F0").pack(pady=10)

        # Campo RA
        frame_ra = Frame(self, bg="#0D1B2A")
        frame_ra.pack(fill=X, pady=5)
        Label(frame_ra, text="Digite seu RA:", width=15, anchor=W, bg="#0D1B2A", fg="#F0F0F0").pack(side=LEFT)
        self.ra_entry = Entry(frame_ra, bg="#FFFFFF", fg="#000000", font=("Arial", 12), bd=1, relief=SOLID)
        self.ra_entry.pack(side=LEFT, fill=X, expand=True, padx=5)

        # Frame dos botões
        self.menu_frame = Frame(self, bg="#0D1B2A")
        self.menu_frame.pack(pady=10)

        def criar_botao(texto, comando, cor_bg="#D4A017"):
            return Button(self.menu_frame, text=texto, width=15, bg=cor_bg, fg="#0D1B2A", font=("Arial", 12, "bold"),
                          activebackground="#e6b800", command=comando)

        self.btn_atividades = criar_botao("Atividades", lambda: self.mostrar_frame("listar_atividades"))
        self.btn_atividades.grid(row=0, column=0, padx=5)

        self.btn_notas = criar_botao("Notas", lambda: self.mostrar_frame("listar_notas"))
        self.btn_notas.grid(row=0, column=1, padx=5)

        self.btn_voltar = criar_botao("Voltar", self.voltar_elimpar, cor_bg="#CCCCCC")
        self.btn_voltar.grid(row=0, column=2, padx=5)

        # Frame de conteúdo
        self.content_frame = Frame(self, bg="#0D1B2A")
        self.content_frame.pack(fill=BOTH, expand=True)

        self.frames = {
            "listar_atividades": Frame(self.content_frame, bg="#0D1B2A"),
            "listar_notas": Frame(self.content_frame, bg="#0D1B2A")
        }

        for f in self.frames.values():
            f.pack_forget()

        self.atividades_completas = []
        self.materias_ids = []
        self.materias_nomes = []

        self.ra_para_id = {}
        self.ras_ordenados = []
        self.inicializar_busca_algoritmica()

        # Treeview style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#f9f9f9", foreground="black", rowheight=25, fieldbackground="#f9f9f9", font=("Calibri", 10))
        self.style.map("Treeview", background=[("selected", "#D4A017")], foreground=[("selected", "#0D1B2A")])
        self.style.configure("Treeview.Heading", font=("Calibri", 11, "bold"), background="#D4A017", foreground="#0D1B2A")

    def inicializar_busca_algoritmica(self):
        alunos = pegar_ra_id_alunos_api()
        if not alunos:
            messagebox.showerror("Erro", "Não foi possível carregar os alunos.")
            self.ra_para_id = {}
            self.ras_ordenados = []
            return
        self.ra_para_id = {int(a["ra"]): a["id_aluno"] for a in alunos}
        self.ras_ordenados = merge_sort(list(self.ra_para_id.keys()))

    def mostrar_frame(self, chave):
        ra_digitado = self.ra_entry.get().strip()
        if not ra_digitado:
            messagebox.showwarning("Atenção", "Digite o RA antes de continuar!")
            return
        try:
            ra_int = int(ra_digitado)
        except ValueError:
            messagebox.showerror("Erro", "RA inválido!")
            return
        pos = busca_binaria(self.ras_ordenados, ra_int)
        if pos == -1:
            messagebox.showerror("Erro", f"RA {ra_digitado} não encontrado!")
            return
        self.id_aluno_atual = self.ra_para_id[ra_int]
        for f in self.frames.values():
            f.pack_forget()
        if chave == "listar_atividades":
            if not self.listar_atividades(): return
        elif chave == "listar_notas":
            if not self.listar_notas(): return
        self.frames[chave].pack(fill=BOTH, expand=True)

    # ---------- LISTAR ATIVIDADES ----------
    def listar_atividades(self):
        frame_atividades = self.frames["listar_atividades"]
        for widget in frame_atividades.winfo_children():
            widget.destroy()

        Label(frame_atividades, text="Selecione a Matéria:", font=("Calibri", 12, "bold"),
              bg="#0D1B2A", fg="#F0F0F0").pack(pady=5)

        materias_resp = listar_materias_aluno_id_api(self.id_aluno_atual)
        if not materias_resp["sucesso"]:
            messagebox.showerror("Erro", "Não foi possível carregar as matérias.")
            return False

        self.materias_notas = materias_resp["materias"]
        nomes = [f'{m["materia"]} - {m["nome_professor"]}' for m in self.materias_notas]

        self.combo_materias_atividades = ttk.Combobox(frame_atividades, values=nomes, state="readonly", width=50)
        self.combo_materias_atividades.pack(pady=5)
        self.combo_materias_atividades.bind("<<ComboboxSelected>>", lambda e: self.carregar_atividades())

        self.tree_frame_atividades = Frame(frame_atividades, bg="#0D1B2A")
        self.tree_frame_atividades.pack(padx=20, pady=10, fill=BOTH, expand=True)

        self.tree_atividades = ttk.Treeview(self.tree_frame_atividades, show="headings", height=10)
        self.tree_atividades.pack(fill=BOTH, expand=True)

        colunas = ("atividade", "nota", "status", "data_entrega")
        self.tree_atividades["columns"] = colunas
        for col in colunas:
            self.tree_atividades.heading(col, text=col.capitalize())
            self.tree_atividades.column(col, anchor=CENTER, width=100)

        scrollbar = Scrollbar(self.tree_frame_atividades, orient=VERTICAL, command=self.tree_atividades.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree_atividades.configure(yscrollcommand=scrollbar.set)

        # Carregar todas as atividades inicialmente
        resultado = listar_atividades_aluno_id_api(self.id_aluno_atual)
        self.atividades_completas = resultado.get("atividades", []) if resultado.get("sucesso") else []
        self.carregar_atividades()
        return True

    def carregar_atividades(self):
        # Limpar tabela
        for row in self.tree_atividades.get_children():
            self.tree_atividades.delete(row)

        idx = self.combo_materias_atividades.current()
        if idx == -1:
            return

        id_professor_selecionado = self.materias_notas[idx]["id_professor"]

        # Filtrar atividades pela matéria/professor selecionado
        atividades_filtradas = [a for a in self.atividades_completas if int(a.get("id_professor", 0)) == id_professor_selecionado]

        for i, atividade in enumerate(atividades_filtradas):
            status = "Entregue" if atividade.get("entregue") else "Pendente"
            cor_fundo = "#f9f9f9" if i % 2 == 0 else "#e6f2ff"
            cor_texto = "green" if status == "Entregue" else "red"
            item = self.tree_atividades.insert("", "end", values=(
                atividade["nome_atividade"],
                atividade.get("nota", "-"),
                status,
                atividade.get("data_entrega", "-")
            ))
            self.tree_atividades.tag_configure(f"linha_{i}", background=cor_fundo, foreground="black")
            self.tree_atividades.item(item, tags=(f"linha_{i}", f"status_{i}"))
            self.tree_atividades.tag_configure(f"status_{i}", foreground=cor_texto)

    # ---------- LISTAR NOTAS ----------
    def listar_notas(self):
        frame_notas = self.frames["listar_notas"]
        for widget in frame_notas.winfo_children():
            widget.destroy()

        Label(frame_notas, text="Selecione a Matéria:", font=("Calibri", 12, "bold"),
              bg="#0D1B2A", fg="#F0F0F0").pack(pady=5)

        materias_resp = listar_materias_aluno_id_api(self.id_aluno_atual)
        if not materias_resp["sucesso"]:
            messagebox.showerror("Erro", "Não foi possível carregar as matérias.")
            return False

        self.materias_notas = materias_resp["materias"]
        nomes = [f'{m["materia"]} - {m["nome_professor"]}' for m in self.materias_notas]

        self.combo_materias_notas = ttk.Combobox(frame_notas, values=nomes, state="readonly", width=50)
        self.combo_materias_notas.pack(pady=5)
        self.combo_materias_notas.bind("<<ComboboxSelected>>", lambda e: self.carregar_notas())

        self.tree_frame_notas = Frame(frame_notas, bg="#0D1B2A")
        self.tree_frame_notas.pack(padx=20, pady=10, fill=BOTH, expand=True)

        self.tree_notas = ttk.Treeview(self.tree_frame_notas, show="headings", height=10)
        self.tree_notas.pack(fill=BOTH, expand=True)

        colunas = ("atividade", "nota", "status", "data_entrega")
        self.tree_notas["columns"] = colunas
        for col in colunas:
            self.tree_notas.heading(col, text=col.capitalize())
            self.tree_notas.column(col, anchor=CENTER, width=100)

        scrollbar = Scrollbar(self.tree_frame_notas, orient=VERTICAL, command=self.tree_notas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.tree_notas.configure(yscrollcommand=scrollbar.set)

        self.carregar_notas()
        return True

    def carregar_notas(self):
        for row in self.tree_notas.get_children():
            self.tree_notas.delete(row)

        idx = self.combo_materias_notas.current()
        if idx == -1:
            return

        id_professor_selecionado = self.materias_notas[idx]["id_professor"]
        resultado = listar_atividades_aluno_id_api(self.id_aluno_atual)
        atividades = resultado.get("atividades", []) if resultado.get("sucesso") else []

        atividades_filtradas = [a for a in atividades if int(a.get("id_professor", 0)) == id_professor_selecionado]

        for i, atividade in enumerate(atividades_filtradas):
            status = "Entregue" if atividade.get("entregue") else "Pendente"
            cor_fundo = "#f9f9f9" if i % 2 == 0 else "#e6f2ff"
            cor_texto = "green" if status == "Entregue" else "red"
            item = self.tree_notas.insert("", "end", values=(
                atividade["nome_atividade"],
                atividade.get("nota", "-"),
                status,
                atividade.get("data_entrega", "-")
            ))
            self.tree_notas.tag_configure(f"linha_{i}", background=cor_fundo, foreground="black")
            self.tree_notas.item(item, tags=(f"linha_{i}", f"status_{i}"))
            self.tree_notas.tag_configure(f"status_{i}", foreground=cor_texto)

    # ---------- VOLTAR ----------
    def voltar_elimpar(self):
        self.ra_entry.delete(0, END)
        if hasattr(self, "materia_combobox"):
            self.materia_combobox.set("")
            self.materia_combobox["values"] = ["Todas"]
        if hasattr(self, "tree"):
            for row in self.tree.get_children():
                self.tree.delete(row)
        for f in self.frames.values(): f.pack_forget()
        self.voltar_callback()
