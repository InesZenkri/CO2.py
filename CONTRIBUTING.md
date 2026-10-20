# Contributing to CO2.py

Thanks for your interest in CO2.py. Bug reports, fixes and improvements are welcome.

## Reporting issues

[Open an issue](https://github.com/InesZenkri/CO2.py/issues) with a clear description,
steps to reproduce, and any logs or error messages.

## Submitting changes

1. Fork the repository and clone your fork.
2. Create a branch: `git checkout -b feature/your-feature-name`
3. Make your change and add tests.
4. Run the tests (see below) and open a pull request against `main`.

## Development setup

Python 3.9 or newer. The library has no runtime dependencies.

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .
python -m unittest discover -s tests
```

## Changing the methodology

If you change a constant or formula, cite the primary source in the code and in
[docs/METHODOLOGY.md](docs/METHODOLOGY.md), and add a test with a hand-computed value.
