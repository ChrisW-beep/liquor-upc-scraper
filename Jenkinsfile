pipeline {
    agent any

    environment {
        PYTHONUNBUFFERED = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/ChrisW-beep/liquor-upc-scraper.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Scraper') {
            steps {
                sh 'python scraper.py'
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'output/**/*.csv', fingerprint: true
                archiveArtifacts artifacts: 'output/**/*.jpg', fingerprint: true
            }
        }
    }
}
