.PHONY: serve build


build:
	docker build . -t kbase_sketch_service --no-cache

serve:
	docker run -p 5000:5000 -v $(pwd):/kb/module -it kbase_sketch_service
