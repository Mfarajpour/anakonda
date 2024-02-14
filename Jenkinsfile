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
                            anakondaImage = docker.build("anakonda:jenkins-pipeline-$BUILD_ID")
                      }
                 } 
          }
          stage("test"){
                       steps{
                           script{
                                docker.image("mysql:8").withRun("--name anakonda-mysql_$BUILD_ID --rm -e MYSQL_ROOTPASSWORD=root -e MYSQL_DATABASE=test -e MYSQL_USER=anakonda -e MYSQL_PASSWORD=anakonda"){
                                    
                                    
                                    mysql ->
                                    anakondaImage.inside("--name anakonda-app-$BUILD_ID --link ${mysql.id} -e ANAKONDA_API_DATABASE_URI=mysql+pymysql://anakonda:anakonda@anakonda-mysql_${BUILD_ID}:3306/test -e ANAKONDA_API_ENV=test -e ANAKONDA-API_DEBUG=1 --entrypoint ''"){
                                        i = 3
                                        
                                        retry(10){
                                           sh "sleep $i"
                                           i *= 2
                                           sh "flask db upgrade 2> /dev/null"  
                                            }
                                        sh "coverage run"
                                      }
                                }
                           }
                         }
          }
    }
}
