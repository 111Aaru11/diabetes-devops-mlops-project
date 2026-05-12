pipeline {
    agent any

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/111Aaru11/diabetes-devops-mlops-project.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t diabetes-app .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 5001:5000 --name diabetes-container diabetes-app'
            }
        }

    }
}