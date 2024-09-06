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


stage('Test image') {
    steps {
        script {
            def maxRetries = 10
            def retryInterval = 10 // in seconds

            for (int i = 0; i < maxRetries; i++) {
                try {
                    sh "python3 /mnt/extra-addons/test.py"
                    break // Exit the loop if the test passes
                } catch (Exception e) {
                    echo "Test failed, retrying in ${retryInterval} seconds..."
                    sleep(time: retryInterval, unit: 'SECONDS')
                }
            }
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
            when {
                expression {
                    return currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
                        // Push the Docker image only if the test passes
                        def app = docker.image("medlas/odoo:${env.DOCKER_TAG}")
                        app.push("${env.DOCKER_TAG}")
                    }
                }
            }
        }

        stage('Trigger ManifestUpdate') {
            when {
                expression {
                    return currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                script {
                    echo "Triggering updatemanifestjob"
                    build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.DOCKER_TAG)]
                }
            }
        }
    }
}