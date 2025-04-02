import os
import subprocess
import json
import requests
from dotenv import load_dotenv
from pathlib import Path

# Cargar las variables desde el archivo .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configuración del Webhook de Slack y credenciales de ArgoCD desde variables de entorno
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
ARGOCD_USERNAME = os.getenv("ARGOCD_USERNAME", "admin")  # Valor por defecto: "admin"
ARGOCD_PASSWORD = os.getenv("ARGOCD_PASSWORD")
ARGOCD_SERVER = os.getenv("ARGOCD_SERVER", "localhost:8080")

# Validar que las variables sensibles estén configuradas
if not SLACK_WEBHOOK_URL:
    raise ValueError("❌ La variable de entorno SLACK_WEBHOOK_URL no está configurada.")
if not ARGOCD_PASSWORD:
    raise ValueError("❌ La variable de entorno ARGOCD_PASSWORD no está configurada.")

# Función para enviar notificación a Slack
def send_slack_notification(app_name, status, attempts, action=""):
    try:
        message_text = (
            f"```\n"
            f"{'Aplicación':<20} {'Estado':<15} {'Intentos':<10}\n"
            f"{'-' * 50}\n"
            f"{app_name:<20} {status:<15} {attempts:<10}\n"
            f"{'-' * 50}\n"
            f"{action}\n"
            f"```"
        )
        message = {
            "text": f"⚠️ *Estado de la aplicación:*",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message_text
                    }
                }
            ]
        }
        response = requests.post(SLACK_WEBHOOK_URL, json=message)
        response.raise_for_status()
        print(f"📩 Notificación enviada a Slack: {app_name} - {status}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al enviar notificación a Slack: {e}")

# Función para iniciar sesión en ArgoCD
def argocd_login():
    try:
        result = subprocess.run(
            ["argocd", "login", ARGOCD_SERVER, "--username", ARGOCD_USERNAME, "--password", ARGOCD_PASSWORD, "--insecure"],
            capture_output=True, text=True, check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al autenticar en ArgoCD: {e}")
        print(f"Detalles del error: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado al autenticar en ArgoCD: {e}")
        return False

# Función para obtener las aplicaciones de ArgoCD
def get_argocd_apps():
    try:
        result = subprocess.run(
            ["argocd", "app", "list", "--output", "json"],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al obtener la lista de aplicaciones: {e}")
        print(f"Detalles del error: {e.stderr}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error al decodificar la respuesta JSON de ArgoCD: {e}")
        return []
    except Exception as e:
        print(f"❌ Error inesperado al obtener las aplicaciones de ArgoCD: {e}")
        return []

# Función principal
def main():
    try:
        if not argocd_login():
            print("❌ Falló la autenticación en ArgoCD.")
            return

        apps = get_argocd_apps()
        if not apps:
            print("⚠️ No se encontraron aplicaciones en ArgoCD o hubo un error al obtener la lista.")
            return

        attempts = {}

        print("\n📋 Estado actual de las aplicaciones:")
        print(f"{'Aplicación':<20} {'Estado':<15} {'Intentos':<10}")
        print("-" * 50)

        for app in apps:
            try:
                app_name = app.get("metadata", {}).get("name", "Desconocido")
                status = app.get("status", {}).get("health", {}).get("status", "Unknown")
                sync_status = app.get("status", {}).get("sync", {}).get("status", "Unknown")

                if app_name not in attempts:
                    attempts[app_name] = 0

                if status == "Healthy" and sync_status == "Synced":
                    print(f"{app_name:<20} {'Healthy':<15} {'-':<10}")
                elif sync_status == "OutOfSync":
                    print(f"{app_name:<20} {'OutOfSync':<15} {attempts[app_name]:<10}")
                    send_slack_notification(app_name, "OutOfSync", attempts[app_name], "La aplicación está fuera de sincronización.")
                elif status in ["Degraded", "Error"]:
                    print(f"{app_name:<20} {status:<15} {attempts[app_name]:<10}")
                    send_slack_notification(app_name, status, attempts[app_name], "La aplicación tiene problemas.")
                else:
                    print(f"{app_name:<20} {'Unknown':<15} {'-':<10}")
            except Exception as e:
                print(f"❌ Error al procesar la aplicación {app.get('metadata', {}).get('name', 'Desconocido')}: {e}")

        print("-" * 50)
    except Exception as e:
        print(f"❌ Error inesperado en la ejecución principal: {e}")

if __name__ == "__main__":
    main()