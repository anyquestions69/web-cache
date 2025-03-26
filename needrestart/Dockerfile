FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y needrestart nginx && \
    rm -rf /var/lib/apt/lists/*

# Пример: Проверка обновлений при сборке
RUN apt-get update && \
    apt-get upgrade -y && \
    needrestart -b -r a || true  # Игнорировать ошибки

EXPOSE 80
CMD ["needrestart"]