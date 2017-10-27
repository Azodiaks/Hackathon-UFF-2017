import mysql.connector
from tkinter import *
from tkinter import messagebox
import grupo


class Janelao(Tk):
    def __init__(self, matricula):
        super().__init__()
        self.geometry("800x400+100+50")
        self.title("JANELÃO DE ESTUDOS D1R1GU1JH0N50N'5 - J.E.D.")

        self.matricula = matricula

        self.cnx = mysql.connector.connect(user="root", database="bd_hackaton", host="127.0.0.1")
        self.cursor = self.cnx.cursor()

        self.info = self.coletar_info()

        self.frame_ativo = Frame(self)

        self.menubar = Menu(self)  # Menu cascata
        self.config(menu=self.menubar)

        self.menu_perfil = Menu(self.menubar, tearoff=0)  # Menu cascata
        self.menu_perfil.add_command(label="Informações", command=self.ir_frame_info)
        self.menu_perfil.add_command(label="Matérias", command=self.ir_frame_mat)
        self.menubar.add_cascade(label="Perfil", menu=self.menu_perfil)

        self.menu_insc = Menu(self.menubar, tearoff=0)  # Menu cascata
        self.menu_insc.add_command(label="Tutor", command=self.ir_frame_tutor)
        self.menu_insc.add_command(label="Aluno", command=self.ir_frame_aluno)
        self.menubar.add_cascade(label="Inscrição", menu=self.menu_insc)

        self.menu_gp = Menu(self.menubar, tearoff=0)  # Menu cascata
        self.menu_gp.add_command(label="Ver grupos", command=self.ir_frame_grupo)
        self.menubar.add_cascade(label="Grupos", menu=self.menu_gp)

        self.menu_calc = Menu(self.menubar, tearoff=0)
        self.menu_calc.add_command(label="Calcular nota", command=self.ir_frame_calc)
        self.menubar.add_cascade(label="Calculadora", menu=self.menu_calc)

        self.menu_sobre = Menu(self.menubar, tearoff=0)  # Menu cascata
        self.menu_sobre.add_command(label="Sobre Nós", command=self.ir_frame_nos)
        self.menu_sobre.add_command(label="Sobre o Programa", command=self.ir_frame_app)
        self.menubar.add_cascade(label="Sobre", menu=self.menu_sobre)

    def coletar_info(self):
        query = ("select nome, email, senha, telefone from aluno where matricula = %s")
        query_val = (int(self.matricula),)

        self.cursor.execute(query, query_val)

        for (nome, email, senha, telefone) in self.cursor:
            info = [self.matricula, nome, senha, email, telefone]

        return info

    # -----------------------------------INFORMACOES--------------------------------------------------
    def ir_frame_info(self):
        self.frame_info = Frame(self)

        Label(self.frame_info, text="Senha", font="callibri").pack()
        self.nova_senha = Entry(self.frame_info, font="callibri", show="*")
        self.nova_senha.pack()

        Label(self.frame_info, text="Telefone", font="callibri").pack()
        self.novo_tel = Entry(self.frame_info, font="callibri")
        self.novo_tel.pack()
        self.novo_tel.insert(0, self.info[4])

        Label(self.frame_info, text=("Nome: %s" % self.info[1]), font="callibri").pack()
        Label(self.frame_info, text=("Matrícula: %s" % self.info[0]), font="callibri").pack()
        Label(self.frame_info, text="Email: %s" % self.info[3], font="callibri").pack()

        self.bt_confirma = Button(self.frame_info, text="Atualizar Dados", command=self.alterar_cad).pack()

        self.frame_ativo.destroy()
        self.frame_ativo = self.frame_info
        self.frame_ativo.pack()

    def alterar_cad(self):
        if self.nova_senha.get() != "":
            query = (
            "update aluno set senha = " + str(self.nova_senha.get()) + " where matricula = %s" % int(self.matricula))
            self.cursor.execute(query)
            messagebox.showinfo("Aviso", "Senha alterada!")
        if self.novo_tel.get() != "":
            query = (
            "update aluno set telefone = " + str(self.novo_tel.get()) + " where matricula = %s" % int(self.matricula))
            messagebox.showinfo("Aviso", "Telefone alterado!")
            self.cursor.execute(query)

    # --------------------------------\INFORMACAO------------------------------------------------------

    # -----------------------------------MATERIA----------------------------------------------------
    def ir_frame_mat(self):
        self.tela_insc = Frame(self)

        self.lbCodigo = Label(self.tela_insc, text="Código da matéria", font="callibri").pack(anchor=CENTER)
        self.entCodigo = Entry(self.tela_insc)
        self.entCodigo.pack(anchor=CENTER)

        self.lbNotaP1 = Label(self.tela_insc, text="Nota da P1", font="callibri").pack(anchor=CENTER)
        self.entNotaP1 = Entry(self.tela_insc)
        self.entNotaP1.pack(anchor=CENTER)

        self.lbNotaP2 = Label(self.tela_insc, text="Nota da P2", font="callibri").pack(anchor=CENTER)
        self.entNotaP2 = Entry(self.tela_insc)
        self.entNotaP2.pack(anchor=CENTER)

        bt1 = Button(self.tela_insc, text="Adicionar", command=self.adicionar_mat)
        bt1.pack(anchor=CENTER)

        self.frame_ativo.destroy()
        self.frame_ativo = self.tela_insc
        self.frame_ativo.pack()

    def adicionar_mat(self):
        self.cursor = self.cnx.cursor()
        cm = ("insert into materias (matricula, codigo, p1, p2) values (%s, %s, %s, %s)")
        cm_arg = (int(self.matricula), self.entCodigo.get(), float(self.entNotaP1.get()), float(self.entNotaP2.get()))

        query = ("select codigo from materias where matricula = %s" % str(self.matricula))

        self.cursor.execute(query)

        for (codigo,) in self.cursor:
            if codigo == str(self.entCodigo.get()):
                messagebox.showwarning("Aviso", "Você já cadastrou essa matéria!")
                return
        else:
            if float(self.entNotaP1.get()) > 10 or float(self.entNotaP1.get()) < 0 or float(
                    self.entNotaP2.get()) > 10 or float(self.entNotaP2.get()) < 0:
                messagebox.showerror("Erro", "Digite notas válidas!")
                return
            else:
                self.cursor.execute(cm, cm_arg)
        self.entCodigo.delete(0, 1000)
        self.entNotaP1.delete(0, 1000)
        self.entNotaP2.delete(0, 1000)
        self.cursor.close()
        messagebox.showinfo("Aviso", "Matéria adicionada!")

    # ---------------------------------------------\MATERIA-----------------------------------------------

    # ----------------------------------------GRUPO----------------------------------------------------
    def ir_frame_grupo(self):
        self.cursor = self.cnx.cursor(buffered=True)
        #self.cursor = self.cnx.cursor()
        #cursoraux = self.cnx.cursor()

        coluna = 0
        lin = 0
        contador = 0
        self.tela_grupos = Frame(self)
        self.frameauxiliar = Frame(self.tela_grupos)

        query = ("select * from grupos where matricula2 = %s or matricula3 = %s or matricula4 = %s or matricula5 = %s" %
                 (int(self.matricula), int(self.matricula), int(self.matricula), int(self.matricula)))
        self.cursor.execute(query)

        for (cod_grupo, codigo, matricula1, matricula2, matricula3, matricula4, matricula5) in self.cursor:
            if contador//3 == contador/3 and contador != 0:
                self.frameauxiliar.pack()
                self.frameauxiliar = Frame(self.tela_grupos)
                contador = 0
            contador +=1

            alunos = []

            if not matricula1 == None:
                query = ("select nome, email from aluno where matricula = %s"%matricula1)
                self.cursor.execute(query)#cursoraux.execute(query)
                for (nome, email) in self.cursor:#cursoraux:
                    alunos.append([nome, email])
                contador += 1
            else:
                alunos.append([None, None])

            #cursoraux = self.cnx.cursor()
            query = ("select nome, email from aluno where matricula = %s"%matricula2)
            self.cursor.execute(query)
            for (nome, email) in self.cursor:
                alunos.append([nome, email])

            if not matricula3 == None:
                #cursoraux = self.cnx.cursor()
                query = ("select nome, email from aluno where matricula = %s"%matricula3)
                self.cursor.execute(query)#cursoraux.execute(query)
                for (nome, email) in self.cursor:#cursoraux:
                    alunos.append([nome, email])
                contador += 1
                #cursoraux.close()
            else:
                alunos.append([None, None])

            if not matricula4 == None:
                #cursoraux = self.cnx.cursor()
                query = ("select nome, email from aluno where matricula = %s"%matricula4)
                self.cursor.execute(query)#cursoraux.execute(query)
                for (nome, email) in self.cursor:#cursoraux:
                    alunos.append([nome, email])
                contador += 1
                #self.cursor.close()#cursoraux.close()
            else:
                alunos.append([None, None])

            if not matricula5 == None:
                #cursoraux = self.cnx.cursor()
                query = ("select nome, email from aluno where matricula = %s"%matricula5)
                self.cursor.execute(query)
                for (nome, email) in self.cursor:#cursoraux:
                    alunos.append([nome, email])
                contador += 1
                #self.cursor.close()
            else:
                alunos.append([None, None])



            Label(self.frameauxiliar, text="Grupo " + codigo + " de " + str(cod_grupo), font="callibri").pack()

            lin += 1
            for dados in alunos:
                if dados[0] != None and dados[1] != None:
                    nome = "Nome: " + dados[0]
                    email = "Email: " + dados[1]
                    if matricula1 != None:
                        Label(self.frameauxiliar, text=nome, fg="blue").pack()
                        Label(self.frameauxiliar, text=email, fg="blue").pack()
                    else:
                        Label(self.frameauxiliar, text=nome).pack()
                        Label(self.frameauxiliar, text=email).pack()
            self.frameauxiliar.pack()
        self.cursor.close()
        self.frameauxiliar.pack()
        self.frame_ativo.destroy()
        self.frame_ativo = self.tela_grupos
        self.frame_ativo.pack()
    # -------------------------------------------\GRUPOS-------------------------------------------------------------------

    # --------------------------------------------INSCRICOES TUTOR----------------------------------------------------------
    def ir_frame_tutor(self):
        contador = 0
        materias6 = []
        self.cursor = self.cnx.cursor()

        query = ("select codigo from materias where matricula = %s and ((p1+p2+p2)/3) > 6" % str(self.matricula))

        self.cursor.execute(query)

        for (codigo,) in self.cursor:
            materias6.append(codigo)

        self.tela_tutor = Frame(self)

        self.framecaixa = Frame(self.tela_tutor)
        list = Listbox(self.framecaixa)
        list.pack()
        for i in materias6:
            list.insert(END, i)
        self.framecaixa.pack(side=LEFT)

        self.frameent = Frame(self.tela_tutor)

        Label(self.frameent, text="MATÉRIAS PARA TUTORIA", font="callibri").pack()

        self.lb = Label(self.frameent, text="Código da matéria").pack()
        self.ent = Entry(self.frameent)
        self.ent.pack()

        self.bt_cad = Button(self.frameent, text="Cadastrar", command=lambda: self.inscreve(self.ent.get(), '1', materias6))
        self.bt_cad.pack()

        self.bt_decad = Button(self.frameent, text="Descadastrar",
                               command=lambda: self.desinscreve(self.ent.get(), '1'))
        self.bt_decad.pack()

        self.frameent.pack()
        self.frame_ativo.destroy()
        self.frame_ativo = self.tela_tutor
        self.frame_ativo.pack()
        self.cursor.close()

    # ----------------------------------------\INSCRICAO TUTOR-------------------------------------------
    # ------------------------------------------INSCRICAO ALUNO--------------------------------------------
    def ir_frame_aluno(self):
        materias = []

        self.cursor = self.cnx.cursor()

        query = (
        "select codigo from materias where matricula = %s" % self.matricula)  # aponta todos os códigos de turma onde a matrícula bate

        self.cursor.execute(query)

        for (codigo,) in self.cursor:  # gera um vetor com todos os codigos de turma

            materias.append(codigo)

        self.tela_aluno = Frame(self)

        self.framecaixa = Frame(self.tela_aluno)
        list = Listbox(self.framecaixa)
        list.pack()
        for i in materias:
            list.insert(END, i)
        self.framecaixa.pack(side=LEFT)

        self.frameent = Frame(self.tela_aluno)
        Label(self.frameent, text="MATÉRIAS PARA ESTUDO", font="callibri").pack()

        self.lb = Label(self.frameent, text="Código da matéria").pack()
        self.ent = Entry(self.frameent)
        self.ent.pack()

        self.bt_cad = Button(self.frameent, text="Cadastrar", command=lambda: self.inscreve(self.ent.get(), '0', materias))
        self.bt_cad.pack()

        self.bt_decad = Button(self.frameent, text="Descadastrar",
                               command=lambda: self.desinscreve(self.ent.get(), '0'))
        self.bt_decad.pack()

        self.frameent.pack()
        self.frame_ativo.destroy()
        self.frame_ativo = self.tela_aluno
        self.frame_ativo.pack()
        self.cursor.close()

    def inscreve(self, key, char, materias):
        existe_cad = False
        self.cursor = self.cnx.cursor()

        # key é o codigo da turma e num é 0\1
        query = (
        "select codigo from aplic where matricula = %s and tutor_aluno = %s" % (int(self.matricula), int(char)))

        # cursor recebe lista de tuplas com todos os códigos onde a matrícula e o
        self.cursor.execute(query)

        for (codigo,) in self.cursor:
            if codigo == key:
                # caso você já esteja inscrito numa matéria que coincida com a key
                messagebox.showwarning("Aviso", "Você já está inscrito!")
                return

        if not key in materias:
            if char == "1":
                messagebox.showerror("Aviso", "Você não está qualificado para aplicar esta matéria como tutor!")
            else:
                messagebox.showerror("Aviso", "Esta matéria não está disponível!")
        else:
            # caso não encontre
            cm = ("insert into aplic (codigo, matricula, tutor_aluno) values(%s, %s, %s)")
            cm_arg = (key, int(self.matricula), char)
            self.cursor.execute(cm, cm_arg)
            messagebox.showinfo("Aviso", "Inscrito com sucesso!")
            grupo.verificar_grupos(self.matricula, self.cursor)
        self.cursor.close()

    def desinscreve(self, key, char):
        self.cursor = self.cnx.cursor(buffered=True)
        # verifica se está inscrito
        query = (
        "select codigo from aplic where matricula = %s and tutor_aluno = %s" % (int(self.matricula), int(char)))
        self.cursor.execute(query)
        for (codigo,) in self.cursor:
            if codigo == key:
                cm = ("DELETE from aplic where matricula = '%s' and codigo = '%s' and tutor_aluno = '%s'" % (
                self.matricula, key, char))
                self.cursor.execute(cm)
                messagebox.showinfo("Aviso", "Desinscrito com sucesso")
                self.cursor.close()
                return

        self.cursor.close()

        # key é o codigo da turma e num é 0\1
        messagebox.showwarning("Aviso", "Você não está inscrito!")

    # -------------------------------------\INSCRICÃO ALUNO-------------------------------------------------------------



    # ------------------------------------SOBRE NOS----------------------------------------------------------------------

    def ir_frame_nos(self):
        self.tela_nos = Frame(self)
        Label(self.tela_nos, text="BREVE RESUMO SOBRE OS CRIADORES", font="callibri", height=3).pack()
        textinho = "Somos quatro amigos que, entre os dias 24/10/2017 e 25/10/2017, participaram de uma Hackathon e \ntiveram o desafio de desenvolver algo. " \
                   + "Tendo em visto que somos do segundo período e não\ntínhamos muitos recursos, decidimos programar em python.\n" \
                   + "O maior problema, depois do algoritmo de criar turmas, foi o banco de dados. Percebemos que um arquivo\n" \
                   + "não seria a melhor forma de trabalhar com os dados e, ao longo da madrugada do dia 25, nós aprendemos MySQL\n" \
                   + "e demos um jeito de fazer conexão do python com a linguagem.\n" \
                   + "Dentre as várias ideias que desenvolvemos, pensamos em criar uma rede de estudos em grupos pra ajudar a\n" \
                   + "encontrar pessoas com quem estudar.\n"
        Label(self.tela_nos, text=textinho).pack()
        self.frame_ativo.destroy()
        self.frame_ativo = self.tela_nos
        self.frame_ativo.pack()
# -------------------------------------\SOBRE NOS------------------------------------------------------------------
# ------------------------------------SOBRE O APLICATIVO-----------------------------------------------------------
    def ir_frame_app(self):
        self.tela_app = Frame(self)

        self.frame_ativo_aux = Frame(self.tela_app)
        Label(self.frame_ativo_aux, text="coe").pack()
        self.frame_dos_botoes = Frame(self.tela_app)
        # botoes

        self.btpi = Button(self.frame_dos_botoes, text="Perfil - Informações", command=self.btpiDesc)
        self.btpi.pack()
        self.btpm = Button(self.frame_dos_botoes, text="Perfil - Matérias", command=self.btpmDesc)
        self.btpm.pack()
        self.btit = Button(self.frame_dos_botoes, text="Inscrição - Tutor", command=self.btitDesc)
        self.btit.pack()
        self.btia = Button(self.frame_dos_botoes, text="Inscrição - Aluno", command=self.btiaDesc)
        self.btia.pack()
        self.btgv = Button(self.frame_dos_botoes, text="Grupos - Ver Grupos", command=self.btgvDesc)
        self.btgv.pack()
        self.frame_dos_botoes.pack(side=LEFT, anchor=W)

        self.frame_ativo.destroy()
        self.frame_ativo = self.tela_app
        self.frame_ativo.pack(fill=X)

    def btpmDesc(self):
        self.framebtpm = Frame(self.tela_app)  # cria o frame
        textinho = "Nesta janela o estudante pode atualizar matérias e suas respectivas notas\n" + \
                   "podendo se inscrever como aluno ou tutor nas matérias adicionadas.\n\n" + \
                   "O primeiro campo é para o código da matéria! Vale ressaltar que:\n" + \
                   "• o código deve ter todas as letras em MAIÚSCULA e não deve ter traços ou pontos;\n" + \
                   "• deve ser precisamente o código da matéria, para que outras pessoas te encontrem.\n" + \
                   "(caso contrário, você vai ser o único no sistema com o código zuado e não vai combinar com ninguém)\n\n" + \
                   "O segundo campo é para sua nota! Vale lembrar que:\n" + \
                   "• as notas não podem, obviamente, ser menores que zero e nem maiores que 10;\n" + \
                   "• as notas não precisam ser numeros naturais, devendo ser apenas reais.\n" + \
                   "(para a galera de humanas, isso significa ser 8 ou 7.4)"
        titulo = "Perfil - Matérias"
        Label(self.framebtpm, text=titulo, font="callibri", height=3).pack()
        Label(self.framebtpm, text=textinho).pack()
        self.frame_ativo_aux.destroy()
        self.frame_ativo_aux = self.framebtpm
        self.frame_ativo_aux.pack(fill=BOTH)  # define como ativo

    def btpiDesc(self):
        self.framebtpi = Frame(self.tela_app)  # cria o frame
        textinho = "Nesta janela, o estudante pode atualizar sua senha, telefone e olhar suas informações.\n\n" + \
                   "O primeiro campo é para trocar sua senha. Você coloca sua senha nova e clica em atualizar!\n" + \
                   "O segundo campo é para seu telefone. Funciona do mesmo jeitinho que a senha!\n" + \
                   "Obs.: teu telefone e email serão divulgados para a pessoa que combinou com você, logo,\n" + \
                   "se você preferir não expor seu telefone, só salvar ele como 000000000 ou algo do tipo."
        titulo = "Perfil - Informações"
        Label(self.framebtpi, text=titulo, font="callibri", height=3).pack()
        Label(self.framebtpi, text=textinho).pack()
        self.frame_ativo_aux.destroy()
        self.frame_ativo_aux = self.framebtpi  # define como ativo
        self.frame_ativo_aux.pack(fill=BOTH)  # define como ativo

    def btitDesc(self):
        frame = Frame(self.tela_app)  # cria o frame
        textinho = "Nesta janela o estudante pode se cadastrar como tutor!\n\n" + \
                   "Vale ressaltar que você deve ter notas superiores a 6 na matéria.\n" + \
                   "Para se inscrever ou desinscrever, basta apertar os botões referentes às matérias."
        titulo = "Inscrição - Tutor"
        Label(frame, text=titulo, font="callibri", height=3).pack()
        Label(frame, text=textinho).pack()
        self.frame_ativo_aux.destroy()
        self.frame_ativo_aux = frame  # define como ativo
        self.frame_ativo_aux.pack(fill=BOTH)  # define como ativo

    def btiaDesc(self):
        frame = Frame(self.tela_app)  # cria o frame
        textinho = "Nesta janela o estudante pode se cadastrar como Aluno!\n\n" + \
                   "Diferente do caso do tutor, para ser aluno basta \nter alguma nota cadastrada na matéria.\n" + \
                   "Para se inscrever ou desinscrever, basta apertar os botões referentes às matérias."
        titulo = "Inscrição - Aluno"
        Label(frame, text=titulo, font="callibri", height=3).pack()
        Label(frame, text=textinho).pack()
        self.frame_ativo_aux.destroy()
        self.frame_ativo_aux = frame  # define como ativo
        self.frame_ativo_aux.pack(fill=BOTH)  # define como ativo

    def btgvDesc(self):
        frame = Frame(self.tela_app)  # cria o frame
        textinho = "Nesta janela são expostos os grupos em quais você está inserido!\n\n" + \
                   "O número é apenas o identificador de quais dos grupos \ndaquela matéria você está inserido\n" + \
                   "Obs.: O nome em azul mostra quem é o tutor. Se não tiver tutor, \ntodos os nomes apareceram em preto. Mesmo não tendo um tutor, já dá pra \n" + \
                   "vocês estudarem juntos, né?"
        titulo = "Grupos - Ver grupos"
        Label(frame, text=titulo, font="callibri", height=3).pack()
        Label(frame, text=textinho).pack()
        self.frame_ativo_aux.destroy()
        self.frame_ativo_aux = frame  # define como ativo
        self.frame_ativo_aux.pack(fill=BOTH)  # define como ativo
# -----------------------------------\SOBRE O APLICATIVO------------------------------------------------------------


#------------------------------------CALCULADORA----------------------------------------------------------------
    def ir_frame_calc(self):
        self.tela_calc = Frame(self)

        self.lb1 = Label(self.tela_calc, text="NOTA E PESO DA P1", font="callibri", height=3)
        self.lb1.pack()
        self.ent1 = Entry(self.tela_calc)
        self.ent1.insert(0, "Nota,Peso")
        self.ent1.pack()

        self.lb2 = Label(self.tela_calc, text="NOTA E PESO DA P2", font="callibri", height=3)
        self.lb2.pack()
        self.ent2 = Entry(self.tela_calc)
        self.ent2.insert(0, "Nota,Peso")
        self.ent2.pack()

        self.lb3 = Label(self.tela_calc, text="NOTA E PESO DA P3", font="callibri", height=3)
        self.lb3.pack()
        self.ent3 = Entry(self.tela_calc)
        self.ent3.insert(0, "Nota,Peso")
        self.ent3.pack()

        bt1 = Button(self.tela_calc, text="Calculadora", command=self.calcular).pack()

        self.frame_ativo.destroy()
        self.frame_ativo = self.tela_calc # define como ativo
        self.frame_ativo.pack(fill=BOTH)  # define como ativo

    def calcular(self):
        p1 = self.ent1.get()
        p2 = self.ent2.get()
        p3 = self.ent3.get()
        if p1 != "Nota, Peso" and p2 != "Nota,Peso" and p3 == "Nota,Peso":
            self.calculamedia(p1, p2, 0)
            return
        elif p1 != "Nota, Peso" and p2 != "Nota,Peso" and p3 != "Nota,Peso":
            self.calculamedia(p1, p2, p3)
            return
        else:
            messagebox.showwarning("Aviso", "Entre com valores válidos")
            return

    def calculamedia(self, p1, p2, p3):
        if p3 == 0:
            vals = p1.split(",")
            if self.verifica(vals[0]) and self.verifica(vals[1]):
                vals2 = p2.split(",")
                if self.verifica(vals2[0]) and self.verifica(vals2[1]):
                    valor = str(((6 * (float(vals[1])+float(vals2[1]))) - (float(vals[0])*float(vals[1])))/float(vals2[1]))
                    self.ent2.delete(0, 100)
                    self.ent2.insert(0, valor)
                    return
            else:
                messagebox.showwarning("Aviso", "Entre com valores válidos!")
                return
        else:
            vals = p1.split(",")
            if self.verifica(vals[0]) and self.verifica(vals[1]):
                vals2 = p2.split(",")
                if self.verifica(vals2[0]) and self.verifica(vals2[1]):
                    vals3 = p3.split(",")
                    if self.verifica(vals3[0]) and self.verifica(vals3[1]):
                        valor = str(((6 * (float(vals[1]) + float(vals2[1]) + float(vals3[1]))) - ((float(vals[0]) * float(vals[1])) + (float(vals2[0]) * float(vals2[1])))) / float(vals3[1]))
                        self.ent3.delete(0, 100)
                        self.ent3.insert(0, valor)
        return

    def verifica(self, val):
        vals = val.split(".")
        numero = True
        if len(vals) > 2:
            return False
        for item in vals:
            if not item.isnumeric():
                numero = False
        return numero
#-------------------------------------------\CALCULADORA------------------------------------------------------