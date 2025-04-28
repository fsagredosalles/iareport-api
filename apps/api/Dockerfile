FROM python:3.13-slim

WORKDIR /app

# Copiar dependencias
COPY pyproject.toml poetry.lock ./

# Instalar Poetry y dependencias
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# Copiar código fuente
COPY . .

# Configurar variables de entorno
ENV DATABASE_URL=sqlite:///./iareport.db
ENV DEBUG=False

# Exponer el puerto y ejecutar la API
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0"]