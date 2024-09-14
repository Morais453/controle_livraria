from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import mysql.connector

# Função para adicionar novos livros no banco de dados
def inserir_livro():
    '''Função para capturar os dados da tela de cadastro de livros'''
    titulo = formulario.txtTitulo.text()
    autor = formulario.txtAutor.text()
    ano_publicacao = formulario.txtAnoPublicacao.text()
    isbn = formulario.txtISBN.text()
    quantidade = formulario.txtQuantidade.text()
    formulario.lblMsg.setText('Livro cadastrado com sucesso!')

    # Insere o livro no banco de dados
    cursor = conexao.cursor()
    comando_SQL = f'''INSERT INTO livros (titulo, autor, ano_publicacao, isbn, quantidade) 
    VALUES ('{titulo}','{autor}','{ano_publicacao}','{isbn}',{quantidade})'''
    cursor.execute(comando_SQL)
    conexao.commit()

    # Limpa os campos após o cadastro
    formulario.txtTitulo.setText('')
    formulario.txtAutor.setText('')
    formulario.txtAnoPublicacao.setText('')
    formulario.txtISBN.setText('')
    formulario.txtQuantidade.setText('')

# Função para exibir o relatório de livros cadastrados
def lista_livros():
    '''Mostra relatório de livros'''
    lista.show()
    cursor = conexao.cursor()
    comando_SQL = 'SELECT * FROM livros'
    cursor.execute(comando_SQL)
    leitura_banco = cursor.fetchall()

    lista.tableWidget.setRowCount(len(leitura_banco))
    lista.tableWidget.setColumnCount(5)  # Define 5 colunas (id, título, autor, ano, quantidade)

    for L in range(len(leitura_banco)):
        for C in range(5):
            lista.tableWidget.setItem(L, C, QTableWidgetItem(str(leitura_banco[L][C])))

# Função para registrar um empréstimo de livro
def registrar_emprestimo():
    '''Registra um empréstimo de livro para um usuário'''
    id_usuario = formulario.txtIdUsuario.text()
    id_livro = formulario.txtIdLivro.text()
    data_emprestimo = formulario.txtDataEmprestimo.text()
    data_devolucao = formulario.txtDataDevolucao.text()
    formulario.lblMsgEmprestimo.setText('Empréstimo registrado com sucesso!')

    # Insere o empréstimo no banco de dados
    cursor = conexao.cursor()
    comando_SQL = f'''INSERT INTO emprestimos (id_usuario, id_livro, data_emprestimo, data_devolucao, status) 
    VALUES ({id_usuario},{id_livro},'{data_emprestimo}','{data_devolucao}','emprestado')'''
    cursor.execute(comando_SQL)
    conexao.commit()

    # Limpa os campos após o registro
    formulario.txtIdUsuario.setText('')
    formulario.txtIdLivro.setText('')
    formulario.txtDataEmprestimo.setText('')
    formulario.txtDataDevolucao.setText('')

# Função para excluir um livro do banco de dados
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

# Função para editar os detalhes de um livro
def editar_livro():
    editar.show()
    global id_atual
    dados = lista.tableWidget.currentRow()
    cursor = conexao.cursor()
    cursor.execute('SELECT id_livro FROM livros')
    leitura_banco = cursor.fetchall()
    valor_id = leitura_banco[dados][0]
    comando_SQL = f'SELECT * FROM livros WHERE id_livro = {valor_id}'
    cursor.execute(comando_SQL)
    leitura_banco = cursor.fetchall()

    id_atual = valor_id
    editar.txtAlterarId.setText(str(leitura_banco[0][0]))
    editar.txtAlterarTitulo.setText(leitura_banco[0][1])
    editar.txtAlterarAutor.setText(leitura_banco[0][2])
    editar.txtAlterarAnoPublicacao.setText(str(leitura_banco[0][3]))
    editar.txtAlterarQuantidade.setText(str(leitura_banco[0][4]))

# Função para salvar os dados editados
def salvar_dados():
    global id_atual

    id = int(editar.txtAlterarId.text())
    titulo = editar.txtAlterarTitulo.text()
    autor = editar.txtAlterarAutor.text()
    ano_publicacao = int(editar.txtAlterarAnoPublicacao.text())
    quantidade = int(editar.txtAlterarQuantidade.text())

    cursor = conexao.cursor()
    sql = "UPDATE livros SET titulo = %s, autor = %s, ano_publicacao = %s, quantidade = %s WHERE id_livro = %s;"
    valores = (titulo, autor, ano_publicacao, quantidade, id)

    cursor.execute(sql, valores)

    editar.close()
    lista.close()
    formulario.show()

    conexao.commit()

# Configuração da conexão com o banco de dados MySQL
conexao = mysql.connector.connect(
    host="localhost",
    user="dev",
    password="1234",
    database="DataBaseStudy"
)

# Configuração da interface gráfica
app = QtWidgets.QApplication([])

formulario = uic.loadUi('formulario.ui')
formulario.btnCadastrarLivro.clicked.connect(inserir_livro)
formulario.btnRelatorioLivros.clicked.connect(lista_livros)
formulario.btnRegistrarEmprestimo.clicked.connect(registrar_emprestimo)

lista = uic.loadUi('lista.ui')
lista.btnAlterarRegistro.clicked.connect(editar_livro)
lista.btnApagarRegistro.clicked.connect(excluir_livro)

editar = uic.loadUi('editar.ui')
editar.btnConfirmarAlteracao.clicked.connect(salvar_dados)

formulario.show()
app.exec()