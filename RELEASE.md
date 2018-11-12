# Release instructions

* Install twine for pypi package uploads and update setuptools, pipenv and wheel packages

  ```sh
  python3 -m pip install --user --upgrade twine setuptools wheel pipenv
  ```

* Open [gvm/__init__.py](https://github.com/greenbone/python-gvm/blob/master/gvm/__init__.py)
  and increment the version number.

* Create a source and wheel distribution

  ```sh
  rm -rf dist build
  python3 setup.py sdist bdist_wheel
  ```

* Create an account at [Test PyPI](https://packaging.python.org/guides/using-testpypi/)

* Upload the archives in dist to [Test PyPI](https://test.pypi.org/)

  ```sh
  twine upload --repository-url https://test.pypi.org/legacy/ dist/*
  ```

* Check if the package is available at https://test.pypi.org/project/python-gvm

* Create a test directory

  ```sh
  mkdir python-gvm-install-test
  cd python-gvm-install-test
  pipenv run pip install --extra-index-url https://test.pypi.org/simple/ python-gvm
  ```

* Check install version with a python script

  ```sh
  pipenv run python -c "from gvm import get_version; print(get_version())"
  ```

* Remove test environment

  ```sh
  pipenv --rm
  cd ..
  rm -rf python-gvm-install-test
  ```

* Create an account at [PyPI](https://pypi.org/) if not exist already

* Upload to real [PyPI](https://pypi.org/)

  ```sh
  twine upload dist/*
  ```

  * Check if new version is available at https://pypi.org/project/python-gvm

  * Create a git tag

    ```sh
    git tag v<version>
    ```

    or even signed with your gpg key

    ```sh
    git tag -s v<version>
    ```

  * Push the tag to Github

    ```sh
    git push --tags upstream
    ```

  * Create a github release

    *TODO*
