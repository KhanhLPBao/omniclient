#!/bin/bash
maindir="~/Program/maindir/maindir.txt"
signaldir=$( echo $maindir -d ";" -f 1 )
storagedir=$( echo $maindir -d ";" -f 1 )

logdir="log/control"
errordir=$storagedir"/error"
statusdir=$storagedir"/status"
scriptdir="~/Programs/scripts/admin/python/"
workingdir=$signaldir"/working/"

