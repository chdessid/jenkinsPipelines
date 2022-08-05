pipeline {
    agent any

    stages {
        stage('Urls to Postgres') {
            steps {
               sh 'python urlspostgres.py'
            }
        }
       
    }
}
