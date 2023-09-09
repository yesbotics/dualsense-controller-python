#!/bin/bash

count=0
prints=0
text=""
oldtext=""

while IFS= read -r line; do			
	
	if [ "$count" -gt 0 ]; then  		
		text="$text \n$line"
	fi		  			
	
	count=$((count + 1))
	
	if [ "$count" -gt 5 ]; then  		
		if ! [ "$text" = "$oldtext" ]; then  			
			clear			
			echo -e "$text"
			echo -e "Prints: ${prints}"
			oldtext="$text"
			prints=$((prints + 1))
		fi		  			
		
		text=""
		count=0		
	fi		  			
done