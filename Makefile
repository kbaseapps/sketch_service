.PHONY: serve

serve:
	docker run -p 5000:5000 -v $(pwd):/kb/module -it kbase_sketch_service
