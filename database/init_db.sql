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
('Clássico da Casa', 24.90, TRUE, 'Hambúrgueres', '/categories/burguer.jpg', TRUE),
('Bacon Supreme', 29.90, TRUE, 'Hambúrgueres', '/categories/burguer.jpg', TRUE),
('Cheddar Melt', 27.90, TRUE, 'Hambúrgueres', '/categories/burguer.jpg', TRUE),
('Duplo Smash', 31.90, TRUE, 'Hambúrgueres', '/categories/burguer.jpg', TRUE),
('Veggie Burger', 26.90, TRUE, 'Hambúrgueres', '/categories/burguer.jpg', TRUE),
('Mussarela', 39.90, TRUE, 'Pizza', '/categories/pizza.jpg', TRUE),
('Calabresa', 44.90, TRUE, 'Pizza', '/categories/pizza.jpg', TRUE),
('Frango com Catupiry', 47.90, TRUE, 'Pizza', '/categories/pizza.jpg', TRUE),
('Quatro Queijos', 49.90, TRUE, 'Pizza', '/categories/pizza.jpg', TRUE),
('Do Chef', 52.90, TRUE, 'Pizza', '/categories/pizza.jpg', TRUE),
('Carne', 9.00, TRUE, 'Pastel', '/categories/pastel.jpg', TRUE),
('Queijo', 9.00, TRUE, 'Pastel', '/categories/pastel.jpg', TRUE),
('Pizza', 10.00, TRUE, 'Pastel', '/categories/pastel.jpg', TRUE),
('Frango com Catupiry', 11.00, TRUE, 'Pastel', '/categories/pastel.jpg', TRUE),
('Chocolate com Banana', 10.00, TRUE, 'Pastel', '/categories/pastel.jpg', TRUE),
('Batata Frita', 18.90, TRUE, 'Porcoes', '/categories/snacks.jpg', TRUE),
('Batata com Cheddar e Bacon', 25.90, TRUE, 'Porcoes', '/categories/snacks.jpg', TRUE),
('Frango à Passarinho', 32.90, TRUE, 'Porcoes', '/categories/snacks.jpg', TRUE),
('Anéis de Cebola', 21.90, TRUE, 'Porcoes', '/categories/snacks.jpg', TRUE),
('Mandioca Frita', 19.90, TRUE, 'Porcoes', '/categories/snacks.jpg', TRUE),
('Refrigerante Lata', 6.00, TRUE, 'Bebidas', '/categories/drinks.jpg', TRUE),
('Refrigerante 1L', 9.00, TRUE, 'Bebidas', '/categories/drinks.jpg', TRUE),
('Suco Natural', 8.00, TRUE, 'Bebidas', '/categories/drinks.jpg', TRUE),
('Água Mineral', 4.00, TRUE, 'Bebidas', '/categories/drinks.jpg', TRUE),
('Chopp Pilsen', 10.00, TRUE, 'Bebidas', '/categories/drinks.jpg', TRUE),
('Cerveja Long Neck', 12.00, TRUE, 'Bebidas', '/categories/drinks.jpg', TRUE),
('Petit Gateau', 18.90, TRUE, 'Sobremesa', '/categories/desserts.jpg', TRUE),
('Brownie com Sorvete', 16.90, TRUE, 'Sobremesa', '/categories/desserts.jpg', TRUE),
('Açaí na Tigela', 14.90, TRUE, 'Sobremesa', '/categories/desserts.jpg', TRUE),
('Milkshake', 12.90, TRUE, 'Sobremesa', '/categories/desserts.jpg', TRUE),
('Pudim da Casa', 10.90, TRUE, 'Sobremesa', '/categories/desserts.jpg', TRUE);