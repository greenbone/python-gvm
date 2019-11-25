# Release Instructions

Before creating a new release carefully consider the version number of the new
release.  We are following [Semantic Versioning](https://semver.org/) and
[PEP440](https://www.python.org/dev/peps/pep-0440/).

## Preparing the Required Python Packages

* Install twine for pypi package uploads and update setuptools, pipenv and wheel packages:

  ```sh
  python3 -m pip install --user --upgrade twine setuptools wheel pipenv
  ```

## Preparing the Release

* Fetch upstream changes and create a branch:

  ```sh
  git fetch upstream
  git checkout -b create-new-release upstream/master
  ```

* Open `gvm/__init__.py` and increment the version number. For example, if the
  file contains `VERSION = (2, 1, 0, 'dev', 1)`, the line should be changed to
  `VERSION = (2, 1, 0)`.

* Update the `CHANGELOG.md` file:
  * Change `[unreleased]` to new release version.
  * Add a release date.
  * Update reference to Github diff.
  * Remove empty sub sections like *Deprecated*.

* Create a git commit:

  ```sh
  git add .
  git commit -m "Prepare release <version>"
  ```

## Configuring the Access to the Python Package Index (PyPI)

*Note:* This is only necessary for users performing the release process for the
first time.

* Create an account at [Test PyPI](https://packaging.python.org/guides/using-testpypi/).

* Create an account at [PyPI](https://pypi.org/).

* Create a pypi configuration file `~/.pypirc` with the following content (Note:
  `<username>` must be replaced):

  ```ini
  [distutils]
  index-servers =
      pypi
      testpypi

  [pypi]
  username = <username>

  [testpypi]
  repository = https://test.pypi.org/legacy/
  username = <username>
  ```

## Uploading to the PyPI Test Instance

* Create a source and wheel distribution:

  ```sh
  rm -rf dist build python_gvm.egg-info
  python3 setup.py sdist bdist_wheel
  ```

* Upload the archives in `dist` to [Test PyPI](https://test.pypi.org/):

  ```sh
  twine upload -r testpypi dist/*
  ```

* Check if the package is available at <https://test.pypi.org/project/python-gvm>.

## Testing the Uploaded Package

* Create a test directory:

  ```sh
  mkdir python-gvm-install-test
  cd python-gvm-install-test
  pipenv run pip install --pre -I --extra-index-url https://test.pypi.org/simple/ python-gvm
  ```

* Check install version with a Python script:

  ```sh
  pipenv run python -c "from gvm import get_version; print(get_version())"
  ```

* Remove test environment:

  ```sh
  pipenv --rm
  cd ..
  rm -rf python-gvm-install-test
  ```

## Performing the Release on GitHub

* Create a pull request (PR) for the earlier commit:

  ```sh
  git push origin
  ```
  Open GitHub and create a PR against <https://github.com/greenbone/python-gvm>.

* Ask another developer/maintainer to review and merge the PR.

* Once the PR is merged, update the local `master` branch:

  ```sh
  git fetch upstream
  git rebase upstream/master master
  ```

* Create a git tag:

  ```sh
  git tag v<version>
  ```

  Or even a tag signed with a personal GPG key:

  ```sh
  git tag --sign --message "Tagging the <version> release" v<version>
  ```

## Uploading to the 'real' PyPI

* Create the final distribution files:

  ```sh
  rm -rf dist build python_gvm.egg-info
  python3 setup.py sdist bdist_wheel
  ```

* Upload the archives in `dist` to [PyPI](https://pypi.org/):

  ```sh
  twine upload dist/*
  ```

* Check if new version is available at <https://pypi.org/project/python-gvm>.

## Bumping `master` Branch to the Next Version

* Open `gvm/__init__.py` and increment the version number to the next
  *development* version number. For example, if the file contains
  `VERSION = (2, 1, 0)`, it should be changed to `VERSION = (2, 2, 0, 'dev', 1)`.

* Create a commit for the version bump:

  ```sh
  git add gvm/__init__.py
  git commit -m "Update version after <version> release"
  ```

## Announcing the Release

* Push changes and tag to the `master` branch on Github:

  ```sh
  git push --tags upstream master
  ```

* Create a Github release:

  See https://help.github.com/articles/creating-releases/
