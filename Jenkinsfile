pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
               sh 'python runSqlite.py'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
