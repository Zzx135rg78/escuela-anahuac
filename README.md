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

### Obtener certificado SSL
```bash
docker-compose run --rm certbot certonly --webroot -w /var/www/certbot -d tu-dominio.com
```

### Actualizar `nginx/conf.d/anahuac.conf` con bloque HTTPS

### Reiniciar Nginx
```bash
docker-compose restart nginx
```

## ✅ Checklist de producción

- [ ] Variables de entorno configuradas
- [ ] Base de datos inicializada
- [ ] Certificado SSL activo
- [ ] App accesible en https://tu-dominio.com

## 📜 Créditos

- **Proyecto**: Escuela Anáhuac Photo Gallery
- **Framework**: Flask + Gunicorn
- **Infraestructura**: Docker, Nginx, Certbot
- **Diseño**: Principios Impeccable