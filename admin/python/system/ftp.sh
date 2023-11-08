#!/bin/bash
"""
Download files using sftp method
"""
IP=$1
ID=$2
pass=$3

filein=$4
fileout=$5
downloadlink="sftp://"$IP"/"$filein

curl -k $downloadlink --user $IP:$pass -o $fileout