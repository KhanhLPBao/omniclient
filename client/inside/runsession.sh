#!/bin/bash
inputdir="/omnipack/debug/omniclient/node/input"
progressdir="/processdir"
sessionout="/omnipack/debug/omniclient/node/output/L2"
statusdir=""
sessionin=$1
scriptdir="omnipack/omniclient/client/inside"
sessiondir="$inputdir/$sessionin"
fileprevious=""
wait=1
tier3=0           #if docker container is running tier 3 jobs, set to 1


if [ "$sessionin" == "debug" ]
then
    wait=0
    echo "Debugging mode enabled"
else
    if [ ! -d $progressdir/$sessionin ]
    then
        echo "Moving files to progression directory"
        mv -f $sessiondir $progressdir
    fi
fi

python $scriptdir/queqe.py add $sessionin

while [[ $wait -eq 1 ]]
do
    fileprevious=$( python $scriptdir/queqe.py check $sessionin )
    if [[ "$fileprevious"=="" ]]    #session on top, gained permission to begin
    then
        case $tier3 in
        1)
            tier3rules=`cat tier3rules.txt`  #specifically for jobs at tier 3, 
            IFS=',' read -ra rules <<< "$tier3rules"
            for rule in "${rules[@]}"
            do
                conda run --name snakemake snakemake --cores all -s mainscript -R $rule --config sessionin="'$sessionin'" sessionout="'$sessionout'"
            done
            wait=0
        ;;
        *)
            conda run --name snakemake snakemake --cores all -s $scriptdir/mainscript --config sessionin="'$sessionin'" sessionout="'$sessionout'"
            wait=0
        ;;
        esac
        echo "=======Results is ========"
        result=$?
        case $result in
        0)
            python $scriptdir/queqe.py delete $sessionin
        ;;
        *)
            python $scriptdir/queqe.py delete $sessionin
        #Extra responses for failed 
        ;;
        esac
        #   <Responses equally to each result>  #
    else
        echo "queqe.py returned with result $fileprevious"
        sleep 1m
    fi
done
