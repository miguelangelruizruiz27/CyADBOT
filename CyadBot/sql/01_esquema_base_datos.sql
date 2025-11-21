-- =========================================================
-- CYADBOT - Base de Datos Oficial (LIMPIA Y FUNCIONAL)
-- =========================================================

CREATE DATABASE IF NOT EXISTS cyadbot_db;
USE cyadbot_db;

-- =========================================================
-- Tabla 1: Preguntas Frecuentes
-- =========================================================
CREATE TABLE IF NOT EXISTS faqs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pregunta TEXT NOT NULL,
    respuesta TEXT NOT NULL,
    categoria VARCHAR(150) NOT NULL,
    INDEX idx_categoria (categoria)
);

-- =========================================================
-- Tabla 2: Documentos TXT (metadatos)
-- =========================================================
CREATE TABLE IF NOT EXISTS documentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_archivo VARCHAR(255) NOT NULL,
    tipo VARCHAR(50) DEFAULT 'txt',
    descripcion TEXT,
    categoria VARCHAR(150),
    INDEX idx_doc_categoria (categoria)
);

-- =========================================================
-- Tabla 3: Consultas no resueltas
-- =========================================================
CREATE TABLE IF NOT EXISTS consultas_sin_respuesta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pregunta TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT '✅ Base de datos creada correctamente' AS Mensaje;
