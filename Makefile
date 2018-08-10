.PHONY: serve build


build:
	docker build . -t kbase_sketch_service --no-cache

serve:
	docker run --net host -p 5000:5000 -v $(shell pwd):/kb/module -it kbase_sketch_service

test:
	docker run --net host -v $(shell pwd):/kb/module -it kbase_sketch_service test
