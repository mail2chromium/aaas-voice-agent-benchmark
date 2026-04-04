.PHONY: benchmark charts report install clean

install:
	pip install -r requirements.txt

benchmark:
	python benchmarks/crm_workflow.py
	python benchmarks/cost_calculator.py

charts:
	python -c "from benchmarks.cost_calculator import run_comparison; run_comparison()"

report: benchmark charts
	@echo "✓ Full report generated in results/"

clean:
	rm -rf results/charts/*.png
	rm -rf __pycache__ **/__pycache__
