#!/bin/sh

python3 -m pylint --rcfile=tests/.pylintrc --output-format=colorized tools.py

# Tests des tests
#for file in `find tests/ -name "*.py" ! -name "__init__.py"`;
#do
#    echo "Check $file with pylint"
#    python3 -m pylint --rcfile=tests/.pylintrc_tests --output-format=colorized $file
#done
