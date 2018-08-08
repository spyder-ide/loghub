#!/bin/bash

export PATH="$HOME/miniconda/bin:$PATH"
source activate test

pytest -x -vv --cov=loghub --cov-report=term-missing loghub
