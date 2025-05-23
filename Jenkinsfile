pipeline {
    agent any

    stages {

        // Stage 1 : Update / Install Packages 
        stage('Install Packages') {
            steps {
                ansiblePlaybook(
                    playbook: 'install_dependencies.yaml',
                    inventory: 'localhost', 
                    extras: '--connection=local'
                )
            }
        }

        // Stage 2 : Check Code Quality 
        stage('Check Code Quality') {
            steps {
                        sh '''
                        pylint netman_netconf_obj2.py --fail-under=5
                        '''
                    }
        }
    

        // Stage 3 : Run Code
        stage('Run Application') {
            steps { 
                sh '''
                python3 netman_netconf_obj2.py
                '''
            }
        }

        // Stage 4 : Run Unit Test
        stage('Run Unit Tests') {
            steps { 
                sh '''
                python3 netman_test.py
                '''
            }
        }

    }


    post {
        success {
            script {
                emailext(
                    subject: "Build Success!", 
                    body: "${env.JOB_NAME} build ${env.BUILD_NUMBER} successful",
                    to: "sarang.kalantre@colorado.edu" 
                )
            }
        }
        failure {
            script {
                emailext(
                    subject: "Build Failure!",
                    body: "${env.JOB_NAME} build ${env.BUILD_NUMBER} failed.",
                    to: "sarang.kalantre@colorado.edu"
                )
            }
        }
    }
}