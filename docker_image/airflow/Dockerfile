FROM apache/airflow:2.7.3-python3.9

# Cài đặt openjdk-11-jdk
USER root
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Thiết lập biến môi trường cho Java
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Trở về người dùng airflow
USER airflow


RUN pip install apache-airflow==2.7.3