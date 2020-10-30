version:
	pycryptex --version

test:
	pytest -v

deploy_test: clean
	@echo "deploy on test..."
	@python3 setup.py bdist_wheel sdist
	twine upload dist/* --repository testpypi
	@echo "done!"

deploy: clean
	@echo "deploy on prod..."
	@python3 setup.py bdist_wheel sdist
	twine upload dist/*
	@echo "done!"

clean:
	@printf "clean dist and build folders..."
	@rm -rf dist/* build/*
	@printf "clean done!\n"