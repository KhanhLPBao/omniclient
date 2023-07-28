#!/bin/bash
signaldir="media/signal"
storagedir="media/storage"
logdir="log/session"
linkdir=$storagedir"/link"

movefile(){
    priority_count=$( ls $signaldir"/processing/*_1_*.request" | wc -l )
    priority_await=$( ls $signaldir"/queqe/priority/*.request" | wc -l )

    if [ $priority_await -gt 1 ]
    then
        workdate=$( date "+%d/%m/%y" )
        worktime=$( date "+%H:%M:%S" )

        #LOG
        echo $worktime" - Detect "$(( priority_await - 1 ))" requestes from priority queqe - Moving... "\
        >> $logdir"/"$workdate"_queqe.adminlog"
        #END LOG 
        
        for file in $signaldir"/queqe/priority/*.request" #Move priority request
        do
            if [ "$file" != $signaldir"/queqe/priority/*.request" ]
            then
                priority_count+=1
                name_origin=$( basename $file )
                name_new=$count"_1_"$name_origin
                mv -f $file $signaldir"/processing/"$name_new                
            fi
        done
    fi
    #Rename all normal files to match with new queqe
        #LOG
    echo $worktime" - Resorting normal requests... "\
    >> $logdir"/"$workdate"_queqe.adminlog"
        #END LOG     
    n=$priority_count
    for file in $signaldir"/processing/*_0_*.request"
    do
        if [ "$file" != $signaldir"/processing/*_0_*.request" ]
        then
            n+=1
            b=`basename $file`
            filename=`echo $b | cut -d "_" -f 3`
            old_count=`echo $b | cut -d "_" -f 1`
            newname=$n"_0_"$filename
            mv -f $file $signaldir"/processing/"$newname
        fi
    done

    normal_count=$(ls $signaldir"/queqe/normal" | wc -l )
    if [ $normal_count -gt 1 ]
    then
        count=$( ls $signaldir"/processing/*.request" | wc -l )
        #LOG
        echo $worktime" - Detect "$(( normal_count - 1 ))" requestes from normal queqe - Moving... "\
        >> $logdir"/"$workdate"_queqe.adminlog"
        #END LOG

        for file in $signaldir"/queqe/normal/*.request" #Move normal request
        do
            if [ "$file" != $signaldir"/queqe/normal/*.request" ]
            then
                name_normal_origin=$( basename $file )
                name_normal_new=$count"_0_"$name_origin            
                mv -f $file $signaldir"/processing/"$name_normal_new
                count+=1
            fi
        done
    fi
}

resort(){
    count=1

}

while :
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

    movefile
    sleep 1m
done