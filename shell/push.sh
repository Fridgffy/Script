# set color variables
GREEN='\033[1;32m'
RED='\033[1;31m'
YELLO='\033[1;33m'
END='\033[0m'

echo -e "${RED}Check Status... ${END}"
status_start="$(git status)"
if echo "$status_start" | grep -q "nothing to commit";then
	echo -e "${GREEN}[ Success ] This is the latest!${END}"
else
	echo -e "${YELLO}[ Notice ] The git repository has changed!${END}"
	echo "$status_start"
	sleep 1
	echo -e "${RED}Start add... ${END}"
	git add .
	sleep 1
	echo -e "${RED}Check Status... ${END}"
	git status
	sleep 1
	echo -e "${RED}Start commit with 1... ${END}"
	git commit -m '1'
	sleep 1
	echo -e "${RED}Start push... ${END}"
	git push -u origin main
fi
