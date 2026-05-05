export interface Grupo {
  id_grupo: string;
  nombre: string;
  descripcion?: string;
  privado: boolean;
  requiere_invitacion: boolean;
  fecha_creacion: string;
  id_usuario_crea: string;
}

export interface GrupoCreate {
  nombre: string;
  descripcion?: string;
  privado?: boolean;
  requiere_invitacion?: boolean;
}

export interface GrupoUpdate {
  nombre?: string;
  descripcion?: string;
  privado?: boolean;
  requiere_invitacion?: boolean;
}

export interface UsuarioGrupo {
  id_usuario_grupo: string;
  id_grupo: string;
  id_usuario: string;
  id_rol_grupo: string;
  id_estado?: string;
  fecha_union: string;
}
