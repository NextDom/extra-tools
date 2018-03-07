#!/bin/bash

pluginName=$1;

sed '/[extra][/extra]/r ../contents/add-assistant.txt'  plugin/desktop/$pluginName.php > plugin/desktop/$pluginName.php
