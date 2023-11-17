#/bin/bash
# Scan for request and proceeded based on the extension
# Also act as the distributor
# Directory
req_input=$1
req_type=$2
debug_aug=$3
req_output="/mnt/share/source/debug/omniclient/output"
scriptdir="/mnt/share/source/omniclient"
req_progress="/mnt/share/source/debug/omniclient/node"    #location of all processing jobs
processdir="/mnt/share/source/debug/signal/processing"

if [ "$debug_aug" == "--debug" ]
then
    echo "Debuging mode detected, logs from crucial steps will be outputed to terminal"
else
    debug=""
fi
case $req_type in
    admin)  #Execute registration request from omniadmin
        echo "Admin request for $req_input detected"
        
        if [ "$debug_aug" == "--debug" ]
        then
            echo "python $scriptdir/admin/python/system/sessioninit.py $req_input $debug_aug"
        fi
        python $scriptdir"/admin/python/system/sessioninit.py" $req_input $debug_aug
    ;;
    interface)  #Decode request first to validate
        interface_type=$3
        case $interface_type in
            login)
                decoderesults=$(python "$scriptdir/admin/account/python/account/hashstring.py" "decode" "'$file'" "'$req_token'")
                if [[ ! $decoderesults -eq 5 ]]   #Valid request
                then
                    #   Check account storage folder
                    #   return result: Accept or reject log in
                    accountcompare=$(python "$scriptdir/admin/account/python/account/login.py login $decoderesults")
                    case $accountcompare in
                        accept)
                            token=$(python "$scriptdir/admin/account/python/account/hashstring.py" "token")
                            echo $token > "$req_output/$req_token-response.$typerequest"
                        ;;
                        deny)
                            echo "Deny" > "$req_output/$req_token-response.$typerequest"
                        ;;
                        *)
                            echo "Server Error - $accountcompare" > "$req_output/$req_token-response.$typerequest"
                        ;;
                    esac
                fi
            ;;
            reg)
                decoderesults=$(python "$scriptdir/admin/account/python/account/hashstring.py" "decode" "'$file'" "'$req_token'")
                accountregis=$(python "$scriptdir/admin/account/python/account/login.py reg  $decoderesults")
                case $accountregis in
                    Done)
                        echo "Done" > "$req_output/$req_token-response.$typerequest"
                    ;;
                    *)
                        echo "ERROR - $accountregis" > "$req_output/$req_token-response.$typerequest"
                    ;;
                esac
            ;;
            req)  #Interface request run
                :
                #   Check valid token
                #   Check account permission
                #   Write .request, .jobs, .files files
            ;;
        esac
    ;;
esac


