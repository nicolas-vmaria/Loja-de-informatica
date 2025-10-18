-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS loja_informatica;
USE loja_informatica;

CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL
);


-- Produtos
CREATE TABLE Produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL
);

-- Carrinho
CREATE TABLE Carrinho (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT,
    quantidade INT DEFAULT 1,
    FOREIGN KEY (produto_id) REFERENCES Produtos(id) ON DELETE CASCADE
);


-- Produtos
INSERT INTO Produtos (nome, preco) VALUES
('Teclado Mecânico', 350.00),
('Mouse Gamer', 150.00),
('Monitor 24"', 900.00);

-- Carrinho
INSERT INTO Carrinho (produto_id, quantidade) VALUES
(1, 1),
(3, 1);

ALTER TABLE Carrinho ADD COLUMN usuario_id INT NULL;
ALTER TABLE Carrinho ADD FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE;

ALTER TABLE Usuarios ADD COLUMN admin TINYINT(1) DEFAULT 0;

-- Definir um usuário como administrador
UPDATE Usuarios SET admin=1 WHERE email='admin@gmail.com';

