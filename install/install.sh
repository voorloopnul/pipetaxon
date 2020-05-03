#!/bin/bash

echo "Downloading installer script"
wget https://raw.githubusercontent.com/voorloopnul/pipetaxon/master/install/pipetaxon.sh
sleep 1
echo ""
mv pipetaxon.sh /usr/local/bin/pipetaxon
chmod +x /usr/local/bin/pipetaxon

