setup: venv
	. .venv/bin/activate && python -m pip install --upgrade pip
	. .venv/bin/activate && pip install -r requirements.txt
	. .venv/bin/activate && python -m ipykernel install --name .env --user

venv:
	test -d .venv || python -m venv .venv

clean:
	rm -rf .venv
	rm .build

clean-pyc:
	find . -name "*.pyc" -exec rm -f {} + 
	find . -name "*.pyo" -exec rm -f {} +
	find . -name "*~" -exec rm -f {} +
	find . -name "__pycache__" -exec rm -fr {} +
