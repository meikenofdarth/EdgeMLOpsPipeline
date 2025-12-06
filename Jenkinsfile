pipeline {
    agent any

    environment {
        // Your Docker Hub Image Name
        DOCKER_IMAGE = "anurag9507/spe-mlops"
        
        // This ID must match what you created in Jenkins -> Credentials
        REGISTRY_CREDS = credentials('dockerhub-creds')
        
        // Vault Password for Automation (Matches the one you set: 1234)
        VAULT_PASS = "1234" 
    }

    // --- NEW: SATISFIES "WEBHOOK/AUTOMATION" REQUIREMENT ---
    triggers {
        // This ensures the pipeline runs automatically on Git Push
        githubPush()
    }
    // -------------------------------------------------------

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
                    sh "docker build -t ${DOCKER_IMAGE}:${BUILD_NUMBER} ."
                    sh "docker tag ${DOCKER_IMAGE}:${BUILD_NUMBER} ${DOCKER_IMAGE}:latest"
                }
            }
        }

        stage('Automated Test') {
            steps {
                script {
                    echo "Running Syntax Checks..."
                    // A simple test to verify code syntax before deploying
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
                    
                    // 1. Update K8s manifest to use the new Build Number
                    sh "sed -i 's|:latest|:${BUILD_NUMBER}|g' k8s/app-deployment.yaml"
                    
                    // 2. Create temporary Vault Password file for automation
                    sh "echo '${VAULT_PASS}' > ansible/.vault_pass"
                    
                    // 3. Run Ansible using the password file (Non-interactive mode)
                    sh "ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --vault-password-file ansible/.vault_pass"
                    
                    // 4. Cleanup password file
                    sh "rm ansible/.vault_pass"
                }
            }
        }
    }

    post {
        always {
            // Clean up Docker images to save disk space
            sh "docker rmi ${DOCKER_IMAGE}:${BUILD_NUMBER} || true"
            sh "docker rmi ${DOCKER_IMAGE}:latest || true"
        }
    }
}