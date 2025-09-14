from tkinter import *
from tkinter import messagebox
from backend.api import autenticar_usuario_api

from frontend.Main_screen import MainScreen
from frontend.Aluno_screen import AlunoScreen  

class TelaLogin:
    def __init__(self, master=None):
        self.master = master
        master.title("Usuário")
        master.geometry("400x300")

        # Frame inicial: escolha de perfil
        self.frame_escolha = Frame(master)
        self.frame_escolha.pack(expand=True)

        Label(self.frame_escolha, text="Escolha o Usuário", font=("Calibri", 18, "bold")).pack(pady=20)
        Button(self.frame_escolha, text="Professor", width=20, command=self.entrar_professor).pack(pady=10)
        Button(self.frame_escolha, text="Aluno", width=20, command=self.entrar_aluno).pack(pady=10)

        # Frame do professor
        self.frame_login_professor = Frame(master)
        Label(self.frame_login_professor, text="Login - Professor", font=("Calibri", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        Label(self.frame_login_professor, text="Usuário:", font=("Arial", 14)).grid(row=1, column=0, padx=5, pady=5)
        self.user_entry = Entry(self.frame_login_professor, width=30)
        self.user_entry.grid(row=1, column=1, padx=5, pady=5, ipady=5)
        Label(self.frame_login_professor, text="Senha:", font=("Arial", 14)).grid(row=2, column=0, padx=5, pady=5)
        self.password_entry = Entry(self.frame_login_professor, width=30, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, ipady=5)

        self.login_button = Button(self.frame_login_professor, text="Logar", width=30, bg="lightblue", command=self.login_professor)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=5, ipady=5)

        # Botão Voltar
        self.voltar_professor = Button(self.frame_login_professor, text="Voltar", width=30, command=self.voltar_escolha)
        self.voltar_professor.grid(row=4, column=0, columnspan=2, pady=5, ipady=5)

        # Tela do aluno (vai ser criada só quando precisar)
        self.aluno_screen = None

    # Mostra Frame login professor
    def entrar_professor(self):
        self.master.title("Login Professor")
        self.frame_escolha.pack_forget()
        self.frame_login_professor.pack(expand=True)

    # Mostra Frame login aluno
    def entrar_aluno(self):
        self.master.title("Buscar Atividades")
        self.master.geometry("700x600")
        self.frame_escolha.pack_forget()

        # Se ainda não criou, cria o AlunoScreen
        if not self.aluno_screen:
            self.aluno_screen = AlunoScreen(self.master, self.voltar_escolha)
        self.aluno_screen.pack(expand=True, fill="both")

    # Volta para a escolha de perfil
    def voltar_escolha(self):
        self.master.title("Usuário")
        self.master.geometry("400x300")

        # Esconde frame do professor e limpa campos
        self.frame_login_professor.pack_forget()
        self.user_entry.delete(0, END)
        self.password_entry.delete(0, END)

        # Esconde frame do aluno e limpa dados
        if self.aluno_screen:
            self.aluno_screen.pack_forget()
            self.aluno_screen.ra_entry.delete(0, END)
            self.aluno_screen.materia_combobox.set("")
            self.aluno_screen.materias_ids = []
            self.aluno_screen.materias_nomes = []
            self.aluno_screen.atividades_completas = []
            self.aluno_screen.atualizar_tabela()

        # Mostra tela de escolha de perfil
        self.frame_escolha.pack(expand=True)
    # Login do professor

    from tkinter import messagebox

    def login_professor(self):
        self.master.title("Login Professor")

        login = self.user_entry.get().strip()
        senha = self.password_entry.get()

        if not login or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            return

        if " " in login:
            messagebox.showwarning("Atenção", "Usuário não pode conter espaços")
            return

        #puxando api
        resultado = autenticar_usuario_api(login, senha)



        if resultado.get("sucesso"):
            self.frame_login_professor.pack_forget()
            usuario = {
                "id": resultado["id_professor"],
                "nome": resultado["nome"],
                "materia": resultado.get("materia", "")
            }
            MainScreen(self.master, usuario)
        else:
            messagebox.showerror("Erro no Login", resultado.get("mensagem", "Erro ao tentar logar"))




if __name__ == "__main__":
    root = Tk()
    TelaLogin(root)
    root.mainloop()
