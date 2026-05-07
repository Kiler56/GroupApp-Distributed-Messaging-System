-- SCRIPT DE CREACIÓN DE BASE DE DATOS: ROLES_DB
-- Motor: PostgreSQL

CREATE TABLE IF NOT EXISTS rol_grupo (
    id_rol_grupo VARCHAR(50) PRIMARY KEY,
    id_grupo VARCHAR(50) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE(id_grupo, nombre)
);

CREATE TABLE IF NOT EXISTS recurso_grupo (
    id_recurso VARCHAR(50) PRIMARY KEY,
    nombre_recurso VARCHAR(100) NOT NULL,
    codigo_interno VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS rol_recurso (
    id_rol_recurso VARCHAR(50) PRIMARY KEY,
    id_rol_grupo VARCHAR(50) NOT NULL REFERENCES rol_grupo(id_rol_grupo) ON DELETE CASCADE,
    id_recurso VARCHAR(50) NOT NULL REFERENCES recurso_grupo(id_recurso)
);

-- POBLADO INICIAL DE RECURSOS (PERMISOS)
INSERT INTO recurso_grupo (id_recurso, nombre_recurso, codigo_interno) VALUES 
('GRP_MOD', 'Modificar información del grupo', 'GRP_MOD'),
('MEM_INV', 'Invitar y eliminar miembros', 'MEM_INV'),
('ROL_MNG', 'Crear y modificar roles', 'ROL_MNG'),
('DSC_MNG', 'Gestionar discusiones', 'DSC_MNG'),
('GRP_DEL', 'Eliminar grupo', 'GRP_DEL'),
('MSG_DIR', 'Enviar solicitudes de DM', 'MSG_DIR')
ON CONFLICT DO NOTHING;
