# Usar una imagen oficial de Python como base
FROM python:3.8-slim

# Establecer un directorio de trabajo
WORKDIR /usr/src/app

# Instalar dependencias
# Copiar 'requirements.txt' antes de otros archivos para aprovechar la cache de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el contenido del directorio actual al contenedor
COPY . .

# Exponer el puerto que utiliza FastAPI (por defecto es 8000)
EXPOSE 8000

# Definir el comando para correr la aplicación
CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8000"]