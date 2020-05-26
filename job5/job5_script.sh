PROJECT_PATH=/home/mr-nobody/Documents/Docker/Project/

echo "Tweaking the code"

docker exec -t cnn_container python3 tweak.py

cp $PROJECT_PATH/run.py .

git config user.email "your github email"
git config user.name "your github name"

git commit run.py -m "Tweaked the code"
git push origin HEAD:master

user="admin"
passwd="your jenkins password"

# give your jenkins trigger from script url
curl --user $user:$passwd 192.168.225.163:8080/view/Task_3/job/Job1/build?token=harharmahadev
