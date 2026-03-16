.PHONY: tests
tests :
	@echo "Running tests..."
	export PYTHONPATH=.  ;\
	echo $$PYTHONPATH ;\
	pytest -v


.PHONY: build
build :
	@echo "Building ${IMAGE} docker image."
	docker build -t ${IMAGE} .

.PHONY: run
run : build 
	@echo "Build and run the container ${IMAGE} with port ${PORT}:${PORT}"
	docker run -p ${PORT}:${PORT} -e PORT=${PORT} ${IMAGE}