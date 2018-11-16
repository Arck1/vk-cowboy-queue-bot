IMAGE = vk_queue:latest

docker/build/bot:
	@docker build -t $(IMAGE_SPARK_UWSGI) -f Dockerfile .

init:
	cp example_vars.env.txt vars.env

local: 
	cp example_local_settings.py.txt local_settings.py
