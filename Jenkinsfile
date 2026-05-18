
pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "aarushi1111/diabetes-app:latest"
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/111Aaru11/diabetes-devops-mlops-project.git'
            }
        }

        stage('Terraform Init') {
            steps {
                dir('terraform') {
                    bat 'terraform init'
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                dir('terraform') {
                    bat 'terraform apply -auto-approve'
                }
            }
        }        
        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %DOCKER_IMAGE% .'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    bat 'docker login -u %DOCKER_USER% -p %DOCKER_PASS%'
                    bat 'docker push %DOCKER_IMAGE%'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f k8s/deployment.yaml'
                bat 'kubectl apply -f k8s/service.yaml'
            }
        }
    }
}
// pipeline {
//     agent any

//     stages {

//         stage('Clone Repository') {
//             steps {
//                 git branch: 'main',
//                 url: 'https://github.com/111Aaru11/diabetes-devops-mlops-project.git'
//             }
//         }

//         stage('Build Docker Image') {
//             steps {
//                 bat 'docker build -t diabetes-app .'
//             }
//         }

//         stage('Run Docker Container') {
//             steps {
//                 bat '''
//                 docker rm -f diabetes-container || exit 0
//                 docker run -d -p 5001:5000 --name diabetes-container diabetes-app
//                 '''
//             }
//         }

//     }
// }