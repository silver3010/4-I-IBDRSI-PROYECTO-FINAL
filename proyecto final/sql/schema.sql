-- =====================================================
-- SISTEMA WEB ESCOLAR
-- Base de datos final para entrega
-- Backend: Flask
-- Base de datos: MySQL
-- =====================================================

DROP DATABASE IF EXISTS control_escolar;
CREATE DATABASE control_escolar
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE control_escolar;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- =====================================================
-- TABLA: usuarios
-- Actores del sistema: Administrador, Docente y Control Escolar
-- Usuario inicial:
--   email: admin@school.local
--   password: admin123
-- =====================================================

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'docente', 'control_escolar') NOT NULL DEFAULT 'control_escolar',
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    ultimo_login DATETIME NULL,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =====================================================
-- TABLA: turnos
-- =====================================================

CREATE TABLE turnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
    hora_inicio TIME,
    hora_fin TIME,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =====================================================
-- TABLA: grupos
-- =====================================================

CREATE TABLE grupos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    semestre INT NOT NULL,
    aula VARCHAR(50),
    turno_id INT NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_grupos_turnos
        FOREIGN KEY (turno_id)
        REFERENCES turnos(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =====================================================
-- TABLA: materias
-- =====================================================

CREATE TABLE materias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clave VARCHAR(20) NOT NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    creditos INT NOT NULL DEFAULT 0,
    horas_semana INT NOT NULL DEFAULT 0,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =====================================================
-- TABLA: docentes
-- =====================================================

CREATE TABLE docentes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_empleado VARCHAR(30) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    telefono VARCHAR(20),
    especialidad VARCHAR(150),
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_contratacion DATE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =====================================================
-- TABLA: planeaciones
-- Relaciona grupo, materia, docente y horario
-- =====================================================

CREATE TABLE planeaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    grupo_id INT NOT NULL,
    materia_id INT NOT NULL,
    docente_id INT NOT NULL,
    dia_semana ENUM('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    aula VARCHAR(50),
    periodo_escolar VARCHAR(50),
    observaciones TEXT,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_planeaciones_grupos
        FOREIGN KEY (grupo_id)
        REFERENCES grupos(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_planeaciones_materias
        FOREIGN KEY (materia_id)
        REFERENCES materias(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_planeaciones_docentes
        FOREIGN KEY (docente_id)
        REFERENCES docentes(id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
) ENGINE=InnoDB;

-- =====================================================
-- TABLA: alumnos
-- =====================================================

CREATE TABLE alumnos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    grupo_id INT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_alumnos_grupos
        FOREIGN KEY (grupo_id)
        REFERENCES grupos(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
) ENGINE=InnoDB;

-- =====================================================
-- TABLA: calificaciones
-- =====================================================

CREATE TABLE calificaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    alumno_id INT NOT NULL,
    planeacion_id INT NULL,
    docente_id INT NULL,
    valor DECIMAL(5,2) NOT NULL,
    tipo ENUM('Parcial', 'Final', 'Tarea', 'Participacion') NOT NULL DEFAULT 'Parcial',
    fecha DATE DEFAULT NULL,
    comentarios TEXT,
    creado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT chk_calificaciones_valor
        CHECK (valor >= 0 AND valor <= 10),

    CONSTRAINT fk_calificaciones_alumnos
        FOREIGN KEY (alumno_id)
        REFERENCES alumnos(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT fk_calificaciones_planeaciones
        FOREIGN KEY (planeacion_id)
        REFERENCES planeaciones(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,

    CONSTRAINT fk_calificaciones_docentes
        FOREIGN KEY (docente_id)
        REFERENCES docentes(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
) ENGINE=InnoDB;

-- =====================================================
-- TABLAS DE APOYO: logs y auditoria
-- =====================================================

CREATE TABLE logs_login (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    email VARCHAR(150),
    ip_address VARCHAR(45),
    user_agent TEXT,
    login_exitoso BOOLEAN NOT NULL DEFAULT TRUE,
    mensaje VARCHAR(255),
    fecha_login TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_logs_login_usuarios
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE audit_logs (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NULL,
    tabla_afectada VARCHAR(100) NOT NULL,
    registro_id INT NOT NULL,
    accion ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    datos_anteriores JSON NULL,
    datos_nuevos JSON NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    fecha_evento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audit_logs_usuarios
        FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
) ENGINE=InnoDB;

-- =====================================================
-- INDICES
-- =====================================================

CREATE INDEX idx_grupos_turno ON grupos(turno_id);
CREATE INDEX idx_alumnos_grupo ON alumnos(grupo_id);
CREATE INDEX idx_planeaciones_grupo ON planeaciones(grupo_id);
CREATE INDEX idx_planeaciones_docente ON planeaciones(docente_id);
CREATE INDEX idx_planeaciones_materia ON planeaciones(materia_id);
CREATE INDEX idx_calificaciones_alumno ON calificaciones(alumno_id);
CREATE INDEX idx_calificaciones_planeacion ON calificaciones(planeacion_id);
CREATE INDEX idx_logs_login_usuario ON logs_login(usuario_id);
CREATE INDEX idx_logs_login_fecha ON logs_login(fecha_login);
CREATE INDEX idx_audit_logs_tabla ON audit_logs(tabla_afectada);
CREATE INDEX idx_audit_logs_usuario ON audit_logs(usuario_id);
CREATE INDEX idx_audit_logs_fecha ON audit_logs(fecha_evento);

-- =====================================================
-- DATOS INICIALES
-- =====================================================

INSERT INTO turnos (nombre, descripcion, hora_inicio, hora_fin)
VALUES
    ('Matutino', 'Turno de manana', '07:00:00', '13:00:00'),
    ('Vespertino', 'Turno de tarde', '14:00:00', '20:00:00');

INSERT INTO usuarios (nombre, apellido, email, password, rol)
VALUES
    (
        'Administrador',
        'Sistema',
        'admin@school.local',
        'scrypt:32768:8:1$sOK0FG6Nbf9Mr321$ffed9e734e28ce4c07b0199cf193a3dd566c439f57780467744a3c55c80d3bf74c738e61710dff50cb30461a6e8eda655090571c872a4deb03bcab4b99eb85e6',
        'admin'
    );

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

SET FOREIGN_KEY_CHECKS = 1;

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================
