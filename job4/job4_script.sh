MIN=85
ACCURACY=`cat /home/mr-nobody/Documents/Docker/Project/accuracy.txt`
ACCURACY=${ACCURACY%.*}

if [ $ACCURACY -lt $MIN ]
then
	echo "Desired accuracy didn't achieved"
	exit 1
else
	docker exec -t cnn_container python3 sendmail.py
	exit 0
fi
