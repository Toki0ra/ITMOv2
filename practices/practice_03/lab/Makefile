.PHONY: install test experiment-baseline experiment-system
install:
	@python3 -c "import sys; assert sys.version_info >= (3,10), 'Python 3.10+ required'; print('Standard library only: ready')"
test: install
	$(MAKE) -C demo test

# Простые эксперименты с локальной моделью Ollama (см. experiment.py)
experiment-baseline:
	@mkdir -p records 2>/dev/null || true
	python3 experiment.py --mode baseline --output records/baseline.json

experiment-system:
	@mkdir -p records 2>/dev/null || true
	python3 experiment.py --mode system --output records/system.json

