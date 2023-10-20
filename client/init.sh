#!/bin/bash

if [ ! -d "/home/$USER/program" ]
then
    mkdir "/home/$USER/program"
fi

if [ ! -f "/home/$USER/program/installed" ]
then
    echo 0 > "/home/$USER/program/installed"
else
    signal=`cat /home/$USER/program/installed`
    if [ "$signal" eq "0" ]
    then
        echo "Initial setup"
        bash install.sh
    else
        echo "Initial script"
        bash run.sh
    fi
fi