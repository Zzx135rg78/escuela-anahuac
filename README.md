# Escuela Anáhuac – Galería Fotográfica

Aplicación web para gestión y publicación de fotografías escolares con enfoque en accesibilidad, seguridad y diseño impecable.

## 🎯 Arquitectura del sistema

```
        ┌──────────────┐
        │   Usuario    │
        │ (Navegador)  │
        └──────┬───────┘
               │ HTTPS
               ▼
        ┌──────────────┐
        │    NGINX     │
        │ Reverse Proxy│
        └──────┬───────┘
               │ Proxy Pass
               ▼
   ┌──────────────────────────┐
   │      Docker Container    │
   │ ┌──────────────────────┐ │
   │ │      Gunicorn        │ │
   │ │  WSGI Server (4w)    │ │
   │ └──────────┬───────────┘ │
   │            │ WSGI Calls   │
   │            ▼              │
   │     Flask Application     │
   │  (Escuela Anáhuac Gallery)│
   └──────────┬────────────────┘
              │
   ┌──────────┴──────────┐
   │ SQLite / PostgreSQL  │
   │(instance/gallery.db) │
   └──────────┬──────────┘
              │
   ┌──────────┴──────────┐
   │   Cloudinary CDN     │
   │ (fotos persistentes) │
   └──────────────────────┘
```

## 📂 Estructura principal

| Archivo | Descripción |
|---------|-------------|
| `PRODUCT.md` | Contexto del producto, flujos de usuario |
| `DESIGN.md` | Sistema de diseño completo |
| `templates/` | Plantillas HTML (index, álbum, admin, login, apoderados, base) |
| `static/` | Logo e imágenes |
| `apoderados.ejemplo.csv` | Formato de la lista de RUTs (la real `apoderados.csv` no se sube a git) |
| `app.py` | Aplicación Flask principal con ProxyFix |
| `Dockerfile` | Imagen de la aplicación con Gunicorn |
| `docker-compose.yml` | Servicios: App, Nginx, Certbot |
| `nginx/conf.d/anahuac.conf` | Configuración proxy + ACME challenge |
| `render.yaml` | Blueprint para deploy en Render |

## 🗺️ Rutas

| Ruta | Acceso | Descripción |
|------|--------|-------------|
| `/` | Público | Portada + subida (admin) + galería aprobada |
| `/album` | Público | Álbum completo con filtros por categoría |
| `/apoderados` | RUT registrado | Ingreso apoderados (valida DV + lista) |
| `/album-familiar` | Apoderados | Álbum exclusivo para apoderados autorizados |
| `/salir` | Apoderados | Cierra sesión familiar |
| `/login` | Clave compartida | Acceso administración |
| `/admin` | Admin | Subir, aprobar, rechazar y eliminar fotos |

## 🚀 Desarrollo local (Windows)

> Usar siempre el entorno `venv` del proyecto. No usar el Python global.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Variables de entorno (`.env`)

| Variable | Ejemplo | Descripción |
|----------|---------|-------------|
| `FLASK_SECRET_KEY` | `dev-secret...` | Clave de sesiones (cambiar en producción) |
| `ADMIN_USERNAME` | `admin` | Usuario admin (solo valor por defecto) |
| `ADMIN_PASSWORD` | `escuelaanahuac` | **Clave compartida**: cualquier usuario entra con ella |
| `DATABASE_URL` | `sqlite:///instance/gallery.db` | BD (local SQLite, Render PostgreSQL) |
| `CLOUDINARY_CLOUD_NAME` / `_API_KEY` / `_API_SECRET` | — | Obligatorio en Render (disco efímero) |
| `PORT` | `5000` | Puerto del servidor |

### Inicializar DB y correr

```powershell
.\venv\Scripts\python.exe -m flask init-db
.\venv\Scripts\python.exe app.py
```

Abrir `http://127.0.0.1:5000`. Las plantillas recargan solas (`TEMPLATES_AUTO_RELOAD`); cambios en `app.py` exigen reiniciar (`Ctrl+C` y correr de nuevo).

### Lista de apoderados

Copiar `apoderados.ejemplo.csv` a `apoderados.csv` con formato `rut,nombre` (export tipo Lirmi). Sin ese archivo, el ingreso por RUT muestra aviso de "no disponible".

## 🌍 Despliegue en producción (Docker + HTTPS)

### Construir y levantar servicios
```bash
docker-compose up --build -d
```

1. **Push a GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/TU_USUARIO/escuela-anahuac.git
   git push -u origin main
   ```

2. **En Render Dashboard** → New Blueprint Instance → Conecta el repo → Apply

3. **Variables de entorno en Render** (auto-provisionadas + manuales):
   - `DATABASE_URL` → PostgreSQL (auto)
   - `FLASK_SECRET_KEY` → generar string aleatorio
   - `ADMIN_PASSWORD` → contraseña segura

4. **URL final**: `https://escuela-anahuac.onrender.com`

> Fotos en Render: el disco es efímero, por eso las imágenes van a **Cloudinary** (ya integrado).

## Credenciales admin (local)

- Usuario: cualquiera (se usa `admin` por defecto)
- Contraseña: `escuelaanahuac` (cambiar con `ADMIN_PASSWORD`)

## Funcionalidades

- Subida múltiple de imágenes con consentimiento obligatorio
- Categorías: Académico, Deportivo, Cultural, General
- Panel admin: aprobar/rechazar/eliminar fotos
- Galería pública solo con fotos aprobadas
- Álbum familiar con acceso por RUT de apoderado (valida dígito verificador + lista)
- Protección: sin descarga con clic derecho, lightbox
- Base de datos: SQLite (local) / PostgreSQL (Render)

## ✅ Checklist de producción

- [ ] Variables de entorno configuradas
- [ ] Base de datos inicializada
- [ ] Cloudinary configurado (Render)
- [ ] `apoderados.csv` real cargado (fuera de git)
- [ ] Certificado SSL activo
- [ ] App accesible en https://tu-dominio.com

## 📜 Créditos

- **Proyecto**: Escuela Anáhuac Photo Gallery
- **Framework**: Flask + Gunicorn
- **Infraestructura**: Docker, Nginx, Certbot / Render
- **Diseño**: Principios Impeccable
