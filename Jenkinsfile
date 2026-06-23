pipeline {

    agent any

    options {
        timeout(time: 20, unit: 'MINUTES')

        buildDiscarder(logRotator(
            numToKeepStr: '20'
        ))
    }

    environment {
        APP_NAME = "task-manager-app"
        IMAGE_NAME = "task-manager-app"
        DEPLOYMENT_FAILED = "false"
        ROLLBACK_PERFORMED = "false"
    }

    stages {

        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Source Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/SaravanaNani/Devops-Task-Manager.git'
            }
        }

        stage('Code Validation') {
            steps {
                sh '''
                python3 -m py_compile app.py
                '''
            }
        }

        stage('Build Candidate Image') {
            steps {
                sh '''
                docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .
                '''
            }
        }

        stage('Security Scan (Trivy)') {
            steps {
                sh '''
                trivy image --severity HIGH,CRITICAL ${IMAGE_NAME}:${BUILD_NUMBER} || true
                '''
            }
        }

        stage('Deploy Candidate Release') {
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

        stage('Verify Application Health') {
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

                        currentBuild.result = 'UNSTABLE'
                        env.DEPLOYMENT_FAILED = "true"

                    } else {

                        echo "Health verification passed."

                    }
                }
            }
        }

        stage('Rollback To Stable Release') {

            when {
                expression {
                    return env.DEPLOYMENT_FAILED == "true"
                }
            }

            steps {

                script {

                    echo "Health verification failed."

                    sh '''
                    docker stop ${APP_NAME} || true
                    docker rm ${APP_NAME} || true
                    '''

                    def stableExists = sh(
                        script: '''
                        docker image inspect ${IMAGE_NAME}:stable >/dev/null 2>&1
                        ''',
                        returnStatus: true
                    )

                    if (stableExists == 0) {

                        echo "Stable image found. Rolling back..."

                        sh '''
                        docker run -d \
                          --name ${APP_NAME} \
                          --env-file /opt/task-manager/.env \
                          -p 5000:5000 \
                          ${IMAGE_NAME}:stable
                        '''

                        env.ROLLBACK_PERFORMED = "true"

                        echo "Rollback completed successfully."

                    } else {

                        echo "No stable image found."
                        echo "This appears to be the first deployment."
                        echo "Candidate image retained for troubleshooting."

                    }
                }
            }
        }

        stage('Promote Release To Stable') {

            when {
                expression {
                    return env.DEPLOYMENT_FAILED != "true"
                }
            }

            steps {

                echo "Health verification passed. Promoting release to stable."

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

                echo "Image cleanup completed."
            }
        }

        stage('Docker Housekeeping') {
            steps {

                sh '''
                docker container prune -f || true
                docker builder prune -f || true
                '''

                echo "Docker housekeeping completed."
            }
        }
    }

    post {

        success {
            echo 'Deployment completed successfully.'
        }

        unstable {

            script {

                if (env.ROLLBACK_PERFORMED == "true") {

                    currentBuild.result = 'FAILURE'

                    echo 'Deployment failed. Rollback completed successfully.'

                } else {

                    currentBuild.result = 'FAILURE'

                    echo 'Deployment failed. No stable image available for rollback.'

                }
            }
        }

        failure {
            echo 'Pipeline execution failed.'
        }

        always {
            cleanWs()
        }
    }
}
