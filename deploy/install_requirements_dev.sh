#!/bin/bash

REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../" && pwd )"

pip install --user -U pip setuptools wheel
pip install --user -U -r "$REPO_DIR/deploy/requirements.txt"
