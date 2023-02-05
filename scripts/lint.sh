#! /bin/sh
pylint $(git ls-files '*.py') --disable=C0114,C0116,E0401 --fail-under=9
