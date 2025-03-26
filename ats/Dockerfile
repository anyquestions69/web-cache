# Используем официальный образ Ubuntu в качестве базового
FROM ubuntu:22.04

# Устанавливаем переменные окружения для избежания интерактивных запросов
ENV DEBIAN_FRONTEND=noninteractive

# Устанавливаем зависимости для сборки ATS
RUN apt-get update && \
    apt-get install -y \
    needrestart \
    curl \
    build-essential \
    libssl-dev \
    libpcre3-dev \
    zlib1g-dev \
    tcl \
    git \
    automake \
    libtool \
    pkg-config \
    tzdata && \ 
    ln -fs /usr/share/zoneinfo/UTC /etc/localtime && \  
    dpkg-reconfigure --frontend noninteractive tzdata  \
    trafficserver



# Копируем конфигурационные файлы (если есть)
COPY records.config /opt/ats/etc/trafficserver/records.config
COPY remap.config /opt/ats/etc/trafficserver/remap.config
COPY cache.config /opt/ats/etc/trafficserver/cache.config
# Открываем порты для ATS
EXPOSE 8080  
EXPOSE 8081  

# Указываем рабочую директорию
WORKDIR /opt/ats

# Запускаем Apache Traffic Server
CMD ["/opt/ats/bin/traffic_server"]