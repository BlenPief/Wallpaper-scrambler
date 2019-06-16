#!/bin/bash
# Sets random pictures as background


#UTILITIES

DIR="$(readlink -f `dirname $0`)/data"

download_pic () {
	# Download picture and write path in temporary file

	python $DIR/get_image.py $DIR
	echo `cat $DIR/tempfile.wl`
	rm $DIR/tempfile.wl
}

set_wallpaper () {
	
	/usr/bin/gsettings set org.gnome.desktop.background picture-uri $1

}


random_file () {
	# Given a directory prints a random file

	local DIR="$1"

	  
	IFS='
	'
	if [[ -d "${DIR}" ]]
	then
		local files=($(ls "${DIR}"))
		local num_files=${#files[*]}
		echo ${DIR}/${files[$((RANDOM%num_files))]}
	fi
}
#MODES

newpics () {
	#Downloads random picture from internet and sets as background

	echo -e "Fetching pictures online. Press any key to exit."
	echo "Current wallpaper is:"

	while [ true ]
	do
		local PICPATH=$(download_pic)
		local PICNAME="${PICPATH##*/}"
		set_wallpaper $PICPATH
		echo -ne "\r$PICNAME                                              "
		sleep $1
	done

}


oldpics () {
	#Chooses a random wallpaper from downloaded pictures

	echo -e "Using pictures from library. Press any key to exit."
        echo "Current wallpaper is:"

	while [ true ]; do

        	local PICPATH=$(random_file "$DIR/backgrounds")
		local PICNAME="${PICPATH##*/}"
                set_wallpaper "$PICPATH"
                echo -ne "\r$PICNAME                                            "
                sleep $1
        done
        read -n 1 -s
	bool=false

	echo -e "\n"
}


#Menu
main () {

	TIMER=30

	echo -e "Welcome to the scrambler!\n\n"

	while true; do
		read -p "Would you like [n]ew pictures, [o]ld pictures, change the [t]imer, or [e]xit? " -n1 -s choice
		echo -e "\n"
		case $choice in
			[nN]* ) newpics $(echo "scale=2;60*$TIMER" | bc) &
				pid=$!; disown
				read -n1 -s; kill $pid; echo -e "\n";;
			[oO]* ) oldpics $(echo "scale=2;60*$TIMER" | bc) &
				pid=$!; disown
			       	read -n1 -s; kill $pid; echo -e "\n";;
			[tT]* ) echo "The timer is currently set to $TIMER minutes."
				read -p "Set the timer:  " TIMER; echo;;
			[eEqQ]* ) break;;
			* ) echo -e "\nPlease, choose one of the options!\n";;
		esac
	done

	echo -e "\nThank you for scrambling today!"

}


main
	




