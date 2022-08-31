
tox-recreate causes tox to recreate its virtualenv's if your `setup.cfg` file has changed.

Normally tox will automatically trigger a recreation of the venv if the test
`deps` in `tox.ini` have changed. But what about your package's requirements in
the `install_requires` setting in `setup.cfg`? If those change tox won't
automatically recreate the venv, you're expected to run `tox --recreate`
yourself.

tox-recreate keeps track of the hash of your `setup.cfg` file and triggers tox
to recreate your venvs if it changes.
