pipeline {
    agent any

    environment {
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        DOCKER_REPO = "your-docker-repo/odoo"
        GIT_REPO = "https://github.com/med-las/jenkins-gitops-k8s.git"
        GIT_CREDENTIALS_ID = "github"
    }

    stages {
        stage('Clone repository') {
            steps {
                checkout scm
            }
        }

        stage('Build image') {
            steps {
                script {
                    def app = docker.build("${DOCKER_REPO}:${DOCKER_TAG}")
                }
            }
        }

        stage('Run Docker Compose') {
            steps {
                script {
                    echo "Using Docker tag: ${DOCKER_TAG}"
                    sh "docker-compose up --build -d"
                }
            }
        }

        stage('Test image') {
            steps {
                script {
                    echo "Waiting for Odoo server to be ready..."
                    sleep(time: 30, unit: 'SECONDS') // Adjust the wait time if needed

                    echo "Checking server status"
                    sh "docker exec odoo curl -s http://localhost:8069/web > /dev/null && echo 'Server is running' || echo 'Server is not running'"

                    echo "Listing files in /mnt/extra-addons"
                    sh "docker exec odoo ls /mnt/extra-addons"
                    
                    // Run the test file
                    sh "docker exec odoo python3 /mnt/extra-addons/test.py"
                }
            }
        }

        stage('Stop and Remove Containers') {
            steps {
                script {
                    // Stop and remove containers created by Docker Compose
                    sh 'docker-compose down'
                }
            }
        }

        stage('Push image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
                        def app = docker.image("${DOCKER_REPO}:${DOCKER_TAG}")
                        app.push("${DOCKER_TAG}")
                    }
                }
            }
        }

        stage('Update Kubernetes Deployment') {
            steps {
                script {
                    catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                        withCredentials([usernamePassword(credentialsId: GIT_CREDENTIALS_ID, passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                            sh "git config user.email 'your-email@example.com'"
                            sh "git config user.name 'Your Name'"
                            sh "sed -i 's+${DOCKER_REPO}:.*+${DOCKER_REPO}:${DOCKER_TAG}+g' deployment.yml"
                            sh "git add deployment.yml"
                            sh "git commit -m 'Update Odoo deployment to ${DOCKER_TAG}'"
                            sh "git push https://${GIT_USERNAME}:${GIT_PASSWORD}@${GIT_REPO} HEAD:main"
                        }
                    }
                }
            }
        }
    }
}