pipeline {
    agent any

    environment {
        DOCKER_TAG = "${env.BUILD_NUMBER}"
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
                    def app = docker.build("medlas/odoo:${env.DOCKER_TAG}")
                }
            }
        }

        stage('Run Docker Compose') {
            steps {
                script {
                    echo "Using Docker tag: ${env.DOCKER_TAG}"
                    sh "docker-compose up --build -d"
                }
            }
        }

        stage('Wait for Odoo to start') {
            steps {
                script {
                    // Wait for the Odoo server to be accessible
                    timeout(time: 2, unit: 'MINUTES') {
                        waitUntil {
                            script {
                                def response = sh(script: "curl -s -o /dev/null -w '%{http_code}' http://localhost:8069/web", returnStdout: true).trim()
                                return response == '200'
                            }
                        }
                    }
                }
            }
        }

        stage('Test image') {
            steps {
                script {
                    try {
                        sh "python3 test.py"
                    } catch (Exception e) {
                        error("Test failed. Aborting pipeline.")
                    }
                }
            }
        }

        stage('Stop and Remove Containers') {
            steps {
                script {
                    sh 'docker-compose down'
                }
            }
        }

        stage('Push image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
                        def app = docker.image("medlas/odoo:${env.DOCKER_TAG}")
                        app.push("${env.DOCKER_TAG}")
                    }
                }
            }
        }

        stage('Trigger ManifestUpdate') {
            steps {
                script {
                    build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.DOCKER_TAG)]
                }
            }
        }
    }
}
