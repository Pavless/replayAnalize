#!/bin/sh

# $1 = replay.out

# remove non-complete replays
./blockFilter.py 1 <"$1" | awk -F";" '{print $1}' | while read line; do rm "$line"; done

# remove duplacates
id=""
./blockFilter.py 2 <"$1" | awk -F';' '{print $1";"$13}' | sort -k 2 -t';' | while read line
do
    c_id="$(echo "$line" | cut -d';' -f 2)"   
    if [ "$c_id" = "$id" ]; then rm "$(echo "$line" | cut -d';' -f 1)"; fi
    id="$c_id"
done
