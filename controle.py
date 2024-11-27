from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import mysql.connector

# Função para listar os livros na tabela da tela principal
def lista_livros():
    lista.show()
    cursor = conexao.cursor()
    comando_SQL = 'SELECT * FROM livros'  # Leitura do banco de dados de livros
    cursor.execute(comando_SQL)
    leitura_banco = cursor.fetchall()

    lista.tableWidget.setRowCount(len(leitura_banco))
    lista.tableWidget.setColumnCount(5)  # ID, Título, Autor, Ano de Publicação, Quantidade

    for L in range(len(leitura_banco)):
        for C in range(5):
            lista.tableWidget.setItem(L, C, QTableWidgetItem(str(leitura_banco[L][C])))

def carregar_cadastro_livro():
    formulario_livro.show()

# Função para cadastrar um novo livro
def cadastrar_livro():
    titulo = formulario_livro.txtTitulo.text()
    autor = formulario_livro.txtAutor.text()
    ano_publicacao = formulario_livro.txtAnoPublicacao.text()
    isbn = formulario_livro.txtISBN.text()
    quantidade = formulario_livro.txtQuantidade.text()

    cursor = conexao.cursor()
    comando_SQL = f'''INSERT INTO livros (titulo, autor, ano_publicacao, isbn, quantidade) VALUES ('{titulo}', '{autor}', '{ano_publicacao}', '{isbn}', '{quantidade}')'''
    cursor.execute(comando_SQL)
    conexao.commit()

    formulario_livro.txtTitulo.setText('')
    formulario_livro.txtAutor.setText('')
    formulario_livro.txtAnoPublicacao.setText('')
    formulario_livro.txtISBN.setText('')
    formulario_livro.txtQuantidade.setText('')
    formulario_livro.close()

    lista_livros()

# Função para excluir um livro
def excluir_livro():
    remover = lista.tableWidget.currentRow()
    lista.tableWidget.removeRow(remover)

    cursor = conexao.cursor()
    cursor.execute('SELECT id_livro FROM livros')
    leitura_banco = cursor.fetchall()
    valor_id = leitura_banco[remover][0]
    comando_SQL = f'DELETE FROM livros WHERE id_livro = {valor_id}'
    cursor.execute(comando_SQL)
    conexao.commit()

# Função para editar um livro
def editar_livro():
    dados = lista.tableWidget.currentRow()
    cursor = conexao.cursor()

    cursor.execute('SELECT id_livro FROM livros')
    leitura_banco = cursor.fetchall()

    valor_id = leitura_banco[dados][0]

    # Busca os detalhes do livro com base no ID
    cursor.execute(f'SELECT * FROM livros WHERE id_livro = "{valor_id}"')
    leitura_banco = cursor.fetchone()

    # Verifica se o livro foi encontrado
    if leitura_banco is None:
        print("Livro não encontrado.")
        return

    # Preenche os campos da janela de edição
    editar_livro_window.txtAlterarId.setText(str(leitura_banco[0]))
    editar_livro_window.txtAlterarTitulo.setText(leitura_banco[1])
    editar_livro_window.txtAlterarAutor.setText(leitura_banco[2])
    editar_livro_window.txtAlterarAnoPublicacao.setText(str(leitura_banco[3]))
    editar_livro_window.txtAlterarQuantidade.setText(str(leitura_banco[4]))

    # Agora, mostra a janela de edição após preencher os campos
    editar_livro_window.show()


def salvar_edicao_livro():
    # Captura dos dados do formulário
    id_livro = int(editar_livro_window.txtAlterarId.text())
    titulo = editar_livro_window.txtAlterarTitulo.text()
    autor = editar_livro_window.txtAlterarAutor.text()
    ano_publicacao = int(editar_livro_window.txtAlterarAnoPublicacao.text())
    quantidade = int(editar_livro_window.txtAlterarQuantidade.text())

    # Atualização no banco de dados
    cursor = conexao.cursor()
    sql = '''UPDATE livros SET titulo = %s, autor = %s, ano_publicacao = %s, quantidade = %s WHERE id_livro = %s'''
    valores = (titulo, autor, ano_publicacao, quantidade, id_livro)

    cursor.execute(sql, valores)
    conexao.commit()

    # Fechar a janela de edição e atualizar a lista de livros
    editar_livro_window.close()
    lista_livros()  # Atualiza a lista de livros sem precisar fechar e reabrir a janela


# Função para registrar empréstimo de um livro
def registrar_emprestimo():
    id_usuario = formulario_emprestimo.txtIdUsuario.text()
    id_livro = formulario_emprestimo.txtIdLivro.text()
    data_emprestimo = formulario_emprestimo.txtDataEmprestimo.text()
    data_devolucao = formulario_emprestimo.txtDataDevolucao.text()

    cursor = conexao.cursor()
    comando_SQL = '''INSERT INTO emprestimos (id_usuario, id_livro, data_emprestimo, data_devolucao) VALUES (%s, %s, %s, %s)'''
    valores = (id_usuario, id_livro, data_emprestimo, data_devolucao)
    cursor.execute(comando_SQL, valores)
    conexao.commit()

    formulario_emprestimo.close()

# Função para cadastrar um novo usuário
def cadastrar_usuario():
    nome = formulario_usuario.txtNomeUsuario.text()
    email = formulario_usuario.txtEmailUsuario.text()
    telefone = formulario_usuario.txtTelefoneUsuario.text()
    endereco = formulario_usuario.txtEnderecoUsuario.text()
    tipo_usuario = formulario_usuario.comboTipoUsuario.currentText()

    cursor = conexao.cursor()
    comando_SQL = f'''INSERT INTO usuarios (nome, email, telefone, endereco, tipo_usuario)
                      VALUES ('{nome}', '{email}', '{telefone}', '{endereco}', '{tipo_usuario}')'''
    cursor.execute(comando_SQL)
    conexao.commit()

    formulario_usuario.txtNomeUsuario.setText('')
    formulario_usuario.txtEmailUsuario.setText('')
    formulario_usuario.txtTelefoneUsuario.setText('')
    formulario_usuario.txtEnderecoUsuario.setText('')
    formulario_usuario.comboTipoUsuario.setCurrentIndex(0)

    formulario_usuario.close()

# Função para verificar o usuário
def verificar_usuario():
    email = formulario_verificar_usuario.txtEmailVerificar.text()

    cursor = conexao.cursor()
    comando_SQL = f"SELECT * FROM usuarios WHERE email = '{email}'"
    cursor.execute(comando_SQL)
    resultado = cursor.fetchone()

    if resultado:
        formulario_verificar_usuario.lblMsgVerificar.setText(
            f'Usuário encontrado: {resultado[1]} ({resultado[2]})\n'
            f'Telefone: {resultado[3]}, Endereço: {resultado[4]}, Tipo: {resultado[5]}'
        )
    else:
        formulario_verificar_usuario.lblMsgVerificar.setText('Usuário não encontrado.')

    formulario_verificar_usuario.txtEmailVerificar.setText('')

# Conexão com o banco de dados
conexao = mysql.connector.connect(
    host="localhost",
    user="dev",
    password="1234",
    database="library"
)

# Inicializando a aplicação PyQt5
app = QtWidgets.QApplication([])

# Carregando as interfaces gráficas
lista = uic.loadUi('lista.ui')
formulario_livro = uic.loadUi('formulario_livro.ui')
editar_livro_window = uic.loadUi('editar_livro.ui')
formulario_emprestimo = uic.loadUi('formulario_emprestimo.ui')
formulario_usuario = uic.loadUi('formulario_usuario.ui')
formulario_verificar_usuario = uic.loadUi('formulario_verificar_usuario.ui')

# Conectando os botões da tela principal
lista.btnCadastrarLivro.clicked.connect(carregar_cadastro_livro)
lista.btnRegistrarEmprestimo.clicked.connect(registrar_emprestimo)
lista.btnAlterarRegistro.clicked.connect(editar_livro)
lista.btnApagarRegistro.clicked.connect(excluir_livro)
lista.btnCadastrarUsuario.clicked.connect(lambda: formulario_usuario.show())
lista.btnVerificarUsuario.clicked.connect(lambda: formulario_verificar_usuario.show())

# Conectando os botões das outras telas
formulario_livro.btnCadastrar.clicked.connect(cadastrar_livro)
formulario_usuario.btnCadastrarUsuario.clicked.connect(cadastrar_usuario)
formulario_verificar_usuario.btnVerificarUsuario.clicked.connect(verificar_usuario)
editar_livro_window.btnConfirmarAlteracao.clicked.connect(salvar_edicao_livro)


# Iniciando a aplicação
lista_livros()
lista.show()
app.exec()
