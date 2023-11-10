#!/bin/bash
server_IP=$1
server_ID=$2
pass=$3
filein=$4
fileout=$5
echo $1 $2 $3 $4 $5
downloadlink="sftp://$server_IP/$filein"
#echo $server_IP $server_ID $pass $filein $fileout
echo "Downloadlink: $downloadlink"
curl -vk $downloadlink --user $server_ID:$pass -o $fileout
