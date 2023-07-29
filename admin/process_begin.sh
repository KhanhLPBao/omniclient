#!/bin/bash
signaldir="media/signal"
storagedir="media/storage"
logdir="log/processing"
linkdir=$storagedir"/link"
workingdir=$signaldir"/working/"
processdir=$signaldir"/processing"
sessiondir=$signaldir"/sessions"
errordir=$storagedir"/error"
statusdir=$storagedir"/status"
scriptdir="~/Programs/scripts/admin/python/"
while :
do
    #<code>
        #<IF>
    if [ $( ls -l $workingdir"/*" | wc -l ) -eq 1 ]
    then
        for file in $workingdir"/*"
        do
            #<IF>
            if [ "$file" != $workingdir"/*" ]
            then
                filename=`basename $file`
                sessionid=$( echo $filename | cut -d "." -f 1 )
                prog_check=$( python $scriptdir"/extractsession.py" \
                    $sessionid $file )
                case $prog_check in
                    0)
                        pass
                    ;;
                    *)  #ERROR
                        pass
                    ;;
                esac
            fi
            #</IF>
            python preparescripts.py $sessionid $file
        done
    fi
        #{/IF}
    #<end code>
    sleep 1m 
done