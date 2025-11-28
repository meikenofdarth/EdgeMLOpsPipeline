pipeline {
    agent any

    environment {
        // Your Docker Hub Image Name
        DOCKER_IMAGE = "anurag9507/spe-mlops"
        
        // This ID must match what you created in Jenkins -> Credentials
        REGISTRY_CREDS = credentials('dockerhub-creds')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building image..."
                    // 1. Build with the specific build number
                    sh "docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} ."
                    sh "docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Automated Test') {
            steps {
                script {
                    echo "Running Syntax Checks (Fast Test)..."
                    sh "docker run --rm ${DOCKER_IMAGE}:${BUILD_NUMBER} python -m py_compile cloud/train.py app/edge_infer.py devices/publisher.py"
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    echo "Pushing to Docker Hub..."
                    sh "echo $REGISTRY_CREDS_PSW | docker login -u $REGISTRY_CREDS_USR --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}"
                    sh "docker push ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Deploy to K8s') {
            steps {
                script {
                    echo "Deploying to Kubernetes..."
                    // Update K8s manifest to use the new Build Number
                    sh "sed -i 's|:latest|:${BUILD_NUMBER}|g' k8s/app-deployment.yaml"
                    
                    // Run Ansible to apply changes
                    sh "ansible-playbook -i ansible/inventory.ini ansible/deploy.yml"
                }
            }
        }
    }

    post {
        always {
            // Clean up to save disk space
            sh "docker rmi ${DOCKER_IMAGE}:${BUILD_NUMBER} || true"
            sh "docker rmi ${DOCKER_IMAGE}:latest || true"
        }
    }
}