#/bin/bash
# Scan for request and proceeded based on the extension
# Also act as the distributor
# Directory
req_input=$1
req_type=$2
req_output="/mnt/share/source/debug/omniclient/output"
scriptdir="/mnt/share/source/omniclient"
req_progress="/mnt/share/source/debug/omniclient/node"    #location of all processing jobs
processdir="/mnt/share/source/debug/signal/processing"
logindir="/mnt/share/source/debug/loginserver/input"
seqdir="/mnt/share/source/debug/omniclient/interface_response"
case $req_type in
    admin)  #Execute registration request from omniadmin
        echo "Admin request for $req_input detected"
        
        if [ "$debug_aug" == "--debug" ]
        then
            echo "python $scriptdir/admin/python/system/sessioninit.py $req_input $debug_aug"
        fi
        python $scriptdir"/admin/python/system/sessioninit.py" $req_input $debug_aug
    ;;
    request)  #Decode request first to validate
        python $scriptdir"/admin/python/request.py" $req_input
    ;;
    register)
        loginfile=`basename $req_input`
        docker cp $loginfile loginserver:/mnt/server/in
        rm $req_input
        docker exec -d loginserver /bin/python3 /home/software/login/login.sh $loginfile register
    ;;
    login)   #Decode and answer login request
        loginfile=`basename $req_input`
        loginseq=$(echo $loginfile | cut -d '.' -f 1)
        echo "Begin to copy loginfile $loginfile"
        docker cp $req_input loginserver:/mnt/server/in
        docker cp $seqdir/$loginseq.seq loginserver:/mnt/server/in
        rm $req_input
        docker exec loginserver /bin/python3 /home/software/login/login.py $loginseq login > $seqdir/$loginseq.log
    ;;
esac


