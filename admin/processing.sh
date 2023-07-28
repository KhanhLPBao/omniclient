#!/bin/bash
signaldir="media/signal"
storagedir="media/storage"
logdir="media/log"
linkdir=$storagedir"/link"

while 0
do
    file_process_count=$( ls $signaldir"/processing" | wc -l )
    case $file_process_count in
        0)
            if [ $(ls $signaldir"/queqe/priority" | wc -l ) -eq 1 ]
            then
                
            else
            fi
        ;;
        *)

        ;;

    esac

done