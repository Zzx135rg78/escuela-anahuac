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
   │   SQLite Database    │
   │ (instance/gallery.db)│
   └──────────┬──────────┘
              │
   ┌──────────┴──────────┐
   │   Cloudinary CDN     │
   │ (Opcional imágenes)  │
   └──────────────────────┘
```

## 📂 Estructura principal

| Archivo | Descripción |
|---------|-------------|
| `PRODUCT.md` | Contexto del producto, flujos de usuario |
| `DESIGN.md` | Sistema de diseño completo |
| `templates/` | Plantillas HTML (index, album, admin, login, base) |
| `static/` | CSS, JS, imágenes |
| `app.py` | Aplicación Flask principal con ProxyFix |
| `Dockerfile` | Imagen de la aplicación con Gunicorn |
| `docker-compose.yml` | Servicios: App, Nginx, Certbot |
| `nginx/conf.d/anahuac.conf` | Configuración proxy + ACME challenge |

## 🚀 Despliegue local

### Clonar repositorio
```bash
git clone https://github.com/tuusuario/escuela-anahuac-gallery.git
cd escuela-anahuac-gallery
```

### Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Configurar `.env` con claves y base de datos

### Inicializar DB
```bash
flask init-db
```

### Ejecutar servidor
```bash
flask run
```

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

> ⚠️ **Fotos en Render**: El sistema de archivos es efímero. Para persistencia, integrar **Cloudinary** o **AWS S3** (pendiente).

## Credenciales admin (local)

- Usuario: `admin`
- Contraseña: `admin123` (cambiar con `ADMIN_PASSWORD`)

## Funcionalidades

- Subida múltiple de imágenes con consentimiento obligatorio
- Categorías: Académico, Deportivo, Cultural, General
- Panel admin: aprobar/rechazar/eliminar fotos
- Galería pública solo con fotos aprobadas
- Navegación responsive: navbar desktop + offcanvas móvil
- Base de datos: SQLite (local) / PostgreSQL (Render)

## Próximos pasos

- [ ] Integrar Cloudinary para almacenamiento persistente de fotos
- [ ] Agregar filtros por grado/evento en galería (botones en offcanvas)
- [ ] Mejorar UX móvil: drag-drop upload, vista previa
- [ ] Roles granulares con Flask-Login
- [ ] Tests automatizados