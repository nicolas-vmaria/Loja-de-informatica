-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS loja_informatica;
USE loja_informatica;

-- ==============================
-- TABELA: Usuários
-- ==============================
CREATE TABLE Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    admin TINYINT(1) DEFAULT 0
);

-- ==============================
-- TABELA: Produtos
-- ==============================
CREATE TABLE Produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    categoria VARCHAR(50),
    estoque INT DEFAULT 0,
    id_imagem VARCHAR(20)
);

-- ==============================
-- TABELA: Carrinho
-- ==============================
CREATE TABLE Carrinho (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT,
    usuario_id INT,
    quantidade INT DEFAULT 1,
    FOREIGN KEY (produto_id) REFERENCES Produtos(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE
);

-- ==============================
-- USUÁRIO ADMINISTRADOR
-- ==============================
INSERT INTO Usuarios (nome, email, senha, admin)
VALUES ('Administrador', 'adm@gmail.com', '123', 1);

-- ==============================
-- PRODUTOS (com estoque e imagem)
-- ==============================
INSERT INTO Produtos (nome, preco, categoria, estoque, id_imagem) VALUES
-- Periféricos
('Teclado Mecânico Redragon Kumara RGB', 289.00, 'Periféricos', 35, '17P01.png'),
('Mouse Gamer Logitech G203', 149.00, 'Periféricos', 22, '18P02.png'),
('Headset Gamer HyperX Cloud II', 699.00, 'Periféricos', 14, '19P03.png'),
('Mousepad RGB Razer Goliathus', 199.00, 'Periféricos', 47, '20P04.png'),
('Webcam Logitech C920 Full HD', 499.00, 'Periféricos', 18, '21P05.png'),
('Teclado sem fio Logitech K380', 239.00, 'Periféricos', 29, '22P06.png'),
('Mouse sem fio Microsoft Bluetooth', 179.00, 'Periféricos', 42, '23P07.png'),
('Headset Razer Kraken X', 399.00, 'Periféricos', 25, '24P08.png'),

-- Monitores
('Monitor LG Ultrawide 29"', 1299.00, 'Monitores', 17, '12M01.png'),
('Monitor Samsung Odyssey G5 27"', 1999.00, 'Monitores', 9, '13M02.png'),
('Monitor AOC 24G2 144Hz', 1099.00, 'Monitores', 26, '14M03.png'),
('Monitor Dell P2422H 24"', 999.00, 'Monitores', 33, '15M04.png'),

-- Componentes
('Placa de Vídeo RTX 3060 12GB', 2499.00, 'Componentes', 11, '05C01.png'),
('Placa-Mãe ASUS Prime B550M', 799.00, 'Componentes', 27, '06C02.png'),
('Memória RAM Corsair Vengeance 16GB DDR4', 379.00, 'Componentes', 38, '07C03.png'),
('Fonte Corsair CV650 650W 80 Plus Bronze', 429.00, 'Componentes', 44, '08C04.png'),
('SSD Kingston NV2 1TB NVMe', 449.00, 'Componentes', 31, '09C05.png'),
('HD Seagate Barracuda 2TB', 379.00, 'Componentes', 36, '10C06.png'),
('Gabinete Cooler Master MB520 RGB', 499.00, 'Componentes', 20, '11C07.png'),

-- Cadeiras
('Cadeira Gamer ThunderX3 TGC12', 1199.00, 'Cadeiras', 12, '01CA01.png'),
('Cadeira Gamer DT3 Elise', 999.00, 'Cadeiras', 21, '02CA02.png'),
('Cadeira Ergonômica Flexform Alpha', 1399.00, 'Cadeiras', 15, '03CA03.png'),
('Cadeira Gamer Razer Iskur', 1899.00, 'Cadeiras', 8, '04CA04.png');

