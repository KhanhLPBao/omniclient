signaldir="/mnt/signal"
clustername=$( hostname )
storagedir="/"$clustername
sleep=5     #Time between retry during login
maxtry=3    #number of maximum try before timedout
run(){
    listprogram=( )
    while IFS= read -r prog
    do  
        listprogram+=( $prog )
    done < $signaldir"/program/"$clustername"/prog.list"

    for task in $signaldir"/"$clustername"/in/*.txt"
    do
        if [[ "task" != $signaldir"/"$clustername"/in/*.txt" ]]
        then
            runnum=`cat program/runnum.txt`
            session=$( basename $task | cut -d "." -f 1 )
            filename=( )
            while IFS= read -r file
            do
                filename+=( $file )
            done < $task
            for mau in ${filename[@]}
            do
                echo $( date "+%d/%m/%y-%H:%M:%S" )" - Run "$[ runnum+1 ]" - Account $account - Session $session - File: $mau" > \
                $storagedir"/"$clustername"/log/Run_"$[ runnum + 1 ]".log"
                for p in ${ listprogram[@] }
                do
                    scriptname=$( cut -d "." -f 1 $p )
                    progname=$( cut -d "." -f 1 $p )
                    progress=$( snakemake -c 1 -s "program/"$scriptname $progname --config SAMPLE="'$mau'" id="'$session'" >\
                    $storagedir"/log/"$session".log" )
                    case $progress in
                        0)
                        echo 0 > $signaldir"/"$clustername"/out/"$session"_"$mau
                        ;;
                        *)
                        echo 1 > $signaldir"/"$clustername"/out/"$session"_"$mau
                        ;;
                    esac
                done
            done    
        fi
}

