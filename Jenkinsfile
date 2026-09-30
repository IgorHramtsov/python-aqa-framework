pipeline {
    agent any

    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['smoke', 'api', 'ui', 'all'],
            description: 'Select test suite to run'
        )
    }

    stages {
        stage('Build Docker image') {
            steps {
                bat 'docker build -t python-aqa-framework .'
            }
        }

        stage('Run tests') {
            steps {
                script {
                    if (params.TEST_SUITE == 'all') {
                        bat 'docker run --rm -v "%CD%\\allure-results:/app/allure-results" python-aqa-framework pytest -v --alluredir=/app/allure-results'
                    } else {
                        bat "docker run --rm -v \"%CD%\\allure-results:/app/allure-results\" python-aqa-framework pytest -m ${params.TEST_SUITE} -v --alluredir=/app/allure-results"
                    }
                }
            }
        }
    }

    post {
        always {
            allure results: [[path: 'allure-results']]
        }
    }
}