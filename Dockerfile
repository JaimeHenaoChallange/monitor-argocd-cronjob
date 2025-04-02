# Usar una imagen base más completa
FROM python:3.9

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema y la CLI de ArgoCD
RUN apt-get update && apt-get install -y curl && \
    curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64 && \
    chmod +x /usr/local/bin/argocd

# Copiar los archivos necesarios
COPY src/monitor_argocd.py /app/
COPY requirements.txt /app/

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto
CMD ["python", "monitor_argocd.py"]