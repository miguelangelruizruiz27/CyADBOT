USE cyadbot_db;

-- FAQs básicas
INSERT INTO faqs (pregunta, respuesta, categoria) VALUES
('donde puedo consultar las calificaciones', 'Puedes ver tus calificaciones en atzoncal.uam.mx', 'academico'),
('Donde pueedo consultar los horarios', 'Los horarios están en la cartelera de CyAD', 'horarios'),
('Donde puedo ir a ver los tramites', 'Para trámites acude a ventanilla de lunes a viernes', 'tramites');

-- Registrar los documentos que tenemos (SOLO metadatos)
INSERT INTO documentos (nombre_archivo, tipo, descripcion) VALUES
('Reglamento Alumnado.txt', 'pdf', 'Reglamento escolar y normas'),
('Guia Nuevo Ingreso.pdf', 'pdf', 'Guía para estudiantes de nuevo ingreso');

SELECT '✅ Datos básicos insertados' AS Mensaje;


USE cyadbot_db;

START TRANSACTION;

INSERT INTO faqs (pregunta, respuesta, categoria) VALUES

('¿Dónde y cómo solicito una beca UAM?',
 'En la UAM hay periodos de registro; consulta las fechas y convocatorias en http://www.becas.uam.mx/ .',
 'becas'),

('¿Cuándo se publica la convocatoria de becas?',
 'Cada trimestre se publica entre la segunda o tercera semana de clases.',
 'becas'),

('¿Quién evalúa y otorga una beca?',
 'El Comité de Becas UAM evalúa las solicitudes conforme a la Convocatoria y a las Reglas de Operación del PNB vigentes.',
 'becas'),

('¿Cuántos tipos de becas hay?',
 'Entre otras: Beca de continuación de estudios; Beca de grupos vulnerables; Beca de excelencia; Beca de movilidad estudiantil; Beca de servicio social; Becas para posgrado.',
 'becas'),

-- QUINTA OPORTUNIDAD
('¿Quiero solicitar una quinta oportunidad para acreditar una UEA?',
 'Puedes inscribir la 5ª oportunidad normal con sinodales del sistema, o solicitar una 5ª especial al Director de la División para integrar un jurado de tres profesores del área y ser evaluado.',
 'quinta_oportunidad'),

-- PLAZOS Y PRÓRROGAS
('¿Cuál es el plazo para realizar los estudios en licenciatura?',
 'Debes cubrir todos los créditos en un plazo no mayor a diez años contados desde tu primer ingreso a la Universidad.',
 'reglamento_academico'),

('¿Si no terminé los créditos en 10 años qué puedo hacer?',
 'Puedes solicitar nuevamente la calidad de alumno mediante una prórroga para concluir los estudios.',
 'prorroga'),

('¿Qué requisitos debo tener para solicitar una prórroga?',
 'Haber cubierto al menos el 75% de los créditos del plan y presentar la solicitud dentro de los seis trimestres lectivos posteriores al vencimiento del plazo máximo.',
 'prorroga'),

('¿Cómo solicito mi prórroga?',
 'Solicita “situación académica para prórroga” e “historial académico” vía Módulo de Información Escolar o caja (Edificio A, PB) con la solicitud de Servicios Escolares; entrega en Registro Escolar o envía a csera@xanum.uam.mx con asunto “solicitud de prórroga”.',
 'prorroga');

COMMIT;
UPDATE documentos
SET categoria = 'nuevo_ingreso'
WHERE nombre_archivo LIKE '%Guia Nuevo Ingreso%';


UPDATE documentos
SET categoria = 'reglamento_alumnado'
WHERE nombre_archivo LIKE '%Reglamento Alumnado%';
