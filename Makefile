IMAGE = vk_queue:latest

docker/build/bot:
	@docker build -t $(IMAGE_SPARK_UWSGI) -f Dockerfile .

