# GroupsApp Auth & Groups Service

Microservicio de autenticación, usuarios y gestión de grupos para el sistema distribuido **GroupsApp**.

---

## Tecnologías

* FastAPI
* SQLAlchemy
* SQLite
* JWT (JSON Web Tokens)
* Passlib (bcrypt)

---

## Instalación

```bash
git clone <repo>
cd auth-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Ejecutar el proyecto

```bash
uvicorn auth_service.main:app --reload
```

---

## Documentación interactiva

Disponible en:

```
http://127.0.0.1:8000/docs
```

---

## Funcionalidades implementadas

### Autenticación

* Registro de usuarios
* Login con JWT
* Perfil protegido

### Grupos

* Creación de grupos
* Creación automática de roles (Administrador / Miembro)
* Agregar usuarios a grupos (solo admin)
* Eliminar usuarios de grupos (solo admin)
* Salir de un grupo
* Validación de permisos por rol

---

## Endpoints principales

### Registro

```
POST /auth/register
```

```json
{
  "username": "usuario",
  "email": "correo@test.com",
  "password": "123456"
}
```

---

### Login

```
POST /auth/login
```

Devuelve:

```json
{
  "access_token": "TOKEN",
  "token_type": "bearer"
}
```

---

### Perfil (Protegido)

```
GET /auth/profile
```

---

## Endpoints de Grupos

### Crear grupo

```
POST /groups
```

---

### Ver grupos

```
GET /groups
```

---

### Ver usuarios de un grupo

```
GET /users-groups/{id_grupo}/usuarios
```

---

### Agregar usuario a grupo (Admin)

```
POST /users-groups/{id_grupo}/usuarios
```

```json
{
  "id_usuario": "2",
  "id_rol_grupo": "ID_ROL_MIEMBRO",
  "id_estado": "ACTIVO"
}
```

---

### Eliminar usuario de grupo (Admin)

```
DELETE /users-groups/{id_grupo}/usuarios/{id_usuario}
```

---

### Salir del grupo

```
DELETE /users-groups/{id_grupo}/leave
```

---

## Autenticación

Este servicio usa **JWT (Bearer Token)**.

En Swagger:

1. Click en "Authorize"
2. Ingresa:

   * username: email
   * password: contraseña

---

## Notas

* La base de datos (`*.db`) no se incluye en el repositorio
* Cada desarrollador genera su propia DB local
* El archivo `.env` no se sube por seguridad

---

## Estado del proyecto

✔ Autenticación completa
✔ Gestión de grupos con roles
✔ Control de acceso por permisos

---

## Autor

Desarrollado como parte del sistema distribuido **GroupsApp**
