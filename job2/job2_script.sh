PROJECT_PATH=/home/mr-nobody/Documents/Docker/Project

if cat $PROJECT_PATH/run.py | grep keras
then
	if docker ps | grep cnn_container
    then
    	echo "Container already running"
    else
    	docker run -dit -v $PROJECT_PATH:/var/project --name cnn_container harsh27/cnn_image:latest
    fi
else
	echo "No file found"
fi
