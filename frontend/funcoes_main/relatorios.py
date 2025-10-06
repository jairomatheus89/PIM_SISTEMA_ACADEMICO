from tkinter import *
from tkinter import ttk, messagebox, filedialog
from backend.api import *
from backend.src.modulo_c import calcular_media_status
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from datetime import datetime

# Cores
BG_COLOR = "#1E2A38"
BTN_COLOR = "#D4A017"
BTN_FG = "black"
LABEL_FG = "white"
TREE_BG = "#0F1A2B"       # azul escuro
TREE_FG = "#FFFFFF"        # branco
TREE_HEADER_BG = "#FFD966" # amarelo cabeçalho
TREE_HEADER_FG = "#0F1A2B"

def mostrar_relatorios(self):
    frame = self.frames["relatorios"]
    for widget in frame.winfo_children():
        widget.destroy()
    frame.config(bg=BG_COLOR)

    Label(frame, text="Selecione a turma:", bg=BG_COLOR, fg=LABEL_FG, font=("Calibri", 11, "bold")).pack(pady=5)

    resultado_turmas = listar_turmas_api(self.professor["id"])
    self.turmas = resultado_turmas.get("turmas", []) if resultado_turmas.get("sucesso") else []
    turmas_nomes = [t["nome_turma"] for t in self.turmas]

    self.combo_turmas_relatorio = ttk.Combobox(frame, values=turmas_nomes, state="readonly", width=110)
    self.combo_turmas_relatorio.pack(pady=5)
    self.combo_turmas_relatorio.bind("<<ComboboxSelected>>", lambda e: carregar_relatorio_turma(self))

    self.frame_tree_relatorio = Frame(frame, bg=BG_COLOR)
    self.frame_tree_relatorio.pack(fill=BOTH, expand=True, padx=20, pady=10)

    # Treeview com estilo
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background=TREE_BG,
                    foreground=TREE_FG,
                    fieldbackground=TREE_BG,
                    rowheight=25,
                    font=("Calibri", 11))
    style.configure("Treeview.Heading",
                    background=TREE_HEADER_BG,
                    foreground=TREE_HEADER_FG,
                    font=("Calibri", 11, "bold"))
    style.map("Treeview", background=[('selected', '#334466')], foreground=[('selected', '#FFFFFF')])

    self.tree_relatorio = ttk.Treeview(self.frame_tree_relatorio, show="headings", height=12)
    self.tree_relatorio.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(self.frame_tree_relatorio, command=self.tree_relatorio.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    self.tree_relatorio.configure(yscrollcommand=scrollbar.set)

    Button(frame, text="Gerar Relatório em PDF", bg=BTN_COLOR, fg=BTN_FG,
           font=("Calibri", 11, "bold"),
           command=lambda: gerar_relatorio_pdf(self)).pack(pady=10)


def carregar_relatorio_turma(self):
    turma_nome = self.combo_turmas_relatorio.get()
    turma = next((t for t in self.turmas if t["nome_turma"] == turma_nome), None)
    if not turma:
        return

    self.tree_relatorio.delete(*self.tree_relatorio.get_children())

    resultado_alunos = listar_alunos_api(turma["id_turma"])
    resultado_atividades = listar_atividades_api(self.professor["id"])
    if not resultado_alunos.get("sucesso") or not resultado_atividades.get("sucesso"):
        return

    alunos = resultado_alunos["alunos"]
    atividades = [a for a in resultado_atividades["atividades"] 
                  if turma_nome in [t["nome_turma"] for t in a.get("turmas", [])]]

    colunas = ["nome", "ra"] + [a["nome_atividade"] for a in atividades] + ["media", "status"]
    self.tree_relatorio["columns"] = colunas

    for col in colunas:
        self.tree_relatorio.heading(col, text=col.capitalize())
        self.tree_relatorio.column(col, anchor=CENTER, width=100)

    for aluno in alunos:
        notas_aluno = []
        for atividade in atividades:
            nota_resp = buscar_nota_api(aluno["id_aluno"], atividade["id_atividade"])
            nota = nota_resp.get("nota", 0) if nota_resp.get("sucesso") else 0
            notas_aluno.append(nota)

        media, status = calcular_media_status(notas_aluno, media_minima=7)
        valores = [aluno["nome"], aluno["ra"]] + notas_aluno + [f"{media:.2f}", status]
        self.tree_relatorio.insert("", END, values=valores)


def gerar_relatorio_pdf(self):
    turma_nome = self.combo_turmas_relatorio.get()
    if not turma_nome:
        messagebox.showwarning("Atenção", "Selecione uma turma para gerar relatório.")
        return

    turma = next((t for t in self.turmas if t["nome_turma"] == turma_nome), None)
    if not turma:
        messagebox.showerror("Erro", "Turma não encontrada.")
        return

    resultado_alunos = listar_alunos_api(turma["id_turma"])
    resultado_atividades = listar_atividades_api(self.professor["id"])
    if not resultado_alunos.get("sucesso") or not resultado_atividades.get("sucesso"):
        messagebox.showerror("Erro", "Falha ao buscar dados da turma.")
        return

    alunos = resultado_alunos["alunos"]
    atividades = [a for a in resultado_atividades["atividades"]
                  if turma_nome in [t["nome_turma"] for t in a.get("turmas", [])]]
    if not atividades:
        messagebox.showinfo("Informação", "Não há atividades cadastradas para esta turma.")
        return

    caminho_pdf = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("Arquivos PDF", "*.pdf")],
        initialfile=f"relatorio_{turma_nome}.pdf",
        title="Salvar relatório como..."
    )
    if not caminho_pdf:
        return

    c = Canvas(caminho_pdf, pagesize=A4)
    largura, altura = A4
    y_inicial = altura - 50
    y = y_inicial

    # Cabeçalho PDF
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Relatório de Notas - {turma_nome}")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Disciplina: {self.professor.get('materia', 'Não informada')}")
    y -= 15
    c.drawString(50, y, f"Professor: {self.professor.get('nome', 'Desconhecido')}")
    y -= 15
    c.drawString(50, y, f"Data de emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    y -= 25

    c.save()
    messagebox.showinfo("Sucesso", f"Relatório salvo em {caminho_pdf}")
