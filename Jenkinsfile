pipeline{
    agent any
    stages{
          stage("prepare"){
                 steps{
                      load "jenkins/config.groovy"
                      dir(pwd(tmp: true)) {
                         git(
                            url: "$ANAKONDA_API_CI_CONFIG_GIT_URL",
                            branch: "$ANAKONDA_API_CI_CONFIG_GIT_BRANCH",
                            credentialsId: "$ANAKONDA_API_CI_CONFIG_GIT_CREDENTIALS",
                            changelog: true,
                            poll: true
                         )
                         load "config.groovy"
                          
                      }
                 }
          }
          stage("build"){
                steps{
                      script {
                            
                            gitcommit = sh(script: "git rev-parse HEAD", returnStdout: true).trim()    
                            gitTag = sh(script: "git tag --points-at HEAD", returnStdout: true).trim()
                            anakondaImage = docker.build("${ANAKONDA_API_DOCKER_REGISTRY_ADDRESS}/${ANAKONDA_API_IMAGE_NAME}:jenkins-pipeline-$BUILD_ID", "--build-arg GIT_COMMIT=${gitcommit} --build-arg JENKINS_PIPELINE=${BUILD_TAG} --build-arg BUILD_TAG=${BUILD_TAG} --build-arg BUILD_ID=${BUILD_ID} .")
                      }
                 } 
          }
          stage("test"){
                       steps{
                           script{
                                docker.image("${ANAKONDA_API_MYSQL_IMAGE}").withRun("--name anakonda-mysql-$BUILD_ID -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=test -e MYSQL_USER=anakonda -e MYSQL_PASSWORD=anakonda"){
                                    
                                    
                                    mysql ->
                                    anakondaImage.inside("--name anakonda-app-$BUILD_ID --link ${mysql.id} -e ANAKONDA_API_DATABASE_URI=mysql+pymysql://anakonda:anakonda@anakonda-mysql-${BUILD_ID}:3306/test -e ANAKONDA_API_ENV=test -e ANAKONDA-API_DEBUG=1 --entrypoint '' ${ANAKONDA_API_CONTAINER_EXTRA_ARGS}"){
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
                                        
                                        if ("$ANAKONDA_API_REPORT_UNIT_TEST_RESULTS" == "true") {
                                           junit "anakonda-pytest-${BUILD_ID}.xml"
                                         }
                                        sh "coverage html"
                                        sh "coverage xml"      
                                       
                                        if ("$ANAKONDA_API_REPORT_CODE_COVERAGE" == "true"){ 
                                           cobertura(
                                               autoUpdateHealth: true,
                                               autoUpdateStability: true,
                                               coberturaReportFile: "coverage.xml"
                                            )
                                         }

                                        if ("$ANAKONDA_API_ARCHIVE_ARTIFACTS" == "true"){
                                            archiveArtifacts(
                                               artifacts: "*.xml,htmlcov/**/*",
                                               fingerprint: true
                                             )
                                         }
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
                    if ("$ANAKONDA_API_LATEST_IMAGE_RELEASE" == "true"){
                        anakondaImage.push("latest")
                    } 
                    if (gitTag != ""){
                         if (gitTag.startsWith("v")) {
                            gitTag = gitTag.minus("v")
                            anakondaFullVersion = gitTag
                            version = gitTag.split("\\.")
                            anakondaMajorVersion = version[0]
                            anakondaMajorMinorVersion = version[0] + "." + version[1]
                            if ("$ANAKONDA_API_TAG_IMAGE_RELEASE" == "true") {
                               anakondaImage.push(anakondaFullVersion)
                             } 
                            if ("$ANAKONDA_API_VERSION_IMAGE_RELEASE" == "true") {
                               anakondaImage.push(anakondaMajorVersion)
                               anakondaImage.push(anakondaMajorMinorVersion)
                            } 
                          }
                    }
                 if ("$ANAKONDA_API_TRIGGER_DEV" == "true") {
                       build ( 
                             wait: false,
                             propagate: false,
                             waitForStart: true, 
                             job: 'anakonda-cd-pipeline',
                             parameters: [
                                        string(name: 'ENV', value: 'development'),
                                        string(name: 'IMAGE_NAME', value: "${ANAKONDA_API_DOCKER_REGISTRY_ADDRESS}/${ANAKONDA_API_IMAGE_NAME}"),
                                        string(name: 'IMAGE_TAG', value: "$ANAKONDA_API_DEV_IMAGE_TYPE" == "stable" ? "${anakondaMajorMinorVersion}" : "latest")
                                        ]
                             ) 
                    }
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
