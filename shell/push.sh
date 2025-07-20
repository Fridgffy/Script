GREEN='\033[3;32m'
RED='\033[1;31m'
END='\033[0m'

echo -e "${RED} Check Status ${END}"
status_start=`git status`
if echo "$status_start" | grep -q "nothing to commit";then
	echo -e "${GREEN}This is the latest!${END}"
else
	sleep 1
	echo -e "${GREEN} Start add ${END}"
	git add .
	sleep 1
	echo -e "${RED} Check Status ${END}"
	git status
	sleep 1
	echo -e "${GREEN} Start commit ${END}"
	git commit -m '1'
	sleep 1
	echo -e "${GREEN} Start push ${END}"
	git push -u origin main
fi
