from tkinter import *
from tkinter import ttk, messagebox
from backend.api import listar_atividades_aluno_id_api, listar_materias_aluno_id_api, pegar_ra_id_alunos_api
from backend.src.algoritimo import merge_sort, busca_binaria  
from backend.src.modulo_c import calcular_media_status


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

        # Dados da busca algorítmica
        self.ra_para_id = {}
        self.ras_ordenados = []

        # Inicializa busca algorítmica ao abrir a tela
        self.inicializar_busca_algoritmica()

    # Inicialização Busca Algorítmica
    def inicializar_busca_algoritmica(self):
        alunos = pegar_ra_id_alunos_api()  # chama API
        
        if not alunos:
            messagebox.showerror("Erro", "Não foi possível carregar os alunos.")
            self.ra_para_id = {}
            self.ras_ordenados = []
            return

        # Cria dicionário RA → id_aluno
        self.ra_para_id = {int(a["ra"]): a["id_aluno"] for a in alunos}

        # Lista de RAs ordenada
        self.ras_ordenados = merge_sort(list(self.ra_para_id.keys()))

    # ---------------------------- Navegação de Frames ----------------------------
    def mostrar_frame(self, chave):
        ra_digitado = self.ra_entry.get().strip()
        if not ra_digitado:
            messagebox.showwarning("Atenção", "Digite o RA antes de continuar!")
            return

        # Converte RA em id_aluno usando busca binária
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

        # Esconde todos os frames
        for f in self.frames.values():
            f.pack_forget()

        # Listar atividades só se RA for válido
        if chave == "listar_atividades":
            sucesso = self.listar_atividades()
            if not sucesso:
                return
            
        elif chave == "listar_notas":
            sucesso = self.listar_notas()
            if not sucesso:
                return

        self.frames[chave].pack(fill=BOTH, expand=True)

    # ---------------------------- Atividades ----------------------------
    def listar_atividades(self):
        frame_atividades = self.frames["listar_atividades"]

        # Limpa frame antes de reconstruir
        for widget in frame_atividades.winfo_children():
            widget.destroy()

        # Frame para Combobox de matérias
        frame_materia = Frame(frame_atividades)
        frame_materia.pack(fill=X, pady=5)
        Label(frame_materia, text="Selecione a Matéria:", width=15, anchor=W).pack(side=LEFT)
        self.materia_combobox = ttk.Combobox(frame_materia, state="readonly", width=35)
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
        self.tree.column("atividade", width=200, anchor=CENTER)
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

        # Busca atividades e retorna sucesso
        return self.buscar_atividades()

    def buscar_atividades(self):
        if not hasattr(self, "id_aluno_atual"):
            return False

        id_aluno = self.id_aluno_atual

        # Chamando API de matérias e atividades usando id_aluno
        materias_resp = listar_materias_aluno_id_api(id_aluno)
        if not materias_resp["sucesso"]:
            messagebox.showerror("Erro", f"Aluno com ID {id_aluno} não encontrado.")
            self.limpar_tabela()
            return False

        materias = materias_resp["materias"]
        self.materias_nomes = [f'{m["materia"]} - {m["nome_professor"]}' for m in materias]
        self.materias_ids = [m["id_professor"] for m in materias]
        self.materia_combobox["values"] = ["Todas"] + self.materias_nomes
        self.materia_combobox.current(0)

        resultado = listar_atividades_aluno_id_api(id_aluno)
        if resultado["sucesso"]:
            self.atividades_completas = resultado["atividades"]
        else:
            self.atividades_completas = []

        self.atualizar_tabela()
        return True

    def atualizar_tabela(self):
        if not hasattr(self, "tree"):
            return

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
        if not hasattr(self, "tree"):
            return
        for row in self.tree.get_children():
            self.tree.delete(row)

    def listar_notas(self):
        frame_notas = self.frames["listar_notas"]
        for widget in frame_notas.winfo_children():
            widget.destroy()

        Label(frame_notas, text="Selecione a Matéria:", font=("Calibri", 12, "bold")).pack(pady=5)

        # Busca matérias do aluno
        materias_resp = listar_materias_aluno_id_api(self.id_aluno_atual)
        if not materias_resp["sucesso"]:
            messagebox.showerror("Erro", "Não foi possível carregar as matérias.")
            return False

        self.materias_notas = materias_resp["materias"]
        materias_nomes = [f'{m["materia"]} - {m["nome_professor"]}' for m in self.materias_notas]

        # Combobox de matérias
        self.combo_materias_notas = ttk.Combobox(frame_notas, values=materias_nomes, state="readonly", width=50)
        self.combo_materias_notas.pack(pady=5)
        self.combo_materias_notas.bind("<<ComboboxSelected>>", lambda e: self.carregar_notas())

        # Frame da tabela de notas
        self.tree_frame_notas = Frame(frame_notas, width=self.master.winfo_width(), height=60)  # altura aproximada para 2 linhas
        self.tree_frame_notas.pack(padx=20, pady=10, fill=X)
        self.tree_frame_notas.pack_propagate(False)  # garante que o Treeview use a altura do frame

        # Treeview
        self.tree_notas = ttk.Treeview(self.tree_frame_notas, show="headings", height=2)
        self.tree_notas.pack(fill=BOTH, expand=True)

        return True

    def carregar_notas(self):
        materia_nome = self.combo_materias_notas.get()
        materia = next((m for m in self.materias_notas
                        if f'{m["materia"]} - {m["nome_professor"]}' == materia_nome), None)

        # Limpa tabela se nenhuma matéria selecionada
        self.tree_notas.delete(*self.tree_notas.get_children())
        if not materia:
            return

        # Busca atividades do aluno
        resultado = listar_atividades_aluno_id_api(self.id_aluno_atual)
        if not resultado.get("sucesso"):
            return

        # Filtra atividades da matéria selecionada
        atividades = [a for a in resultado["atividades"]
                    if int(a.get("id_professor", 0)) == int(materia["id_professor"])]

        # Define colunas
        colunas = ["nome", "ra"] + [a["nome_atividade"] for a in atividades] + ["media", "status"]
        self.tree_notas["columns"] = colunas

        for col in colunas:
            largura = 120 if col == "nome" else 80
            if col not in ("nome", "ra"):
                largura = max(80, min(len(col) * 10, 150))
            self.tree_notas.heading(col, text=col.capitalize())
            self.tree_notas.column(col, anchor=CENTER, width=largura, stretch=False)

        # Coleta notas como float
        notas = [float(a.get("nota", 0) or 0) for a in atividades]

        #CALCULA MEDIA PELO MODULO C
        media, status = calcular_media_status(notas)

        # Nome e RA do aluno
        nome_aluno = resultado.get("nome_aluno", "Aluno")
        ra_aluno = resultado["ra"]

        valores = [nome_aluno, ra_aluno] + notas + [f"{media:.2f}", status]
        self.tree_notas.insert("", END, values=valores)

    # ---------------------------- Voltar ----------------------------
    def voltar_elimpar(self):
        # Limpa RA
        self.ra_entry.delete(0, END)

        # Limpa combobox se existir
        if hasattr(self, "materia_combobox"):
            self.materia_combobox.set("")
            self.materia_combobox["values"] = ["Todas"]

        # Limpa tabela se existir
        if hasattr(self, "tree"):
            self.limpar_tabela()

        # Esconde frames de conteúdo
        for f in self.frames.values():
            f.pack_forget()

        # Chama callback original
        self.voltar_callback()


