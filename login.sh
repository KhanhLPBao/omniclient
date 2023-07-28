L=0
signaldir="/mnt/signal"
clustername=$( hostname )
storagedir="/"$clustername
sleep=5     #Time between retry during login
maxtry=3    #number of maximum try before timedout
prerun=0
logintime=$1

output="account/logintmp_$logintime.tmp"

while [ $prerun -eq 0 ]             #Cleanning cache from previous login
do
    if [ -f "account/logintmp_*.tmp" ]
    then
        rm -f "account/logintmp_*.tmp"
        if [ ! -f "account/logintmp_*.tmp" ]
        then
            prerun=1
        fi
    else
        prerun=1
    fi
done

while [ $L == 0 ]
do
    read -p "Enter the name of account: " account
    pass=$( echo -n $( read -sp "$account password: " ) | openssl sha3-512 | openssl sha512-256 | cut -d "=" -f 2 )
    timelogin=$( date "+%d/%m/%y-%H:%M:%S" )
    echo $pass" "$timelogin > $storagedir"/account/login/"$account
    wait=1
    
    while [ $wait -eq 1 ]
    do
        retry=0
        if [ ! -f $storagedir"/account/response/"$account"_response" ] && [ $maxtry -gt $retry ]
        then
            sleep $time
            retry+=1
            echo 1 > $signaldir"/clusters/"$clustername"/status/account"
        elif [ $mastry -eq $retry ]
        then
            echo "e L 0" > $signaldir"/clusters/"$clustername"/status/account"   #Error L0: Login timed out
            echo "Login timed out, re-enter information"
            echo "$( date "+%d/%m/%y-%H:%M:%S" ) - Encountered error L0" > $storagedir"/"$clustername"/log/login_attemp_$( date "+%d/%m/%y-%H:%M:%S" ).log"
            echo 0 > $output
            wait=0
        else
            retry=0
            response=`$storagedir"/account/response/"$account".login.response" 
            if [ "$response" == "pass" ]
            then
                echo "Login completed!"
                certificate=`cat $signaldir"/account/"$timelogin".certificate"
                echo $( date "+%d/%m/%y-%H:%M:%S" )" - Login completed - Account: $account"
                echo 1 > $signaldir"/clusters/"$clustername"/status/account"                
                echo $account" "$certificate > $output
                L=1
            elif [ "$response" == "InvalidID" ]
            then
                echo "Invalid username, please relogin"
                echo $( date "+%d/%m/%y-%H:%M:%S" )" - Invalid username $account"
                echo "e L 1" > $signaldir"/clusters/"$clustername"/status/account"  #Error L1: Invalid username
                echo "L1" > $output
            elif [ "$response" == "InvalidPWD" ]
            then
                echo "Invalid password, please relogin"
                echo $( date "+%d/%m/%y-%H:%M:%S" )" - Invalid password for username $account"
                echo "e L 2" > $signaldir"/clusters/"$clustername"/status/account"  #Error L2: Invalid password
                echo "L2" > $output            
            fi
        fi
    done
