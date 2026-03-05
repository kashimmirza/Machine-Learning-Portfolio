FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
# gnupg2 and curl are for installing MS SQL ODBC Driver
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    gnupg2 \
    libpq-dev \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Install ODBC Driver for SQL Server
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
