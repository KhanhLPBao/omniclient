#!/bin/bash
signaldir="media/signal"
storagedir="media/storage"
logdir="log/processing"
linkdir=$storagedir"/link"

movefile(){
    count=$1
    priority_count=$(ls $signaldir"/queqe/priority" | wc -l )
    if [ $priority_count -gt 1 ]
    then
        workdate=$( date "+%d/%m/%y" )
        worktime=$( date "+%H:%M:%S" )
        #LOG
        echo $worktime" - Detect "$(( priority_count - 1 ))" requestes from priority queqe - Moving... "\
        >> $logdir"/"$workdate
        #END LOG 
        
        for file in $signaldir"/queqe/priority/*.request" #Move priority request
        do
            if [ "$file" != $signaldir"/queqe/priority/*.request" ]
            then
                name_origin=$( basename $file )
                name_new=$count"_"$name_origin
                mv $file $signaldir"/processing/"$name_new
                count+=1
            fi
        done
    fi

    normal_count=$(ls $signaldir"/queqe/normal" | wc -l )
    if [ $normal_count -gt 1 ]
    then
        #LOG
        echo $worktime" - Detect "$(( normal_count - 1 ))" requestes from normal queqe - Moving... "\
        >> $logdir"/"$workdate
        #END LOG

        for file in $signaldir"/queqe/normal/*.request" #Move normal request
        do
            if [ "$file" != $signaldir"/queqe/normal/*.request" ]
            then
                name_normal_origin=$( basename $file )
                name_normal_new=$count"_"$name_origin            
                mv $file $signaldir"/processing/"$name_normal_new
            fi
        done
    fi
}

while 0
do
    file_process_count=$( ls $signaldir"/processing" | wc -l )
    case $file_process_count in
        0)
            count=1                        
        ;;
        *)
            count=$file_process_count
        ;;
    esac

    movefile $count
    sleep 1m
done