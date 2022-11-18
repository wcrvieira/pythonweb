/* Criação da base de dados perfil  */
CREATE DATABASE IF NOT EXISTS perfil DEFAULT CHARACTER SET utf8
    COLLATE utf8_general_ci;

/* Definição da base de dados padrão */
USE perfil;

/* Criação da tabela contas */
CREATE TABLE IF NOT EXISTS contas (
    id int(6) NOT NULL AUTO_INCREMENT,
    usuario varchar(50) NOT NULL,
    senha varchar(255) NOT NULL,
    email varchar(100) NOT NULL,
    celular varchar(20) NOT NULL,
    cidade varchar(60) NOT NULL,
    estado varchar(40) NOT NULL,
    PRIMARY KEY(id)
);


