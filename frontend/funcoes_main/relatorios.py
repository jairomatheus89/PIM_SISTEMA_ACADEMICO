from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from backend.api import *

def mostrar_relatorios(self):
    frame = self.frames["relatorios"]
    for widget in frame.winfo_children():
        widget.destroy()

    Label(frame, text="Selecione a turma:").pack(pady=5)

    resultado_turmas = listar_turmas_api(self.professor["id"])
    self.turmas = resultado_turmas.get("turmas", []) if resultado_turmas.get("sucesso") else []
    turmas_nomes = [t["nome_turma"] for t in self.turmas]

    self.combo_turmas_relatorio = ttk.Combobox(frame, values=turmas_nomes, state="readonly", width=110)
    self.combo_turmas_relatorio.pack(pady=5)
    self.combo_turmas_relatorio.bind("<<ComboboxSelected>>", lambda e: carregar_relatorio_turma(self))

    self.frame_tree_relatorio = Frame(frame)
    self.frame_tree_relatorio.pack(fill=BOTH, expand=True, padx=20, pady=10)

    # Treeview com colunas dinâmicas
    self.tree_relatorio = ttk.Treeview(self.frame_tree_relatorio, show="headings", height=12)
    self.tree_relatorio.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = Scrollbar(self.frame_tree_relatorio, command=self.tree_relatorio.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    self.tree_relatorio.configure(yscrollcommand=scrollbar.set)

    Button(frame, text="Gerar Relatório em PDF", command=lambda: gerar_relatorio_pdf(self)).pack(pady=10)


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

    # Criar colunas dinâmicas: Nome, RA, atividades..., Média, Status
    colunas = ["nome", "ra"] + [a["nome_atividade"] for a in atividades] + ["media", "status"]
    self.tree_relatorio["columns"] = colunas

    for col in colunas:
        self.tree_relatorio.heading(col, text=col.capitalize())
        self.tree_relatorio.column(col, anchor=CENTER, width=100)

    # Preencher os dados
    for aluno in alunos:
        notas_aluno = []
        for atividade in atividades:
            nota_resp = buscar_nota_api(aluno["id_aluno"], atividade["id_atividade"])
            nota = nota_resp.get("nota", 0) if nota_resp.get("sucesso") else 0
            notas_aluno.append(nota)

        media = sum(notas_aluno)/len(notas_aluno) if notas_aluno else 0
        status = "Aprovado" if media >= 7 else "Reprovado"

        valores = [aluno["nome"], aluno["ra"]] + notas_aluno + [f"{media:.2f}", status]
        self.tree_relatorio.insert("", END, values=valores)






from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib import colors
from datetime import datetime
from tkinter import messagebox

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

    
    semestre = "1º semestre" if datetime.now().month <= 6 else "2º semestre"
    ano = datetime.now().year
    c = Canvas(f"relatorio_{turma_nome}.pdf", pagesize=A4)
    largura, altura = A4
    y_inicial = altura - 50
    y = y_inicial
    
    todas_medias = []
    aprovados, reprovados = 0, 0
    linha = 0  # para zebra style

    # ---------- Cabeçalho ----------
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Relatório de Notas - {turma_nome}")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Disciplina: {self.professor.get('materia', 'Não informada')}")
    y -= 15
    c.drawString(50, y, f"Professor: {self.professor.get('nome', 'Desconhecido')}")
    y -= 15
    c.drawString(50, y, f"Período letivo: {semestre} {ano}")
    y -= 15
    c.drawString(50, y, f"Data de emissão: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    y -= 25

    def desenhar_cabecalho():
        nonlocal y
        c.setFont("Helvetica-Bold", 10)

        # Colunas fixas
        x_nome, largura_nome = 50, 50
        x_ra, largura_ra = x_nome + largura_nome, 40

        # Colunas atividades
        x_atividades, largura_atividades = [], []
        x_atual = x_ra + largura_ra + 10
        for atividade in atividades:
            largura_col = stringWidth(atividade["nome_atividade"][:12], "Helvetica-Bold", 10) + 20
            x_atividades.append(x_atual)
            largura_atividades.append(largura_col)
            x_atual += largura_col

        # Colunas finais
        x_media, largura_media = x_atual + 10, 40
        x_status, largura_status = x_media + largura_media + 10, 50

        # Fundo cinza
        c.setFillColor(colors.lightgrey)
        c.rect(45, y - 3, largura - 90, 18, fill=1, stroke=0)
        c.setFillColor(colors.black)

        # Títulos
        c.drawString(x_nome + (largura_nome - stringWidth("Nome", "Helvetica-Bold", 10))/2, y, "Nome")
        c.drawString(x_ra + (largura_ra - stringWidth("RA", "Helvetica-Bold", 10))/2, y, "RA")
        for idx, atividade in enumerate(atividades):
            texto = atividade["nome_atividade"][:12]
            c.drawString(x_atividades[idx] + (largura_atividades[idx] - stringWidth(texto, "Helvetica-Bold", 10))/2, y, texto)
        c.drawString(x_media + (largura_media - stringWidth("Média", "Helvetica-Bold", 10))/2, y, "Média")
        c.drawString(x_status + (largura_status - stringWidth("Status", "Helvetica-Bold", 10))/2, y, "Status")

        y -= 20
        return x_nome, largura_nome, x_ra, largura_ra, x_atividades, largura_atividades, x_media, largura_media, x_status, largura_status

    x_nome, largura_nome, x_ra, largura_ra, x_atividades, largura_atividades, x_media, largura_media, x_status, largura_status = desenhar_cabecalho()
    c.setFont("Helvetica", 10)

    for aluno in alunos:
        notas_aluno = []

        # Zebra style
        if linha % 2 == 0:
            c.setFillColor(colors.whitesmoke)
            c.rect(45, y - 2, largura - 90, 15, fill=1, stroke=0)
            c.setFillColor(colors.black)

        # Nome e RA
        c.drawString(x_nome + (largura_nome - stringWidth(aluno["nome"][:10], "Helvetica", 10))/2, y, aluno["nome"][:10])
        c.drawString(x_ra + (largura_ra - stringWidth(aluno["ra"][:8], "Helvetica", 10))/2, y, aluno["ra"][:8])

        # Atividades
        for idx, atividade in enumerate(atividades):
            nota_resp = buscar_nota_api(aluno["id_aluno"], atividade["id_atividade"])
            nota = nota_resp.get("nota", 0) if nota_resp.get("sucesso") else 0
            notas_aluno.append(nota)
            c.drawString(x_atividades[idx] + (largura_atividades[idx] - stringWidth(str(nota), "Helvetica", 10))/2, y, str(nota))

        # Média e status
        media = sum(notas_aluno)/len(notas_aluno) if notas_aluno else 0
        todas_medias.append(media)
        status = "Aprovado" if media >= 7 else "Reprovado"

        c.drawString(x_media + (largura_media - stringWidth(f"{media:.2f}", "Helvetica", 10))/2, y, f"{media:.2f}")

        # Cor no status
        if status == "Aprovado":
            c.setFillColor(colors.green)
            aprovados += 1
        else:
            c.setFillColor(colors.red)
            reprovados += 1

        c.drawString(x_status + (largura_status - stringWidth(status, "Helvetica", 10))/2, y, status)
        c.setFillColor(colors.black)

        y -= 20
        linha += 1

        if y < 80:
            c.showPage()
            y = y_inicial
            x_nome, largura_nome, x_ra, largura_ra, x_atividades, largura_atividades, x_media, largura_media, x_status, largura_status = desenhar_cabecalho()
            c.setFont("Helvetica", 10)

    # ---------- Estatísticas ----------
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Estatísticas da Turma:")
    y -= 15
    c.setFont("Helvetica", 10)

    if todas_medias:
        media_geral = sum(todas_medias)/len(todas_medias)
        maior_media = max(todas_medias)
        menor_media = min(todas_medias)
        percentual_aprov = (aprovados/len(todas_medias))*100
    else:
        media_geral = maior_media = menor_media = percentual_aprov = 0

    c.drawString(60, y, f"Média geral da turma: {media_geral:.2f}")
    y -= 15
    c.drawString(60, y, f"Maior média: {maior_media:.2f} | Menor média: {menor_media:.2f}")
    y -= 15
    c.drawString(60, y, f"Aprovados: {aprovados} | Reprovados: {reprovados}")
    y -= 15
    c.drawString(60, y, f"Percentual de aprovação: {percentual_aprov:.1f}%")

    c.save()
    messagebox.showinfo("Sucesso", f"Relatório salvo como relatorio_{turma_nome}.pdf")









