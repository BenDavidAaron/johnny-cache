#! /bin/sh
black --check --diff --line-length=80 $(git ls-files '*.py')
