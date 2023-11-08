#!/bin/bash
progressdir=""
sessionout=""
statusdir=""
sessionin=$1

sessiondir="$inputdir/$sessionin"
fileprevious=""
mv -f $sessiondir $progressdir
wait=1

tier3=1            #if docker container is running tier 3 jobs, set to 1
tier3rules=`cat tier3rules.txt`  #specifically for jobs at tier 3, 

while [[ $wait -eq 1 ]]
do
done
    fileprevious=$( python queqe.py check $sessionin )
    if [[ "$fileprevious"=="" ]]    #session on top, gained permission to begin
    then
        case $tier3 in
        1)
            IFS=',' read -ra rules <<< "$tier3rules"
            for rule in "${rules[@]}"
            do
                ./snakemake -s mainscript -R $rule --config session="'$sessionin'" 
            done
            wait=0
        ;;
        *)
            ./snakemake -s mainscript --config session="'$sessionin'"
            wait=0
        ;;
        esac
        #   <Responses equally to each result>  #
    else
        sleep 1m
    fi
done
