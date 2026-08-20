# Escuela Anahuac - Galería de Fotos Escolares

Aplicación Flask para gestionar y publicar galerías de fotos escolares con panel administrativo.

## Estado actual

- **Instagram integration removida** - ya no hay dependencia de Instagram Graph API
- **Galería pública** con tarjetas responsivas (alturas reducidas en móvil/tablet/desktop)
- **Panel administrativo** para aprobar/rechazar fotos subidas
- **Offcanvas navigation** en móvil (panel lateral deslizable)
- **Despliegue configurado** para Render (Blueprint: Web Service + PostgreSQL)
- **Acceso temporal público** vía cloudflared tunnel

## Estructura del proyecto

```
proyecto Anahuac/
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias Python (incluye gunicorn)
├── render.yaml           # Blueprint de Render (web + PostgreSQL)
├── .gitignore            # Excluye venv, DB local, fotos subidas
├── photos/               # Carpeta de uploads (ephemeral en Render)
│   └── .gitkeep
├── static/
│   └── logo.png
└── templates/
    ├── base.html         # Layout base con navbar + offcanvas
    ├── index.html        # Galería pública
    ├── admin.html        # Panel administrativo
    ├── login.html        # Login admin
    └── upload.html       # Formulario de subida con consentimiento
```

## Ejecución local

```bash
# 1. Entorno virtual
python -m venv .venv
.venv\Scripts\activate

# 2. Dependencias
pip install -r requirements.txt

# 3. Variables de entorno (opcional, usa defaults)
set FLASK_SECRET_KEY=dev-secret
set ADMIN_PASSWORD=admin123
set DATABASE_URL=sqlite:///app.db

# 4. Inicializar BD
flask init-db

# 5. Ejecutar
flask run
# o: python app.py
```

Accede a `http://127.0.0.1:5000` (LAN: `http://192.168.104.225:5000`)

## Despliegue en Render (gratis)

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