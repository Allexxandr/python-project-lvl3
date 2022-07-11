install:
	poetry install

loader:
	poetry run page_loader https://www.google.com

debug-loader:
	poetry run page_loader -l DEBUG https://www.google.com

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl

lint:
	poetry run flake8 page_loader

test:
	poetry run pytest -vv --color=yes
