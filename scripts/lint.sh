#! /bin/sh
pylint $(git ls-files '*.py') --disable=C0114,C0116 --fail-under=9
