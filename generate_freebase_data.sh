#!/bin/bash
#Author: Michal Cab <xcabmi00@stud.fit.vutbr.cz>

_now=$(date +"%d%m%Y")

_path="/mnt/minerva1/nlp/projects/decipher_freebase/crawler/"

display_usage()
{
  echo -e "Usage: $0 [arguments] \n-i/--info\t: Generate .info files\n-t/--tsv\t: Generate tabulator separated values (.info files necessary)\n-d path/--dump path\t: Path to freebase dump (if not set, will be downloaded automatically)"
}

if [ "$1" == "-h" ] || [ $# -eq 0 ] || [ "$1" == "--help" ] || [ $# -gt 4 ]
then
  display_usage
  exit 0
fi

#init variables
file="freebase-rdf.gz"
generate_info=0
generate_tsv=0
download_dump=1

#get arguments
n=0
for arg in $@
do
    if [ "$arg" == "-i" ] || [ "$arg" == "--info" ] 
    then
      generate_info=1
    elif [ "$arg" == "-t" ] || [ "$arg" == "--tsv" ] 
    then
      generate_tsv=1
    elif [ "$arg" == "-d" ] || [ "$arg" == "--dump" ] 
    then
      download_dump=0
      if [ $# -gt 1 ] 
      then 
        m=$((n+2))
        file=${!m}
      else 
        display_usage
        exit 1
      fi
    fi
  n=$((n+1))
done

#make folder
mkdir ${_now}
cd ${_now}

# download freebase dump
if [ $download_dump == 1 ] 
then
	echo -e "---\nDownloading freebase-rdf.gz from http://download.freebaseapps.com ... \n---"
	wget http://download.freebaseapps.com -O $file
	echo -e "---\nfreebase-rdf.gz downloaded\n---"
else
  file=../$file
fi

#control dump
if [ ! -r "${file}" ]
then
	echo "ERROR: File $file have not right format or doesn't exist" 2>&1
	exit 1
fi

#make dirs
if [ ! -d "ids" ]; then
  mkdir ids
fi
if [ ! -d "info" ]; then
  mkdir info
fi
if [ ! -d "help" ]; then
  mkdir help
fi
if [ ! -d "freebase" ]; then
  mkdir freebase
fi

# generate help files to help folder
echo -e "---\nGenerating ids files and labels file ...\n---"
python ${_path}convertFreebaseDumpToDic.py -t ids --dump-loc ${file}
echo -e "---\nIds files and labels files are ready\n---"

entity_types=( artist art_period_movement artwork visual_art_form visual_art_genre visual_art_medium event museum person location )

i=0

echo -e "---\nGenerating .info files ...\n---"

if [ $generate_info == 1 ] 
then
    for entity_type in "${entity_types[@]}"
    do
      if [ -r ids/${entity_type}s_ids ]
      then
		    cat ids/${entity_type}s_ids | python ${_path}convertFreebaseDumpToDic.py -t ${entity_type} --dump-loc ${file} > info/${entity_type}.info
      fi
    done
fi
echo -e "---\nInfo files are ready\n---"

if [ $generate_tsv == 1 ] 
then
	for entity_type in "${entity_types[@]}"
	do
		if [ -r info/${entity_type}.info ]
		then
			echo "---\nRun generating freebase.${entity_type}s in background\n---"
		  cat info/${entity_type}.info | python ${_path}convertJsonToColumns.py -b -t ${entity_type} > freebase/freebase.${entity_type}s &
			echo "---\nGo sleep for 15s\n---"
			sleep 20
		fi
	done
  cat info/location.info | python ${_path}convertJsonToColumns.py -b -t nationalities > freebase/freebase.nationalities
fi

#entity_types2=( art_period_movements nationalities visual_art_forms visual_art_mediums )
#
#for entity_type in "${entity_types_2[@]}"
#do
#  cat freebase/freebase.{$entity_type} > freebase/findDuplicity.py > help/{$entity_type}.only_duplicities
#done

#${_path}removeDuplicity.sh ${_now}

