#!/bin/bash
clientdir="/mnt/share/source/omniclient"
bash $clientdir/admin/bash/system/cleanuprequest.sh &
bash $clientdir/admin/bash/system/requestcheck.sh &