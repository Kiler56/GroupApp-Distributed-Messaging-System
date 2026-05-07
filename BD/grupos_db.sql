-- SCRIPT DE CREACIÓN DE BASE DE DATOS: GRUPOS_DB
-- Motor: PostgreSQL

CREATE TABLE IF NOT EXISTS tipo_estado_usr_grp (
    id_estado VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS grupo (
    id_grupo VARCHAR(50) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_creacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_usuario_crea VARCHAR(50) NOT NULL,
    privado BOOLEAN NOT NULL DEFAULT FALSE,
    requiere_invitacion BOOLEAN NOT NULL DEFAULT FALSE,
    id_grupo_padre VARCHAR(50) REFERENCES grupo(id_grupo) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS usuarios_grupo (
    id_usuario_grupo VARCHAR(50) PRIMARY KEY,
    id_grupo VARCHAR(50) NOT NULL REFERENCES grupo(id_grupo) ON DELETE CASCADE,
    id_usuario VARCHAR(50) NOT NULL,
    id_rol_grupo VARCHAR(50) NOT NULL,
    fecha_union TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_estado VARCHAR(20) NOT NULL REFERENCES tipo_estado_usr_grp(id_estado),
    UNIQUE(id_grupo, id_usuario)
);

-- POBLADO INICIAL
INSERT INTO tipo_estado_usr_grp (id_estado, nombre) VALUES ('ACTIVO', 'Activo') ON CONFLICT DO NOTHING;
INSERT INTO tipo_estado_usr_grp (id_estado, nombre) VALUES ('INACTIVO', 'Inactivo') ON CONFLICT DO NOTHING;
