pipeline {
    agent any

    environment {
        IMAGE = "nevs025/meteo-api"
        TAG   = "${env.BUILD_NUMBER}"
    }

    options {
        timeout(time: 40, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '15'))
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Tester') {
            steps {
                echo "Tests de la revision ${env.GIT_COMMIT?.take(7)}"

                sh 'docker build --target test -t meteo-api:test-$TAG .'

                sh '''
                    docker rm -f meteo-tests-$TAG 2>/dev/null || true
                    docker create --name meteo-tests-$TAG meteo-api:test-$TAG \
                      python -m pytest -q --junitxml=/tmp/rapport.xml
                    docker start -a meteo-tests-$TAG || true
                    docker cp meteo-tests-$TAG:/tmp/rapport.xml rapport.xml
                    docker rm -f meteo-tests-$TAG
                '''

                junit 'rapport.xml'
            }
        }


        stage('Construire') {
            steps {
                sh 'docker build -t $IMAGE:$TAG -t $IMAGE:latest .'
                sh 'docker images $IMAGE'
            }
        }

        stage('Publier') {
            steps {
                withCredentials([usernamePassword(
                        credentialsId: 'docker-hub',
                        usernameVariable: 'REGISTRE_USER',
                        passwordVariable: 'REGISTRE_PASS')]) {
                    sh '''
                        echo "$REGISTRE_PASS" | docker login -u "$REGISTRE_USER" --password-stdin
                        docker push $IMAGE:$TAG
                        docker push $IMAGE:latest
                    '''
                }
            }
        }

        stage('Deployer') {
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-kind', variable: 'KUBECONFIG')]) {
                    sh '''
                        kubectl set image deployment/meteo-api api=$IMAGE:$TAG
                        kubectl rollout status deployment/meteo-api --timeout=180s
                        kubectl get pods -l app=meteo-api
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "OK : ${env.IMAGE}:${env.TAG} est deploye dans le cluster."
        }
        failure {
            echo "ECHEC a l'etape affichee en rouge. Rien n'a ete deploye si l'echec est avant 'Deployer'."
        }
        always {
            sh 'docker logout || true'
            sh 'docker image prune -f || true'
        }
    }
}
