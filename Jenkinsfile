pipeline {
    agent any

    stages {
        stage('Create Sqlite') {
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
