node {
    def app

    stage('Clone repository') {
        checkout scm
    }

    stage('Build image') {
       app = docker.build("medlas/odoo:${env.BUILD_NUMBER}")
    }

stage('Test image') {
    app.inside {
        sh 'echo "Running Odoo tests"'
        // Install the required Python packages for testing
        sh 'pip3 install requests'
        // Run the test script
        sh 'python3 /mnt/extra-addons/test.py'
    }
}


    stage('Push image') {
        docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
            app.push("${env.BUILD_NUMBER}")
        }
    }
    
    stage('Trigger ManifestUpdate') {
        echo "triggering updatemanifestjob"
        build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER)]
    }
}
