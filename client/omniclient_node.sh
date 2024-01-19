#!/bin/bash
jobname=$1
type=`cat nodetype`
sessioninput=$2
sessionoutput=$3
internal_processor=$4
previousoutput=$5
errordir=$6
nodename=$7
joblvl="Lx"   #   x = Job level
dockerrun(){
   stopswitch=`cat $queqe_working`
   case $stopswitch in
      0)
         for session in $sessioninput/$level/*
         do
            if [ -d $session ] && [ -f $previousoutput"/"$sessionname"/status.txt" ]
            then
               sessionname=$( basename $session )
               sessionstatus=`cat $previousoutput"/"$sessionname"/status.txt"`
               case $sessionstatus in
                  DONE)
                     docker exec -d $nodename ./runsession.sh $sessionname
                  ;;
                  STOP)
                  #     Job failed due to level 1 cannot retrieved any files or all files failed MD5 check
                  :  #<Extra notification for failed jobs
                  ;;
               esac
            fi
         done
         sleep 1m
      ;;
      *) 
         sleep 1m
      ;;
   esac
}

queqe_working="queqeworking.txt"    #queqe.py is working or not
while :
do
   if [ ! -f $queqe_working ]
   then
      echo 2 > $queqe_working
   else
   dockerrun
done