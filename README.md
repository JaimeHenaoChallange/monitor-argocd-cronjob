# Monitor ArgoCD CronJob

This project is designed to monitor ArgoCD applications and send notifications to Slack. It utilizes a Kubernetes CronJob to run a Python script at specified intervals, ensuring that the status of applications is regularly checked and reported.

## Project Structure

The project is organized as follows:

```
monitor-argocd-cronjob
├── charts
│   └── monitor-argocd
│       ├── Chart.yaml          # Metadata about the Helm chart
│       ├── values.yaml         # Default configuration values for the Helm chart
│       ├── templates
│       │   ├── cronjob.yaml     # Defines the Kubernetes CronJob resource
│       │   ├── deployment.yaml   # Defines the Kubernetes Deployment resource
│       │   ├── serviceaccount.yaml # Defines the Kubernetes ServiceAccount
│       │   └── _helpers.tpl      # Helper templates for the Helm chart
├── src
│   └── monitor_argocd.py        # Python script for monitoring ArgoCD applications
├── .github
│   └── workflows
│       └── ci-cd.yaml           # GitHub Actions workflow for CI/CD
├── Dockerfile                    # Instructions for building the Docker image
├── .dockerignore                 # Files to ignore when building the Docker image
├── requirements.txt              # Python dependencies required by the script
├── helmfile.yaml                 # Helm releases and their configurations
└── README.md                     # Documentation for the project
```

## Setup Instructions

1. **Clone the Repository**: 
   Clone this repository to your local machine.

   ```
   git clone <repository-url>
   cd monitor-argocd-cronjob
   ```

2. **Install Dependencies**: 
   Ensure you have Python and pip installed, then install the required Python packages.

   ```
   pip install -r requirements.txt
   ```

3. **Build the Docker Image**: 
   Build the Docker image for the application.

   ```
   docker build -t <your-dockerhub-username>/monitor-argocd:latest .
   ```

4. **Deploy to Kubernetes**: 
   Use Helm to deploy the CronJob and other resources to your Kubernetes cluster.

   ```
   helm install monitor-argocd charts/monitor-argocd
   ```

5. **Configure Slack Webhook**: 
   Set up your Slack webhook URL in the environment variables to enable notifications.

## Usage

- The CronJob is configured to run every minute for testing purposes. Once verified, it can be adjusted to run every five minutes.
- The Python script will monitor the status of ArgoCD applications and send notifications to Slack based on their health and sync status.
- You can manually trigger the deployment if needed.

## CI/CD Automation

The project includes a GitHub Actions workflow that automates the following processes:

- Building the Docker image
- Pushing the image to Docker Hub
- Updating the Helm chart in the GitHub repository

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.