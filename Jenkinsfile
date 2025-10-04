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
    
        stage('Build') {
            steps {
                echo '=== Build Stage: Compile Application Code ==='
                script {
                    sh '''#!/bin/bash
                        echo "Creating Python virtual environment..."
                        python3 -m venv venv
                        . venv/bin/activate
                        
                        echo "Installing Python dependencies..."
                        pip install -r requirements.txt
                        
                        echo "Compiling Python bytecode..."
                        python3 -m py_compile app/*.py
                        
                        echo "Build completed successfully"
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
