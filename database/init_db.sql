-- database/init_db.sql
-- Script de Inicialização para MariaDB (VERSÃO CORRIGIDA)
-- ----------------------------------------------------

-- 1. DROP E CRIAÇÃO DO BANCO DE DADOS
DROP DATABASE IF EXISTS mdk_db;
CREATE DATABASE mdk_db
CHARACTER SET utf8mb4 
COLLATE utf8mb4_general_ci;

-- 2. SELEÇÃO DO BANCO DE DADOS
USE mdk_db;

-- 3. CRIAÇÃO DAS TABELAS (DDL)

-- Tabela de Usuários (users)
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    -- (CORRIGIDO) VARCHAR para Bcrypt, que tem tamanho variável
    hashed_password VARCHAR(255) NOT NULL, 
    roles JSON NOT NULL
);

-- Tabela de Produtos (products)
DROP TABLE IF EXISTS products;
CREATE TABLE IF NOT EXISTS products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    availability BOOLEAN DEFAULT TRUE,
    category VARCHAR(100),
    imageUrl VARCHAR(255),
    visibility BOOLEAN DEFAULT TRUE
);

-- Tabela de Mesas (Tables)
DROP TABLE IF EXISTS tables;
CREATE TABLE IF NOT EXISTS tables (
    id INT PRIMARY KEY AUTO_INCREMENT, -- O número da mesa
    -- (MELHORIA) Adiciona restrição CHECK para garantir integridade
    status VARCHAR(50) NOT NULL CHECK (status IN ('available', 'occupied')),
    number_of_people INT NOT NULL DEFAULT 0
);

-- Tabela de Pedidos (Orders)
DROP TABLE IF EXISTS orders;
CREATE TABLE IF NOT EXISTS orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    table_number INT NOT NULL,
    -- (MELHORIA) Adiciona waiter_id para rastrear quem criou o pedido
    waiter_id INT NOT NULL, 
    -- (MELHORIA) Adiciona restrição CHECK para garantir integridade
    status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'in_progress', 'completed', 'cancelled')),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- (CORRIGIDO) Chaves estrangeiras são essenciais
    FOREIGN KEY (table_number) REFERENCES tables(id),
    FOREIGN KEY (waiter_id) REFERENCES users(id)
);

-- Tabela de Itens do Pedido (ItemOrders)
DROP TABLE IF EXISTS order_items;
CREATE TABLE IF NOT EXISTS order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price_at_order DECIMAL(10, 2) NOT NULL,
    
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id)
);


-- Não vai precisar, pois agora a cli lida com isso e a criação de waiter vai ser via api com um usuário admin

-- 4. INSERÇÃO DE DADOS INICIAIS (DML)

-- -- Dados para a tabela 'users'
-- INSERT INTO users (username, name, hashed_password, roles) VALUES 
-- ('admin', 'Admin do Sistema', 'hash_admin_seguro', '["admin"]'),
-- ('garcom_ana', 'Ana Silva (Garçonete)','hash_garcom_seguro_1', '["waiter"]'),
-- ('garcom_bruno', 'Bruno Costa (Garçom)','hash_garcom_seguro_2', '["waiter"]'),
-- ('super_bia', 'Bia Gerente (Admin e Garçonete)', 'hash_super_seguro', '["admin", "waiter"]');

-- Dados de Exemplo para as Mesas
INSERT INTO tables (id, status, number_of_people) VALUES
(1, 'available', 0), (2, 'available', 0), (3, 'available', 0),
(4, 'available', 0), (5, 'available', 0), (6, 'available', 0),
(7, 'available', 0), (8, 'available', 0), (9, 'available', 0),
(10, 'available', 0);

-- Dados da Tabela de Produtos (products)
INSERT INTO products (name, price, availability, category, imageUrl, visibility) VALUES
('Clássico da Casa', 24.90, 1, 'Hambúrgueres', '/images/categories/burguer.jpg', 1),
('Bacon Supreme', 29.90, 1, 'Hambúrgueres', '/images/categories/burguer.jpg', 1),
('Cheddar Melt', 27.90, 1, 'Hambúrgueres', '/images/categories/burguer.jpg', 1),
('Duplo Smash', 31.90, 1, 'Hambúrgueres', '/images/categories/burguer.jpg', 1),
('Veggie Burger', 26.90, 1, 'Hambúrgueres', '/images/categories/burguer.jpg', 1),
('Mussarela', 39.90, 1, 'Pizza', '/images/categories/pizza.jpg', 1),
('Calabresa', 44.90, 1, 'Pizza', '/images/categories/pizza.jpg', 1),
('Frango com Catupiry', 47.90, 1, 'Pizza', '/images/categories/pizza.jpg', 1),
('Quatro Queijos', 49.90, 1, 'Pizza', '/images/categories/pizza.jpg', 1),
('Do Chef', 52.90, 1, 'Pizza', '/images/categories/pizza.jpg', 1),
('Carne', 9.00, 1, 'Pastel', '/images/categories/pastel.jpg', 1),
('Queijo', 9.00, 1, 'Pastel', '/images/categories/pastel.jpg', 1),
('Pizza', 10.00, 1, 'Pastel', '/images/categories/pastel.jpg', 1),
('Frango com Catupiry', 11.00, 1, 'Pastel', '/images/categories/pastel.jpg', 1),
('Chocolate com Banana', 10.00, 1, 'Pastel', '/images/categories/pastel.jpg', 1),
('Batata Frita', 18.90, 1, 'Porcoes', '/images/categories/snacks.jpg', 1),
('Batata com Cheddar e Bacon', 25.90, 1, 'Porcoes', '/images/categories/batata_bac_chedd.jpg', 1),
('Frango à Passarinho', 32.90, 1, 'Porcoes', '/images/categories/frango.jpg', 1),
('Anéis de Cebola', 21.90, 1, 'Porcoes', '/images/categories/onion_rings.jpg', 1),
('Refrigerante Lata', 6.00, 1, 'Bebidas', '/images/categories/cokel.jpg', 1),
('Refrigerante 1L', 9.00, 1, 'Bebidas', '/images/categories/coke.jpg', 1),
('Suco Natural', 8.00, 1, 'Bebidas', '/images/categories/drinks.jpg', 1),
('Água Mineral', 4.00, 1, 'Bebidas', '/images/categories/water.jpg', 1),
('Chopp Pilsen', 10.00, 1, 'Bebidas', '/images/categories/chopp.jpg', 1),
('Cerveja Long Neck', 12.00, 1, 'Bebidas', '/images/categories/beer.jpg', 1),
('Brownie com Sorvete', 16.90, 1, 'Sobremesa', '/images/categories/brownie.jpg', 1),
('Açaí na Tigela', 14.90, 1, 'Sobremesa', '/images/categories/desserts.jpg', 1),
('Milkshake', 12.90, 1, 'Sobremesa', '/images/categories/milkshake.jpg', 1),
('Pudim da Casa', 10.90, 1, 'Sobremesa', '/images/categories/pudim.jpg', 1);
