🚀 Automated MLOps Pipeline for Diabetes Prediction using DevOps Tools
📌 Project Overview

This project demonstrates an end-to-end MLOps pipeline for a Diabetes Prediction System by integrating Machine Learning with modern DevOps practices.

The objective was not only to build a Machine Learning model but also to automate its deployment, monitoring, and management using industry-standard DevOps tools such as Docker, Jenkins, Terraform, Ansible, Kubernetes, Prometheus, and Grafana.

The complete setup is implemented locally using Minikube Kubernetes Cluster, Docker Desktop, Local Jenkins, and WSL-based Ansible.

🎯 Objectives
Develop a Machine Learning model for diabetes prediction.
Deploy the model as a Flask web application.
Containerize the application using Docker.
Implement CI/CD using Jenkins.
Provision infrastructure using Terraform.
Automate configuration using Ansible.
Deploy containers on Kubernetes.
Monitor application and cluster health using Prometheus and Grafana.
Automate deployments through GitHub Webhooks.
🏗️ System Architecture
Developer
    │
    ▼
GitHub Repository
    │
    ▼
GitHub Webhook
    │
    ▼
ngrok
    │
    ▼
Jenkins CI/CD Pipeline
    │
    ├── Terraform
    ├── Docker Build
    ├── Docker Push
    ├── Ansible Playbook
    └── Kubernetes Deployment
            │
            ▼
      Minikube Cluster
            │
            ▼
      Diabetes Prediction App
            │
            ▼
 Prometheus Monitoring
            │
            ▼
    Grafana Dashboards
🧠 Machine Learning Workflow
Dataset Collection
Data Preprocessing
Feature Engineering
ANN Model Training using PyTorch
Model Evaluation
Model Serialization
Flask Integration
Deployment Automation
🛠️ Technologies Used
Category	Tools
Machine Learning	PyTorch, Pandas, NumPy, Scikit-Learn
Backend	Flask
Version Control	Git, GitHub
Containerization	Docker
Image Registry	DockerHub
CI/CD	Jenkins
Infrastructure as Code	Terraform
Configuration Management	Ansible
Container Orchestration	Kubernetes
Local Kubernetes	Minikube
Monitoring	Prometheus
Visualization	Grafana
Webhook Exposure	ngrok
📂 Project Workflow
1. Source Code Management

Git and GitHub are used for version control and collaboration.

git add .
git commit -m "commit message"
git push origin main
2. Docker Containerization

Build Docker Image:

docker build -t aarushi1111/diabetes-app:latest .

Push Image:

docker push aarushi1111/diabetes-app:latest
3. Jenkins CI/CD Pipeline

Pipeline Stages:

Clone Repository
Terraform Init
Terraform Apply
Docker Build
Docker Push
Run Ansible Playbook
Kubernetes Deployment

Jenkins automatically triggers on every GitHub push using Webhooks.

4. Terraform Integration

Terraform is used to automate infrastructure provisioning.

Commands:

terraform init
terraform plan
terraform apply
5. Ansible Automation

Ansible is integrated with Jenkins through WSL.

Playbook Execution:

ansible-playbook -i inventory playbook.yml

Current implementation validates successful automation and integration with Jenkins.

6. Kubernetes Deployment

Deployment and Service are managed through Kubernetes.

Commands:

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

View Pods:

kubectl get pods

Restart Deployment:

kubectl rollout restart deployment diabetes-deployment
7. Minikube

Local Kubernetes Cluster Setup:

minikube start

Access Application:

minikube service diabetes-service
📊 Monitoring & Observability
Prometheus

Prometheus continuously collects metrics from:

Kubernetes Cluster
Nodes
Pods
Containers

Access:

kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090:9090

Prometheus UI:

http://localhost:9090
Grafana

Grafana visualizes metrics collected by Prometheus.

Monitored Metrics:

CPU Usage
Memory Usage
Pod Health
Node Status
Cluster Metrics
Container Metrics

Access:

kubectl port-forward svc/monitoring-grafana 3000:80

Grafana UI:

http://localhost:3000
🔄 Complete CI/CD Workflow
Code Push
    │
    ▼
GitHub Webhook
    │
    ▼
ngrok
    │
    ▼
Jenkins Trigger
    │
    ▼
Terraform
    │
    ▼
Docker Build
    │
    ▼
DockerHub Push
    │
    ▼
Ansible
    │
    ▼
Kubernetes Deployment
    │
    ▼
Prometheus Monitoring
    │
    ▼
Grafana Dashboard
🚧 Challenges Faced
Jenkins + WSL Integration
Passwordless Sudo Configuration for Ansible
Docker Image Caching Issues
Kubernetes Stale Image Updates
ngrok Webhook Configuration
Long Docker Build Times
Minikube Networking Issues
Monitoring Stack Configuration
✅ Project Outcomes
Automated end-to-end deployment pipeline.
Reduced manual deployment effort.
Containerized Machine Learning application.
Infrastructure provisioning through Terraform.
Kubernetes-based orchestration and deployment.
Automated Jenkins CI/CD workflow.
Real-time monitoring using Prometheus and Grafana.
Production-style local MLOps environment.
🔮 Future Enhancements
AWS / Azure / GCP Deployment
Advanced Ansible Configuration Management
ML Model Retraining Pipeline
Model Versioning
Auto Scaling
Security Hardening
Alerting through Grafana & Prometheus
👩‍💻 Author

Aarushi

Final Year Engineering Student
Data Science | AI | DevOps | MLOps Enthusiast

⭐ If you found this project useful, consider giving it a star!
