requestfile="/mnt/share/source/debug/omniclient/interface_request"
responsefile="/mnt/share/source/debug/omniclient/interface_response"
serverresponsefile="/home/guestftp"
scriptfile="/mnt/share/source/omniclient/admin/bash/account"
echo "Begin requestcheck"
width=$(tput cols)
while :
do
    for file in $requestfile/*
    do
        sleep 1s
        if [ -f $file ]
        then
            echo "$(date) - Received $file"
            filesuffix=`echo $file | cut -d "." -f 2`  
            case $filesuffix in
                response)
                    mv $file $responsefile
                ;;
                seq)
                    mv $file $responsefile
                ;;
                certificate)
                    mv $file $responsefile
                ;;
                txt)
                    mv $file $responsefile
                ;;
                *)
                    cp $file $requestfile/requestbackup
                    bash $scriptfile"/accountscan.sh" $file $filesuffix &
                ;;
            esac
        fi
    done
    for file in $serverresponsefile/*
    do
        if [ -f $file ]
        then
            sudo -i -u guestftp mv $file $responsefile
        fi
    done
done
