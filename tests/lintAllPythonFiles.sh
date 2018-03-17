#!/bin/sh

for file in `find . -name "*.py"`;
do
    echo $file
    pylint --disable=C --disable=R --disable=W $file
done
