#!/bin/bash
sessiondir="/mnt/share/source/debug/signal/session"
scriptdir="/mnt/share/source/omniclient/admin/python"   #directory of python script
sessionname=$(cat $1 | cut -d "==" -f 3)

if [ -d $sessiondir/$sessionname ]
then
    reg_session=$(python $scriptdir"/system/sessioninit.py" $sessionname)
fi