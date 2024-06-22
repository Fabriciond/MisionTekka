CREATE DATABASE Teeka;
USE Teeka;

CREATE TABLE lanzamientos (
    id INT(11) PRIMARY KEY AUTO_INCREMENT,
    lugar VARCHAR(45),
    descripcion VARCHAR(500),
    hora VARCHAR(45)
);

CREATE TABLE ili (
    id INT(11) PRIMARY KEY AUTO_INCREMENT,
    tiempo VARCHAR(45),
    humedad DECIMAL(6, 2),
    temperatura_dht DECIMAL(6, 2),
    temperatura_bmp DECIMAL(6, 2),
    co2 DECIMAL(10, 2),
    presion DECIMAL(6, 2),
    altitud DECIMAL(10, 2),
    indice_uv INT(11),
    id_lanzamiento INT(11),
    FOREIGN KEY (id_lanzamiento) REFERENCES lanzamientos(id)
);

CREATE TABLE suawaka (
    id INT(11) PRIMARY KEY AUTO_INCREMENT,
    tiempo VARCHAR(45),
    temperatura DECIMAL(6, 2),
    presion DECIMAL(6, 2),
    altitud DECIMAL(6, 2),
    aceleracion_x DECIMAL(6, 2),
    aceleracion_y DECIMAL(6, 2),
    aceleracion_z DECIMAL(6, 2),
    -- longitud DECIMAL(10, 6),
    -- latitud DECIMAL(10, 6),
    id_lanzamiento INT(11),
    FOREIGN KEY (id_lanzamiento) REFERENCES lanzamientos(id)
);