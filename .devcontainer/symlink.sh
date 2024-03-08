#!/bin/bash

NAME=$(python3 -c 'print(eval(open("package").read())["name"])')

ln -sv $WORKSPACE $OMD_ROOT/local/lib/python3/cmk_addons/plugins/$NAME