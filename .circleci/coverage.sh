#!/bin/bash

export PATH="$HOME/miniconda/bin:$PATH"
source activate test

coveralls
