setup:
	if [[ "$(VIRTUAL_ENV)" != "" ]]; then deactivate; fi
	pip install --target=./virtualenv/ virtualenv
	python ./virtualenv/virtualenv.py -p python3 venv

	bash -c "source venv/bin/activate; \
	pip install -r requirements.txt;"

client:
	if [[ "$(VIRTUAL_ENV)" != "" ]]; then deactivate; fi
	bash -c "source venv/bin/activate; \
	python ./src/client.py;"

server:
	if [[ "$(VIRTUAL_ENV)" != "" ]]; then deactivate; fi
	bash -c "source venv/bin/activate; \
	python ./src/server.py;"

clean:
	if [[ "$(VIRTUAL_ENV)" != "" ]]; then deactivate; fi
	rm -rf venv
	rm -rf virtualenv
