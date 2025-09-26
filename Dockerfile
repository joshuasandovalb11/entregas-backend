# Dockerfile (Versión Final y Simplificada)

# 1. Usar una imagen oficial de Python
FROM python:3.11.9-slim

# 2. Establecer el directorio de trabajo
WORKDIR /app

# 3. Instalar los drivers de Microsoft ODBC
RUN apt-get update && apt-get install -y curl gnupg \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y unixodbc-dev msodbcsql17 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. Instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar SOLO el código de la aplicación (la carpeta 'app')
# a la raíz del directorio de trabajo.
COPY ./app .

# 6. Exponer el puerto y definir el comando de inicio
# Como ahora main.py está en /app/main.py, el comando es más simple.
EXPOSE 8000
CMD ["gunicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]