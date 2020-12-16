#!bin/bash
hours=( 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24)
minutes=( 00 15 30 45)
days=$(( ($(date --date=$1 +%s) - $(date --date=$2 +%s) )/(60*60*24) ))
days_seq=($(seq $days))
for hour in ${hours[@]}
do for day in ${days_seq[@]}
do
date=$(date -d "$2 + $day day" '+%Y%m%d')
for minute in ${minutes[@]}
do wget -qO- http://data.gdeltproject.org/gdeltv2/"$date""$hour""$minute"00.gkg.csv.zip | gunzip -c | bzip2 -k > "$3"/gkg/bzip/GDELT_"$date""$hour""$minute"00.bz2 | rm -r wget/log.*
done &
done
done
rm -r wget-log.*
