#/bin/bash
# Directory
req_input="/mnt/share/source/debug/omniclient/input"
req_output="/mnt/share/source/debug/omniclient/output"
scriptdir="/mnt/share/source/omniclient"
#
for file in req_input/*
do
    if [ -f $file ]
    then
        content=`cat $file`
        ip=ip
        source=source
        destination=destination
        req_token=$(basename $file | cut -d '.' -f 1)
        typerequest=$(basename $file | cut -d '.' -f 2)
        #Create local value
        #
        case $typerequest in
            .admin)
                :   #Execute request from omniadmin
            ;;
            interface_login)  #Decode request first to validate
                decoderesults=$(python "$scriptdir/admin/account/python/account/hashstring.py" "decode" "'$file'" "'$req_token'")
                if [[ ! $decoderesults -eq 5 ]]   #Valid request
                then
                    #   Check account storage folder
                    #   return result: Accept or reject login
                    accountcompare=$(python "$scriptdir/admin/account/python/account/login.py" $decoderesults)
                    case $accountcompare in
                        accept)
                            token=$(python "$scriptdir/admin/account/python/account/hashstring.py" "token")
                            echo $token > "$req_output/$req_token-response.$typerequest"
                        ;;
                fi
            ;;
        esac

    fi
done


