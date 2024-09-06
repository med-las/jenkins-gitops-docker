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

//         stage('Build image') {
//             steps {
//                 script {
//                     def app = docker.build("medlas/odoo:${env.DOCKER_TAG}")
//                 }
//             }
//         }

//         stage('Run Docker Compose') {
//             steps {
//                 script {
//                     echo "Using Docker tag: ${env.DOCKER_TAG}"
//                     sh "docker-compose up --build -d"
//                 }
//             }
//         }


// stage('Test image') {
//     steps {
//         script {
//             echo "Waiting for Odoo server to be ready..."
//             sleep(time: 60, unit: 'SECONDS') // Adjust the wait time if needed

//             echo "Checking server status"
//             sh "docker-compose exec odoo curl -s http://localhost:8069/web > /dev/null && echo 'Server is running' || echo 'Server is not running'"

//             echo "Listing files in /mnt/extra-addons"
//             sh "docker-compose exec odoo ls /mnt/extra-addons"
            
//             // Run the test file
//             sh "docker-compose exec odoo python3 /mnt/extra-addons/test.py"
//         }
//     }
// }



//         stage('Stop and Remove Containers') {
//             steps {
//                 script {
//                     // Stop and remove containers created by Docker Compose
//                     sh 'docker-compose down'
//                 }
//             }
//         }

//         stage('Push image') {
//             when {
//                 expression {
//                     return currentBuild.result == 'SUCCESS'
//                 }
//             }
//             steps {
//                 script {
//                     docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
//                         // Push the Docker image only if the test passes
//                         def app = docker.image("medlas/odoo:${env.DOCKER_TAG}")
//                         app.push("${env.DOCKER_TAG}")
//                     }
//                 }
//             }
//         }

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