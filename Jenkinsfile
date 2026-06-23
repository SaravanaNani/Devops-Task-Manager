pipeline {
    agent any

    environment {
        APP_NAME = "task-manager-app"
        IMAGE_NAME = "task-manager-app"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/SaravanaNani/Devops-Task-Manager.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t task-manager-app:${BUILD_NUMBER} .
                docker tag task-manager-app:${BUILD_NUMBER} task-manager-app:latest
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                docker stop task-manager-app || true
                docker rm task-manager-app || true

                docker run -d \
                  --name task-manager-app \
                  --env-file /opt/task-manager/.env \
                  -p 5000:5000 \
                  task-manager-app:latest
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                sleep 20

                for i in 1 2 3
                do
                    curl -f http://localhost:5000/health && exit 0
                    echo "Health check failed. Retrying..."
                    sleep 10
                done

                exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment Successful'
        }

        failure {
            echo 'Deployment Failed'
        }
    }
}
