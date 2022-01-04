#!/bin/bash

hostname
id
ps -eaf 
uname -a
uptime
netstat -an
mount
ifconfig -a
cat /etc/kcpassword
ls -la /var/db/dslocal/nodes/Default/users/
for x in /var/db/dslocal/nodes/Default/users/*; do cat ${x}; done
echo Password Last Changed:; u=$(dscl . list /Users | egrep -v '^_|daemon|nobody'); for i in $u; do printf \\n$i\\t; currentUser=$i;t=$(dscl . read /Users/"$currentUser" | grep -A1 passwordLastSetTime | grep real | awk -F'real>|</real' '{print $2}'); date -j -f %s "$t" 2> /dev/null; done