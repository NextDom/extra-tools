#!/bin/bash
pluginName=$1
find ./ -type f -print0 | xargs -0 sed -i 's/template/'$pluginName'/g'
