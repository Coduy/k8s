# Use the official Airflow image as a base
FROM apache/airflow:2.6.0

# Install dependencies as root
USER root

# Install msodbcsql18
RUN apt-get update && ACCEPT_EULA=Y apt-get install msodbcsql18 -y

# Install other dependencies (curl, Java, Kerberos, etc.)
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        curl \
        openjdk-11-jdk \
        gcc \
        krb5-user \
        libkrb5-dev && \
    # Download kubectl
    curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl && \
    # Clean up
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch back to airflow user
USER airflow

# Install Python packages for HDFS provider
RUN pip install requests apache-airflow-providers-apache-spark

