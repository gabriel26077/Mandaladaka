-- database/init_db.sql
-- Script de Inicialização para MariaDB
-- ----------------------------------------------------

-- 1. DROP E CRIAÇÃO DO BANCO DE DADOS (MariaDB/MySQL)
-- IMPORTANTE: Este comando apaga todo o banco de dados se ele existir!
DROP DATABASE IF EXISTS mdk_db;
CREATE DATABASE mdk_db
CHARACTER SET utf8mb4 
COLLATE utf8mb4_general_ci;

-- 2. SELEÇÃO DO BANCO DE DADOS
USE mdk_db;

-- 3. CRIAÇÃO DAS TABELAS (DDL)
-- Exemplo da Tabela de Usuários (Mantenha se for usar)
DROP TABLE IF EXISTS usuarios;
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha_hash CHAR(64) NOT NULL
);

-- Sua Tabela de Produtos (products)
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

-- Adicione outras tabelas aqui (Ex: orders, customers, etc.)
-- ...

---

-- 4. INSERÇÃO DE DADOS INICIAIS (DML)

-- Dados de Exemplo para a tabela usuarios
INSERT INTO usuarios (nome, email, senha_hash) VALUES 
('Alice Dev', 'alice@projeto.com', 'hash_exemplo_1'),
('Bob Teste', 'bob@projeto.com', 'hash_exemplo_2');


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

-- Adicione outros INSERTs de dados iniciais aqui