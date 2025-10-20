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
INSERT INTO Usuarios (nome, email, senha, admin)
VALUES ('Administrador', 'adm@gmail.com', '123', 1);

ALTER TABLE Produtos ADD categoria VARCHAR(50);

SELECT DISTINCT categoria FROM Produtos;

SET SQL_SAFE_UPDATES = 0;
UPDATE Produtos SET categoria='Periféricos' WHERE nome LIKE '%Mouse%' OR nome LIKE '%Teclado%';
UPDATE Produtos SET categoria='Monitores' WHERE nome LIKE '%Monitor%';
UPDATE Produtos SET categoria='Cadeiras' WHERE nome LIKE '%Cadeira%';
SET SQL_SAFE_UPDATES = 1;



INSERT INTO Produtos (nome, preco, categoria) VALUES
-- Periféricos
('Teclado Mecânico Redragon Kumara RGB', 289.00, 'Periféricos'),
('Mouse Gamer Logitech G203', 149.00, 'Periféricos'),
('Headset Gamer HyperX Cloud II', 699.00, 'Periféricos'),
('Mousepad RGB Razer Goliathus', 199.00, 'Periféricos'),
('Webcam Logitech C920 Full HD', 499.00, 'Periféricos'),
('Teclado sem fio Logitech K380', 239.00, 'Periféricos'),
('Mouse sem fio Microsoft Bluetooth', 179.00, 'Periféricos'),
('Headset Razer Kraken X', 399.00, 'Periféricos'),

-- Monitores
('Monitor LG Ultrawide 29"', 1299.00, 'Monitores'),
('Monitor Samsung Odyssey G5 27"', 1999.00, 'Monitores'),
('Monitor AOC 24G2 144Hz', 1099.00, 'Monitores'),
('Monitor Dell P2422H 24"', 999.00, 'Monitores'),

-- Componentes
('Placa de Vídeo RTX 3060 12GB', 2499.00, 'Componentes'),
('Placa-Mãe ASUS Prime B550M', 799.00, 'Componentes'),
('Memória RAM Corsair Vengeance 16GB DDR4', 379.00, 'Componentes'),
('Fonte Corsair CV650 650W 80 Plus Bronze', 429.00, 'Componentes'),
('SSD Kingston NV2 1TB NVMe', 449.00, 'Componentes'),
('HD Seagate Barracuda 2TB', 379.00, 'Componentes'),
('Gabinete Cooler Master MB520 RGB', 499.00, 'Componentes'),

-- Cadeiras
('Cadeira Gamer ThunderX3 TGC12', 1199.00, 'Cadeiras'),
('Cadeira Gamer DT3 Elise', 999.00, 'Cadeiras'),
('Cadeira Ergonômica Flexform Alpha', 1399.00, 'Cadeiras'),
('Cadeira Gamer Razer Iskur', 1899.00, 'Cadeiras');



