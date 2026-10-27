.PHONY: test bench doctor run docker

test:
	python -m unittest discover -s tests -t .

bench:
	python -m simulforge.bench

doctor:
	python -m simulforge.cli doctor

run:
	python -m simulforge.cli serve --host 0.0.0.0 --port 8432

docker:
	docker build -t simulforge:latest .
