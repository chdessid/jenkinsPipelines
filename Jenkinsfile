pipeline {
    agent any

    stages {
        stage('Create Sqlite') {
            steps {
               sh 'python create_sqlite.py'
            }
        }
        stage('Get Main Sitemap') {
            steps {
                sh 'python main_sitemaps.py'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
