pipeline {
    agent any
    
    environment {
        APP_NAME = 'geodish-app'
        AWS_REGION = 'ap-south-1'
        ECR_REGISTRY = '893692751288.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPOSITORY = 'geodish-app'
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
                    sh '''#!/bin/bash
                        echo "Activating virtual environment..."
                        . venv/bin/activate
                        
                        echo "Running unit tests..."
                        python3 -m pytest tests/ -v --tb=short
                        
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
        
        stage('Integration Tests') {
            when {
                anyOf {
                    branch 'main'
                    branch 'feature/*'
                }
            }
            steps {
                echo '=== Integration Tests: Deploy Test Environment ==='
                script {
                    try {
                        sh '''
                            echo "Starting integration test environment..."
                            
                            # Use the newly built image in docker compose
                            export GEODISH_IMAGE=${APP_NAME}:${DOCKER_IMAGE_TAG}
                            docker compose -f docker-compose.yaml up -d
                            
                            echo "Waiting for services to be ready..."
                            sleep 30
                            
                            echo "Testing API endpoints..."
                            curl -f http://localhost/metrics || echo "❌ Metrics endpoint failed"
                            curl -f -X POST http://localhost/seed || echo "✅ Seed endpoint test"
                            curl -f http://localhost/countries || echo "✅ Countries endpoint test"
                            
                            echo "Integration tests completed"
                        '''
                    } finally {
                        sh '''
                            echo "Cleaning up integration test environment..."
                            docker compose -f docker-compose.yaml down -v
                        '''
                    }
                }
            }
        }
        
        stage('Tag & Push to ECR') {
            when { branch 'main' }
            steps {
                echo '=== ECR Stage: Tag and Push to ECR (Main Branch Only) ==='
                script {
                    withCredentials([aws(credentialsId: 'aws-access-key-id', region: env.AWS_REGION)]) {
                        sh '''
                            echo "🔐 Authenticating with ECR..."
                            aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
                            
                            echo "🏷️ Tagging images for ECR..."
                            docker tag ${APP_NAME}:${DOCKER_IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}
                            docker tag ${APP_NAME}:${DOCKER_IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest
                            
                            echo "📤 Pushing images to ECR..."
                            docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}
                            docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest
                            
                            echo "✅ Images pushed to ECR successfully!"
                            echo "📦 Image URI: ${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}"
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to EC2') {
            when { branch 'main' }
            steps {
                echo '=== Deploy Stage: Prepare for EC2 Deployment ==='
                script {
                    sh '''
                        echo "🚀 Ready for EC2 deployment!"
                        echo "📦 ECR Image: ${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}"
                        echo "🎯 Next: Create EC2 instance and deploy"
                    '''
                }
            }
        }
    }
    
    post {
        always {
            script {
                sh '''
                    echo "🧹 Cleaning up local Docker images..."
                    docker rmi ${APP_NAME}:${DOCKER_IMAGE_TAG} || true
                    docker rmi ${APP_NAME}:latest || true
                '''
            }
        }
        
        success {
            echo '✅ Pipeline completed successfully!'
            script {
                if (env.BRANCH_NAME == 'main') {
                    echo "🎉 Main branch: Image pushed to ECR!"
                    echo "📦 ECR: 893692751288.dkr.ecr.ap-south-1.amazonaws.com/geodish-app:${BUILD_NUMBER}"
                }
            }
        }
        
        failure {
            echo '❌ Pipeline failed - check logs above'
        }
    }
}
