pipeline {
    agent any
    
    environment {
        APP_NAME = 'geodish-app'
        AWS_REGION = 'ap-south-1'
        ECR_REGISTRY = '893692751288.dkr.ecr.ap-south-1.amazonaws.com'
        ECR_REPOSITORY = 'geodish-app'
        DOCKER_IMAGE_TAG = "${BUILD_NUMBER}"
        PYTHONPATH = "${WORKSPACE}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '=== Checking out source code ==='
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                echo '=== Setting up Python environment ==='
                sh 'python3 -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }
        
        stage('Build') {
            steps {
                echo '=== Compiling Python bytecode ==='
                sh '. venv/bin/activate && python3 -m py_compile app/*.py'
            }
        }
        
        stage('Unit Tests') {
            steps {
                echo '=== Running unit tests ==='
                sh '. venv/bin/activate && python3 -m pytest tests/test.py -v --tb=short'
            }
        }
        
        stage('Package') {
            steps {
                echo '=== Building Docker image ==='
                sh "docker build -t ${APP_NAME}:${DOCKER_IMAGE_TAG} ."
                sh "docker tag ${APP_NAME}:${DOCKER_IMAGE_TAG} ${APP_NAME}:latest"
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
                echo '=== Running integration tests ==='
                sh 'docker compose -f docker-compose.test.yml up --build --abort-on-container-exit'
            }
            post {
                always {
                    sh 'docker compose -f docker-compose.test.yml down -v || true'
                }
            }
        }
        
        stage('Push to ECR') {
            when { branch 'main' }
            steps {
                echo '=== Pushing to Amazon ECR ==='
                withCredentials([
                    aws(credentialsId: 'aws-ecr-credentials', 
                        accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
                        secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                        aws ecr get-login-password --region ${AWS_REGION} | \
                            docker login --username AWS --password-stdin ${ECR_REGISTRY}
                        docker tag ${APP_NAME}:${DOCKER_IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}
                        docker tag ${APP_NAME}:latest ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest
                        docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}
                        docker push ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest
                    '''
                }
            }
        }
        
        stage('Update GitOps Repo') {
            when { branch 'main' }
            steps {
                echo '=== Updating GitOps repository ==='
                withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
                    sh '''
                        rm -rf gitops-repo
                        git clone https://${GITHUB_TOKEN}@github.com/kfiros94/geodish-gitops.git gitops-repo
                        cd gitops-repo
                        git config user.name "Jenkins Pipeline"
                        git config user.email "jenkins@geodish.com"
                        sed -i 's/tag: "[0-9]*"/tag: "'${DOCKER_IMAGE_TAG}'"/' helm-charts/geodish-app/values.yaml
                        git diff --quiet || (git add helm-charts/geodish-app/values.yaml && git commit -m "Update image tag to ${DOCKER_IMAGE_TAG}" && git push origin main)
                    '''
                }
            }
            post {
                always {
                    sh 'rm -rf gitops-repo'
                }
            }
        }
    }
    
    post {
        always {
            sh "docker rmi ${APP_NAME}:${DOCKER_IMAGE_TAG} || true"
            sh "docker rmi ${APP_NAME}:latest || true"
        }
        
        success {
            script {
                def message = """✅ GeoDish CI Pipeline Succeeded
Job: ${env.JOB_NAME} #${env.BUILD_NUMBER}
Duration: ${currentBuild.durationString}
Image: ${ECR_REGISTRY}/${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}
GitHub: <https://github.com/kfiros94/geodish-app|Repository>
Console: <${env.BUILD_URL}console|View Logs>"""
                
                try {
                    slackSend(
                        channel: '#cowsay-slack',
                        color: 'good',
                        message: message,
                        teamDomain: 'develeapbootcamp26',
                        tokenCredentialId: 'slacktoken3'
                    )
                } catch (Exception e) {
                    echo "Failed to send Slack notification: ${e.message}"
                }
            }
            echo '=== Pipeline completed successfully ==='
        }
        
        failure {
            script {
                def message = """❌ GeoDish CI Pipeline Failed
Job: ${env.JOB_NAME} #${env.BUILD_NUMBER}
Duration: ${currentBuild.durationString}
Branch: ${env.GIT_BRANCH ?: 'N/A'}
GitHub: <https://github.com/kfiros94/geodish-app|Repository>
Console: <${env.BUILD_URL}console|View Logs>"""
                
                try {
                    slackSend(
                        channel: '#cowsay-slack',
                        color: 'danger',
                        message: message,
                        teamDomain: 'develeapbootcamp26',
                        tokenCredentialId: 'slacktoken3'
                    )
                } catch (Exception e) {
                    echo "Failed to send Slack notification: ${e.message}"
                }
            }
            echo '=== Pipeline failed ==='
        }
    }
}