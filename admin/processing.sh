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
while :
do
    workdate=$( date "+%d/%m/%y" )
    worktime=$( date "+%H:%M:%S" )

    if [ $(ls $processdir | wc -l ) -gt 0 ] && \
    [ (ls $workingdir | wc -l ) -eq 0 ]
    then
        nextfile=$( ls $processdir | cut -d " " -f 1 )
        filename=`basename $nextfile | cut -d "." -f 2`
        sessionid=`echo $filename | cut -d "_" -f 3`
        contentfile=$sessiondir"/"$sessionid".contents"
        if [ -f  $contentfile ]
        then
            contents= ( )
            mv -f $contentfile $workingdir"/"$sessionid".contents"
            while IFS= read -r $LINE
            do
                contents+=$LINE
            done < $workingdir"/"$sessionid".contents"
            
            method=""
            sample=( )
            for d in ${contents[@]}
            do
                prefix=$( echo $d | cut -d " " -f 1 )
                case $prefix in
                    method)
                        method=$( echo $d | cut -d " " -f 2 )
                    ;;
                    sample)
                        sample+=$( echo $d | cut -d " " -f 2 )     
                    ;;
                    *)
                        pass
                    ;;
                esac
            if [ "$method" == "" ]
            then
        #LOG
                echo "$worktime - Session $sessionid encountered Method Null error, moved to errordir" >> \
                $logdir"/"$workdate".adminlog"
        #END LOG
                echo "S1" > $statusdir"/"$sessionid".sessionstatus" #S1 Error: No method indicated
                mv -f $nextfile $errordir"/"
            else
                if [ ! -f $storagedir"/method/"$method".sh" ]
                then
s
                    echo "$worktime - Session $sessionid encountered Method Wrong error, moved to errordir" >> \
                    $logdir"/"$workdate".adminlog"
            #END LOG
                    echo "S2" > $statusdir"/"$sessionid".sessionstatus" #S1 Error: No method indicated in server
                    mv -f $nextfile $errordir"/"
                else
                    bash $storagedir"/method/"$method".sh" $sample
                fi
            fi
        else
        #LOG
            echo "$worktime - Session $sessionid invalid, moved to errordir" >> \
            $logdir"/"$workdate".adminlog"
        #END LOG
            echo "S0" > $statusdir"/"$sessionid".sessionstatus" #S0 Error: No content file
            mv -f $nextfile $errordir"/"
        fi
    fi
    sleep 1m
done