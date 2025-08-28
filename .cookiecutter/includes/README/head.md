tox-recreate causes tox to automatically recreate its virtualenvs if your
`pyproject.toml`, `setup.cfg` or `setup.py` files have changed.

Normally tox will automatically trigger a recreation of the venv if the test
`deps` in `tox.ini` have changed. But what about your package's requirements in
`pyproject.toml`, `setup.cfg` or `setup.py`? If those change tox won't
automatically recreate the venv, you're expected to run `tox --recreate`
yourself.

tox-recreate keeps track of the hashes of your `pyproject.toml`, `setup.cfg`
and `setup.py` files and triggers tox to recreate your venvs if they change.
