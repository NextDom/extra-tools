#!/bin/bash
touch /tmp/Template_dep
echo 0 > /tmp/Template_dep

if [[ $EUID -ne 0 ]]; then
  sudo_prefix=sudo;
fi

echo "############################################################################"
echo "# Installation in progress"
echo "############################################################################"
[extra]@@add-dependencies@@[/extra]
echo 50 > /tmp/Template_dep

[extra]@@add-linking-scripts@@[/extra]
echo 75 > /tmp/Template_dep


[extra]@@add-symbolic-link@@[/extra]
echo 80 > /tmp/Template_dep

echo 100 > /tmp/Template_dep
rm /tmp/Template_dep
echo "############################################################################"
echo "# Installation finnished"
echo "############################################################################"
