docker build -t hub_closures:v1 .
docker run -v "$(pwd):/app" hub_closures:v1 python script/main.py
