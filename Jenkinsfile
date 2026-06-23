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
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                trivy image --severity HIGH,CRITICAL ${IMAGE_NAME}:${BUILD_NUMBER} || true
                '''
            }
        }

        stage('Deploy Candidate') {
            steps {
                sh '''
                docker stop ${APP_NAME} || true
                docker rm ${APP_NAME} || true

                docker run -d \
                  --name ${APP_NAME} \
                  --env-file /opt/task-manager/.env \
                  -p 5000:5000 \
                  ${IMAGE_NAME}:${BUILD_NUMBER}
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
                            curl -f --max-time 5 http://localhost:5000/health && exit 0

                            echo "Health check failed. Retrying..."
                            sleep 10
                        done

                        exit 1
                        ''',
                        returnStatus: true
                    )

                    if (healthStatus != 0) {

                        echo "Deployment failed. Checking for stable image..."

                        def stableExists = sh(
                            script: '''
                            docker image inspect ${IMAGE_NAME}:stable >/dev/null 2>&1
                            ''',
                            returnStatus: true
                        )

                        if (stableExists == 0) {

                            echo "Stable image found. Rolling back..."

                            sh '''
                            docker stop ${APP_NAME} || true
                            docker rm ${APP_NAME} || true

                            docker run -d \
                              --name ${APP_NAME} \
                              --env-file /opt/task-manager/.env \
                              -p 5000:5000 \
                              ${IMAGE_NAME}:stable
                            '''

                            error("Rollback executed successfully.")

                        } else {

                            echo "No stable image found."
                            echo "This appears to be the first deployment."
                            echo "Candidate image retained for troubleshooting."

                            error("Deployment failed and rollback is unavailable.")
                        }
                    }
                }
            }
        }

        stage('Promote Stable') {
            steps {
                sh '''
                docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:stable
                '''
            }
        }

        stage('Cleanup Old Images') {
            steps {
                sh '''
                docker images ${IMAGE_NAME} --format "{{.Tag}}" | \
                grep -E '^[0-9]+$' | \
                sort -nr | \
                tail -n +3 | \
                xargs -r -I {} docker rmi ${IMAGE_NAME}:{} || true
                '''
            }
        }

        stage('Docker Cleanup') {
            steps {
                sh '''
                docker container prune -f || true
                docker builder prune -f || true
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

        always {
            cleanWs()
        }
    }
}
