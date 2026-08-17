# Proyecto Anahuac - Automatización de Instagram

Este proyecto contiene un ejemplo básico para organizar fotos y preparar una publicación automática en la cuenta de Instagram de la escuela.

## Estructura

- `photos/` - Carpeta donde debes colocar las fotos que quieres publicar.
- `instagram_upload.js` - Script de ejemplo para publicar las fotos en Instagram.
- `javascript.js` - Archivo vacío por ahora; puedes usarlo para funciones del frontend si deseas agregar una página web más adelante.

## Instrucciones rápidas

1. Coloca las imágenes en `photos/`.
2. Abre `instagram_upload.js` y reemplaza:
   - `INSTAGRAM_USER_ID`
   - `ACCESS_TOKEN`
   - `IMAGE_URL_BASE`
3. Asegúrate de que `IMAGE_URL_BASE` apunte a una URL pública donde se puedan ver las imágenes.
4. Ejecuta el script:

```bash
deno run -A instagram_upload.js
```

## Qué necesitas para Instagram

- Cuenta de Instagram Business o Creator.
- Una aplicación configurada en Meta Developer Portal.
- Token de acceso válido para Instagram Graph API.
- `IG User ID` de la cuenta de Instagram.

## Nota técnica

El script usa el flujo de Instagram Graph API que crea un objeto de media y luego publica ese contenido.

En este ejemplo, las fotos se publican a partir de una URL pública (`image_url`). Si tus fotos están en el equipo, el paso ideal es que primero las subas a un servidor del colegio o a un servicio de almacenamiento con URL pública.

## Aplicación Flask disponible

Esta versión ahora incluye una aplicación Flask para cargar fotos con consentimientos, revisar el contenido y publicar la galería aprobada.

### Archivos principales

- `app.py` — aplicación Flask principal.
- `templates/` — vistas HTML con Bootstrap 5.
- `photos/` — carpeta de almacenamiento de imágenes.
- `requirements.txt` — dependencias para instalar.

### Cómo ejecutar

1. Crea un entorno virtual:

```bash
python -m venv venv
```

2. Activa el entorno:

```bash
venv\Scripts\activate
```

3. Instala dependencias:

```bash
pip install -r requirements.txt
```

4. Inicializa la base de datos:

```bash
flask init-db
```

5. Ejecuta la aplicación:

```bash
flask run
```

6. Abre `http://127.0.0.1:5000` en el navegador.

### Usuario administrador

- Usuario: `admin`
- Contraseña: `admin123`

Puedes cambiar estas credenciales con las variables de entorno `ADMIN_USERNAME` y `ADMIN_PASSWORD`.

### Funcionalidades incluidas

- Subida de múltiples imágenes con confirmación de consentimiento.
- Categorías de contenido (`Académico`, `Deportivo`, `Cultural`, `General`).
- Panel administrativo para aprobar o rechazar fotos.
- Galería pública de fotos aprobadas.

## Ideas para mejorar

- Conectar con una API de redes sociales para publicar imágenes automáticamente.
- Agregar manejo de roles más preciso con `Flask-Login`.
- Añadir carga desde dispositivos móviles y previsualización antes de enviar.
- Implementar un flujo de aprobación con estados `pendiente`, `aprobado`, `publicado`.
