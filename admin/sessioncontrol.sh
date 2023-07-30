#!/bin/bash
maindir="~/Program/maindir/maindir.txt"
signaldir=$( echo $maindir -d ";" -f 1 )
storagedir=$( echo $maindir -d ";" -f 1 )

logdir="log/control"
errordir=$storagedir"/error"
statusdir=$storagedir"/status"
scriptdir="~/Programs/scripts/admin/python/"
workingdir=$signaldir"/working/"
processir=$signaldir"/processing"

session_working="session/working.l"
session_done="session/done"
session_error="session/error"
session_status="session/status"

checksession(){
    ss=( )
    IFS=" " read -r -a $ss <<< $session_working #input array
    if [[ " ${ss[*]} " =~ *"$1"*]]
    then
        pass
    else
        #regis session
        python $scriptdir"/regissession.py" $1
    fi

    for a in ${ss[@]}
    do       
        python $scriptdir"/sessioncheck.py scan " $a
        status=`cat $sessoionstatus"/"$a".s"`
        case $status in
            e)          #Error
                python $scriptdir"/sessioncheck.py error " $a
                ss=( "${ss[@]}/$a" )
                echo ${ss[@]} > $session_working
            ;;
            c)          #Completed
                python $scriptdir"/sessioncheck.py done " $a
                ss=( "${ss[@]}/$a" )
                workdate=$( date "+%d/%m/%y" )
                worktime=$( date "+%H:%M:%S" )
                echo $a"-"$worktime >> $session_done"/"$workdate".l"
            ;;
            *)
                pass
            ;;
        esac
    done
}

while 0
do
    for file in $processir
    do
        session=`echo $( basename $file ) | cut -d "_" -f 3`
        checksession $session
    done
    sleep 2m
done
