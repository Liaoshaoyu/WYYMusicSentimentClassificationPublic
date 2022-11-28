pipeline {
    agent any

    environment {
        JENKINS_WORKSPACE="/var/jenkins_home/workspace"    //jenkins存放文件的地址
        PROJECT_NAME="${JOB_NAME}"                      // 项目名
        IMAGE_NAME="wyy_fastapi"                    // 镜像名一般和项目名相同
        VERSION_ID="${BUILD_ID}"
        ROOT_PATH="WYYFastAPI"
    }

    stages {
        stage('拉取代码') {
            steps {
                git branch: 'main', credentialsId: '', url: 'git@github.com:Liaoshaoyu/WYYMusicSentimentClassification.git'
                // pipeline下方有个生成语法的地方（Pipeline Syntax）
                echo '拉取成功'
            }
        }

        stage('执行构建') {
            steps {
                echo '构建完成'
            }
        }

        stage('docker部署') {
            steps {
                sh '''
            	container_id=`docker ps|grep ${IMAGE_NAME}|awk '{print $1}'`
                    if [ -n "${container_id}" ]; then
                        docker stop "${container_id}"
                    	docker rm "${container_id}"
                    fi

                    ole_image_id=`docker images|grep ${IMAGE_NAME}|awk '{print $3}'`
                    if [[ -n "${ole_image_id}" ]]; then
                        docker rmi -f ${ole_image_id}
                    fi

                    cp ${JENKINS_WORKSPACE}/${PROJECT_NAME}/${ROOT_PATH}/Dockerfile ${JENKINS_WORKSPACE}/${PROJECT_NAME}
                    cd ${JENKINS_WORKSPACE}/${PROJECT_NAME}
                    docker build -f Dockerfile -t ${IMAGE_NAME}:${VERSION_ID} .
                '''

                sh '''
                    container_id=`docker ps|grep ${IMAGE_NAME}|awk '{print $1}'`
                    if [ -n "${container_id}" ]; then
                    	docker rm -f "${container_id}"
                    fi

                    docker run --name "${IMAGE_NAME}_${VERSION_ID}" -p 8001:8001 -d ${IMAGE_NAME}:${VERSION_ID}
                '''
                echo '运行成功'
            }
        }
    }
}
