pipeline {

    agent any

    environment {
        APP_NAME = "task-manager-app"
        IMAGE_NAME = "task-manager-app"
    }

    stages {

        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/SaravanaNani/Devops-Task-Manager.git'
            }
        }

        stage('Python Validation') {
            steps {
                sh '''
                python3 -m py_compile app.py
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                trivy image --severity HIGH,CRITICAL ${IMAGE_NAME}:latest || true
                '''
            }
        }

        stage('Backup Current Image') {
            steps {
                sh '''
                docker image inspect ${IMAGE_NAME}:latest >/dev/null 2>&1 && \
                docker tag ${IMAGE_NAME}:latest ${IMAGE_NAME}:previous || true
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                docker stop ${APP_NAME} || true
                docker rm ${APP_NAME} || true

                docker run -d \
                  --name ${APP_NAME} \
                  --env-file /opt/task-manager/.env \
                  -p 5000:5000 \
                  ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Health Check') {
            steps {
                script {

                    def healthStatus = sh(
                        script: '''
                        sleep 20

                        for i in 1 2 3
                        do
                            curl -f http://localhost:5000/health && exit 0
                            echo "Health check failed. Retrying..."
                            sleep 10
                        done

                        exit 1
                        ''',
                        returnStatus: true
                    )

                    if (healthStatus != 0) {

                        echo "Deployment failed. Starting rollback..."

                        sh '''
                        docker stop task-manager-app || true
                        docker rm task-manager-app || true

                        docker run -d \
                          --name task-manager-app \
                          --env-file /opt/task-manager/.env \
                          -p 5000:5000 \
                          task-manager-app:previous
                        '''

                        error("Rollback executed due to failed health check.")
                    }
                }
            }
        }

        stage('Docker Cleanup') {
            steps {
                sh '''
                docker image prune -f
                docker container prune -f
                '''
            }
        }
    }

    post {

        success {
            echo 'Deployment Successful'
        }

        failure {
            echo 'Deployment Failed and Rollback Executed'
        }

        always {
            cleanWs()
        }
    }
}
