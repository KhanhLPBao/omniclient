#!/bin/bash
signaldir="/mnt/signal"
clustername=$( hostname )
storagedir="/"$clustername

install(){
    echo "OMNICLIENT INSTALLATION"
    echo "Make sure that you have mounted shared signal folder to VM"
    read stopvalue
    echo "Enter the directory of mounted shared signal folder"
    read signaldir
    echo "Validating $signaldir"
    if [ -d $signaldir ]
    then
        echo "Searching for node management"
        if [ ! -d $signaldir"/nodes" ]
        then
            echo "ERROR!!! NO NODE MANAGEMENT FOUND, PLEASE REMOUNT THE CORRECT SIGNAL FOLDER AND RELAUNCH THE SCRIPT"
            exit 1
        else
            read -p "Type r if you want to create account, type l if you want to login: " account_command
            case $account_command in
                r || R)
                    echo "Begin registration"
                    loop=0
                    while [ $loop == 0 ]
                    do
                        read -p "System's account: " account
                        read -sp "Please enter password: " pass_tmp
                        pass1=$( echo -n "$pass_tmp" | openssl sha3-512 | openssl sha512-256 | cut -d "=" -f 2 )
                        read -sp "Confirm password: "  pass_tmp
                        pass2=$( echo -n "$pass_tmp" | openssl sha3-512 | openssl sha512-256 | cut -d "=" -f 2 )

                        if [ "$pass1" == "$pass2" ]
                        then
                            pass=$pass1
                            echo $pass
                            echo $pass > "$storagedir/account/$account.pass"
                            loop=1
                        else
                            echo "WRONG PASSWORD, PLEASE REENTER"
                        fi         
                    done  
                ;;
                l || L)
                    loop=0
                    while [ $loop == 0 ]
                    do
                        logintime=$( date "+%d/%m/%y-%H:%M:%S" )
                        bash login.sh "$logintime"
                        while [ ! -f "account/logintmp_$logintime.tmp" ]
                        do sleep 3s
                        done
                    done
                    account=`cat "account/logintmp_$logintime.tmp" | cut -d " " -f 1`
                    case $account in
                        L1)
                        echo "Invalid User!"
                        ;;
                        L2)
                        echo "Invalid password"
                        ;;
                        0)
                        echo "Login timedout, please relogin"
                        ;;
                        *)
                        echo "LOGIN COMPLETED! Proceed"
                        loop=1
                        ;;
                    esac
                *)
                    echo "UNIDENTIFY STATEMENT!"
                ;;
            esac
        fi
    fi

    echo "Begin setup program"
    mkdir $storagedir"/"$clustername
    echo "Account $account regist cluster $clustername to the system" > "$storagedir/account/$account.pass"
    mkdir "$signaldir/$clustername/in"
    mkdir "$signaldir/$clustername/out"
    mkdir "$signaldir/$clustername/log"
    cat "tutorial.txt"
    echo ""
    echo "Command: "
    read choose
    loop2=0
    while [ $loop2 -eq 0 ]
    do
        if [ "$choose" == "scriptlist" ]
        then
            while IFS= read -r LINE
            do echo "$LINE"
            done < "$signaldir/workflow/summarise.txt"
            echo ""
            read -p "Command: " choose
        elif grep -q "program" <<< $choose
        then
            progname=$( echo $choose | cut -d ":" -f 1)
            while IFS= read -r LINE
            do echo "$LINE"
            done < $signaldir"/programs/platformscript/"$progname"_summarise.txt"
        elif [ "$choose" == "help" ]
        then
            cat "tutorial.txt"
            echo ""
            read -p "Command: " choose
        elif [ "$choose" == "Done" ]
        then
            echo "1" > "/home/"$USER"/program/installed.confirm"
            $loop2=1
        else
            if [ ! -d $signaldir"/programs/platformscript_summarise.txt" ]
            then
                echo "NO WORKFLOW FOUNDED, MAKE SURE YOU TYPE EXACTLY THE NAME OF WORKFLOW"
                echo ""
                read -p "Command: " choose
            else
                echo "Workflow detected, begin scanning for programs inside"
                workflow=$( echo $choose | cut -d ":" -f 1)
                prog=$( echo $choose | cut -d ":" -f 2)
                echo $prog > $signaldir"/tmp/"$workflow".program"
                search_prog=$(python workflowprocess.py $workflow)
                if [ "$search_prog" == "0" ]
                then
                    echo "PROGRAM FOUNDED, BEGIN REGISTRATION"
                    python workflowregistration.py $account $workflow $prog
                else
                    echo "ERROR! NO PROGRAM FOUND ON WORKFLOW"
                fi
            fi
        fi
    done
}
install