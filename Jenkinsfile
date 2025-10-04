pipeline {
    agent any
    
    environment {
        APP_NAME = 'geodish-app'
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Source') {
            steps {
                echo '=== Source Stage: Repository Cloned ==='
                script {
                    sh 'echo "Current branch: ${BRANCH_NAME}"'
                    sh 'echo "Build number: ${BUILD_NUMBER}"'
                    sh 'ls -la'
                }
            }
        }
    
       stage('Test') {
    steps {
        echo '=== Test Stage: Running Unit Tests ==='
        script {
            sh '''#!/bin/bash
                echo "Activating virtual environment..."
                . venv/bin/activate
                
                echo "Running unit tests..."
                python3 -m pytest test.py -v --tb=short
                
                echo "Tests completed successfully"
            '''
        }
    }
}



        
        stage('Test') {
            steps {
                echo '=== Test Stage: Running Unit Tests ==='
                script {
                    sh '''
                        echo "Running unit tests..."
                        python3 -m pytest test.py -v --tb=short
                        
                        echo "Tests completed successfully"
                    '''
                }
            }
        }
        
        stage('Package') {
            steps {
                echo '=== Package Stage: Creating Docker Image ==='
                script {
                    sh '''
                        echo "Building Docker image..."
                        docker build -t ${APP_NAME}:${DOCKER_IMAGE_TAG} .
                        docker build -t ${APP_NAME}:latest .
                        
                        echo "Docker image built successfully"
                        docker images | grep ${APP_NAME}
                    '''
                }
            }
        }
    }
    
    post {
        always {
            echo '=== Pipeline Cleanup ==='
            script {
                sh '''
                    echo "Cleaning up Docker images..."
                    docker rmi ${APP_NAME}:${DOCKER_IMAGE_TAG} || true
                    docker rmi ${APP_NAME}:latest || true
                '''
            }
        }
        
        success {
            echo '✅ Pipeline completed successfully!'
        }
        
        failure {
            echo '❌ Pipeline failed - check logs above'
        }
    }
}
