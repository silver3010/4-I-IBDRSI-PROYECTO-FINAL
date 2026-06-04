# Sistema Web Escolar - Gestión Académica

## Descripción

Sistema web integral para la gestión académica de instituciones educativas. Permite administrar:

- **Alumnos**: Registro, edición y gestión de estudiantes
- **Grupos**: Creación y administración de grupos por semestre y turno
- **Materias**: Catálogo de materias con créditos y horas
- **Docentes**: Registro de maestros y sus especialidades
- **Calificaciones**: Sistema de evaluación con tipos (parcial, final, tarea, participación)
- **Reportes**: Reportes por alumno y por grupo
- **Autenticación**: Sistema de login seguro con roles

## Tecnologías

- **Backend**: Flask 3.0.0
- **ORM**: SQLAlchemy 2.0.23
- **Base de Datos**: MySQL 8.0+
- **Frontend**: HTML5, CSS3, Bootstrap 5.3.0
- **Autenticación**: Werkzeug (Hash de contraseñas)

## Requisitos

- Python 3.8+
- MySQL 8.0+
- pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/EfrenAlexander-Robles/gestion_web_escolar.git
cd gestion_web_escolar/proyecto_escolar
```

### 2. Crear entorno virtual

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requeriments.txt
```

### 4. Configurar base de datos

#### Opción A: Base de datos local

```bash
# En Windows (PowerShell)
$env:DATABASE_URL="mysql+pymysql://usuario:password@localhost:3306/control_escolar"

# En Linux/macOS
export DATABASE_URL="mysql+pymysql://usuario:password@localhost:3306/control_escolar"
```

#### Opción B: Usar archivo .env

Copia `.env.example` a `.env` y actualiza los valores:

```bash
cp .env.example .env
```

Edita `.env`:

```
DATABASE_URL=mysql+pymysql://usuario:password@localhost:3306/control_escolar
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=tu-clave-secreta
```

### 5. Crear base de datos

```bash
mysql -u root -p < database/schema.sql
```

### 6. Ejecutar la aplicación

```bash
python run.py
```

La aplicación estará disponible en: **http://127.0.0.1:5000**

## Uso

### Acceso Inicial

**Email:** `admin@school.local`  
**Contraseña:** Debe ser actualizada en la base de datos

Para cambiar la contraseña del admin, ejecuta en MySQL:

```sql
UPDATE usuarios SET password = 'tu-nueva-contraseña' WHERE email = 'admin@school.local';
```

### Roles

- **Admin**: Acceso completo al sistema
- **Docente**: Gestionar calificaciones y ver reportes
- **Control Escolar**: Gestionar alumnos, grupos y materias

## Estructura del Proyecto

```
proyecto_escolar/
├── app/
│   ├── models/              # Modelos de datos
│   │   ├── usuario.py
│   │   ├__ alumno.py
│   │   ├── grupo.py
│   │   ├── materia.py
│   │   ├── docente.py
│   │   ├── planeacion.py
│   │   ├── calificacion.py
│   │   ├── turno.py
│   │   ├└─ __init__.py
│   ├── routes/              # Rutas y vistas
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── alumnos.py
│   │   ├── grupos.py
│   │   ├── materias.py
│   │   ├── docentes.py
│   │   ├── calificaciones.py
│   │   ├└─ test.py
│   ├── templates/           # Plantillas HTML
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── alumnos/
│   │   ├── grupos/
│   │   ├── materias/
│   │   ├── docentes/
│   │   ├└─ calificaciones/
│   └─ __init__.py
├── database/
│   └─ schema.sql             # Script de base de datos
├── .env.example
├── .gitignore
├── config.py
├── create_key.py
├── requeriments.txt
├── run.py
├└─ README.md
```

## Características Principales

### 📚 Dashboard
- Estadísticas generales del sistema
- Promedio general de calificaciones
- Estudiantes con bajo rendimiento
- Accesos rápidos a funciones principales

### 👤 Gestión de Alumnos
- CRUD completo
- Filtrado por grupo
- Visualización de calificaciones
- Cálculo automático de promedios

### 👥 Gestión de Grupos
- Creación por semestre y turno
- Vista de alumnos por grupo
- Estadísticas de desempeño

### 📚 Gestión de Materias
- Catálogo de materias
- Créditos y horas semanales
- Descripciones detalladas

### 🐺 Gestión de Docentes
- Registro de maestros
- Especialidades
- Contacto directo

### ⭐ Sistema de Calificaciones
- Tipos: Parcial, Final, Tarea, Participación
- Escala 0-10
- Cálculo automático de promedios
- Estados (Aprobado/Reprobado)

### 📈 Reportes
- Reporte por alumno
- Reporte por grupo
- Imprimibles en PDF

## API REST

El sistema incluye endpoints JSON para integraciones:

```
GET  /alumnos/api/listar
GET  /grupos/api/listar
GET  /materias/api/listar
GET  /docentes/api/listar
GET  /calificaciones/api/listar
```

## Seguridad

- Contraseñas hasheadas con Werkzeug
- Sesión con cookies seguras
- Validaciones server-side
- Protección contra CSRF (a implementar)
- Control de acceso por rol

## Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'flask'"

```bash
pip install -r requeriments.txt
```

### Error: "Error de conexión a base de datos"

Verifica:
1. MySQL está ejecutándose
2. Credenciales correctas en DATABASE_URL
3. Base de datos existe

### Error: "Table doesn't exist"

Ejecuta el schema SQL:

```bash
mysql -u root -p control_escolar < database/schema.sql
```

## Roadmap Futuro

- [ ] Exportar reportes a PDF
- [ ] Autenticación con LDAP
- [ ] Médulo de asistencia
- [ ] Notificaciones por email
- [ ] Sistema de tareas
- [ ] Calificaciones con rúbrica
- [ ] API GraphQL
- [ ] Aplicación móvil

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para detalles.

## Autor

**Efrén Alexander Robles Gómez**  
Estudiante de 4to I  
Centro de Bachillerato Tecnológico Industrial y de Servicios No. 246  

## Contacto

- GitHub: [@EfrenAlexander-Robles](https://github.com/EfrenAlexander-Robles)
- Email: efren.robles@cbtis246.edu.mx

---

**Última actualización:** 27 de Mayo de 2026
