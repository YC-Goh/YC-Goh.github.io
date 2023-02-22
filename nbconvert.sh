#!/bin/bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate base-python
jupyter nbconvert --to markdown ./public/*/*.ipynb
