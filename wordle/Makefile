.PHONY: build build_with_api run_local llm_tests run_mac run_windows doc test clean

build:
	pyinstaller --onefile --noconsole --noconfirm ./src/game.py

build_with_api:
	pyinstaller --onefile --noconfirm ./src/game.py

run_local:
	python ./src/game.py --disable-logging

llm_tests:
	python ./src/llm_tests.py

run_mac:
	./dist/game

run_windows:
	./dist/game.exe

doc:
	doxygen Doxyfile

test:
	PYTHONPATH=src/ pytest -v

clean:
	rm -rf dist build game.spec html wandb
