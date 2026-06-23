pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                git 'https://github.com/SaravanaNani/Devops-Task-Manager.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t task-manager-app:${BUILD_NUMBER} .'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                docker stop task-manager-app || true
                docker rm task-manager-app || true

                docker run -d \
                --name task-manager-app \
                -p 5000:5000 \
                --env-file .env \
                task-manager-app:${BUILD_NUMBER}
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                sleep 20

                curl -f http://localhost:5000/health
                '''
            }
        }
    }
}
