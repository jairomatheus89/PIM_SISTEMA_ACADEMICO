import customtkinter as ctk
from tkinter import messagebox
from backend.api import autenticar_usuario_api

from frontend.Main_screen import MainScreen
from frontend.Aluno_screen import AlunoScreen  


class TelaLogin:
    def __init__(self, master=None):
        self.master = master
        master.title("Usuário")
        master.geometry("400x300")
        master.resizable(False, False)
        
        try:
            master.iconbitmap('frontend/favicon.ico')  # ainda funciona
        except Exception as e:
            print("Não foi possível carregar ícone:", e)
        
        # Configuração do tema
        ctk.set_appearance_mode("dark")   # "light" ou "system"
        ctk.set_default_color_theme("blue")  # cores padrão
        
        # Frame inicial: escolha de perfil 
        self.frame_escolha = ctk.CTkFrame(master, fg_color="royalblue4")
        self.frame_escolha.pack(expand=True, fill="both")
        
        ctk.CTkLabel(
            self.frame_escolha,
            text="Escolha o Usuário",
            text_color="white",
            font=("Calibri", 18, "bold")
        ).pack(pady=20)
        
        ctk.CTkButton(
            self.frame_escolha,
            text="Professor",
            width=200,
            fg_color="deepskyblue4",
            text_color="white",
            command=self.entrar_professor
        ).pack(pady=10)
        
        ctk.CTkButton(
            self.frame_escolha,
            text="Aluno",
            width=200,
            fg_color="deepskyblue4",
            text_color="white",
            command=self.entrar_aluno
        ).pack(pady=10)

        # Frame do professor
        self.frame_login_professor = ctk.CTkFrame(master, fg_color="royalblue4")
        
        ctk.CTkLabel(
            self.frame_login_professor,
            text="Login - Professor",
            text_color="white",
            font=("Calibri", 18, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=20)
        
        ctk.CTkLabel(
            self.frame_login_professor,
            text="Usuário:",
            text_color="white",
            font=("Arial", 14)
        ).grid(row=1, column=0, padx=5, pady=5)
        
        self.user_entry = ctk.CTkEntry(self.frame_login_professor, width=200)
        self.user_entry.grid(row=1, column=1, padx=5, pady=5, ipady=5)
        
        ctk.CTkLabel(
            self.frame_login_professor,
            text="Senha:",
            text_color="white",
            font=("Arial", 14)
        ).grid(row=2, column=0, padx=5, pady=5)
        
        self.password_entry = ctk.CTkEntry(self.frame_login_professor, width=200, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, ipady=5)

        self.login_button = ctk.CTkButton(
            self.frame_login_professor,
            text="Logar",
            width=200,
            fg_color="deepskyblue4",
            text_color="white",
            command=self.login_professor
        )
        self.login_button.grid(row=3, column=0, columnspan=2, pady=5, ipady=5)

        # Botão Voltar
        self.voltar_professor = ctk.CTkButton(
            self.frame_login_professor,
            text="Voltar",
            width=200,
            command=self.voltar_escolha
        )
        self.voltar_professor.grid(row=4, column=0, columnspan=2, pady=5, ipady=5)

        # Tela do aluno
        self.aluno_screen = None

    # Mostra Frame login professor
    def entrar_professor(self):
        self.master.title("Login Professor")
        self.frame_escolha.pack_forget()
        self.frame_login_professor.pack(expand=True, fill="both")

    # Mostra Frame login aluno
    def entrar_aluno(self):
        self.master.title("Buscar Atividades")
        self.master.geometry("700x600")
        self.frame_escolha.pack_forget()

        if not self.aluno_screen:
            self.aluno_screen = AlunoScreen(self.master, self.voltar_escolha)
        self.aluno_screen.pack(expand=True, fill="both")

    # Volta para a escolha de perfil
    def voltar_escolha(self):
        self.master.title("Usuário")
        self.master.geometry("400x300")
        self.frame_login_professor.pack_forget()
        if self.aluno_screen:
            self.aluno_screen.pack_forget()
        self.frame_escolha.pack(expand=True, fill="both")

    # Login do professor
    def login_professor(self):
        login = self.user_entry.get().strip()
        senha = self.password_entry.get()

        if not login or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos")
            return

        if " " in login:
            messagebox.showwarning("Atenção", "Usuário não pode conter espaços")
            return

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
    root = ctk.CTk()  # substitui Tk()
    TelaLogin(root)
    root.mainloop()
