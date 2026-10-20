.PHONY: doctor bench test serve

doctor:
	python -m taskforge doctor

bench:
	python -m taskforge bench

test:
	python -m unittest discover -s taskforge/tests -t .

serve:
	python -m taskforge serve --host 127.0.0.1 --port 8787
