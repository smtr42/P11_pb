#!/bin/sh

black --line-length=79 .
docformatter --recursive --in-place .
isort -rc .
flake8