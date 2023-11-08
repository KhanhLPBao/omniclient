#/bin/bash
# Scan for request and proceeded based on the extension
# Also act as the distributor
# Directory
req_input="/mnt/share/source/debug/omniclient/input"
req_output="/mnt/share/source/debug/omniclient/output"
req_progress="/mnt/share/source/debug/omniclient/progress"
scriptdir="/mnt/share/source/omniclient"
#
for file in req_input/*
do
    if [ -f $file ]
    then
        req_token=$(basename $file | cut -d '.' -f 1)
        typerequest=$(basename $file | cut -d '.' -f 2)
        #Create local value
        #
        case $typerequest in
            admin)  #Execute registration request from omniadmin
                bash $scriptdir/admin/system/requesttransfer.sh $req_token
                mkdir $req_progress/$req_token
                mv $file $req_progress/$req_token
            ;;
            interface_login)  #Decode request first to validate
                decoderesults=$(python "$scriptdir/admin/account/python/account/hashstring.py" "decode" "'$file'" "'$req_token'")
                if [[ ! $decoderesults -eq 5 ]]   #Valid request
                then
                    #   Check account storage folder
                    #   return result: Accept or reject login
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
            interface_registration)
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
            interface_request)  #Interface request run
                :
                #   Check valid token
                #   Check account permission
                #   Write .request, .jobs, .files files
            ;;
        esac
    fi
done


