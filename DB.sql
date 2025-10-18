-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS loja_informatica;
USE loja_informatica;

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
