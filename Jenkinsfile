pipeline {
    agent any

    stages {
        stage('Urls to Postgres') {
            steps {
               sh 'python3 urls_postgres.py'
            }
        }
       
    }
}
