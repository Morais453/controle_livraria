use library;

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    endereco TEXT,
    tipo_usuario ENUM('administrador', 'voluntário', 'membro') NOT NULL
);
CREATE TABLE livros (
    id_livro INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(100),
    ano_publicacao YEAR,
    isbn VARCHAR(20) UNIQUE,
    quantidade INT DEFAULT 1
);
CREATE TABLE emprestimos (
    id_emprestimo INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    id_livro INT,
    data_emprestimo DATE NOT NULL,
    data_devolucao DATE,
    status ENUM('emprestado', 'devolvido') DEFAULT 'emprestado',
    data_devolvido DATE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_livro) REFERENCES livros(id_livro)
);
