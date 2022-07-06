<a href="https://github.com/hypothesis/tox-recreate/actions/workflows/ci.yml?query=branch%3Amain"><img src="https://img.shields.io/github/workflow/status/hypothesis/tox-recreate/CI/main"></a>
<a href="https://pypi.org/project/tox-recreate"><img src="https://img.shields.io/pypi/v/tox-recreate"></a>
<a><img src="https://img.shields.io/badge/python-3.10 | 3.9 | 3.8-success"></a>
<a href="https://github.com/hypothesis/tox-recreate/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-BSD--2--Clause-success"></a>
<a href="https://github.com/hypothesis/cookiecutters/tree/main/pypackage"><img src="https://img.shields.io/badge/cookiecutter-pypackage-success"></a>
<a href="https://black.readthedocs.io/en/stable/"><img src="https://img.shields.io/badge/code%20style-black-000000"></a>

# tox-recreate

Recreate tox virtual environments when setup.cfg changes.

For installation instructions see [INSTALL.md](https://github.com/hypothesis/tox-recreate/blob/main/INSTALL.md).

For how to set up a tox-recreate development environment see
[HACKING.md](https://github.com/hypothesis/tox-recreate/blob/main/HACKING.md).

tox-recreate causes tox to recreate its virtualenv's if your `setup.cfg` file has changed.

Normally tox will automatically trigger a recreation of the venv if the test
`deps` in `tox.ini` have changed. But what about your package's requirements in
the `install_requires` setting in `setup.cfg`? If those change tox won't
automatically recreate the venv, you're expected to run `tox --recreate`
yourself.

tox-recreate keeps track of the hash of your `setup.cfg` file and triggers tox
to recreate your venvs if it changes.
