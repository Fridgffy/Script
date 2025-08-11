# set color variables
GREEN='\033[1;32m'
RED='\033[1;31m'
YELLO='\033[1;33m'
END='\033[0m'

set -u
c=False

function push()
{
	# echo -e "${RED}Check Status ${END}"
	status_start="$(git status)"
	if echo "$status_start" | grep -q "nothing to commit";then
		echo -e "${GREEN}    [ Success ] This is the latest!${END}"
	else
		echo -e "${YELLO}    [ Notice ] The git repository has changed!${END}"
		# git status
		# sleep 1
		# echo -e "${RED}    Start add ${END}"
		git add .
		sleep 1

		echo -e "${YELLO}    [ Status ]${END}"
		git status
		sleep 1

		# echo -e "${RED}    [ Commit with 1 ]${END}"
		git commit -m '1' > /dev/null 2>&1
		if [ $? -ne 0 ];then
			echo -e "${RED}[ Error ] git commit"
			exit 1
		fi
		sleep 1

		# echo -e "${RED}    [ Push ]${END}"
		git push -u origin main > /dev/null 2>&1
		if [ $? -ne 0 ];then
			echo -e "${RED}[ Error ] git push"
			exit 1
		fi
		echo -e "${GREEN}    [ Success ] Repository update complete!${END}"
	fi
}

function push_alone()
{
	echo -e "${YELLO}    [ Notice ] Check Status ${END}"
	status_start="$(git status)"
	if echo "$status_start" | grep -q "nothing to commit";then
		echo -e "${GREEN}    [ Success ] This is the latest! ${END}"
	else
		echo -e "${RED}    [ Notice ] The git repository has changed! ${END}"
		git status
		sleep 1

		echo -e "${YELLO}    [ Notice ] Start add ${END}"
		git add .
		sleep 1

		echo -e "${YELLO}    [ Notice ] Check Status ${END}"
		git status
		sleep 1

		echo -e "${YELLO}    [ Notice ] Start commit with 1 ${END}"
		git commit -m '1'1
		if [ $? -ne 0 ];then
			echo -e "${YELLO}[ Error ] git commit ${END}"
			exit 1
		fi
		sleep 1

		echo -e "${YELLO}    [ Notice ] Start push ${END}"
		git push -u origin main
		if [ $? -ne 0 ];then
			echo -e "${RED}[ Error ] git push"
			exit 1
		fi
		echo -e "${GREEN}    [ Success ] Repository update complete!${END}"
	fi
}

while getopts ":c" opt
do
	case $opt in
		c)
			c=True
			;;
		\?)
			echo -e "${RED}[ Error ] Ivalid option: -${OPTARG} ${END}" >&2
			exit 1
			;;
		*)
			;;
	esac
done
			
if [ $c == True ];then
	echo -e "${RED}Start checking the status of all repositories\n${END}"

	if ! [ -z "$repo" ];then
		cd $repo
		for i in */
		do
			cd ${i}
			echo -e "${YELLO}[ Notice ] Enter the directory: $(pwd)"
			push
			cd ..
		done
	else
		exit 1
	fi
else
	echo -e "${RED}Start checking status of this repository${END}"
	push_alone
fi










