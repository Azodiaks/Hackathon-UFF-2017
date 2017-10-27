from tkinter import *
from tkinter import messagebox
from cadastro import *
from janelao import *
from mysql import connector


class Login(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("175x140+400+300")
        self.title("Login")

        self.lbMatricula = Label(self, text ="Matrícula", font="callibri")
        self.lbMatricula.pack()

        self.entMatricula = Entry(self)
        self.entMatricula.pack()

        self.lbSenha = Label(self, text="Senha", font="callibri")
        self.lbSenha.pack()

        self.entSenha = Entry(self, show="*")
        self.entSenha.pack()

        Label(self).pack()
        self.botoes = Frame(self)

        self.btEntrar = Button(self.botoes, text="Entrar", command=self.entrar)
        self.btEntrar.pack(side=LEFT)
        self.btCadastro = Button(self.botoes, text="Cadastre-se", command=self.cadastrar)
        self.btCadastro.pack(side=RIGHT)

        self.botoes.pack(fill=X)

        self.cnx = mysql.connector.connect(user="root", database="bd_hackaton", host="127.0.0.1")
        self.cursor = self.cnx.cursor()

    def entrar(self):
        login_cm = ("select senha from aluno where matricula = %s")
        matIn = (int(self.entMatricula.get()),)

        cad_existe = False

        self.cursor.execute(login_cm, matIn)
        a = self.cursor.lastrowid

        for (senha,) in self.cursor:
            if senha == self.entSenha.get():
                jan = Janelao(int(self.entMatricula.get()))
                self.cnx.commit()
                self.cursor.close()
                self.cnx.close()
                self.destroy()
            else:
                messagebox.showwarning("Aviso", "Senha ou usuário incorretos!")
            cad_existe = True

        if not cad_existe:
            messagebox.showerror("Erro", "Cadastre-se primeiro!")

    def cadastrar(self):
        Cadastro()