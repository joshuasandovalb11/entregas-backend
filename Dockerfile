# Dockerfile

# 1. Usar una imagen oficial de Python como base
FROM python:3.11.9-slim

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Instalar los drivers de Microsoft ODBC (¡LA PARTE CLAVE!)
# Aquí sí tenemos permisos para instalar lo que necesitemos.
RUN apt-get update && apt-get install -y curl gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y unixodbc-dev msodbcsql17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. Instalar las dependencias de Python
# Copiamos solo el requirements.txt primero para aprovechar el cache de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar el resto del código de tu aplicación
# Asume que tu código está en una carpeta 'app' y otros archivos en la raíz
COPY . .

# 6. Exponer el puerto y definir el comando de inicio
EXPOSE 8000
CMD ["gunicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]