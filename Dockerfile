# Imagen base oficial de Python
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias primero (aprovecha caché de capas)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar resto del proyecto
COPY . /app

# Exponer puerto
EXPOSE 8000

# Comando de arranque con Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]