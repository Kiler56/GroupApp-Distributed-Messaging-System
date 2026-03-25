#  GroupsApp Auth Service

Microservicio de autenticación y gestión de usuarios para el sistema distribuido **GroupsApp**.

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
uvicorn main:app --reload
```

---

## Documentación interactiva

Disponible en:

```
http://127.0.0.1:8000/docs
```

---

##  Endpoints principales

###  Registro

```
POST /auth/register
```

Body:

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

Se usa desde Swagger con:

* username → email
* password → contraseña

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

Requiere autenticación con JWT.

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

## Autor

Microservicio desarrollado como parte del sistema distribuido **GroupsApp**
