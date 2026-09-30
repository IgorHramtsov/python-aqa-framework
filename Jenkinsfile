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
                        bat 'docker run --rm python-aqa-framework pytest -v'
                    } else {
                        bat "docker run --rm python-aqa-framework pytest -m ${params.TEST_SUITE} -v"
                    }
                }
            }
        }
    }
}