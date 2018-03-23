#!/bin/sh

python3 -m pylint --rcfile=tests/.pylintrc tools.py
# Tests des sources
for file in `find scripts/ -name "*.py" ! -name "__init__.py"`;
do
    echo "Check $file with pylint"
    python3 -m pylint --rcfile=tests/.pylintrc $file
done

for file in `find scripts/libs -name "*.py" ! -name "__init__.py"`;
do
    echo "Check $file with pylint"
    python3 -m pylint --rcfile=tests/.pylintrc $file
done
exit()
# Tests des tests
for file in `find tests/ -name "*.py" ! -name "__init__.py"`;
do
    echo "Check $file with pylint"
    python3 -m pylint --rcfile=tests/.pylintrc_tests $file
done
