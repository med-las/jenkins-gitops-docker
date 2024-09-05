node {
    def app

    stage('Clone repository') {
        checkout scm
    }

    stage('Install Docker Compose') {
        sh '''
        if ! [ -x "$(command -v docker-compose)" ]; then
            echo "Docker Compose not found. Installing..."
            sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
            sudo chmod +x /usr/local/bin/docker-compose
        else
            echo "Docker Compose is already installed."
        fi
        '''
    }

    stage('Build image') {
       app = docker.build("medlas/odoo:${env.BUILD_NUMBER}")
    }

    stage('Run Docker Compose') {
        sh '''
        docker-compose up --build -d
        '''
    }

    stage('Test image') {
        app.inside {
            sh 'echo "Running Odoo tests"'
            // Install the required Python packages for testing
            sh 'pip install requests'
            // Run the test script
            sh 'python test.py'
        }
    }

    stage('Stop and Remove Containers') {
        sh '''
        docker-compose down
        '''
    }

    stage('Push image') {
        docker.withRegistry('https://registry.hub.docker.com', 'dockerhub') {
            app.push("${env.BUILD_NUMBER}")
        }
    }
    
    stage('Trigger ManifestUpdate') {
        echo "Triggering updatemanifestjob"
        build job: 'updatemanifest', parameters: [string(name: 'DOCKERTAG', value: env.BUILD_NUMBER)]
    }
}
