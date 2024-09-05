pipeline {
    agent any

    stages {
        stage('Clone repository') {
            steps {
                checkout scm
            }
        }

        stage('Build image') {
            steps {
                script {
                    // Build Docker image
                    def app = docker.build("medlas/odoo:${env.BUILD_NUMBER}")
                }
            }
        }

        stage('Run Docker Compose') {
            steps {
                script {
                    // Create and start Docker containers using Docker Compose
                    sh 'docker-compose up --build -d'
                }
            }
        }

        stage('Test image') {
            steps {
                script {
                    // Run tests using Docker Compose
                    sh 'docker-compose run --rm test'
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
                        // Push the Docker image
                        def app = docker.image("medlas/odoo:${env.BUILD_NUMBER}")
                        app.push("${env.BUILD_NUMBER}")
                    }
                }
            }
        }

        stage('Trigger ManifestUpdate') {
            steps {
                script {
                    echo "triggering updatemanifestjob"
                    build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER)]
                }
            }
        }
    }
}
