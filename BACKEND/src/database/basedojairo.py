# ANOTAÇÕES PARA OS DEVS:

import sqlite3

class DataBaseService:
    def __init__(self):
        self.db = sqlite3.connect("../../database.db")
        self.__class__.create_db()
        
    ### STATIC CLASS METHODS ### STATIC CLASS METHODS ### STATIC CLASS METHODS ### STATIC CLASS METHODS

    #METODO STATIC DA CLASSE QUE JA É CHAMADO ASSIM QUE A CLASSE É INICIALIZADA PARA GARANTIR QUE SEMPRE EXISTIRÁ UM BANCO
    @staticmethod
    def create_db():
        db = sqlite3.connect("../../database.db")
        return db.execute("CREATE TABLE IF NOT EXISTS teachers(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
    
    #METODO PARA CHECAR SE O PROFESSOR CADASTRADO JA EXISTE
    @staticmethod
    def check_person_already_exists(name):
        db = sqlite3.connect("../../database.db")
        cu = db.cursor()
        cu.execute("SELECT COUNT(*) FROM teachers WHERE name = ?", (name,))
        result = cu.fetchone()[0]
        db.close()
        return result > 0

    ### INSTANCE METHODS ### INSTANCE METHODS ### INSTANCE METHODS ### INSTANCE METHODS ###
    
    #METODO DE REGISTRO DE PROFESSOR PARA ADMIN/DIRETOR
    def insert_teacher(self, name):
        if(DataBaseService.check_person_already_exists(name)):
            print(f"O PROFESSOR {name} JA EXISTE!")
            return None

        self.db.cursor()
        self.db.execute("INSERT INTO teachers (name) VALUES (?)", (name,))
        self.db.commit()
        return print(f"PROFESSOR {name} SALVO COM SUCESSO!")