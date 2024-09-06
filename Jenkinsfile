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

        stage('Run Tests') {
            steps {
                script {
                    // Run the container with the test script
                    def testContainer = docker.image("medlas/odoo:${env.DOCKER_TAG}").run("-d")
                    try {
                        // Wait for Odoo to start
                        sleep 60
                        // Run the test script
                        sh 'docker exec test-container python3 /mnt/extra-addons/test.py'
                    } finally {
                        // Clean up the container
                        sh 'docker stop test-container'
                        sh 'docker rm test-container'
                    }
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
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials-id') {
                        def app = docker.image("medlas/odoo:${env.DOCKER_TAG}")
                        app.push('latest')
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
                    echo "Triggering ManifestUpdate job"
                    build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.DOCKER_TAG)]
                }
            }
        }
    }
}
