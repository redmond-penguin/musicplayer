#!/bin/bash
PYTHONPATH=$(dirname $0)/..
export PYTHONPATH
cd $(dirname $0)/..
python3 -m unittest discover
