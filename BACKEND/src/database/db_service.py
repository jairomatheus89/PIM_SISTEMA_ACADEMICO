import sqlite3

class DataBaseService:
    def __init__(self):
        self.db = sqlite3.connect("./database.db")
        self.create_db()

    def create_db(self):
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS Professores (
            id_professor INTEGER PRIMARY KEY AUTOINCREMENT,
            nome VARCHAR(100) NOT NULL,
            usuario VARCHAR(50) UNIQUE NOT NULL,
            senha VARCHAR(255) NOT NULL,
            materia VARCHAR(100)
        );

        CREATE TABLE IF NOT EXISTS Turma (
            id_turma INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_turma VARCHAR(100) NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Aluno (
            id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
            id_turma INT NOT NULL,
            nome VARCHAR(100) NOT NULL,
            ra VARCHAR(20) UNIQUE NOT NULL,
            FOREIGN KEY (id_turma) REFERENCES Turma(id_turma)
        );

        CREATE TABLE IF NOT EXISTS Atividades (
            id_atividade INTEGER PRIMARY KEY AUTOINCREMENT,
            id_professor INT NOT NULL,
            nome_atividade VARCHAR(100) NOT NULL,
            descricao TEXT,
            data_entrega DATE,  
            FOREIGN KEY (id_professor) REFERENCES Professores(id_professor)
        );

        CREATE TABLE IF NOT EXISTS Turma_Professor (
            id_turma INT,
            id_professor INT,
            PRIMARY KEY (id_turma, id_professor),
            FOREIGN KEY (id_turma) REFERENCES Turma(id_turma),
            FOREIGN KEY (id_professor) REFERENCES Professores(id_professor)
        );

        CREATE TABLE IF NOT EXISTS Turma_Atividade (
            id_turma INT,
            id_atividade INT,
            PRIMARY KEY (id_turma, id_atividade),
            FOREIGN KEY (id_turma) REFERENCES Turma(id_turma),
            FOREIGN KEY (id_atividade) REFERENCES Atividades(id_atividade)
        );

        CREATE TABLE IF NOT EXISTS Notas (
            id_aluno INT,
            id_atividade INT,
            nota DECIMAL(5,2),
            entregue BOOLEAN DEFAULT 0,
            PRIMARY KEY (id_aluno, id_atividade),
            FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno),
            FOREIGN KEY (id_atividade) REFERENCES Atividades(id_atividade)
        );
        """)
        self.db.commit()  
        

db = DataBaseService()
