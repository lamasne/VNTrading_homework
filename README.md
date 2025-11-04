# Quant Researcher Assignment

Solution for the **VNTrading Quantitative Researcher Internship** task.
Time-series analysis and modeling in Python.

## Environment

Python 3.12, managed with **uv** (`pyproject.toml`).
Main libs: `numpy`, `pandas`, `matplotlib`.

## Structure

```
inputs/      # provided data files
outputs/     # generated plots and report
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