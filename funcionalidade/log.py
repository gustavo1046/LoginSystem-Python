import sys
from hashlib import md5
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect
import mysql.connector
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget
from PyQt5.uic import loadUi

banco = mysql.connector.connect(
   host = "localhost",
   user = "root",
   password = "jinjoe0067",
   database = "db_login"
)

# def banco_conectado(): #funçao teste da conexão com o banco de dados
#     if banco.is_connected():
#         print("banco conectado!!")
#     else:
#         print("oh no!")
# banco_conectado()
        

class Login(QMainWindow):
    def __init__(self): #construtor da classe
        super(Login,self).__init__() #referencia a superclasse
        loadUi("./telas/login.ui", self) #carrega a tela de login
        self.warning_login_nome.setText("") #limpa os campos de erros
        self.warning_login_senha.setText("")
        self.senha.setEchoMode(QtWidgets.QLineEdit.Password) #configura o campo de senha para caracteres ocultos
        self.entrar.clicked.connect(self.procura_login) #ativa a funçao de login
        self.cadastrar.clicked.connect(self.troca_cadastro)

    def procura_login(self): #pesquisa no banco de dados
        nome = self.nome.text()
        senha = self.senha.text()
        cursor = banco.cursor()
        
        query_login = "select nome, senha from usuarios;"
        cursor.execute(query_login)
        resultado = cursor.fetchall()
        if nome == '' or senha == '':
            if nome == '':
                self.warning_login_nome.setText("Campo Obrigatório!")
            if senha == '':
                self.warning_login_senha.setText("Campo Obrigatório!")
        else:
            
            for x in range(len(resultado)):
                if nome == resultado[x][0] and senha == resultado[x][1]:
                    self.troca_inicio()
                    
                else:
                    self.warning_login_nome.setText("Usuário não encontrado!")
    def troca_inicio(self):
        inicio = Inicio()
        widget.addWidget(inicio)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def troca_cadastro(self):
        cadastro = Cadastro()
        widget.addWidget(cadastro) #adiciona a tela de cadastro a pilha de telas para fazer o salto
        widget.setCurrentIndex(widget.currentIndex()+1)


class Cadastro(QMainWindow):
    def __init__(self):
        super(Cadastro,self).__init__()
        loadUi("./telas/cadastro.ui",self)
        self.senha.setEchoMode(QtWidgets.QLineEdit.Password) #converte a estilização para password
        self.confirmasenha.setEchoMode(QtWidgets.QLineEdit.Password) #converte a estilização para password
        self.cadastrarse.clicked.connect(self.conferecampos)
        self.voltar.clicked.connect(self.voltatela)

    def voltatela(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def conferecampos(self): #confere se os campos estão vazios e se são validos
        self.warning_nome.setText("") #configura as labels toda vez que o botão é apertado
        self.warning_email.setText("")
        self.warning_senha.setText("")
        self.warning_confirmasenha.setText("")

        nome = self.nome.text()
        email = self.email.text()
        senha = self.senha.text()
        confirmasenha = self.confirmasenha.text()

        if nome == '' or email == '' or senha == '' or confirmasenha == '':
            if nome == '':
                self.warning_nome.setText("Campo obrigatório!")

            if senha == '':
                self.warning_senha.setText("Campo obrigatório!")
            
            if confirmasenha == '':
                self.warning_senha.setText("Campo obrigatório!")
        
        if "@" not in email or "." not in email:
                self.warning_email.setText("O email digitado é inválido!")
        else:
            emailFormat = email.split("@")
            userName = emailFormat[0]
            dominioFormat = emailFormat[1].split(".")
            dominio = dominioFormat[0]
            if len(userName) >= 3 and len(dominio) >= 1: # O username deve ter no mínimo 3 caracteres, dompinio ter no mínimo 1 caracter
                print("email valido!")
            else:
                self.warning_email.setText("O email digitado é inválido!")

        if senha != confirmasenha or confirmasenha == '': #se as senhas nao forem iguais ele exibe uma mensagem
            self.warning_confirmasenha.setText("senhas diferentes, digite novamente!")
        else:
            self.validacaocadastro()#se tudo estiver correto ele chama a funçao de escrever no banco
            
    def validacaocadastro(self): #funçao que cadastra os dados recolhidos na funçao cadastro no banco de dados
        
        nome = self.nome.text()
        email = self.email.text()
        senha = self.senha.text()

        cursor = banco.cursor() #cursor do banco de dados
       
        cursor.execute("create table if not exists usuarios (id int auto_increment not null primary key, nome varchar(25) not null, senha varchar(40) not null, email varchar(25) not null);")
        cursor.execute("insert into usuarios(nome, senha, email) values ('"+nome+"', '"+senha+"', '"+email+"');") #funçao de cadastro no banco com valores vazios
        banco.commit()
        login=Login() #volta para a tela de login apos realizar o cadastro com sucesso
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Inicio(QMainWindow):
    def __init__(self):
        super(Inicio, self).__init__()
        print("A partir daqui pode criar oque quiser :))")


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.showMaximized()
app.exec()


