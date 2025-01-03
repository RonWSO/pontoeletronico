FROM python:3.13.1-slim-bookworm

# Cria o diretório de trabalho
WORKDIR /app

COPY . .

# update e instala pkg-config para poder utilizar mysql
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev build-essential pkg-config  \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y gcc && apt-get install -y locales && \
    sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen \
    && locale-gen

# da upgrade no pip e instala as dependências
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV $(cat .env | xargs)

# Define a porta de escuta
EXPOSE 8000

# executa a aplicação
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]