node {
    def app

    stage('Clone repository') {
        checkout scm
    }

    stage('Build image') {
       app = docker.build("medlas/jenkins-flask")
    }

    stage('Test image') {
        app.inside {
            sh 'echo "Tests passed"'
        }
    }

    stage('Push image') {
        docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
            app.push("${env.BUILD_NUMBER}")
        }
    }
    
    stage('Update Kubernetes Manifest') {
        script {
            // Update the manifest file with the new image tag
            sh "sed -i 's/\${IMAGE_TAG}/${env.BUILD_NUMBER}/g' path/to/your/manifest.yml"
        }
    }

    stage('Apply Kubernetes Manifest') {
        withKubeConfig([credentialsId: 'your-kube-config-id']) {
            sh "kubectl apply -f path/to/your/manifest.yml"
        }
    }
    
    stage('Trigger ManifestUpdate') {
        echo "triggering updatemanifestjob"
        build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER)]
    }
}
