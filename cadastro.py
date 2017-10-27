from tkinter import *
from tkinter import messagebox
import mysql.connector
import os


class Cadastro(Tk):
    def __init__(self):
        super().__init__()
        self.title("Cadastro")

        self.texto_mat = Label(self, text="Matricula", font="callibri").grid(row=0, column=0)
        self.texto_nome = Label(self, text="Nome", font="callibri").grid(row=1, column=0)
        self.texto_email = Label(self, text="Email", font="callibri").grid(row=2, column=0)
        self.texto_senha = Label(self, text="Senha", font="callibri").grid(row=3, column=0)
        self.texto_tel = Label(self, text="Telefone", font="callibri").grid(row=4, column=0)

        self.matIn = Entry(self)
        self.matIn.grid(row=0, column=1)

        self.nomeIn = Entry(self)
        self.nomeIn.grid(row=1, column=1)

        self.senhaIn = Entry(self, show="*")
        self.senhaIn.grid(row=3, column=1)

        self.emailIn = Entry(self)
        self.emailIn.grid(row=2, column=1)

        self.telIn = Entry(self)
        self.telIn.grid(row=4, column=1)

        self.botao_ent = Button(self, text="Cadastrar", command=self.cadastrar)
        self.botao_ent.grid(row=5, column=0)

        self.botao_cancelar = Button(self, text="Cancelar", command=self.destroy)
        self.botao_cancelar.grid(row=5, column=1)

        self.cnx = mysql.connector.connect(user="root", database="bd_hackaton", host="127.0.0.1")
        self.cursor = self.cnx.cursor()

    def cadastrar(self):
        cad_existe = True

        add_aluno = ("INSERT INTO aluno"
                     "(nome, matricula, email, senha, telefone)"
                     "VALUES (%s, %s, %s, %s, %s)")

        aluno_values = (self.nomeIn.get(), int(self.matIn.get()), self.emailIn.get(), self.senhaIn.get(), self.telIn.get())

        query_cad = ("select matricula from aluno where matricula = %s")
        query_val = (int(self.matIn.get()),)

        self.cursor.execute(query_cad, query_val)
        emp_no = self.cursor.lastrowid

        for (matricula,) in self.cursor:
            cad_existe = False

        if not cad_existe:
            messagebox.showwarning("Aviso", "Usuário já cadastrado!")
            return
        else:
            self.cursor.execute(add_aluno, aluno_values)
            emp_no = self.cursor.lastrowid

        self.cnx.commit()

        self.cursor.close()
        self.cnx.close()

        self.destroy()