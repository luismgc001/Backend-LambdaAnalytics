# Backend Django/ Django Rest Framework

Este proyecto es un backend desarrollado con Django y Django Rest Framework que incluye funcionalidades de gestión de usuarios, autenticación con JWT, y control de roles y permisos.

## Características Principales
- Registro y autenticación de usuarios con JWT.
- Gestión de usuarios (listado, edición, desactivación).
- Roles de usuario: Administrador y Usuario.

---

## Requisitos

- Python 3.9 o superior
- Django 4.0 o superior
- Django Rest Framework
- Simple JWT

---

## Instalación

Sigue estos pasos para instalar y ejecutar el proyecto:

1. Clona este repositorio:
   ```bash
   git clone <URL del repositorio>
   cd <nombre_del_proyecto>
   ```

2. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```

3. Activa el entorno virtual:
   - En Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - En Windows:
     ```bash
     venv\Scripts\activate
     ```

4. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

5. Configura las variables de entorno (opcional):
   - Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:
     ```env
     SECRET_KEY=tu_clave_secreta
     DEBUG=True
     ```

6. Realiza las migraciones:
   ```bash
   python manage.py migrate
   ```

7. Inicia el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

---

## Endpoints Principales

### Registro de Usuarios
- **Endpoint:** `/api/register/`
- **Método:** `POST`
- **Descripción:** Permite registrar un nuevo usuario.

### Autenticación de Usuarios
- **Endpoint:** `/api/login/`
- **Método:** `POST`
- **Descripción:** Permite autenticar a un usuario y devuelve un token JWT.

### Listado de Usuarios
- **Endpoint:** `/api/users/`
- **Método:** `GET`
- **Descripción:** Lista todos los usuarios. Solo accesible para administradores.

### Edición de Usuarios
- **Endpoint:** `/api/users/<id>/`
- **Método:** `PUT`
- **Descripción:** Permite editar los datos de un usuario. Solo accesible para administradores.

### Desactivación de Usuarios
- **Endpoint:** `/api/users/<id>/deactivate/`
- **Método:** `DELETE`
- **Descripción:** Desactiva a un usuario en lugar de eliminarlo. Solo accesible para administradores.

---

## Tecnologías Utilizadas
- **Django:** Framework principal para el backend.
- **Django Rest Framework:** Para la creación de APIs RESTful.
- **Simple JWT:** Para autenticación mediante tokens.

---

## Estructura del Proyecto
```
<raiz_del_proyecto>/
├── manage.py
├── usuarios/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
├── requirements.txt
├── .env (opcional)
```

---

## Autor
Proyecto desarrollado por Luis Galvan Coneo.

