#!/bin/bash
requestdir="/mnt/share/source/debug/omniclient/interface_request/"
responsedir="/mnt/share/source/debug/omniclient/interface_response"
seqdir="/mnt/share/source/debug/omniclient/seq/"
while :
do
    find $requestdir -type f -mmin +10 -delete
    find $responsedir -type f -mmin +10 -delete
    find $seqdir -type f -mmin +15 -delete
    sleep 5m
done