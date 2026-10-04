pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    parameters {
        choice(
            name: 'TEST_SUITE',
            choices: ['smoke', 'api', 'ui', 'all'],
            description: 'Select test suite to run'
        )
    }

    stages {
        stage('Prepare results') {
            steps {
                dir('allure-results') {
                    deleteDir()
                }
                script {
                    if (isUnix()) {
                        sh 'mkdir -p allure-results'
                    } else {
                        bat 'if not exist allure-results mkdir allure-results'
                    }
                }
            }
        }

        stage('Build Docker image') {
            steps {
                script {
                    if (isUnix()) {
                        sh 'docker build -t python-aqa-framework .'
                    } else {
                        bat 'docker build -t python-aqa-framework .'
                    }
                }
            }
        }

        stage('Run tests') {
            steps {
                script {
                    def suite = params.TEST_SUITE == 'all' ? '' : "-m ${params.TEST_SUITE}"
                    def command = "docker run --rm --mount \"type=bind,source=${pwd()}/allure-results,target=/app/allure-results\" -e BASE_API_URL -e BASE_UI_URL -e REQUEST_TIMEOUT python-aqa-framework pytest ${suite} -v --alluredir=/app/allure-results"
                    if (isUnix()) {
                        sh command
                    } else {
                        bat command
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
