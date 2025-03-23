# Используем официальный образ Ubuntu в качестве базового
FROM ubuntu:22.04

# Устанавливаем переменные окружения для избежания интерактивных запросов
ENV DEBIAN_FRONTEND=noninteractive

# Устанавливаем зависимости для сборки ATS
RUN apt-get update && \
    apt-get install -y \
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
    dpkg-reconfigure --frontend noninteractive tzdata  

# Клонируем исходный код Apache Traffic Server
RUN git clone https://github.com/apache/trafficserver.git /ats-src

# Переходим в директорию с исходным кодом
WORKDIR /ats-src

# Выбираем версию (например, 9.2.x)
RUN git checkout 9.0.x

# Собираем и устанавливаем ATS
RUN autoreconf -if && \
    ./configure --prefix=/opt/ats && \
    make && \
    make install

# Копируем конфигурационные файлы (если есть)
COPY records.config /opt/ats/etc/trafficserver/records.config
COPY remap.config /opt/ats/etc/trafficserver/remap.config

# Открываем порты для ATS
EXPOSE 8080  
EXPOSE 8081  

# Указываем рабочую директорию
WORKDIR /opt/ats

# Запускаем Apache Traffic Server
CMD ["/opt/ats/bin/traffic_server"]