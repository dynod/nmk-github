# nmk-github
Github plugin for **`nmk`** build system

<!-- NMK-BADGES-BEGIN -->
[![License: MIT License](https://img.shields.io/github/license/dynod/nmk-github)](https://github.com/dynod/nmk-github/blob/main/LICENSE)
[![Checks](https://img.shields.io/github/actions/workflow/status/dynod/nmk-github/build.yml?branch=main&label=build%20%26%20u.t.)](https://github.com/dynod/nmk-github/actions?query=branch%3Amain)
[![Issues](https://img.shields.io/github/issues-search/dynod/nmk?label=issues&query=is%3Aopen+is%3Aissue+label%3Aplugin%3Agithub)](https://github.com/dynod/nmk/issues?q=is%3Aopen+is%3Aissue+label%3Aplugin%3Agithub)
[![Supported python versions](https://img.shields.io/badge/python-3.9%20--%203.13-blue)](https://www.python.org/)
[![PyPI](https://img.shields.io/pypi/v/nmk-github)](https://pypi.org/project/nmk-github/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://astral.sh/ruff)
[![Code coverage](https://img.shields.io/codecov/c/github/dynod/nmk-github)](https://app.codecov.io/gh/dynod/nmk-github)
[![Documentation Status](https://readthedocs.org/projects/nmk-github/badge/?version=stable)](https://nmk-github.readthedocs.io/)
<!-- NMK-BADGES-END -->

This plugin adds support for Github features in an **`nmk`** project:
* [Github workflow file](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) generation
* README badges generation (if [**`nmk-badges`**](https://github.com/dynod/nmk-badges) plugin is also used):
  * link to license
  * build action status
  * opened issues

## Usage

To use this plugin in your **`nmk`** project, insert this reference:
```
refs:
    - pip://nmk-github!plugin.yml
```

## Documentation

This plugin documentation is available [here](https://nmk-github.readthedocs.io/)

## Issues

Issues for this plugin shall be reported on the [main  **`nmk`** project](https://github.com/dynod/nmk/issues), using the **plugin:github** label.
