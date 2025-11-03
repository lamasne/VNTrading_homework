# Quant Researcher Assignment

Solution for the **VNTrading Quantitative Researcher Internship** task.
Time-series analysis and modeling in Python.

## Environment

Python 3.12, managed with **uv** (`pyproject.toml`).
Main libs: `numpy`, `pandas`, `polars`, `matplotlib`, `scikit-learn`.

## Structure

```
inputs/      # provided data files
src/         # code
outputs/     # results
```

## Usage

To set up the environment, unzip archive and open terminal in the project folder. Then, run
```bash
uv venv
uv sync
```

You can run the main script with
```bash
uv run python main.py
```

All required files (`inputs/`, `src/`, `outputs/`, `pyproject.toml`) are included in the archive.