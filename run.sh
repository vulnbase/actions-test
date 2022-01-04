export RED='\033[0;31m'
export GREEN='\033[0;32m'
export NC='\033[0m'
while read x; do
    printf "${GREEN}${x}${NC}\n"
    if ! sudo /bin/bash -c "${x} 2>&1"
    then
    printf "${RED}Exit code $?${NC}\n"
    fi
done < commands.sh