pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'dimondmelov03/ml-app'
        DOCKER_TAG   = 'latest'
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
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}", ".")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                        docker.image("${DOCKER_IMAGE}:${DOCKER_TAG}").push()
                    }
                }
            }
        }

        stage('Apply Kubernetes Manifests') {
            steps {
                script {
                    sh 'minikube kubectl -- apply -f k8s/namespace.yaml'
                    sh 'minikube kubectl -- apply -f k8s/deployment.yaml'
                    sh 'minikube kubectl -- apply -f k8s/service.yaml'
                }
            }
        }

        stage('Verify Minikube Access') {
            steps {
                script {
                    sh 'minikube kubectl -- get nodes'
                }
            }
        }

        stage('Update Kubernetes Deployment') {
            steps {
                script {
                    sh 'minikube kubectl -- rollout restart deployment/ml-app --namespace=default'
                    sh 'minikube kubectl -- rollout status deployment/ml-app --namespace=default --timeout=300s'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}