.PHONY: help install test run

APP_PATH=./miner/app.py
TEST_PATH=./tests/

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3


.DEFAULT: help
help:
	@echo "First time only use one of the install options below:"
	@echo "make installubuntu"
	@echo "    prepare development environment using apt (Ubuntu)"
	@echo "make installarch"
	@echo "    prepare development environment using pacman (Arch based)"
	@echo " "
	@echo "After installing all requirements you can use:"
	@echo "make test"
	@echo "    run tests in main modules using pytest"
	@echo "make runall"
	@echo "    run all agents in two different example maps"
	@echo "make run MAP=./file.map ALG=ALGORITHM LIMIT=L"
	@echo "    run a specific algorithm and map file"
	@echo "    ex.: make run MAP=./tests/mini.map ALG=LDS LIMIT=10"


installubuntu:
	sudo apt -y install python3 python3-pip
	python3 -m pip install poetry
	poetry install
	poetry shell


installarch:
	sudo pacman -Syu python3 pip
	pip install --user poetry
	poetry install
	poetry shell


test:
	pytest --verbose --color=yes


runall:
	@echo "Projeto desenvolvido para a disciplina INE5430"
	@echo "Aluno: Diogo Junior de Souza"
	@echo "Matricula: 16100721"
	@echo "Running all agents in mini example map"
	python $(APP_PATH) $(TEST_PATH)mini.map LDS 20
	python $(APP_PATH) $(TEST_PATH)mini.map BFS 20
	python $(APP_PATH) $(TEST_PATH)mini.map Astar
	python $(APP_PATH) $(TEST_PATH)mini.map ImprovedAstar
	@echo " "
	@echo "Running all agents in required example map"
	python $(APP_PATH) $(TEST_PATH)example.map LDS 100
	python $(APP_PATH) $(TEST_PATH)example.map BFS 100
	python $(APP_PATH) $(TEST_PATH)example.map Astar
	python $(APP_PATH) $(TEST_PATH)example.map ImprovedAstar

run:
	python $(APP_PATH) $(MAP) $(ALG) $(LIMIT)