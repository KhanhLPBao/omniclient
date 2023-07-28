#!/bin/bash
signaldir="media/signal"
storagedir="media/storage"
logdir="media/log"
linkdir=$storagedir"/link"
###################################3
# Requestest from GUI come at 2 files: .request and .contents
# .request contain session id and priority status
# .contents contain filename and method to get it

while 0
do
    for request in $signaldir"/request/*.request"
    do
        if [ "$( basename $request )" != "*.request" ]
        then
            account=$( basename $request | cut -d "." -f 1 | cut -d "-" -f 2 )
            normalcount=$( ls $signaldir"/queqe/normal" | wc -l ) 
            prioritycount=$( ls $signaldir"/queqe/priority" | wc -l )     
            queqebefore=$(( $normalcount + $prioritycount ))
            content=`cat $request`
            session=`cut -d " " -f 1 $content`
            prio=`cut -d " " -f 2 $content`
            case $prio in
                0)
                    priority="normal"
                    session_queqe=$(( $( cat $signaldir"/queqe/normal/number" ) + 1 ))
                    echo $session_queqe > $signaldir"/queqe/normal/number"
                ;;
                1)
                    priority="high"
                    session_queqe=$(( $( cat $signaldir"/queqe/priority/number" ) + 1 ))
                    echo $session_queqe > $signaldir"/queqe/priority"/number
                ;;
            esac
            echo "Account $account request session $session as $priority priority, \
            number of Session(s) need to reprocess before this: $queqebefore ))" \
            > $logdir"/"$( date "+%d/%m/%y-%H:%M:%S" )"_"$account"_add.log"
            mv -f $request $signaldir"/queqe/"$priority"/"$session_queqe"_"$session".request"
            mkdir $storagedir"/storage/"$session
            mv -f $signaldir"/request/"$session.contents $storagedir"/storage/"$session"/filenames.files"
        fi
    done
done
