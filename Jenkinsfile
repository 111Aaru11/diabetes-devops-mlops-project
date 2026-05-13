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
                bat 'docker build -t diabetes-app -f docker/Dockerfile .'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat '''
                docker rm -f diabetes-container || exit 0
                docker run -d -p 5001:5000 --name diabetes-container diabetes-app
                '''
            }
        }

    }
}