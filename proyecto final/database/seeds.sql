USE control_escolar;

-- Datos opcionales de ejemplo.
-- database/schema.sql ya incluye estos datos para una instalacion completa.

INSERT INTO docentes (numero_empleado, nombre, apellido, email, telefono, especialidad)
VALUES
    ('EMP001', 'Ana', 'Gomez', 'ana.gomez@school.local', '555-1001', 'Matematicas'),
    ('EMP002', 'Luis', 'Perez', 'luis.perez@school.local', '555-1002', 'Fisica');

INSERT INTO materias (clave, nombre, descripcion, creditos, horas_semana)
VALUES
    ('MAT101', 'Matematicas I', 'Algebra y trigonometria', 5, 6),
    ('FIS101', 'Fisica I', 'Mecanica basica', 5, 6),
    ('PROG101', 'Programacion I', 'Fundamentos de programacion', 5, 6);

INSERT INTO grupos (nombre, semestre, aula, turno_id)
VALUES
    ('1A', 1, '101', 1),
    ('1B', 1, '102', 1);

INSERT INTO alumnos (matricula, nombre, apellido, grupo_id)
VALUES
    ('A001', 'Carlos', 'Lopez', 1),
    ('A002', 'Maria', 'Sanchez', 1),
    ('A003', 'Jose', 'Martinez', 2);

INSERT INTO planeaciones (grupo_id, materia_id, docente_id, dia_semana, hora_inicio, hora_fin, aula, periodo_escolar)
VALUES
    (1, 1, 1, 'Lunes', '08:00:00', '10:00:00', '101', '2026-1'),
    (1, 2, 2, 'Martes', '10:00:00', '12:00:00', '101', '2026-1');

INSERT INTO calificaciones (alumno_id, planeacion_id, docente_id, valor, tipo, fecha, comentarios)
VALUES
    (1, 1, 1, 8.50, 'Parcial', '2026-05-20', 'Buen desempeno'),
    (2, 1, 1, 9.00, 'Parcial', '2026-05-20', 'Entrega completa');
