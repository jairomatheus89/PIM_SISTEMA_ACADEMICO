import sqlite3
from algoritimo import gerar_ras  # Importa a função de outro módulo

# -----------------------------
# Conexão com o banco
# -----------------------------
banco = sqlite3.connect("database.db")
cursor = banco.cursor()

# -----------------------------
# Lista de professores com matérias fixas
# -----------------------------
professores = [
    ("Valter", "valter", "11", "Matemática"),
    ("Fabio", "fabio", "22", "Português"),
    ("Vitoria", "vitoria", "33", "História"),
    ("Otavio", "otavio", "44", "Geografia")
]

# -----------------------------
# Lista de alunos por turma
# -----------------------------
nomes = [
    # Turma A
    [
        "Ana Beatriz",
        "Camila Ferreira",
        "Carlos Eduardo",
        "Gabriel Costa",
        "João Pedro",
        "Juliana Lima",
        "Letícia Almeida",
        "Lucas Santos",
        "Mariana Souza",
        "Rafael Oliveira"
    ],
    # Turma B
    [
        "Amanda Silva",
        "Bianca Rodrigues",
        "Daniel Araújo",
        "Felipe Carvalho",
        "Fernanda Gomes",
        "Larissa Pereira",
        "Matheus Ribeiro",
        "Patrícia Mendes",
        "Thiago Martins",
        "Vinícius Barbosa"
    ],
    # Turma C
    [
        "Bruno Lopes",
        "Camila Pinto",
        "Gustavo Fernandes",
        "Isabela Rocha",
        "Larissa Dias",
        "Leonardo Ramos",
        "Mariana Castro",
        "Pedro Henrique",
        "Sofia Nunes",
        "Vitor Hugo"
    ]
]

# -----------------------------
# Inserir professores
# -----------------------------
for nome, usuario, senha, materia in professores:
    cursor.execute("""
        INSERT INTO Professores (nome, usuario, senha, materia)
        VALUES (?, ?, ?, ?)
    """, (nome, usuario, senha, materia))

# -----------------------------
# Criar 3 turmas
# -----------------------------
turmas_nome = [("Turma A",), ("Turma B",), ("Turma C",)]
cursor.executemany("""
    INSERT INTO Turma (nome_turma)
    VALUES (?)
""", turmas_nome)

# -----------------------------
# Buscar IDs das turmas e professores
# -----------------------------
cursor.execute("SELECT id_turma, nome_turma FROM Turma ORDER BY id_turma")
todas_turmas = cursor.fetchall()

cursor.execute("SELECT id_professor, nome FROM Professores")
todos_professores = cursor.fetchall()

# -----------------------------
# Vincular todos os professores em todas as turmas
# -----------------------------
for id_turma, nome_turma in todas_turmas:
    for id_professor, nome_prof in todos_professores:
        cursor.execute("""
            INSERT INTO Turma_Professor (id_turma, id_professor)
            VALUES (?, ?)
        """, (id_turma, id_professor))

# -----------------------------
# Gerar RAs aleatórios para todos os alunos
# -----------------------------
total_alunos = sum(len(turma) for turma in nomes)
ras_gerados = gerar_ras(total_alunos)  # gera RAs únicos aleatórios
indice_ra = 0

# -----------------------------
# Inserir alunos usando nomes e RAs aleatórios
# -----------------------------
for turma_index, (id_turma, nome_turma) in enumerate(todas_turmas):
    for nome_aluno in nomes[turma_index]:
        ra = str(ras_gerados[indice_ra])
        cursor.execute("""
            INSERT INTO Aluno (id_turma, nome, ra)
            VALUES (?, ?, ?)
        """, (id_turma, nome_aluno, ra))
        indice_ra += 1

# -----------------------------
# Finalizar
# -----------------------------
banco.commit()
banco.close()
print("Dados iniciais inseridos com sucesso!")
