if docker ps | grep cnn_container
then
	docker exec -t cnn_container python3 run.py
    docker exec -t cnn_container python3 measure_accuracy.py
else
if docker ps | grep sk_container
then
	docker exec -t sk_container python3 run.py
else
	echo "No containers running"
fi 
fi
