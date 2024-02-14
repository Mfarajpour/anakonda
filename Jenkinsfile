pipeline{
    agent any
    stages{
          stage("prepare"){
                 steps{
                      sh "true"
                 }
          }
          stage("build"){
                steps{
                      script {
                            
                            gitcommit = sh(script: "git rev-parse HEAD", returnStdout: true).trim()    
                            anakondaImage = docker.build("103.216.61.74/anakonda:jenkins-pipeline-$BUILD_ID", "--build-arg GIT_COMMIT=${gitcommit} --build-arg JENKINS_PIPELINE=${BUILD_TAG} --build-arg BUILD_TAG=${BUILD_TAG} --build-arg BUILD_ID=${BUILD_ID} .")
                      }
                 } 
          }
          stage("test"){
                       steps{
                           script{
                                docker.image("mysql:8").withRun("--name anakonda-mysql-$BUILD_ID -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=test -e MYSQL_USER=anakonda -e MYSQL_PASSWORD=anakonda"){
                                    
                                    
                                    mysql ->
                                    anakondaImage.inside("--name anakonda-app-$BUILD_ID --link ${mysql.id} -e ANAKONDA_API_DATABASE_URI=mysql+pymysql://anakonda:anakonda@anakonda-mysql-${BUILD_ID}:3306/test -e ANAKONDA_API_ENV=test -e ANAKONDA-API_DEBUG=1 --entrypoint ''"){
                                        i = 1
                                        retry(10) {
                                            sh "sleep $i"
                                            i *=2
                                            sh "flask db upgrade 2> /dev/null"
                                        }
                                        coverageStatus = sh (
                                            script: "coverage run -m pytest --junit-xml=anakonda-pytest-${BUILD_ID}.xml",
                                            returnStatus: true
                                             )
                                        junit "anakonda-pytest-${BUILD_ID}.xml"
                                        sh "coverage html"
                                        sh "coverage xml"      
                                        cobertura(
                                           autoUpdateHealth: true,
                                           autoUpdateStability: true,
                                           coberturaReportFile: "coverage.xml"
                                         )
                                        archiveArtifacts(
                                            artifacts: "*.xml,htmlcov/**/*",
                                            fingerprint: true
                                        )
                                        if ( coverageStatus != 0) {
                                          sh "false"
                                          } 
                                      }
                                }
                           }
                         }
          }
          stage("Release"){
              steps {
                 script{
                    anakondaImage.push("latest")
                 }
              }
          }  
    }
    post {
         always{
             deleteDir()
             }
    }    
}
