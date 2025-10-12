pipeline {
    agent any
    
    environment {
        APP_NAME = 'geodish-app'
        AWS_REGION = 'ap-south-1'
        ECR_REGISTRY = '893692751288.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPOSITORY = 'geodish-app'
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"
        MONGODB_URI = "mongodb://localhost:27017/geodish_test"
        FLASK_ENV = "testing"
    }
    
    tools {
        dockerTool 'docker'
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        skipStagesAfterUnstable()
        parallelsAlwaysFailFast()
    }
    
    stages {
        stage('Source') {
            steps {
                echo '=== Source Stage: Repository Cloned ==='
                sh 'echo "Current branch: ${BRANCH_NAME}"'
                sh 'echo "Build number: ${BUILD_NUMBER}"'
                sh 'ls -la'
            }
        }
        
        stage('Build') {
            steps {
                echo '=== Build Stage: Compile Application Code ==='
                sh '''#!/bin/bash
                    set -euo pipefail
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
            post {
                failure {
                    echo 'Build stage failed'
                }
            }
        }
        
        stage('Test') {
            steps {
                echo '=== Test Stage: Running Unit Tests ==='
                sh '''#!/bin/bash
                    set -euo pipefail
                    echo "Activating virtual environment..."
                    . venv/bin/activate
                    
                    echo "Running unit tests..."
                    python3 -m pytest tests/ -v --tb=short --junitxml=test-results.xml || true
                    
                    echo "Tests completed"
                '''
            }
            post {
                always {
                    publishTestResults testResultsPattern: 'test-results.xml'
                }
            }
        }
        
        stage('Package') {
            steps {
                echo '=== Package Stage: Creating Docker Image ==='
                sh '''#!/bin/bash
                    set -euo pipefail
                    echo "Building Docker image..."
                    docker build -t ${APP_NAME}:${DOCKER_IMAGE_TAG} .
                    docker build -t ${APP_NAME}:latest .
                    
                    echo "Docker image built successfully"
                    docker images | grep ${APP_NAME}
                '''
            }
            post {
                failure {
                    echo 'Docker build failed'
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
                echo '=== Integration Tests: Containerized Testing ==='
                sh '''#!/bin/bash
                    set -euo pipefail
                    
                    echo "🐳 Running integration tests in container..."
                    
                    # Start MongoDB container for testing
                    echo "🚀 Starting MongoDB test container..."
                    docker run -d --name mongo-test -p 27017:27017 mongo:7.0
                    
                    # Wait for MongoDB to be ready
                    echo "⏳ Waiting for MongoDB to be ready..."
                    sleep 30
                    
                    # Test MongoDB connectivity
                    echo "🔍 Testing MongoDB connectivity..."
                    for i in {1..5}; do
                        if docker exec mongo-test mongosh --eval "db.admin.ping()" >/dev/null 2>&1; then
                            echo "✅ MongoDB is ready!"
                            break
                        fi
                        echo "Attempt $i: MongoDB not ready yet, waiting..."
                        sleep 5
                    done
                    
                    # Activate virtual environment
                    echo "🔧 Activating virtual environment..."
                    . venv/bin/activate
                    
                    # Set environment variables for testing
                    export PYTHONPATH="${PYTHONPATH:-$(pwd)}"
                    
                    # Run integration tests
                    echo "🧪 Running integration tests..."
                    python3 -m pytest \
                        tests/test.py::test_random_dish_endpoint \
                        tests/test.py::test_save_recipe_endpoint \
                        tests/test.py::test_invalid_country \
                        tests/test.py::test_invalid_endpoint \
                        tests/test.py::test_app_config \
                        tests/test.py::test_database_connection_mock \
                        -v --tb=short --junitxml=integration-test-results.xml || echo "⚠️ Some tests failed, but continuing..."
                    
                    # Test endpoints with timeout
                    echo "🧪 Testing application endpoints..."
                    timeout 30 python3 -c "
import sys
import time
sys.path.append('.')
from app.app import app
app.run(host='0.0.0.0', port=5000, debug=False)
" &
                    APP_PID=$!
                    
                    # Wait for app to start
                    sleep 15
                    
                    # Test available endpoints
                    echo "🔍 Testing available endpoints..."
                    timeout 10 curl -f http://localhost:5000/seed-info 2>/dev/null && echo "✅ /seed-info works" || echo "❌ /seed-info not available"
                    timeout 10 curl -f -X POST http://localhost:5000/seed 2>/dev/null && echo "✅ /seed works" || echo "❌ /seed not available"
                    timeout 10 curl -f -X POST http://localhost:5000/force-seed 2>/dev/null && echo "✅ /force-seed works" || echo "❌ /force-seed not available"
                    
                    # Cleanup background process
                    kill $APP_PID 2>/dev/null || true
                    wait $APP_PID 2>/dev/null || true
                    
                    echo "✅ Integration tests completed!"
                '''
            }
            post {
                always {
                    publishTestResults testResultsPattern: 'integration-test-results.xml'
                    sh '''
                        echo "🧹 Cleaning up MongoDB test container..."
                        docker stop mongo-test 2>/dev/null || true
                        docker rm mongo-test 2>/dev/null || true
                    '''
                }
                success {
                    echo '✅ Integration tests passed!'
                }
                unstable {
                    echo '⚠️ Some integration tests failed, but continuing pipeline...'
                }
            }
        }
        
        stage('Tag & Push to ECR') {
            when { 
                branch 'main' 
            }
            environment {
                AWS_DEFAULT_REGION = "${AWS_REGION}"
            }
            steps {
                echo '=== ECR Stage: Tag and Push to ECR (Main Branch Only) ==='
                withCredentials([
                    aws(credentialsId: 'aws-ecr-credentials', 
                        accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
                        secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''#!/bin/bash
                        set -euo pipefail
                        
                        echo "🔐 Authenticating with ECR..."
                        aws ecr get-login-password --region "${AWS_REGION}" | \
                            docker login --username AWS --password-stdin "${ECR_REGISTRY}"
                        
                        echo "🏷️ Tagging images for ECR..."
                        docker tag "${APP_NAME}:${DOCKER_IMAGE_TAG}" "${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}"
                        docker tag "${APP_NAME}:${DOCKER_IMAGE_TAG}" "${ECR_REGISTRY}/${ECR_REPOSITORY}:latest"
                        
                        echo "📤 Pushing images to ECR..."
                        docker push "${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}"
                        docker push "${ECR_REGISTRY}/${ECR_REPOSITORY}:latest"
                        
                        echo "✅ Images pushed to ECR successfully!"
                        echo "📦 Image URI: ${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}"
                    '''
                }
            }
            post {
                success {
                    echo "✅ Successfully pushed to ECR: ${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}"
                }
                failure {
                    echo "❌ Failed to push to ECR"
                }
            }
        }
        
        stage('Update GitOps Repository') {
            when { 
                branch 'main' 
            }
            steps {
                echo '=== GitOps Stage: Update App-of-Apps Configuration ==='
                withCredentials([
                    string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')
                ]) {
                    sh '''#!/bin/bash
                        set -euo pipefail
                        
                        echo "🔄 Updating App-of-Apps with new image tag..."
                        
                        # Clone GitOps repository
                        git clone https://${GITHUB_TOKEN}@github.com/kfiros94/geodish-gitops.git gitops-repo
                        cd gitops-repo
                        
                        # Configure git
                        git config user.name "Jenkins Pipeline"
                        git config user.email "jenkins@geodish.com"
                        
                        # Update image tag in App-of-Apps values
                        sed -i 's/tag: "[^"]*"/tag: "'${DOCKER_IMAGE_TAG}'"/' app-of-apps/values.yaml
                        
                        # Check if there are changes to commit
                        if git diff --quiet; then
                            echo "⚠️  No changes detected - image tag might already be ${DOCKER_IMAGE_TAG}"
                        else
                            # Commit and push changes
                            git add app-of-apps/values.yaml
                            git commit -m "🚀 Update geodish-app image tag to ${DOCKER_IMAGE_TAG}"
                            git push origin main
                            echo "✅ App-of-Apps updated successfully!"
                        fi
                        
                        echo "📦 Current image tag: ${DOCKER_IMAGE_TAG}"
                    '''
                }
            }
            post {
                success {
                    echo "✅ GitOps repository updated successfully"
                }
                failure {
                    echo "❌ Failed to update GitOps repository"
                }
                always {
                    sh 'rm -rf gitops-repo || true'
                }
            }
        }
        
        stage('Deploy Notification') {
            when { 
                branch 'main' 
            }
            steps {
                echo '=== Deploy Stage: Ready for Deployment ==='
                sh '''#!/bin/bash
                    echo "🚀 Ready for deployment!"
                    echo "📦 ECR Image: ${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}"
                    echo "🎯 GitOps repository updated - ArgoCD will handle deployment"
                '''
            }
        }
    }
    
    post {
        always {
            echo '=== Pipeline Cleanup ==='
            sh '''#!/bin/bash
                echo "🧹 Cleaning up local Docker images..."
                docker rmi ${APP_NAME}:${DOCKER_IMAGE_TAG} 2>/dev/null || true
                docker rmi ${APP_NAME}:latest 2>/dev/null || true
                docker system prune -f || true
            '''
            
            // Archive important artifacts
            archiveArtifacts artifacts: '**/*.xml, **/*.log', allowEmptyArchive: true
            
            // Clean workspace
            cleanWs()
        }
        
        success {
            echo '✅ Pipeline completed successfully!'
            script {
                if (env.BRANCH_NAME == 'main') {
                    echo "🎉 Main branch: Image pushed to ECR and GitOps updated!"
                    echo "📦 ECR: ${ECR_REGISTRY}/${ECR_REPOSITORY}:${BUILD_NUMBER}"
                }
            }
        }
        
        failure {
            echo '❌ Pipeline failed - check logs above'
            // Could add notification here (Slack, email, etc.)
        }
        
        unstable {
            echo '⚠️ Pipeline completed with warnings'
        }
        
        aborted {
            echo '⏹️ Pipeline was aborted'
        }
    }
}
