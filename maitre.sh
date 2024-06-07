docker build -t flask-app -f Dockerfile .

./net.sh

./run_sql.sh

docker run -p 5000:5000 flask-app

