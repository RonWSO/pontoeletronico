FROM mysql:8.0.40-bookworm

RUN apt-get update -y && apt-get install -y tzdata

ENV TZ=America/Fortaleza
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY scripts/init.sql /docker-entrypoint-initdb.d/

# Expose the MySQL port
EXPOSE 3306