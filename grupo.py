import mysql.connector
from tkinter import *
from tkinter import messagebox


def verificar_grupos(matricula, cursorOut):
    cnx = mysql.connector.connect(user="root", database="bd_hackaton", host="127.0.0.1")
    cursor = cnx.cursor(buffered=True)

    query = ("select codigo, tutor_aluno from aplic where matricula = %s"%matricula)
    cursor.execute(query)

    for (codigo, tutor_aluno) in cursor:
        query = ("select cod_grupo, matricula1, matricula2, matricula3, matricula4, matricula5 from grupos where cod_mat = '%s'" %codigo)

        cursorOut.execute(query)

        not_vaga = True
        for (cod_grupo, matricula1, matricula2, matricula3, matricula4, matricula5) in cursorOut:
            not_vaga = True
            if tutor_aluno == 0:
                if matricula3 == None:
                    cm = ("update grupos set matricula3 = %s where cod_grupo = %s" %(matricula, cod_grupo))
                    cursor.execute(cm)
                    messagebox.showinfo("Info", "Entrou no grupo!")
                    not_vaga = False
                elif matricula4 == None:
                    cm = ("update grupos set matricula4 = %s where cod_grupo = %s" %(matricula, cod_grupo))
                    cursor.execute(cm)
                    messagebox.showinfo("Info", "Entrou no grupo!")
                    not_vaga = False
                elif matricula5 == None:
                    cm = ("update grupos set matricula5 = %s where cod_grupo = %s" %(matricula, cod_grupo))
                    cursor.execute(cm)
                    messagebox.showinfo("Info", "Entrou no grupo!")
                    not_vaga = False
                else:
                    not_vaga = True
            elif tutor_aluno == 1:
                if matricula1 == None:
                    cm = ("update grupos set matricula1 = %s where cod_grupo = %s" %(matricula, cod_grupo))
                    cursor.execute(cm)
                    messagebox.showinfo("Info", "Entrou no grupo!")
                else:
                    cm = ("insert into grupos"
                  "(cod_mat, matricula1)"
                  "values ('%s', %s)" %(codigo, matricula))
                    messagebox.showinfo("Info", "Grupo criado, porém, ainda não tem alunos!")
                    cursor.execute(cm)

        if tutor_aluno == 0 and not_vaga:
            cm = ("insert into grupos"
                  "(cod_mat, matricula2)"
                  "values ('%s', %s)" %(codigo, matricula))
            cursor.execute(cm)
            messagebox.showinfo("Info", "Grupo criado!")
