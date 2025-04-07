pipeline {
    agent any

    stages {

        stage('Debug') {
            steps {
                sh 'ls -la'
                sh 'cat install_dependencies.yaml'
            }
        }

        
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
                script {
                    try {
                        sh '''
                        pylint netman_netconf_obj2.py --fail-under=5
                        '''
                    }
                    catch (Exception e){
                        echo 'Pylint Violation! Please fix code.'
                        error('Codestyle Violation')
                    }
                }
            }
        }

        // Stage 3 : Run Code
        stage('Run Application') {
            steps { 
                sh '''
                sudo python3 netman_netconf_obj2.py
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