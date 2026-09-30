import csv
import os
import uuid
from functools import wraps
from pathlib import Path
from datetime import datetime, timezone
try:
    from dotenv import load_dotenv
    load_dotenv()  # carga .env para que python app.py y gunicorn vean las correcciones
except ImportError:
    pass  # python-dotenv no instalado: se usan variables de entorno del sistema

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, session  # componentes core de Flask
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user  # utilidades de autenticación
from flask_sqlalchemy import SQLAlchemy  # ORM para base de datos SQLite
from werkzeug.utils import secure_filename  # sanitiza nombres de archivo para evitar traversal
from werkzeug.middleware.proxy_fix import ProxyFix  # para manejar headers de proxy reverso
import cloudinary  # SDK de Cloudinary para almacenamiento de imágenes
import cloudinary.uploader  # utilidad para subir archivos a Cloudinary

BASE_DIR = Path(__file__).resolve().parent  # directorio base del proyecto (donde está app.py)
UPLOAD_FOLDER = BASE_DIR / "photos"  # carpeta donde se guardarán las fotos subidas (fallback local)
INSTANCE_FOLDER = BASE_DIR / "instance"  # carpeta para BD en Docker
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}  # extensiones permitidas para subida
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")  # usuario admin desde variable de entorno (default: admin)
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "escuelaanahuac")  # contraseña admin desde variable de entorno (default: escuelaanahuac)
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "cambiar_por_una_clave_segura")  # clave secreta para sesiones
# Ruta única de BD para evitar doble archivo (root app.db vs instance/gallery.db)
DB_PATH = INSTANCE_FOLDER / "gallery.db"
DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{DB_PATH}")  # URI de BD
# Normaliza sqlite relativo contra BASE_DIR: Flask-SQLAlchemy resuelve rutas
# relativas contra instance_path (quedaría instance/instance/... inexistente)
if DATABASE_URL.startswith("sqlite:///") and not DATABASE_URL.startswith("sqlite:////"):
    _rel = DATABASE_URL[len("sqlite:///"):]
    if ":memory:" not in _rel and not os.path.isabs(_rel):
        DATABASE_URL = f"sqlite:///{(BASE_DIR / _rel).resolve()}"

# Cloudinary config (requerido en Render para persistencia de fotos)
CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET")

if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
        secure=True
    )

app = Flask(__name__)  # crea la aplicación Flask
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL.replace("postgres://", "postgresql://")  # fix para PostgreSQL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # desactiva tracking de modificaciones para ahorrar memoria
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)  # configura carpeta de subida para Flask
app.config["TEMPLATES_AUTO_RELOAD"] = True  # recarga plantillas al refrescar (sin reiniciar servidor)

if not UPLOAD_FOLDER.exists():  # si la carpeta photos no existe
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)  # la crea (incluyendo padres si hiciera falta)

if not INSTANCE_FOLDER.exists():  # si la carpeta instance no existe (Docker)
    INSTANCE_FOLDER.mkdir(parents=True, exist_ok=True)  # la crea

db = SQLAlchemy(app)  # inicializa SQLAlchemy con la app
login_manager = LoginManager(app)  # inicializa Flask-Login con la app
login_manager.login_view = "login"  # endpoint al que redirigir cuando se requiere login
login_manager.login_message_category = "warning"  # categoría del mensaje flash al requerir login
login_manager.login_message = "Inicia sesión como administrador para acceder a este panel."  # mensaje flash al requerir login


def allowed_file(filename):  # valida si la extensión del archivo está permitida
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS  # true si tiene punto y extensión en lista permitida


class AdminUser(UserMixin):  # modelo de usuario admin para Flask-Login
    def __init__(self, username):  # constructor recibe username
        self.id = username  # Flask-Login requiere atributo id


@login_manager.user_loader  # decorador para cargar usuario desde session
def load_user(user_id):  # callback que recibe el id almacenado en session
    if user_id:  # si hay user_id en la sesión
        return AdminUser(user_id)  # retorna instancia de AdminUser
    return None  # sino retorna None (usuario no encontrado)


def save_image(file):  # sube archivo a Cloudinary (o guarda local si no configurado)
    filename = secure_filename(file.filename)  # sanitiza nombre original
    if not filename or not allowed_file(filename):  # si nombre vacío o extensión no permitida
        return None, None  # rechaza el archivo

    # Extraer extensión original
    ext = filename.rsplit(".", 1)[1].lower() if "." in filename else "jpg"
    # Generar ID único para evitar conflictos
    unique_id = str(uuid.uuid4())[:8]
    safe_filename = f"{unique_id}.{ext}"

    # Guardar local primero (siempre funciona)
    target = UPLOAD_FOLDER / safe_filename

    file.save(target)
    local_url = url_for('uploaded_file', filename=safe_filename, _external=True)

    # Si Cloudinary está configurado, subir allí también
    if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
        try:
            result = cloudinary.uploader.upload(
                target,
                folder="escuela-anahuac",
                resource_type="image",
                overwrite=False
            )
            public_id = result.get("public_id")
            secure_url = result.get("secure_url")
            # Eliminar archivo local después de subir a Cloudinary
            if target.exists():
                target.unlink()
            return public_id, secure_url
        except Exception as e:
            print(f"Cloudinary upload failed, using local: {e}")
            return safe_filename, local_url

    # Sin Cloudinary: usar URL local
    return safe_filename, local_url


class Photo(db.Model):  # modelo SQLAlchemy para tabla photos
    __tablename__ = "photos"  # nombre explícito de la tabla
    id = db.Column(db.Integer, primary_key=True)  # PK autoincremental
    cloudinary_public_id = db.Column(db.String(255), nullable=False, unique=True)  # ID público en Cloudinary (único)
    cloudinary_url = db.Column(db.String(500), nullable=False)  # URL segura de la imagen en Cloudinary
    caption = db.Column(db.String(255), nullable=True)  # texto descriptivo opcional
    category = db.Column(db.String(64), nullable=True)  # categoría opcional
    consent = db.Column(db.Boolean, default=False, nullable=False)  # flag consentimiento apoderados
    status = db.Column(db.String(32), nullable=False, default="pending")  # estado: pending/approved/rejected
    uploaded_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))  # timestamp de subida


@app.cli.command("init-db")  # comando CLI: flask init-db
def init_db():  # crea todas las tablas definidas en modelos
    db.create_all()  # crea tablas en BD si no existen
    print("Base de datos inicializada.")  # mensaje de confirmación


def is_valid_admin_password(password):  # valida contraseña contra la configurada
    return bool(password and password.strip() == ADMIN_PASSWORD)  # true si no vacía y coincide (sin espacios extra)


@app.route("/")  # ruta raíz: galería pública
def index():  # vista principal
    photos = Photo.query.filter_by(status="approved").order_by(Photo.uploaded_at.desc()).all()  # fotos aprobadas, más nuevas primero
    pending_count = Photo.query.filter_by(status="pending").count()  # cuenta fotos pendientes para badge
    return render_template("index.html", photos=photos, pending_count=pending_count)  # renderiza plantilla con datos


@app.route("/album")  # álbum público (solo vista, sin descarga)
def album():  # vista del álbum público
    photos = Photo.query.filter_by(status="approved").order_by(Photo.uploaded_at.desc()).all()  # fotos aprobadas
    return render_template("álbum.html", photos=photos)  # renderiza plantilla del álbum


@app.route("/upload", methods=["POST"])  # endpoint para subir fotos (solo POST)
@login_required  # requiere sesión admin
def upload():  # procesa subida múltiple de archivos
    if "photos" not in request.files:  # si no viene campo 'photos' en formulario
        flash("Selecciona al menos una imagen para subir.", "warning")  # mensaje de advertencia
        return redirect(url_for("admin"))  # redirige a panel admin

    files = request.files.getlist("photos")  # lista de archivos subidos (múltiple)
    if not files or files == [None]:  # si lista vacía o solo None
        flash("Selecciona archivos válidos.", "warning")  # mensaje de advertencia
        return redirect(url_for("admin"))  # redirige a panel admin

    caption = request.form.get("caption", "").strip()  # caption del formulario (vacío si no hay)
    category = request.form.get("category", "General")  # categoría del formulario (default: General)
    consent = request.form.get("consent") == "on"  # checkbox consentimiento (true si checked)

    if not consent:  # si no aceptó consentimiento
        flash("Debes confirmar el consentimiento de los apoderados para continuar.", "danger")  # mensaje error
        return redirect(url_for("admin"))  # redirige a panel admin

    uploaded = 0  # contador de archivos subidos exitosamente
    for file in files:  # itera cada archivo
        if file and allowed_file(file.filename):  # si archivo existe y extensión válida
            public_id, cloudinary_url = save_image(file)  # sube a Cloudinary o local
            if public_id and cloudinary_url:  # si se subió correctamente
                photo = Photo(  # crea instancia modelo Photo
                    cloudinary_public_id=public_id,
                    cloudinary_url=cloudinary_url,
                    caption=caption,
                    category=category,
                    consent=True,
                    status="pending",
                )
                db.session.add(photo)  # agrega a sesión BD
                uploaded += 1  # incrementa contador

    if uploaded > 0:  # si se subió al menos uno
        db.session.commit()  # confirma transacción
        flash(f"{uploaded} imagen(es) cargada(s) y en espera de aprobación.", "success")  # mensaje éxito
    else:  # si no se subió ninguno válido
        flash("No se subieron imágenes válidas. Usa JPG, PNG, GIF o WEBP.", "danger")  # mensaje error

    return redirect(url_for("admin"))  # redirige a panel admin


@app.route("/login", methods=["GET", "POST"])  # ruta login: GET muestra form, POST procesa
def login():  # vista de login admin
    if current_user.is_authenticated:  # si ya hay sesión activa
        return redirect(url_for("admin"))  # redirige a panel admin

    if request.method == "POST":  # si es envío de formulario
        username = request.form.get("username", "").strip() or ADMIN_USERNAME  # usuario del form (default: ADMIN_USERNAME)
        password = request.form.get("password", "")  # password del form
        if is_valid_admin_password(password):  # valida solo la contraseña: clave compartida (apoderados)
            user = AdminUser(username)  # crea usuario con el nombre ingresado
            login_user(user)  # inicia sesión (Flask-Login)
            flash("Sesión iniciada como administrador.", "success")  # mensaje éxito
            return redirect(url_for("admin"))  # redirige a panel admin
        flash("Contraseña incorrecta.", "danger")  # mensaje error

    return render_template("login.html")  # renderiza formulario login (GET o POST fallido)


APODERADOS_CSV = BASE_DIR / "apoderados.csv"  # lista tipo Lirmi: rut,nombre (no se sube a git)


def normalizar_rut(rut):  # deja solo dígitos + DV en mayúscula: "12.345.678-5" -> "123456785"
    return (rut or "").upper().replace(".", "").replace("-", "").replace(" ", "")


def digito_verificador(num):  # calcula DV con módulo 11
    s, m = 0, 2
    for d in reversed(num):
        s += int(d) * m
        m = 2 if m == 7 else m + 1
    r = 11 - (s % 11)
    return "0" if r == 11 else "K" if r == 10 else str(r)


def rut_valido(rut):  # valida formato y dígito verificador chileno
    rut = normalizar_rut(rut)
    if len(rut) < 8 or not rut[:-1].isdigit() or not rut[-1].isalnum():
        return False
    return rut[-1] == digito_verificador(rut[:-1])


def cargar_apoderados():  # lee apoderados.csv -> {rut_normalizado: nombre}
    autorizados = {}
    if not APODERADOS_CSV.exists():  # lista aún no cargada (se hará más adelante)
        return autorizados
    with APODERADOS_CSV.open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            rut = normalizar_rut(row.get("rut", ""))
            if rut_valido(rut):  # ignora filas con RUT inválido
                autorizados[rut] = (row.get("nombre", "") or "").strip()
    return autorizados


def apoderado_required(view):  # exige sesión de apoderado con RUT autorizado
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get("apoderado_rut"):  # sin RUT validado
            flash("Ingresa tu RUT de apoderado para ver el álbum familiar.", "warning")
            return redirect(url_for("apoderados"))  # al formulario RUT
        return view(*args, **kwargs)
    return wrapper


@app.route("/logout")  # ruta logout
@login_required  # requiere sesión activa
def logout():  # cierra sesión
    logout_user()  # cierra sesión (Flask-Login)
    flash("Has cerrado sesión.", "info")  # mensaje info
    return redirect(url_for("index"))  # redirige a inicio


@app.route("/apoderados", methods=["GET", "POST"])  # ingreso apoderados con RUT
def apoderados():  # valida RUT contra lista tipo Lirmi
    if session.get("apoderado_rut"):  # si ya ingresó
        return redirect(url_for("album_familiar"))  # va directo al álbum

    if request.method == "POST":  # si envía el formulario
        rut = normalizar_rut(request.form.get("rut", ""))  # normaliza lo ingresado
        autorizados = cargar_apoderados()  # lee lista vigente
        if not autorizados:  # lista aún no cargada
            flash("El registro de apoderados aún no está disponible. Intenta más tarde.", "warning")
        elif not rut_valido(rut):  # formato o DV inválido
            flash("RUT inválido. Revísalo e intenta de nuevo (ej: 12.345.678-5).", "danger")
        elif rut not in autorizados:  # RUT válido pero no registrado
            flash("Este RUT no está registrado. Contacta a la escuela.", "danger")
        else:  # RUT autorizado
            session["apoderado_rut"] = rut  # guarda sesión de apoderado
            session["apoderado_nombre"] = autorizados[rut]  # guarda nombre para saludo
            flash("Bienvenido/a al álbum familiar.", "success")
            return redirect(url_for("album_familiar"))  # entra al álbum

    return render_template("apoderados.html")  # muestra formulario RUT


@app.route("/album-familiar")  # álbum solo para apoderados autorizados
@apoderado_required  # exige RUT validado
def album_familiar():  # reutiliza la vista del álbum con fotos aprobadas
    photos = Photo.query.filter_by(status="approved").order_by(Photo.uploaded_at.desc()).all()
    return render_template("álbum.html", photos=photos)


@app.route("/salir")  # cierra sesión de apoderado
def salir():  # limpia solo la sesión familiar (no toca admin)
    session.pop("apoderado_rut", None)
    session.pop("apoderado_nombre", None)
    flash("Sesión de apoderado cerrada.", "info")
    return redirect(url_for("apoderados"))


@app.route("/admin")  # panel de administración
@login_required  # requiere sesión admin
def admin():  # vista panel admin
    pending = Photo.query.filter_by(status="pending").order_by(Photo.uploaded_at.asc()).all()  # fotos pendientes (más antiguas primero)
    approved = Photo.query.filter_by(status="approved").order_by(Photo.uploaded_at.desc()).all()  # fotos aprobadas (más nuevas primero)
    return render_template(  # renderiza plantilla admin
        "admin.html",
        pending=pending,
        approved=approved,
    )


@app.route("/photo/<int:photo_id>")  # redirige a la URL de Cloudinary (o sirve local)
def photo_file(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    return redirect(photo.cloudinary_url)


@app.route("/uploads/<filename>")  # sirve archivos locales desde la carpeta photos
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.route("/approve/<int:photo_id>", methods=["POST"])  # aprueba foto por ID (solo POST)
@login_required  # requiere sesión admin
def approve(photo_id):  # cambia estado a approved
    photo = Photo.query.get_or_404(photo_id)  # busca foto o 404
    photo.status = "approved"  # actualiza estado
    db.session.commit()  # guarda en BD
    flash(f"Foto '{photo.cloudinary_public_id}' aprobada.", "success")  # mensaje éxito
    return redirect(url_for("admin"))  # redirige a panel


@app.route("/reject/<int:photo_id>", methods=["POST"])  # rechaza foto por ID (solo POST)
@login_required  # requiere sesión admin
def reject(photo_id):  # cambia estado a rejected
    photo = Photo.query.get_or_404(photo_id)  # busca foto o 404
    photo.status = "rejected"  # actualiza estado
    db.session.commit()  # guarda en BD
    flash(f"Foto '{photo.cloudinary_public_id}' rechazada.", "danger")  # mensaje error
    return redirect(url_for("admin"))  # redirige a panel


@app.route("/delete/<int:photo_id>", methods=["POST"])  # elimina foto por ID (solo POST)
@login_required  # requiere sesión admin
def delete(photo_id):  # elimina foto de la BD
    photo = Photo.query.get_or_404(photo_id)  # busca foto o 404
    flash("Foto eliminada.", "warning")  # mensaje
    db.session.delete(photo)  # elimina de BD
    db.session.commit()  # guarda cambios
    return redirect(url_for("admin"))  # redirige a panel


if __name__ == "__main__":  # solo si se ejecuta directamente (no importado)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)  # inicia servidor accesible en red
