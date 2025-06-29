# 🏆 Tournament Management API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.13-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat&logo=python&logoColor=white)](https://python.org)
[![SQLite](https://img.shields.io/badge/SQLite-3.x-003B57.svg?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat)](LICENSE)

Un sistema completo de gestión de torneos construido con FastAPI que permite la organización y administración integral de competencias deportivas y de eSports.

## ✨ Características Principales

- 👥 **Gestión de Usuarios**: Registro, autenticación, actualización y eliminación de participantes
- 🏅 **Gestión de Equipos**: Creación, modificación y eliminación de equipos con asignación de capitanes
- 👤 **Gestión de Miembros**: Administración de membresías de equipos con roles específicos (jugador, capitán, suplente)
- 🏆 **Gestión de Torneos**: Configuración detallada de torneos con fechas, descripciones y capacidad máxima
- 📝 **Gestión de Inscripciones**: Manejo de la participación de equipos en torneos
- 💰 **Gestión de Pagos**: Registro y seguimiento de pagos asociados a las inscripciones
- ⚽ **Gestión de Partidos**: Programación y registro de resultados de encuentros

## 🏗️ Arquitectura del Proyecto

```
back/
├── app/
│   ├── crud/                  # Operaciones CRUD para cada entidad
│   │   ├── crud_user.py
│   │   ├── crud_team.py
│   │   ├── crud_member.py
│   │   ├── crud_tournament.py
│   │   ├── crud_inscription.py
│   │   ├── crud_payment.py
│   │   └── crud_match.py
│   ├── db/                    # Configuración de base de datos
│   │   └── database.py
│   ├── routers/               # Endpoints organizados por módulos
│   │   ├── users.py
│   │   ├── teams.py
│   │   ├── members.py
│   │   ├── tournaments.py
│   │   ├── inscriptions.py
│   │   ├── payments.py
│   │   └── matches.py
│   ├── schemas/               # Modelos Pydantic para validación
│   │   ├── user.py
│   │   ├── team.py
│   │   ├── member.py
│   │   ├── tournament.py
│   │   ├── inscription.py
│   │   ├── payment.py
│   │   ├── token.py
│   │   └── match.py
│   └── security/              # Autenticación y seguridad
│       └── security.py
├── main.py                    # Aplicación principal FastAPI
├── run.py                     # Script para iniciar el servidor
├── requirements.txt           # Dependencias del proyecto
└─── postman_collection.json   # Colección de Postman para testing

front/
├── node_modules/
├── index.js
├── package-lock.json
└── package.json

.gitignore
README.md                      # Este archivo
```


## 🚀 Running the Project

### Backend

1.  Navigate to the `back` directory:
    ```bash
    cd back
    ```
2.  Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
3.  Run the application:
    ```bash
    python run.py
    ```

### Frontend (Console App)

1.  Navigate to the `front` directory:
    ```bash
    cd front
    ```
2.  Install the dependencies:
    ```bash
    npm install
    ```
3.  Run the application:
    ```bash
    node index.js
    ```

## 🔮 Next Steps for the Frontend

This project includes a basic Node.js console application for interacting with the API. To create a more user-friendly and visually appealing experience, we recommend building a mobile application using the following technologies:

*   **React Native:** A popular framework for building native mobile apps using JavaScript and React.
*   **Expo:** A platform that simplifies React Native development, providing tools and services to build, deploy, and iterate on your apps.
*   **Gluestack UI:** A component library that provides a set of accessible, themeable, and production-ready components to build your UI quickly.

### Why this stack?

*   **Cross-platform:** Build for both iOS and Android with a single codebase.
*   **Fast development:** Expo and Gluestack UI provide a great developer experience and allow you to build and iterate quickly.
*   **Native performance:** React Native apps are compiled to native code, providing excellent performance.
*   **Vibrant ecosystem:** React Native has a large and active community, so you'll find plenty of resources and support.

### Getting Started

1.  **Set up your environment:** Follow the [Expo documentation](https://docs.expo.dev/get-started/installation/) to set up your development environment.
2.  **Create a new project:**
    ```bash
    npx create-expo-app@latest my-tournament-app
    cd my-tournament-app
    ```
3.  **Install Gluestack UI:**
    ```bash
    npx gluestack-ui@latest
    ```
4.  **Start building your UI:** Use the components from Gluestack UI to build the different screens of your application, such as:
    *   Login and registration screens
    *   A dashboard to display upcoming tournaments
    *   A screen to view the details of a tournament, including the stream
    *   A screen to view the user's profile and their teams
    *   A form to create and manage tournaments (for organizers)

## 🌐 Acceso a la API

- **API Base URL**: `http://localhost:8000`
- **Documentación Interactiva (Swagger UI)**: `http://localhost:8000/docs`
- **Documentación Alternativa (ReDoc)**: `http://localhost:8000/redoc`
- **Esquema OpenAPI**: `http://localhost:8000/openapi.json`

## 📊 Base de Datos

El sistema utiliza **SQLite** como base de datos, que se inicializa automáticamente al ejecutar la aplicación por primera vez. El archivo de base de datos se crea como `app_db.db` en el directorio raíz.

### Esquema de Base de Datos

#### Tablas Principales:

- **usuarios**: Información de usuarios registrados
- **equipos**: Datos de equipos y sus capitanes
- **miembros_equipo**: Relación usuarios-equipos con roles
- **torneos**: Configuración de torneos
- **inscripciones**: Registro de equipos en torneos
- **pagos**: Pagos asociados a inscripciones
- **partidos**: Programación y resultados de encuentros

## 🔌 Endpoints de la API

### 👥 Usuarios (`/users`)
- `POST /users/` - Crear nuevo usuario
- `GET /users/` - Listar todos los usuarios
- `GET /users/{user_id}` - Obtener usuario por ID
- `GET /users/nickname/{nickname}` - Obtener usuario por nickname
- `PUT /users/{user_id}` - Actualizar usuario
- `DELETE /users/{user_id}` - Eliminar usuario
- `POST /users/token` - Autenticación y obtención de token

### 🏅 Equipos (`/teams`)
- `POST /teams/` - Crear nuevo equipo
- `GET /teams/` - Listar todos los equipos
- `GET /teams/{team_id}` - Obtener equipo por ID
- `PUT /teams/{team_id}` - Actualizar equipo
- `DELETE /teams/{team_id}` - Eliminar equipo

### 👤 Miembros (`/members`)
- `POST /members/` - Añadir miembro a equipo
- `GET /members/` - Listar todas las membresías
- `DELETE /members/{member_id}` - Eliminar miembro de equipo

### 🏆 Torneos (`/tournaments`)
- `POST /tournaments/` - Crear nuevo torneo
- `GET /tournaments/` - Listar todos los torneos
- `GET /tournaments/{tournament_id}` - Obtener torneo por ID
- `PUT /tournaments/{tournament_id}` - Actualizar torneo
- `DELETE /tournaments/{tournament_id}` - Eliminar torneo

### 📝 Inscripciones (`/inscriptions`)
- `POST /inscriptions/` - Crear nueva inscripción
- `GET /inscriptions/` - Listar todas las inscripciones
- `DELETE /inscriptions/{inscription_id}` - Eliminar inscripción

### 💰 Pagos (`/payments`)
- `POST /payments/` - Registrar nuevo pago
- `GET /payments/` - Listar todos los pagos
- `DELETE /payments/{payment_id}` - Eliminar pago

### ⚽ Partidos (`/matches`)
- `POST /matches/` - Crear nuevo partido
- `GET /matches/` - Listar todos los partidos
- `DELETE /matches/{match_id}` - Eliminar partido

## 🔒 Seguridad

- **Autenticación**: Sistema basado en JWT (JSON Web Tokens)
- **Contraseñas**: Hash seguro usando bcrypt
- **Validación**: Validación completa de datos usando Pydantic
- **CORS**: Configuración de CORS para acceso desde diferentes dominios

### Variables de Entorno

```bash
SECRET_KEY=tu_clave_secreta_aqui  # Clave para firmar JWT (por defecto: "secret_key_123")
ACCESS_TOKEN_EXPIRE_MINUTES=30   # Duración del token en minutos
```

## 🧪 Testing

### Colección de Postman

El proyecto incluye una colección de Postman (`postman_collection.json`) con ejemplos de requests para todos los endpoints.

### Importar en Postman:
1. Abrir Postman
2. Hacer clic en "Import"
3. Seleccionar el archivo `postman_collection.json`
4. ¡Listo para probar la API!

### Testing Manual

Puedes probar la API directamente desde la documentación interactiva en `/docs`.

## 🛠️ Tecnologías Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com)**: Framework web moderno y rápido para construir APIs
- **[Pydantic](https://pydantic-docs.helpmanual.io)**: Validación de datos usando type hints
- **[SQLite](https://www.sqlite.org)**: Base de datos ligera y sin servidor
- **[Uvicorn](https://www.uvicorn.org)**: Servidor ASGI para aplicaciones Python async
- **[python-jose](https://python-jose.readthedocs.io)**: Implementación de JWT para Python
- **[passlib](https://passlib.readthedocs.io)**: Biblioteca para hash de contraseñas
- **[bcrypt](https://github.com/pyca/bcrypt)**: Función de hash adaptativa para contraseñas

## 📈 Ejemplos de Uso

### Crear un usuario
```bash
curl -X POST \"http://localhost:8000/users/\" \
     -H \"Content-Type: application/json\" \
     -d '{
       \"nombre\": \"Juan Pérez\",
       \"nickname\": \"jperez\",
       \"email\": \"juan.perez@example.com\",
       \"pwd_hash\": \"password123\"
     }'
```

### Crear un equipo
```bash
curl -X POST \"http://localhost:8000/teams/\" \
     -H \"Content-Type: application/json\" \
     -d '{
       \"nombre\": \"Los Campeones\",
       \"id_capitan\": 1
     }'
```

### Obtener todos los torneos
```bash
curl -X GET \"http://localhost:8000/tournaments/\" 
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Soporte

Si tienes alguna pregunta o problema:

- 🐛 Reporta bugs en [Issues](https://github.com/tu-usuario/tournament-api/issues)
- 💡 Sugiere nuevas características en [Issues](https://github.com/tu-usuario/tournament-api/issues)
- 📧 Contacto directo: tu-email@example.com

---

⭐ ¡No olvides dar una estrella al proyecto si te ha sido útil!
